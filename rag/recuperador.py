"""Recuperador con la configuracion ganadora fija en rag/config.json."""
import json
from pathlib import Path

from rag.indice import Indice

CONFIG = Path(__file__).with_name("config.json")


def cargar_config(ruta=CONFIG):
    return json.loads(Path(ruta).read_text(encoding="utf-8"))


class Recuperador:
    def __init__(self, config=None):
        self.config = config or cargar_config()
        self.indice = Indice(self.config["encoder"], self.config["chunking"])

    def recuperar(self, consulta):
        """Textos de los fragmentos mas relevantes, en orden."""
        c = self.config
        hits = self.indice.buscar(consulta, c["k"], c.get("umbral", 0.0), c.get("caida"))
        return [h["texto"] for h in hits]
