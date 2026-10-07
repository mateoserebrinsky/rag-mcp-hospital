"""Indice vectorial del corpus: chunking + encoder + busqueda por coseno."""
import hashlib
import json
from pathlib import Path

import numpy as np

from rag.chunking import chunk_secciones, chunk_ventanas
from rag.encoders import cargar_encoder

RAIZ = Path(__file__).resolve().parent.parent
CORPUS = RAIZ / "datos" / "corpus"
CACHE = RAIZ / ".cache"


def seleccionar(sims, k, umbral, caida=None):
    """Indices de los fragmentos a devolver: top-k, coseno >= umbral y, opcionalmente, corte por caida.

    `caida`: se descarta un fragmento cuya similitud queda mas de `caida` por debajo de la del primero.
    Siempre devuelve al menos el mejor.
    """
    orden = [int(i) for i in np.argsort(-sims)[:k]]
    mejor = sims[orden[0]]
    elegidos = [i for i in orden if sims[i] >= umbral and (caida is None or mejor - sims[i] <= caida)]
    return elegidos or orden[:1]


def construir_chunks(chunking):
    """chunking: {"modo": "secciones"|"ventanas", "tamano", "solape", "metadatos": bool}."""
    chunks = []
    for ruta in sorted(CORPUS.glob("*.md")):
        texto = ruta.read_text(encoding="utf-8")
        if chunking["modo"] == "secciones":
            partes = chunk_secciones(texto, ruta.stem)
        else:
            partes = chunk_ventanas(texto, ruta.stem, chunking.get("tamano", 400), chunking.get("solape", 80))
        chunks.extend(partes)
    return chunks


def texto_a_codificar(chunk, metadatos):
    if not metadatos:
        return chunk["texto"]
    cabecera = chunk["titulo"] + (f" - {chunk['seccion']}" if chunk["seccion"] else "")
    return f"{cabecera}\n{chunk['texto']}"


class Indice:
    def __init__(self, encoder, chunking):
        self.nombre_encoder = encoder
        self.enc = cargar_encoder(encoder)
        self.chunking = chunking
        self.chunks = construir_chunks(chunking)
        textos = [self.enc.prefijo_pasaje + texto_a_codificar(c, chunking.get("metadatos", False)) for c in self.chunks]
        self.vectores = self._vectores(textos)

    def _vectores(self, textos):
        clave = hashlib.sha1(json.dumps([self.nombre_encoder, textos], ensure_ascii=False).encode()).hexdigest()
        archivo = CACHE / f"{clave}.npy"
        if archivo.exists():
            return np.load(archivo)
        V = self.enc.codificar(textos)
        CACHE.mkdir(exist_ok=True)
        np.save(archivo, V)
        return V

    def similitudes(self, consulta):
        q = self.enc.codificar([self.enc.prefijo_consulta + consulta])[0]
        return self.vectores @ q

    def buscar(self, consulta, k=3, umbral=0.0, caida=None):
        sims = self.similitudes(consulta)
        return [{**self.chunks[i], "similitud": float(sims[i])} for i in seleccionar(sims, k, umbral, caida)]
