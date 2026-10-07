import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

import herramientas


class _Fake(BaseHTTPRequestHandler):
    visto = []

    def do_GET(self):
        _Fake.visto.append(self.path)
        if "malo" in self.path:
            code, cuerpo = 404, {"error": "no existe", "opciones": ["pediatria"]}
        else:
            code, cuerpo = 200, {"datos": {"libres": 3}}
        data = json.dumps(cuerpo).encode()
        self.send_response(code)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *a):
        pass


@pytest.fixture
def api(monkeypatch):
    srv = HTTPServer(("localhost", 0), _Fake)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    monkeypatch.setattr(herramientas, "API", f"http://localhost:{srv.server_port}")
    _Fake.visto.clear()
    yield
    srv.shutdown()


def test_camas_arma_la_url_con_parametro_codificado(api):
    out = herramientas.consultar_camas("terapia intensiva")
    assert json.loads(out) == {"datos": {"libres": 3}}
    assert _Fake.visto == ["/camas?sector=terapia+intensiva"]


def test_espera_no_lleva_parametros(api):
    herramientas.consultar_espera()
    assert _Fake.visto == ["/espera"]


def test_error_de_la_api_vuelve_como_texto_con_opciones(api):
    out = herramientas.consultar_guardia("malo")
    assert "opciones" in out and "pediatria" in out


def test_api_caida_devuelve_mensaje_en_vez_de_excepcion(monkeypatch):
    monkeypatch.setattr(herramientas, "API", "http://localhost:1")
    assert "no se pudo" in herramientas.consultar_espera().lower()
