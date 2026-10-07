"""Parte 3. Agente cliente MCP: descubre las herramientas del servidor con tools/list y las llama con tools/call. Uso:

    python3 agente_mcp.py --preguntas datos/preguntas_agente_dev.jsonl --salida respuestas_mcp.jsonl

No tiene codigo propio para la API ni para el recuperador: todo sale de servidor_mcp.py.
"""
import sys
from contextlib import asynccontextmanager
from pathlib import Path

from agents.mcp import MCPServerStdio

from comun import crear_agente, crear_modelo, main_cli

SERVIDOR = Path(__file__).with_name("servidor_mcp.py")


@asynccontextmanager
async def abrir_agente():
    modelo, usos = crear_modelo()
    async with MCPServerStdio(params={"command": sys.executable, "args": [str(SERVIDOR)]},
                              client_session_timeout_seconds=120) as servidor:
        yield crear_agente(modelo, mcp_servers=[servidor]), usos


if __name__ == "__main__":
    main_cli("agente_mcp", abrir_agente)
