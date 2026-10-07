"""Piezas compartidas por agente.py y agente_mcp.py: modelo, instrucciones, corrida del benchmark y log."""
import argparse
import asyncio
import json
import os
import time
from datetime import datetime
from pathlib import Path

import httpx
from agents import Agent, ModelSettings, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
from openai import AsyncOpenAI

MODELO = "deepseek/deepseek-v4-flash-0731"
RAIZ = Path(__file__).resolve().parent

INSTRUCCIONES = """Sos el asistente del Hospital Provincial Arroyo Claro. Contestás preguntas de pacientes y familiares, en español rioplatense, de forma clara y breve.

Tenés dos fuentes y ninguna otra:
- Documentos del hospital (normas y procedimientos): herramienta buscar_documentos.
- API con el estado de hoy (camas, guardia, turnos, farmacia, espera): herramientas consultar_*.

Reglas:
1. Antes de responder, consultá las herramientas. Nunca contestes de memoria.
2. Si la pregunta mezcla una norma con el estado de hoy (por ejemplo, "¿hay camas en pediatría y los padres pueden quedarse?"), usá buscar_documentos Y la herramienta de la API que corresponda.
3. Afirmá solo lo que está en lo que devolvieron las herramientas. Si algo no está, decí que no tenés ese dato. No inventes horarios, cifras ni requisitos.
4. Si una herramienta de la API devuelve un error con opciones válidas, corregí el nombre y reintentá.
5. Incluí los datos concretos (horarios, cantidades, fechas) tal como los devolvieron las herramientas, y respondé todo lo que se preguntó."""

CAMPOS_USAGE = ("prompt_tokens", "completion_tokens", "total_tokens")


def crear_modelo():
    """Modelo en OpenRouter. Devuelve (modelo, usos): `usos` acumula el usage (con costo) de cada respuesta."""
    usos = []

    async def capturar(resp):
        if resp.request.url.path.endswith("/chat/completions"):
            await resp.aread()
            try:
                u = resp.json().get("usage")
            except Exception:
                u = None
            if u:
                usos.append(u)

    cliente = AsyncOpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ["OPENROUTER_API_KEY"],
                          http_client=httpx.AsyncClient(event_hooks={"response": [capturar]}, timeout=120))
    set_tracing_disabled(True)  # el tracing manda datos a OpenAI y sin una key de OpenAI falla
    return OpenAIChatCompletionsModel(model=MODELO, openai_client=cliente), usos


def crear_agente(modelo, tools=None, mcp_servers=None):
    return Agent(name="asistente-hospital", instructions=INSTRUCCIONES, model=modelo,
                 model_settings=ModelSettings(temperature=0, extra_body={"usage": {"include": True}}),
                 tools=tools or [], mcp_servers=mcp_servers or [])


def _campo(obj, nombre, defecto=None):
    return obj.get(nombre, defecto) if isinstance(obj, dict) else getattr(obj, nombre, defecto)


def extraer_llamadas(result):
    """[(nombre, argumentos, salida)] en orden, a partir de los items de la corrida."""
    llamadas, por_id = [], {}
    for item in result.new_items:
        if item.type == "tool_call_item":
            raw = item.raw_item
            llamada = {"nombre": _campo(raw, "name"), "argumentos": _campo(raw, "arguments", "{}"), "salida": None}
            por_id[_campo(raw, "call_id")] = llamada
            llamadas.append(llamada)
        elif item.type == "tool_call_output_item":
            llamada = por_id.get(_campo(item.raw_item, "call_id"))
            if llamada is not None:
                llamada["salida"] = str(item.output)
    return llamadas


def _costo(u):
    return float(u.get("cost") or 0)


async def correr_benchmark(preguntas, salida, abrir_agente, etiqueta):
    """Corre cada pregunta. `abrir_agente` es un context manager async que da el agente y `usos`."""
    log = [f"# Corrida {etiqueta}\n", f"- Fecha: {datetime.now().isoformat(timespec='seconds')}",
           f"- Modelo: `{MODELO}`", f"- Preguntas: `{preguntas}`\n"]
    filas, total_costo, total_tokens = [], 0.0, 0
    async with abrir_agente() as (agente, usos):
        for linea in Path(preguntas).read_text(encoding="utf-8").splitlines():
            if not linea.strip():
                continue
            p = json.loads(linea)
            usos.clear()
            t0 = time.time()
            result = await Runner.run(agente, p["pregunta"], max_turns=10)
            llamadas = extraer_llamadas(result)
            respuesta = str(result.final_output)
            costo, tokens = sum(_costo(u) for u in usos), sum(u.get("total_tokens", 0) for u in usos)
            total_costo += costo
            total_tokens += tokens
            filas.append({"id": p["id"], "respuesta": respuesta,
                          "contextos": [c["salida"] for c in llamadas if c["salida"]],
                          "herramientas": sorted({c["nombre"] for c in llamadas})})
            log += [f"## {p['id']}: {p['pregunta']}\n"]
            for i, c in enumerate(llamadas, 1):
                log += [f"**Llamada {i}:** `{c['nombre']}({c['argumentos']})`\n", "```", str(c["salida"]), "```\n"]
            log += [f"**Respuesta:** {respuesta}\n", "**Usage por llamada al modelo:**\n"]
            for i, u in enumerate(usos, 1):
                log.append(f"- llamada {i}: {u.get('prompt_tokens', 0)} tokens de entrada, "
                           f"{u.get('completion_tokens', 0)} de salida, USD {_costo(u):.6f}")
            log += [f"\nTotal pregunta: {tokens} tokens, USD {costo:.6f}, {time.time() - t0:.1f} s\n"]
            print(f"{p['id']}: {', '.join(filas[-1]['herramientas'])}  USD {costo:.5f}", flush=True)
    log += [f"## Total\n", f"{len(filas)} preguntas, {total_tokens} tokens, **USD {total_costo:.5f}** (solo el agente, sin el juez)"]
    Path(salida).write_text("\n".join(json.dumps(f, ensure_ascii=False) for f in filas) + "\n", encoding="utf-8")
    carpeta = RAIZ / "logs"
    carpeta.mkdir(exist_ok=True)
    ruta_log = carpeta / f"{etiqueta}_{datetime.now():%Y%m%d_%H%M%S}.md"
    ruta_log.write_text("\n".join(log) + "\n", encoding="utf-8")
    print(f"respuestas: {salida}\nlog: {ruta_log}\ncosto del agente: USD {total_costo:.5f}")


def main_cli(etiqueta, abrir_agente):
    ap = argparse.ArgumentParser()
    ap.add_argument("--preguntas", required=True)
    ap.add_argument("--salida", required=True)
    args = ap.parse_args()
    if not os.environ.get("OPENROUTER_API_KEY"):
        raise SystemExit("falta la variable OPENROUTER_API_KEY")
    asyncio.run(correr_benchmark(args.preguntas, args.salida, abrir_agente, etiqueta))
