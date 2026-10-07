"""Parte 2. Agente con tool calling (SDK de agentes de OpenAI sobre OpenRouter). Uso:

    python3 agente.py --preguntas datos/preguntas_agente_dev.jsonl --salida respuestas.jsonl
"""
from contextlib import asynccontextmanager

from agents import function_tool

import herramientas as h
from comun import crear_agente, crear_modelo, main_cli


def _tool(nombre):
    """Envuelve una funcion de herramientas.py como @function_tool con la descripcion compartida."""
    return function_tool(h.FUNCIONES[nombre], name_override=nombre, description_override=h.DESCRIPCIONES[nombre])


TOOLS = [_tool(n) for n in h.FUNCIONES]


@asynccontextmanager
async def abrir_agente():
    modelo, usos = crear_modelo()
    yield crear_agente(modelo, tools=TOOLS), usos


if __name__ == "__main__":
    main_cli("agente", abrir_agente)
