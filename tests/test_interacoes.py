# -*- coding: utf-8 -*-
"""Interações que só o Selenium resolve com recursos próprios."""

import allure
import pytest

from pages.interacoes_page import (
    AlertasPage,
    AutenticacaoBasicaPage,
    CarregamentoDinamicoPage,
    FramesPage,
    JanelasPage,
    MenuDeContextoPage,
    UploadPage,
)


@allure.feature("Alertas JavaScript")
class TestAlertas:
    @allure.title("Alerta simples: o texto aparece e o OK é registrado")
    def test_alerta(self, driver):
        pagina = AlertasPage(driver)
        pagina.abrir_pagina()
        alerta = pagina.disparar_alerta()
        assert alerta.text == "I am a JS Alert"
        alerta.accept()
        assert pagina.resultado() == "You successfully clicked an alert"

    @allure.title("Confirmação: aceitar e cancelar dão resultados diferentes")
    @pytest.mark.parametrize(("acao", "esperado"), [("accept", "You clicked: Ok"), ("dismiss", "You clicked: Cancel")])
    def test_confirmacao(self, driver, acao, esperado):
        pagina = AlertasPage(driver)
        pagina.abrir_pagina()
        getattr(pagina.disparar_confirmacao(), acao)()
        assert pagina.resultado() == esperado

    @allure.title("Pergunta: o texto digitado volta na página")
    def test_pergunta_com_texto(self, driver):
        pagina = AlertasPage(driver)
        pagina.abrir_pagina()
        alerta = pagina.disparar_pergunta()
        alerta.send_keys("Ester")
        alerta.accept()
        assert pagina.resultado() == "You entered: Ester"

    @allure.title("Pergunta cancelada não envia nada")
    def test_pergunta_cancelada(self, driver):
        pagina = AlertasPage(driver)
        pagina.abrir_pagina()
        pagina.disparar_pergunta().dismiss()
        assert pagina.resultado() == "You entered: null"


@allure.feature("Frames")
class TestFrames:
    @allure.title("Quadro aninhado: topo, depois meio")
    def test_quadro_do_meio(self, driver):
        pagina = FramesPage(driver)
        pagina.abrir_pagina()
        assert pagina.texto_do_quadro("frame-top", "frame-middle") == "MIDDLE"

    @allure.title("Quadro de baixo, sem relação com o do topo")
    def test_quadro_de_baixo(self, driver):
        pagina = FramesPage(driver)
        pagina.abrir_pagina()
        assert pagina.texto_do_quadro("frame-bottom") == "BOTTOM"


@allure.feature("Janelas")
@allure.title("Abrir uma nova aba, ler nela e voltar para a original")
def test_nova_janela(driver):
    pagina = JanelasPage(driver)
    pagina.abrir_pagina()
    original = pagina.abrir_nova_janela()
    assert pagina.titulo_da_pagina() == "New Window"
    pagina.voltar_para(original)
    assert pagina.titulo_da_pagina() == "Opening a new window"
    assert len(driver.window_handles) == 1


@allure.feature("Espera dinâmica")
class TestCarregamentoDinamico:
    @allure.title("Exemplo 1: o elemento já está no HTML, mas escondido")
    def test_elemento_escondido(self, driver):
        pagina = CarregamentoDinamicoPage(driver)
        pagina.abrir_exemplo(1)
        assert pagina.resultado_existe_no_html()
        assert not pagina.resultado_esta_visivel()
        assert pagina.iniciar() == "Hello World!"

    @allure.title("Exemplo 2: o elemento só passa a existir depois do carregamento")
    def test_elemento_criado_depois(self, driver):
        pagina = CarregamentoDinamicoPage(driver)
        pagina.abrir_exemplo(2)
        assert not pagina.resultado_existe_no_html()
        assert pagina.iniciar() == "Hello World!"
        assert pagina.resultado_existe_no_html()


@allure.feature("Upload")
@allure.title("Enviar um arquivo e ver o nome na página")
def test_upload(driver, tmp_path):
    arquivo = tmp_path / "exemplo-selenium.txt"
    arquivo.write_text("arquivo de teste", encoding="utf-8")
    pagina = UploadPage(driver)
    pagina.abrir_pagina()
    pagina.enviar(arquivo)
    assert pagina.titulo() == "File Uploaded!"
    assert pagina.nome_do_arquivo() == arquivo.name


@allure.feature("Autenticação")
class TestAutenticacaoBasica:
    @allure.title("Com a credencial na URL, o acesso é liberado")
    def test_com_credencial(self, driver):
        pagina = AutenticacaoBasicaPage(driver)
        pagina.abrir_com_credenciais("admin", "admin")
        assert "Congratulations! You must have the proper credentials." in pagina.texto()

    @allure.title("Sem credencial, o servidor responde 401")
    def test_sem_credencial(self):
        assert AutenticacaoBasicaPage.status_sem_credenciais() == 401


@allure.feature("Menu de contexto")
@allure.title("Clique com o botão direito abre o alerta da página")
def test_menu_de_contexto(driver):
    pagina = MenuDeContextoPage(driver)
    pagina.abrir_pagina()
    alerta = pagina.clicar_com_o_botao_direito()
    assert alerta.text == "You selected a context menu"
    alerta.accept()
