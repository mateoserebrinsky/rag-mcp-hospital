"""Capa de atencion del transformer, solo con NumPy (parte 4)."""
import numpy as np


def softmax(M):
    """Softmax por fila (ultimo eje), estable: resta el maximo antes de exponenciar."""
    M = np.asarray(M, dtype=float)
    e = np.exp(M - M.max(axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)


def atencion(Q, K, V, mascara=False):
    """softmax(Q K^T / sqrt(d_k)) V. Devuelve (salida, A)."""
    d_k = K.shape[-1]
    S = Q @ K.T / np.sqrt(d_k)
    if mascara:
        S = np.where(np.triu(np.ones(S.shape, dtype=bool), k=1), -np.inf, S)
    A = softmax(S)
    return A @ V, A


def autoatencion(X, Wq, Wk, Wv, mascara=False):
    """Proyecta X a Q, K, V y aplica atencion. Devuelve (salida, A)."""
    return atencion(X @ Wq, X @ Wk, X @ Wv, mascara)


def multicabeza(X, cabezas, Wo, mascara=False):
    """Concatena la salida de cada cabeza (Wq, Wk, Wv) y la proyecta con Wo."""
    salidas = [autoatencion(X, Wq, Wk, Wv, mascara)[0] for Wq, Wk, Wv in cabezas]
    return np.concatenate(salidas, axis=-1) @ Wo


def layer_norm(x, eps=1e-5):
    """Normaliza cada fila a media 0 y varianza 1."""
    x = np.asarray(x, dtype=float)
    media = x.mean(axis=-1, keepdims=True)
    var = x.var(axis=-1, keepdims=True)
    return (x - media) / np.sqrt(var + eps)
