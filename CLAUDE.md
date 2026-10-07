# rag-mcp-hospital

Asistente del Hospital Provincial Arroyo Claro: RAG vectorial, agente con herramientas, servidor MCP y capa de atención en NumPy. La consigna está en `SPEC.md`. Todo el código es Python.

## Comandos

```bash
python -m venv .venv && .venv/Scripts/activate      # en Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt pytest
python api/servidor.py &                            # API del hospital, http://localhost:8765
pytest tests/                                       # tests propios
python atencion/test_atencion.py atencion.py        # tests de la cátedra (14)
python recuperar.py --preguntas datos/preguntas_recuperacion_dev.jsonl --salida resultados.jsonl
python evaluar/evaluar.py recuperacion --preguntas datos/preguntas_recuperacion_dev.jsonl --resultados resultados.jsonl
python agente.py --preguntas datos/preguntas_agente_dev.jsonl --salida respuestas.jsonl
python agente_mcp.py --preguntas datos/preguntas_agente_dev.jsonl --salida respuestas_mcp.jsonl
```

Los agentes y el juez necesitan `OPENROUTER_API_KEY` en el entorno (o en `.env`, que está en `.gitignore`).

## No tocar

`evaluar/evaluar.py`, `api/`, `datos/` y `atencion/test_atencion.py` son de la cátedra. La cátedra corre sus propias copias, así que nada de lo nuestro puede depender de que estén modificados.

## Convenciones

- TDD para la lógica propia (`tests/`). Un commit por paso lógico, mensajes en español.
- Las herramientas viven en un solo lugar, `herramientas.py`. `agente.py` las envuelve con `@function_tool` y `servidor_mcp.py` con `@mcp.tool()`. `agente_mcp.py` no tiene código propio de API ni de recuperador.
- Los nombres de herramienta son fijos (`buscar_documentos`, `consultar_camas`, `consultar_guardia`, `consultar_turnos`, `consultar_farmacia`, `consultar_espera`): el evaluador los usa para medir el ruteo.
- Cada configuración del barrido de la parte 1 deja su `.eval.json` en `experimentos/`.
- Cada corrida de agente deja un log `.md` en `logs/`.
- La configuración ganadora del recuperador queda fija en `rag/config.json`.
