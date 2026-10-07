import numpy as np

from rag.indice import seleccionar


def test_top_k_ordena_por_similitud():
    sims = np.array([0.2, 0.9, 0.5])
    assert seleccionar(sims, k=2, umbral=0.0) == [1, 2]


def test_umbral_descarta_pero_deja_al_menos_uno():
    sims = np.array([0.2, 0.3, 0.1])
    assert seleccionar(sims, k=3, umbral=0.9) == [1]


def test_umbral_filtra_los_bajos():
    sims = np.array([0.8, 0.7, 0.3])
    assert seleccionar(sims, k=3, umbral=0.5) == [0, 1]


def test_caida_relativa_corta_cuando_baja_mucho():
    sims = np.array([0.9, 0.85, 0.5])
    assert seleccionar(sims, k=3, umbral=0.0, caida=0.1) == [0, 1]
