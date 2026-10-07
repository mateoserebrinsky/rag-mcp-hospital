"""Recalcula con atencion.py el bloque de transformer de a_mano/ejercicio.md, para contrastar las cuentas de solucion.md.

    python a_mano/verificar.py
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from atencion import atencion, layer_norm, softmax  # noqa: E402

np.set_printoptions(precision=3, suppress=True)

VOCAB = ["El", "banco", "aguanta", "presta", "peso", "dinero"]
E = {"El": [0, 0, 0, 1], "banco": [1, 1, 0, 0], "aguanta": [1, 0, 1, 0], "presta": [0, 1, 1, 0],
     "peso": [1, 0, 0, 0], "dinero": [0, 1, 0, 0]}
P = np.array([[0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 0, 2]], float)
I = np.eye(4)
Wk = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0]], float)
W1 = np.array([[1, -1, 0, 0], [-1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], float)
Wout = np.array([[0, 0, 0, 0, 2, 0], [0, 0, 0, 0, 0, 2], [0, 0, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0]], float)


def bloque(frase, mascara):
    X = np.array([E[w] for w in frase], float) + P
    Q, K, V = X @ I, X @ Wk, X @ I
    S = Q @ K.T
    out, A = atencion(Q, K, V, mascara)
    Z = X + out @ I
    LNZ = layer_norm(Z)
    FFN = np.maximum(LNZ @ W1, 0) @ I
    H = Z + FFN
    LNH = layer_norm(H)
    logits = LNH[-1] @ Wout
    return dict(X=X, Q=Q, K=K, V=V, S=S, Sd=S / 2, A=A, AV=out, Z=Z, LNZ=LNZ, FFN=FFN, H=H, LNH=LNH,
                logits=logits, prob=softmax(logits[None])[0])


if __name__ == "__main__":
    for frase in (["El", "banco", "aguanta"], ["El", "banco", "presta"]):
        for mascara in (True, False):
            print("=" * 70)
            print(" ".join(frase), "| con máscara causal (decoder)" if mascara else "| sin máscara (encoder)")
            r = bloque(frase, mascara)
            for k, v in r.items():
                print(f"\n{k}:\n{v}")
            if mascara:
                print("\npredicción:", {w: round(float(p), 3) for w, p in zip(VOCAB, r["prob"])})
            print("fila de 'banco' en LN(Z):", r["LNZ"][1])
