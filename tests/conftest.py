# -*- coding: utf-8 -*-
"""Fixtures compartilhadas e captura de evidência em caso de falha."""

import os
from pathlib import Path

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

EVIDENCIAS = Path(__file__).resolve().parents[1] / "evidencias"


def _opcoes() -> Options:
    opcoes = Options()
    # Sem janela por padrão (CI e máquina local). HEADED=1 abre o navegador
    # para quem quer ver o teste rodando.
    if os.getenv("HEADED") != "1":
        opcoes.add_argument("--headless=new")
    opcoes.add_argument("--window-size=1280,900")
    if os.getenv("CI"):  # o runner do GitHub Actions exige estas duas
        opcoes.add_argument("--no-sandbox")
        opcoes.add_argument("--disable-dev-shm-usage")
    return opcoes


@pytest.fixture
def driver(request):
    """Um navegador novo por teste: nenhum teste herda cookie ou aba do outro.

    O Selenium Manager (embutido no Selenium 4) baixa o chromedriver certo
    para a versão do Chrome instalada, então não há driver para gerenciar à mão.
    """
    navegador = webdriver.Chrome(options=_opcoes())
    yield navegador
    navegador.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Em caso de falha, anexa a evidência ao próprio teste no relatório.

    Tem de ser aqui, e não no teardown da fixture: o Allure guarda anexos do
    teardown no contêiner da fixture, e o print não apareceria no corpo do teste.
    """
    resultado = yield
    relatorio = resultado.get_result()
    if relatorio.when == "call" and relatorio.failed and "driver" in item.funcargs:
        _anexar_evidencia(item.funcargs["driver"], item.name)


def _anexar_evidencia(navegador, nome: str) -> None:
    """Print, URL e HTML no Allure; o print também em disco, em `evidencias/`.

    O arquivo em disco serve a quem roda localmente; o anexo serve a quem só
    vai abrir o relatório publicado. Print que ninguém encontra não é evidência.
    """
    png = navegador.get_screenshot_as_png()
    allure.attach(png, name="print da tela", attachment_type=allure.attachment_type.PNG)
    allure.attach(navegador.current_url, name="URL na falha", attachment_type=allure.attachment_type.TEXT)
    allure.attach(navegador.page_source, name="HTML da página", attachment_type=allure.attachment_type.HTML)
    EVIDENCIAS.mkdir(exist_ok=True)
    seguro = "".join(c if c.isalnum() or c in "-_" else "_" for c in nome)
    (EVIDENCIAS / f"{seguro}.png").write_bytes(png)
