# -*- coding: utf-8 -*-
"""Base comum aos Page Objects: espera explícita e ações simples."""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

URL_BASE = "https://the-internet.herokuapp.com"
TEMPO_LIMITE = 10  # segundos


class BasePage:
    """Guarda o driver e centraliza as esperas.

    Não há `time.sleep` nem espera implícita em lugar nenhum do projeto: toda
    ação espera uma condição concreta (elemento visível, clicável, alerta
    aberto). É isso que evita o teste que passa na máquina e falha no CI.
    """

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.espera = WebDriverWait(driver, TEMPO_LIMITE)

    def abrir(self, caminho: str = "/") -> None:
        self.driver.get(f"{URL_BASE}{caminho}")

    @property
    def url_atual(self) -> str:
        return self.driver.current_url

    def esperar_visivel(self, localizador: tuple) -> WebElement:
        return self.espera.until(EC.visibility_of_element_located(localizador))

    def esperar_clicavel(self, localizador: tuple) -> WebElement:
        return self.espera.until(EC.element_to_be_clickable(localizador))

    def clicar(self, localizador: tuple) -> None:
        self.esperar_clicavel(localizador).click()

    def digitar(self, localizador: tuple, texto: str) -> None:
        campo = self.esperar_visivel(localizador)
        campo.clear()
        campo.send_keys(texto)

    def texto_de(self, localizador: tuple) -> str:
        return self.esperar_visivel(localizador).text.strip()
