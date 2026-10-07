"""Barrido de configuraciones de la parte 1. Cada una deja experimentos/<nombre>.jsonl y su .eval.json.

    python experimentos/barrido.py [--encoders a,b] [--solo-nuevos]
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from rag.indice import Indice  # noqa: E402

PREGUNTAS = RAIZ / "datos" / "preguntas_recuperacion_dev.jsonl"
SALIDA = RAIZ / "experimentos"

ENCODERS = {
    "bert": "google-bert/bert-base-multilingual-cased",
    "minilm": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    "e5s": "intfloat/multilingual-e5-small",
    "e5b": "intfloat/multilingual-e5-base",
    "bgem3": "BAAI/bge-m3",
}
CHUNKINGS = {
    "sec": {"modo": "secciones"},
    "secmeta": {"modo": "secciones", "metadatos": True},
    "v300": {"modo": "ventanas", "tamano": 300, "solape": 60},
    "v500": {"modo": "ventanas", "tamano": 500, "solape": 100},
}

def leer_preguntas():
    return [json.loads(l) for l in PREGUNTAS.read_text(encoding="utf-8").splitlines() if l.strip()]


def correr(nombre, indice, k, umbral, caida, preguntas):
    ruta = SALIDA / f"{nombre}.jsonl"
    lineas = []
    for p in preguntas:
        hits = indice.buscar(p["pregunta"], k, umbral, caida)
        lineas.append(json.dumps({"id": p["id"], "fragmentos": [h["texto"] for h in hits]}, ensure_ascii=False))
    ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    subprocess.run([sys.executable, str(RAIZ / "evaluar" / "evaluar.py"), "recuperacion", "--preguntas", str(PREGUNTAS),
                    "--resultados", str(ruta)], check=True, capture_output=True)
    res = json.loads((SALIDA / f"{nombre}.jsonl.eval.json").read_text(encoding="utf-8"))["resumen"]
    print(f"{nombre:45s} CR {res['context_relevance']:.3f}  R {res['recall']:.3f}  P {res['precision']:.3f}  k {res['k']:.2f}", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--encoders", default=",".join(ENCODERS))
    ap.add_argument("--chunkings", default=",".join(CHUNKINGS))
    ap.add_argument("--umbrales", default="0,0.5,0.7", help="umbrales de coseno a probar con k=3")
    ap.add_argument("--caidas", default="0.05,0.1", help="caidas relativas a probar con k=3")
    args = ap.parse_args()
    preguntas = leer_preguntas()
    SALIDA.mkdir(exist_ok=True)
    for e in args.encoders.split(","):
        for c in args.chunkings.split(","):
            indice = Indice(ENCODERS[e], CHUNKINGS[c])
            base = f"{e}__{c}"
            for k in (1, 2, 3, 5):
                correr(f"{base}__k{k}", indice, k, 0.0, None, preguntas)
            for u in args.umbrales.split(","):
                if float(u) > 0:
                    correr(f"{base}__k3__u{u}", indice, 3, float(u), None, preguntas)
            for d in args.caidas.split(","):
                correr(f"{base}__k3__caida{d}", indice, 3, 0.0, float(d), preguntas)


if __name__ == "__main__":
    main()
