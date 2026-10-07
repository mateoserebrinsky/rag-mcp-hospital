"""Encoders de texto a vectores normalizados.

- BertMeanPool: BERT sin ajustar para similitud, promedio de los tokens de la ultima capa (linea de base).
- SentenceEncoder: modelos entrenados para embeddings de oraciones (sentence-transformers).
"""
import numpy as np

BASE_BERT = "google-bert/bert-base-multilingual-cased"


def _normalizar(M):
    return M / np.clip(np.linalg.norm(M, axis=1, keepdims=True), 1e-12, None)


class BertMeanPool:
    prefijo_consulta = ""
    prefijo_pasaje = ""

    def __init__(self, nombre=BASE_BERT):
        import torch
        from transformers import AutoModel, AutoTokenizer
        self.torch = torch
        self.tok = AutoTokenizer.from_pretrained(nombre)
        self.modelo = AutoModel.from_pretrained(nombre).eval()

    def codificar(self, textos, lote=16):
        torch = self.torch
        salida = []
        for i in range(0, len(textos), lote):
            enc = self.tok(textos[i:i + lote], padding=True, truncation=True, max_length=512, return_tensors="pt")
            with torch.no_grad():
                h = self.modelo(**enc).last_hidden_state
            m = enc["attention_mask"].unsqueeze(-1).to(h.dtype)
            salida.append(((h * m).sum(1) / m.sum(1)).numpy())
        return _normalizar(np.concatenate(salida))


class SentenceEncoder:
    def __init__(self, nombre):
        from sentence_transformers import SentenceTransformer
        self.modelo = SentenceTransformer(nombre, device="cpu")
        self.modelo.max_seq_length = min(self.modelo.max_seq_length or 512, 512)
        e5 = "e5" in nombre.lower()
        self.prefijo_consulta = "query: " if e5 else ""
        self.prefijo_pasaje = "passage: " if e5 else ""

    def codificar(self, textos, lote=16):
        return np.asarray(self.modelo.encode(textos, batch_size=lote, normalize_embeddings=True))


def cargar_encoder(nombre):
    if nombre == BASE_BERT or "bert-base-spanish" in nombre:
        return BertMeanPool(nombre)
    return SentenceEncoder(nombre)
