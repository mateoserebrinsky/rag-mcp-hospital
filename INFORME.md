# Informe: RAG, MCP y Transformers en el Hospital Arroyo Claro

## 1. Parte 1: recuperación vectorial

Se probaron 128 configuraciones sobre `datos/preguntas_recuperacion_dev.jsonl` (20 preguntas). Cada una tiene su `.eval.json` en `experimentos/`; la tabla completa, ordenada por context_relevance, está en [`experimentos/tabla.md`](experimentos/tabla.md) y la genera `experimentos/barrido.py` con `experimentos/tabla.py`.

Mejor configuración de cada encoder (de las 32 que se probaron con cada uno: 4 chunkings × top-k 1/2/3/5, umbrales 0,5 y 0,7, y cortes por caída de similitud de 0,05 y 0,1):

| Encoder | Mejor configuración | recall | precision | context_relevance |
|---|---|---|---|---|
| BERT multilingüe sin ajustar (línea de base) | secciones + título, k=3, umbral 0,7 | 0,300 | 0,300 | **0,300** |
| paraphrase-multilingual-MiniLM-L12-v2 | secciones + título, k=3, caída 0,05 | 1,000 | 0,892 | **0,925** |
| multilingual-e5-small | secciones + título, k=1 | 0,900 | 0,900 | **0,900** |
| multilingual-e5-base | ventanas 500/100, k=1 | 1,000 | 1,000 | **1,000** |
| multilingual-e5-base | secciones + título, k=1 | 0,950 | 0,950 | **0,950** |

**Configuración entregada** (`rag/config.json`): `intfloat/multilingual-e5-base`, un fragmento por sección de Markdown con el título del documento y de la sección antepuestos al texto que se codifica, top-k = 1, sin umbral. Resultado en dev: **0,950**, contra 0,300 de la línea de base BERT.

**Por qué ganó el encoder.** BERT sin ajustar no está entrenado para que la distancia coseno signifique parecido de sentido: con mean pooling de la última capa, todos los fragmentos quedan muy cerca entre sí y el ranking casi no discrimina (su mejor resultado, 0,30, ni siquiera llega al 0,35 del recuperador léxico de la consigna). Los tres modelos entrenados para embeddings de oraciones llegan a 0,90 o más. Entre ellos, e5-base fue el más consistente: con k=1 saca entre 0,85 y 1,00 en las cuatro estrategias de chunking, y el pequeño y MiniLM necesitan más ajuste (MiniLM solo llega a 0,70 con secciones sin título), y con k=1 no hace falta umbral ni corte por caída para cuidar la precisión. MiniLM llega a recall 1,0 pero necesita el corte por caída para no perder precisión.

**Decisiones y límites.**
- Elegí secciones + título (0,950) antes que ventanas de 500 caracteres (1,000): la diferencia es una sola pregunta de 20, y una ventana fija puede partir la evidencia en el set de test, mientras que la sección sigue la estructura de los documentos. El título ayuda: sin él, e5-base baja de 0,950 a 0,850.
- Ninguna pregunta de dev tiene más de una evidencia, así que k=1 está favorecido por el set. Si el set de test tiene preguntas con varias evidencias, k=1 perdería recall. La alternativa más segura sería e5-base con k=3 y corte por caída (0,692 en dev, recall 1,0), a costa de precisión.
- No probé `BAAI/bge-m3` ni un reranker con cross-encoder (ambos opcionales).

## 2. Parte 2: agente con dos fuentes

`agente.py` usa el SDK `openai-agents` con `deepseek/deepseek-v4-flash-0731` por OpenRouter y las seis herramientas de `herramientas.py`. Log de la corrida: [`logs/agente_20261007_133225.md`](logs/agente_20261007_133225.md). Evaluación: `respuestas.jsonl.eval.json`.

| Métrica | Resultado |
|---|---|
| ruteo | 1,000 |
| context_relevance | 5,000 |
| faithfulness | 5,000 |
| answer_relevance | 5,000 |

**Análisis de fallas: en dev no hubo ninguna.** Las 12 preguntas sacaron 5 en las tres métricas y usaron exactamente las herramientas esperadas; las tres preguntas que necesitan las dos fuentes (A10 camas + visitas, A11 turnos + documentación, A12 farmacia + norma) llamaron a `buscar_documentos` y a la herramienta de la API correspondiente. Un 5,0 parejo en dev no garantiza lo mismo en test, y el set de dev es chico (12 preguntas). Lo que puede fallar en test es lo que el set de dev no ejercita: preguntas cuya respuesta está en un documento que el recuperador con k=1 no trae primero (el agente puede reformular y volver a buscar, pero en dev nunca lo necesitó), o nombres de sector o medicamento que la API no reconoce (el agente recibe la lista de opciones válidas y puede corregirse, según las instrucciones).

## 3. Parte 3: las mismas herramientas como servidor MCP

`servidor_mcp.py` (FastMCP del SDK oficial `mcp` 1.x, stdio) registra las seis herramientas desde `herramientas.py`, con los mismos nombres y descripciones. `agente_mcp.py` las descubre con `tools/list` y las llama con `tools/call` (`MCPServerStdio` del SDK de agentes), sin código propio de API ni de recuperador. Log: [`logs/agente_mcp_20261007_133539.md`](logs/agente_mcp_20261007_133539.md).

| | Parte 2 (agente directo) | Parte 3 (agente MCP) |
|---|---|---|
| ruteo | 1,000 | 1,000 |
| context_relevance | 5,000 | 5,000 |
| faithfulness | 5,000 | 5,000 |
| answer_relevance | 5,000 | 5,000 |
| tokens del agente (12 preguntas) | 42.578 | 41.751 |
| costo del agente (USD) | 0,00409 | 0,00425 |
| costo del juez (USD) | 0,01725 | 0,01764 |

Las métricas son idénticas y el conjunto de herramientas usadas coincide en las 12 preguntas, como corresponde: el modelo recibe los mismos nombres y descripciones, y el servidor ejecuta las mismas funciones. Las diferencias en tokens y costo (menos de 4 %) son chicas; lo más probable es que vengan de la variación del texto que genera el modelo en cada corrida (no lo medí aparte): el protocolo MCP no agrega tokens al prompt, porque el modelo ve las mismas descripciones. Lo que MCP agrega es tiempo, porque el servidor es un proceso aparte que carga el índice al arrancar, y el cliente hace un `tools/list` antes de cada pregunta (se ve en el log del servidor).

**MCP Inspector.** Las seis herramientas se llamaron con `@modelcontextprotocol/inspector` en modo CLI (que no usa ningún LLM) y las respuestas están en `experimentos/inspector/` (`cli_*.json`). Las capturas de pantalla de la interfaz web del Inspector todavía no están.

## 4. Parte 4: capa de atención

`atencion.py` pasa los 14 tests de la cátedra (`python atencion/test_atencion.py atencion.py`), con el archivo de tests sin modificar.

## 5. Parte 5: bloque a mano

El desarrollo con la justificación de cada operación está en `a_mano/solucion.md`, verificado con `a_mano/verificar.py`. Está resuelto en formato digital, no en hojas escaneadas.

## 6. Costo en OpenRouter

| Concepto | USD |
|---|---|
| Agente, parte 2 (12 preguntas) | 0,00409 |
| Agente MCP, parte 3 (12 preguntas) | 0,00425 |
| Juez, parte 2 | 0,01725 |
| Juez, parte 3 | 0,01764 |
| **Total medido** | **0,04323** |

La parte 1 corre localmente y no tiene costo. Es el costo de las dos corridas finales; no hubo corridas de iteración, porque funcionaron a la primera. **Pendiente:** contrastar este total con el dashboard de actividad de OpenRouter de la cuenta del grupo.

No hizo falta reemplazar ningún id de modelo del catálogo.
