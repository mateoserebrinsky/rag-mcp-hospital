"""Las seis herramientas del asistente, en un solo lugar.

agente.py las envuelve con @function_tool y servidor_mcp.py con @mcp.tool(). Las descripciones que ve el
modelo (docstrings) viven en DESCRIPCIONES para que los dos frameworks muestren exactamente lo mismo.
Todas devuelven texto.
"""
import json
import os
import urllib.error
import urllib.parse
import urllib.request

API = os.environ.get("HOSPITAL_API", "http://localhost:8765")

_recuperador = None


def _get_recuperador():
    global _recuperador
    if _recuperador is None:
        from rag.recuperador import Recuperador
        _recuperador = Recuperador()
    return _recuperador


def _api(ruta, **params):
    url = f"{API}{ruta}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            return r.read().decode("utf-8")
    except urllib.error.HTTPError as e:  # 400/404 traen las opciones validas en el cuerpo
        return e.read().decode("utf-8")
    except Exception as e:
        return json.dumps({"error": f"no se pudo consultar la API del hospital: {e}"}, ensure_ascii=False)


def buscar_documentos(consulta: str) -> str:
    fragmentos = _get_recuperador().recuperar(consulta)
    return "\n\n---\n\n".join(fragmentos) if fragmentos else "No se encontraron documentos relevantes."


def consultar_camas(sector: str) -> str:
    return _api("/camas", sector=sector)


def consultar_guardia(especialidad: str) -> str:
    return _api("/guardia", especialidad=especialidad)


def consultar_turnos(especialidad: str) -> str:
    return _api("/turnos", especialidad=especialidad)


def consultar_farmacia(medicamento: str) -> str:
    return _api("/farmacia", medicamento=medicamento)


def consultar_espera() -> str:
    return _api("/espera")


DESCRIPCIONES = {
    "buscar_documentos": (
        "Busca en los documentos del hospital (normas y procedimientos que casi no cambian): horarios y reglas de "
        "visita, preparación para estudios y ayunos, documentación para turnos, derechos del paciente, "
        "coberturas, alta, internación, guardia y triage, vacunatorio, farmacia, etc. Usala para cualquier "
        "pregunta sobre CÓMO funciona algo, QUÉ hay que hacer o QUÉ se necesita. NO tiene datos del día (camas, "
        "turnos, stock). Argumento: `consulta`, la pregunta o los términos clave en español."),
    "consultar_camas": (
        "Consulta en vivo cuántas camas hay en un sector del hospital: total, ocupadas y libres hoy. "
        "Usala cuando pregunten si hay lugar o camas disponibles. Argumento: `sector` (por ejemplo "
        "'pediatria', 'terapia intensiva', 'clinica medica', 'maternidad'). Si el nombre no existe devuelve las "
        "opciones válidas."),
    "consultar_guardia": (
        "Consulta en vivo qué profesionales están de guardia hoy en una especialidad y en qué horario. "
        "Usala cuando pregunten quién atiende hoy o si hay un médico de guardia. Argumento: `especialidad` "
        "(por ejemplo 'pediatria', 'cardiologia', 'traumatologia'). Si el nombre no existe devuelve las opciones "
        "válidas."),
    "consultar_turnos": (
        "Consulta en vivo los próximos turnos disponibles (fecha y hora) de una especialidad. Usala cuando "
        "pregunten cuándo hay turno o por la disponibilidad de turnos. No explica cómo se saca un turno ni qué "
        "documentos llevar (eso está en los documentos). Argumento: `especialidad`. Si el nombre no existe "
        "devuelve las opciones válidas."),
    "consultar_farmacia": (
        "Consulta en vivo el stock de un medicamento en la farmacia del hospital y, si no hay, la fecha de "
        "reposición. Usala cuando pregunten si hay un medicamento hoy. Argumento: `medicamento`, el nombre "
        "con su dosis si la tiene (por ejemplo 'enalapril 10 mg'). Si el nombre no existe devuelve las opciones "
        "válidas."),
    "consultar_espera": (
        "Consulta en vivo cuántos minutos de espera hay hoy en la guardia, por nivel de triage (rojo, naranja, "
        "amarillo, verde, azul). Usala cuando pregunten cuánto se demora la atención en la guardia ahora. No "
        "recibe argumentos. Cómo funciona el triage y qué significa cada color está en los documentos."),
}

FUNCIONES = {
    "buscar_documentos": buscar_documentos,
    "consultar_camas": consultar_camas,
    "consultar_guardia": consultar_guardia,
    "consultar_turnos": consultar_turnos,
    "consultar_farmacia": consultar_farmacia,
    "consultar_espera": consultar_espera,
}
