"""Parte 3. Servidor MCP (stdio) con las seis herramientas del hospital. Uso:

    python3 servidor_mcp.py
    npx @modelcontextprotocol/inspector python3 servidor_mcp.py
"""
from mcp.server.fastmcp import FastMCP

import herramientas as h

mcp = FastMCP("hospital")

for _nombre, _funcion in h.FUNCIONES.items():
    mcp.tool(name=_nombre, description=h.DESCRIPCIONES[_nombre])(_funcion)

if __name__ == "__main__":
    h._get_recuperador()  # carga el indice al arrancar para que la primera llamada no tarde
    mcp.run(transport="stdio")
