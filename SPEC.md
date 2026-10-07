# SPEC

Resumen de los contratos de la misión (la consigna completa está en `mission.md` de la cátedra). Entrega: viernes 9 de octubre de 2026.

## Parte 1 — `recuperar.py`

```bash
python recuperar.py --preguntas datos/preguntas_recuperacion_dev.jsonl --salida resultados.jsonl
```

Salida: una línea por pregunta, `{"id": "R01", "fragmentos": ["texto", ...]}`, en orden de relevancia. La configuración (encoder, chunking, top-k, umbral) está fija en `rag/config.json`. Métrica: context_relevance (media armónica de recall y precision) con `evaluar/evaluar.py recuperacion`. Línea de base obligatoria: BERT multilingüe sin ajustar, mean pooling de la última capa. Se comparan al menos tres encoders, y cada fila de la tabla tiene su `.eval.json` en `experimentos/`.

## Parte 2 — `agente.py`

Agente con tool calling sobre `deepseek/deepseek-v4-flash-0731` vía OpenRouter (SDK `openai-agents`). Herramientas: `buscar_documentos(consulta)`, `consultar_camas(sector)`, `consultar_guardia(especialidad)`, `consultar_turnos(especialidad)`, `consultar_farmacia(medicamento)`, `consultar_espera()`.

```bash
python agente.py --preguntas datos/preguntas_agente_dev.jsonl --salida respuestas.jsonl
```

Salida: `{"id", "respuesta", "contextos": [...], "herramientas": [...]}`. Log `.md` por corrida con llamadas, resultados, respuesta, tokens y costo. Objetivo: ruteo ≈ 1 y las tres métricas del juez por encima de 4.

## Parte 3 — `servidor_mcp.py` y `agente_mcp.py`

Las mismas seis herramientas en un servidor FastMCP (`mcp.server.fastmcp`, SDK `mcp` 1.x, stdio). `agente_mcp.py` las descubre con `tools/list` y las llama con `tools/call`; no tiene código propio de API ni de recuperador. Capturas del MCP Inspector en `experimentos/inspector/`. Tabla comparativa de las partes 2 y 3 en `INFORME.md`.

## Parte 4 — `atencion.py`

Solo NumPy: `softmax`, `atencion`, `autoatencion` (máscara causal opcional), `multicabeza`, `layer_norm`. Se verifica con `python atencion/test_atencion.py atencion.py` (14 tests).

## Parte 5 — `a_mano/`

Bloque de transformer completo para "El banco aguanta" y "El banco presta", con y sin máscara causal; cada operación con su justificación y las cinco preguntas finales. `a_mano/solucion.md` tiene el desarrollo y `a_mano/verificar.py` lo recalcula con `atencion.py`.

## Informe — `INFORME.md`

Tabla de experimentos y elección del encoder, resultados de la parte 2 con análisis de fallas, comparación entre las partes 2 y 3, y costo total en OpenRouter.
