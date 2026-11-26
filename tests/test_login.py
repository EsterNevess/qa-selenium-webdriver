# -*- coding: utf-8 -*-
"""Login: o fluxo mais importante de qualquer sistema."""

import allure
import pytest

from pages.login_page import LoginPage

USUARIO = "tomsmith"
SENHA = "SuperSecretPassword!"


@allure.feature("Login")
@allure.title("Credenciais válidas levam à área segura")
def test_login_valido(driver):
    pagina = LoginPage(driver)
    pagina.abrir_login()
    pagina.entrar(USUARIO, SENHA)
    assert pagina.mensagem() == "You logged into a secure area!"
    assert pagina.url_atual.endswith("/secure")


@allure.feature("Login")
@allure.title("Credenciais inválidas são recusadas: {usuario!r} / {senha!r}")
@pytest.mark.parametrize(
    ("usuario", "senha", "esperado"),
    [
        ("usuario-que-nao-existe", SENHA, "Your username is invalid!"),
        (USUARIO, "senha-errada", "Your password is invalid!"),
        ("", "", "Your username is invalid!"),
    ],
)
def test_login_invalido(driver, usuario, senha, esperado):
    pagina = LoginPage(driver)
    pagina.abrir_login()
    pagina.entrar(usuario, senha)
    assert pagina.mensagem() == esperado
    assert pagina.url_atual.endswith("/login")


@allure.feature("Login")
@allure.title("Sair volta para o login e avisa o usuário")
def test_logout(driver):
    pagina = LoginPage(driver)
    pagina.abrir_login()
    pagina.entrar(USUARIO, SENHA)
    pagina.sair()
    assert pagina.mensagem() == "You logged out of the secure area!"
    assert pagina.url_atual.endswith("/login")
