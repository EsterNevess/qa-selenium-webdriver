# -*- coding: utf-8 -*-
"""Elementos de interface: o que o Selenium precisa fazer de especial em cada um."""

import allure
import pytest
from selenium.webdriver.common.keys import Keys

from pages.elementos_page import (
    AdicionarRemoverPage,
    CheckboxesPage,
    DropdownPage,
    HoversPage,
    TabelasPage,
    TeclasPage,
)


@allure.feature("Elementos")
class TestDropdown:
    @allure.title("A lista começa sem opção escolhida")
    def test_estado_inicial(self, driver):
        pagina = DropdownPage(driver)
        pagina.abrir_pagina()
        assert pagina.opcao_escolhida() == "Please select an option"

    @allure.title("Escolher {opcao}")
    @pytest.mark.parametrize("opcao", ["Option 1", "Option 2"])
    def test_escolher_opcao(self, driver, opcao):
        pagina = DropdownPage(driver)
        pagina.abrir_pagina()
        pagina.escolher(opcao)
        assert pagina.opcao_escolhida() == opcao


@allure.feature("Elementos")
class TestCheckboxes:
    @allure.title("Estado inicial: a primeira desmarcada, a segunda marcada")
    def test_estado_inicial(self, driver):
        pagina = CheckboxesPage(driver)
        pagina.abrir_pagina()
        assert not pagina.marcada(0)
        assert pagina.marcada(1)

    @allure.title("Marcar a primeira e desmarcar a segunda")
    def test_alternar(self, driver):
        pagina = CheckboxesPage(driver)
        pagina.abrir_pagina()
        pagina.alternar(0)
        pagina.alternar(1)
        assert pagina.marcada(0)
        assert not pagina.marcada(1)


@allure.feature("Elementos")
@allure.title("Passar o mouse mostra o nome e o link do usuário {numero}")
@pytest.mark.parametrize("numero", [1, 2, 3])
def test_hover(driver, numero):
    pagina = HoversPage(driver)
    pagina.abrir_pagina()
    legenda = pagina.passar_o_mouse(numero - 1)
    assert legenda["nome"] == f"name: user{numero}"
    assert legenda["link"].endswith(f"/users/{numero}")


@allure.feature("Elementos")
class TestTabelas:
    @allure.title("Clicar no cabeçalho ordena o sobrenome de A a Z, e clicar de novo inverte")
    def test_ordenacao_por_sobrenome(self, driver):
        pagina = TabelasPage(driver)
        pagina.abrir_pagina()
        pagina.ordenar_por("Last Name")
        crescente = pagina.valores_da_coluna(1)
        assert crescente == sorted(crescente)  # a lista inteira, não só o primeiro item
        pagina.ordenar_por("Last Name")
        assert pagina.valores_da_coluna(1) == sorted(crescente, reverse=True)

    @allure.title("A coluna de e-mail da tabela traz endereços válidos")
    def test_emails_tem_arroba(self, driver):
        pagina = TabelasPage(driver)
        pagina.abrir_pagina()
        emails = pagina.valores_da_coluna(3)
        assert emails and all("@" in e for e in emails)


@allure.feature("Elementos")
@allure.title("A tecla {nome} é reconhecida pela página")
# O ENTER fica de fora de propósito: o campo está dentro de um <form>, o Enter o envia e a página recarrega sem o resultado.
@pytest.mark.parametrize(("tecla", "nome"), [(Keys.BACK_SPACE, "BACK_SPACE"), (Keys.ESCAPE, "ESCAPE"), (Keys.SPACE, "SPACE"), ("a", "A")])
def test_teclas(driver, tecla, nome):
    pagina = TeclasPage(driver)
    pagina.abrir_pagina()
    assert pagina.teclar(tecla) == f"You entered: {nome}"


@allure.feature("Elementos")
class TestAdicionarRemover:
    @allure.title("Adicionar três elementos e remover um deixa dois")
    def test_adicionar_e_remover(self, driver):
        pagina = AdicionarRemoverPage(driver)
        pagina.abrir_pagina()
        assert pagina.quantidade() == 0
        pagina.adicionar(3)
        assert pagina.quantidade() == 3
        pagina.remover_primeiro()
        assert pagina.quantidade() == 2

    @allure.title("Remover todos volta ao estado inicial")
    def test_remover_todos(self, driver):
        pagina = AdicionarRemoverPage(driver)
        pagina.abrir_pagina()
        pagina.adicionar(2)
        pagina.remover_primeiro()
        pagina.remover_primeiro()
        assert pagina.quantidade() == 0
