"""Tabla Markdown de experimentos a partir de los .eval.json de experimentos/.

    python experimentos/tabla.py > experimentos/tabla.md
"""
import json
from pathlib import Path

ENCODERS = {"bert": "BERT multilingüe (línea de base)", "minilm": "paraphrase-multilingual-MiniLM-L12-v2",
            "e5s": "multilingual-e5-small", "e5b": "multilingual-e5-base"}
CHUNKINGS = {"sec": "secciones", "secmeta": "secciones + título", "v300": "ventanas 300/60", "v500": "ventanas 500/100"}


def fila(ruta):
    enc, chunk, *corte = ruta.name.removesuffix(".jsonl.eval.json").split("__")
    r = json.loads(ruta.read_text(encoding="utf-8"))["resumen"]
    corte = {"k": corte[0][1:], "u": "0", "c": "-"} | {p[0]: p[1:] for p in corte[1:]}
    corte["c"] = corte["c"].removeprefix("aida")
    return (r["context_relevance"], f"| {ENCODERS[enc]} | {CHUNKINGS[chunk]} | {corte['k']} | {corte['u']} | {corte['c']} | "
            f"{r['recall']:.3f} | {r['precision']:.3f} | **{r['context_relevance']:.3f}** | `{ruta.name.removesuffix('.jsonl.eval.json')}` |")


if __name__ == "__main__":
    filas = sorted((fila(p) for p in Path(__file__).parent.glob("*.eval.json")), key=lambda f: -f[0])
    print("| Encoder | Chunking | top-k | umbral | caída | recall | precision | context_relevance | archivo |")
    print("|---|---|---|---|---|---|---|---|---|")
    print("\n".join(f[1] for f in filas))
