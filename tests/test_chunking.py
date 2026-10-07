from rag.chunking import chunk_secciones, chunk_ventanas

DOC = """# Régimen de visitas

Intro del documento.

## Pediatría

Madre, padre o tutor pueden permanecer las 24 horas.

## Neonatología

Los abuelos pueden visitar martes y jueves.
"""


def test_secciones_una_por_encabezado_con_intro():
    chunks = chunk_secciones(DOC, "visitas")
    assert [c["seccion"] for c in chunks] == ["", "Pediatría", "Neonatología"]
    assert chunks[0]["texto"] == "Intro del documento."
    assert chunks[1]["texto"] == "Madre, padre o tutor pueden permanecer las 24 horas."
    assert all(c["titulo"] == "Régimen de visitas" for c in chunks)
    assert all(c["doc"] == "visitas" for c in chunks)


def test_secciones_no_devuelve_vacios():
    chunks = chunk_secciones("# T\n\n## A\n\n## B\n\ntexto\n", "d")
    assert [c["seccion"] for c in chunks] == ["B"]


def test_ventanas_respetan_tamano_y_solapan():
    texto = " ".join(f"pal{i:03d}" for i in range(60))
    chunks = chunk_ventanas(f"# T\n\n{texto}\n", "d", tamano=150, solape=50)
    assert all(len(c["texto"]) <= 150 for c in chunks)
    assert len(chunks) >= 2
    # el final de un fragmento reaparece al inicio del siguiente
    assert chunks[0]["texto"].split()[-1] in chunks[1]["texto"].split()


def test_ventanas_cubren_todo_el_texto():
    texto = " ".join(f"palabra{i}" for i in range(200))
    chunks = chunk_ventanas(f"# T\n\n{texto}\n", "d", tamano=200, solape=40)
    unido = " ".join(c["texto"] for c in chunks)
    for i in range(200):
        assert f"palabra{i}" in unido
