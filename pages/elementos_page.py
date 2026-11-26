# -*- coding: utf-8 -*-
"""Elementos de formulário e de interface: lista suspensa, caixas de marcar, tabelas, hover, teclas e adicionar/remover."""

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class DropdownPage(BasePage):
    LISTA = (By.ID, "dropdown")

    def abrir_pagina(self) -> None:
        self.abrir("/dropdown")

    def escolher(self, texto: str) -> None:
        Select(self.esperar_visivel(self.LISTA)).select_by_visible_text(texto)

    def opcao_escolhida(self) -> str:
        return Select(self.esperar_visivel(self.LISTA)).first_selected_option.text


class CheckboxesPage(BasePage):
    CAIXAS = (By.CSS_SELECTOR, "#checkboxes input[type='checkbox']")

    def abrir_pagina(self) -> None:
        self.abrir("/checkboxes")

    def caixa(self, posicao: int):
        self.esperar_visivel(self.CAIXAS)
        return self.driver.find_elements(*self.CAIXAS)[posicao]

    def alternar(self, posicao: int) -> None:
        self.caixa(posicao).click()

    def marcada(self, posicao: int) -> bool:
        return self.caixa(posicao).is_selected()


class HoversPage(BasePage):
    FIGURAS = (By.CSS_SELECTOR, ".figure")

    def abrir_pagina(self) -> None:
        self.abrir("/hovers")

    def passar_o_mouse(self, posicao: int) -> dict:
        """Passa o mouse sobre o usuário e devolve o que apareceu embaixo da foto."""
        self.esperar_visivel(self.FIGURAS)
        figura = self.driver.find_elements(*self.FIGURAS)[posicao]
        ActionChains(self.driver).move_to_element(figura).perform()
        legenda = figura.find_element(By.CSS_SELECTOR, ".figcaption")
        self.espera.until(lambda _: legenda.is_displayed())
        return {
            "nome": legenda.find_element(By.TAG_NAME, "h5").text,
            "link": legenda.find_element(By.TAG_NAME, "a").get_attribute("href"),
        }


class TabelasPage(BasePage):
    TABELA = (By.ID, "table1")

    def abrir_pagina(self) -> None:
        self.abrir("/tables")

    def ordenar_por(self, coluna: str) -> None:
        self.clicar((By.XPATH, f"//table[@id='table1']//th/span[text()='{coluna}']"))

    def valores_da_coluna(self, posicao: int) -> list[str]:
        """Valores da coluna (1 = primeira) na ordem em que aparecem na tela."""
        self.esperar_visivel(self.TABELA)
        celulas = self.driver.find_elements(By.CSS_SELECTOR, f"#table1 tbody tr td:nth-of-type({posicao})")
        return [c.text for c in celulas]


class TeclasPage(BasePage):
    CAMPO = (By.ID, "target")
    RESULTADO = (By.ID, "result")

    def abrir_pagina(self) -> None:
        self.abrir("/key_presses")

    def teclar(self, tecla: str) -> str:
        self.esperar_visivel(self.CAMPO).send_keys(tecla)
        return self.texto_de(self.RESULTADO)


class AdicionarRemoverPage(BasePage):
    ADICIONAR = (By.CSS_SELECTOR, "button[onclick='addElement()']")
    BOTOES_REMOVER = (By.CSS_SELECTOR, ".added-manually")

    def abrir_pagina(self) -> None:
        self.abrir("/add_remove_elements/")

    def adicionar(self, quantidade: int = 1) -> None:
        for _ in range(quantidade):
            self.clicar(self.ADICIONAR)

    def remover_primeiro(self) -> None:
        self.clicar(self.BOTOES_REMOVER)

    def quantidade(self) -> int:
        return len(self.driver.find_elements(*self.BOTOES_REMOVER))
