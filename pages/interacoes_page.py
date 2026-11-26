# -*- coding: utf-8 -*-
"""Interações que exigem recursos específicos do Selenium: alertas, frames, janelas, espera dinâmica, upload e menu de contexto."""

import urllib.error
import urllib.request
from pathlib import Path

from selenium.webdriver import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import URL_BASE, BasePage


class AlertasPage(BasePage):
    ALERTA = (By.CSS_SELECTOR, "button[onclick='jsAlert()']")
    CONFIRMACAO = (By.CSS_SELECTOR, "button[onclick='jsConfirm()']")
    PERGUNTA = (By.CSS_SELECTOR, "button[onclick='jsPrompt()']")
    RESULTADO = (By.ID, "result")

    def abrir_pagina(self) -> None:
        self.abrir("/javascript_alerts")

    def _alerta_aberto(self) -> Alert:
        return self.espera.until(EC.alert_is_present())

    def disparar_alerta(self) -> Alert:
        self.clicar(self.ALERTA)
        return self._alerta_aberto()

    def disparar_confirmacao(self) -> Alert:
        self.clicar(self.CONFIRMACAO)
        return self._alerta_aberto()

    def disparar_pergunta(self) -> Alert:
        self.clicar(self.PERGUNTA)
        return self._alerta_aberto()

    def resultado(self) -> str:
        return self.texto_de(self.RESULTADO)


class FramesPage(BasePage):
    def abrir_pagina(self) -> None:
        self.abrir("/nested_frames")

    def texto_do_quadro(self, *caminho: str) -> str:
        """Entra nos quadros na ordem dada, lê o corpo e volta para a página principal.

        O Selenium só enxerga o que está no quadro em que o driver está. Por
        isso o `finally`: se a leitura falhar, o driver não fica preso lá dentro.
        """
        self.driver.switch_to.default_content()
        try:
            for nome in caminho:
                self.espera.until(EC.frame_to_be_available_and_switch_to_it(nome))
            return self.driver.find_element(By.TAG_NAME, "body").text.strip()
        finally:
            self.driver.switch_to.default_content()


class JanelasPage(BasePage):
    LINK = (By.LINK_TEXT, "Click Here")
    TITULO = (By.TAG_NAME, "h3")

    def abrir_pagina(self) -> None:
        self.abrir("/windows")

    def abrir_nova_janela(self) -> str:
        """Clica no link, espera a segunda aba e passa o foco para ela. Devolve a aba original."""
        original = self.driver.current_window_handle
        self.clicar(self.LINK)
        self.espera.until(EC.number_of_windows_to_be(2))
        nova = next(h for h in self.driver.window_handles if h != original)
        self.driver.switch_to.window(nova)
        return original

    def titulo_da_pagina(self) -> str:
        return self.texto_de(self.TITULO)

    def voltar_para(self, aba: str) -> None:
        self.driver.close()
        self.driver.switch_to.window(aba)


class CarregamentoDinamicoPage(BasePage):
    INICIAR = (By.CSS_SELECTOR, "#start button")
    RESULTADO = (By.ID, "finish")

    def abrir_exemplo(self, numero: int) -> None:
        self.abrir(f"/dynamic_loading/{numero}")

    def resultado_existe_no_html(self) -> bool:
        return bool(self.driver.find_elements(*self.RESULTADO))

    def resultado_esta_visivel(self) -> bool:
        encontrados = self.driver.find_elements(*self.RESULTADO)
        return bool(encontrados) and encontrados[0].is_displayed()

    def iniciar(self) -> str:
        """Clica em Start e espera o texto aparecer (a página leva alguns segundos)."""
        self.clicar(self.INICIAR)
        return self.texto_de(self.RESULTADO)


class UploadPage(BasePage):
    CAMPO = (By.ID, "file-upload")
    ENVIAR = (By.ID, "file-submit")
    TITULO = (By.TAG_NAME, "h3")
    ARQUIVO_ENVIADO = (By.ID, "uploaded-files")

    def abrir_pagina(self) -> None:
        self.abrir("/upload")

    def enviar(self, arquivo: Path) -> None:
        # Em um <input type="file"> não se clica: manda-se o caminho do arquivo.
        self.driver.find_element(*self.CAMPO).send_keys(str(arquivo))
        self.clicar(self.ENVIAR)

    def titulo(self) -> str:
        return self.texto_de(self.TITULO)

    def nome_do_arquivo(self) -> str:
        return self.texto_de(self.ARQUIVO_ENVIADO)


class AutenticacaoBasicaPage(BasePage):
    CORPO = (By.TAG_NAME, "body")

    def abrir_com_credenciais(self, usuario: str, senha: str) -> None:
        # A autenticação HTTP básica é um diálogo do navegador, fora do HTML:
        # o Selenium não o enxerga. O caminho é mandar a credencial na própria URL.
        self.driver.get(URL_BASE.replace("https://", f"https://{usuario}:{senha}@") + "/basic_auth")

    @staticmethod
    def status_sem_credenciais() -> int:
        """Status HTTP de /basic_auth sem credencial.

        Limite do Chrome: ao recusar o diálogo de login ele mostra uma página
        vazia, mesmo que o servidor tenha mandado o corpo "Not authorized". O
        Selenium só vê o HTML da tela, então o 401 é conferido por HTTP direto.
        """
        try:
            with urllib.request.urlopen(f"{URL_BASE}/basic_auth", timeout=15) as resposta:
                return resposta.status
        except urllib.error.HTTPError as erro:
            return erro.code

    def texto(self) -> str:
        return self.texto_de(self.CORPO)


class MenuDeContextoPage(BasePage):
    AREA = (By.ID, "hot-spot")

    def abrir_pagina(self) -> None:
        self.abrir("/context_menu")

    def clicar_com_o_botao_direito(self) -> Alert:
        area = self.esperar_visivel(self.AREA)
        ActionChains(self.driver).context_click(area).perform()
        return self.espera.until(EC.alert_is_present())
