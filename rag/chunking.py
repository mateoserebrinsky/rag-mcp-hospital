"""Corte de los documentos Markdown del corpus en fragmentos."""
import re


def _partes(texto):
    """Devuelve (titulo, [(seccion, cuerpo), ...]) a partir de un Markdown con # y ##."""
    titulo = ""
    secciones = [("", [])]
    for linea in texto.splitlines():
        if linea.startswith("## "):
            secciones.append((linea[3:].strip(), []))
        elif linea.startswith("# ") and not titulo:
            titulo = linea[2:].strip()
        else:
            secciones[-1][1].append(linea)
    return titulo, [(s, "\n".join(c).strip()) for s, c in secciones]


def chunk_secciones(texto, doc):
    """Un fragmento por seccion (##). El texto previo al primer ## es un fragmento sin seccion."""
    titulo, secciones = _partes(texto)
    return [{"doc": doc, "titulo": titulo, "seccion": s, "texto": cuerpo}
            for s, cuerpo in secciones if cuerpo]


def chunk_ventanas(texto, doc, tamano=400, solape=80):
    """Ventanas de hasta `tamano` caracteres, cortadas en espacios, con `solape` caracteres de solapamiento."""
    titulo, secciones = _partes(texto)
    cuerpo = re.sub(r"\s+", " ", " ".join(c for _, c in secciones)).strip()
    chunks, ini = [], 0
    while ini < len(cuerpo):
        fin = min(ini + tamano, len(cuerpo))
        if fin < len(cuerpo):
            corte = cuerpo.rfind(" ", ini + tamano // 2, fin)
            fin = corte if corte > ini else fin
        chunks.append({"doc": doc, "titulo": titulo, "seccion": "", "texto": cuerpo[ini:fin].strip()})
        if fin >= len(cuerpo):
            break
        sig = fin - solape
        espacio = cuerpo.find(" ", sig)
        ini = espacio + 1 if 0 <= espacio < fin else fin
    return chunks
