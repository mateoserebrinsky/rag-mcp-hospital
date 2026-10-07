"""Parte 1. Uso:

    python3 recuperar.py --preguntas datos/preguntas_recuperacion_dev.jsonl --salida resultados.jsonl

La configuracion (encoder, chunking, top-k, umbral) esta fija en rag/config.json.
"""
import argparse
import json
from pathlib import Path

from rag.recuperador import Recuperador


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preguntas", required=True)
    ap.add_argument("--salida", required=True)
    args = ap.parse_args()
    rec = Recuperador()
    lineas = []
    for linea in Path(args.preguntas).read_text(encoding="utf-8").splitlines():
        if linea.strip():
            p = json.loads(linea)
            lineas.append(json.dumps({"id": p["id"], "fragmentos": rec.recuperar(p["pregunta"])}, ensure_ascii=False))
    Path(args.salida).write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print(f"{len(lineas)} preguntas -> {args.salida}")


if __name__ == "__main__":
    main()
