# -*- coding: utf-8 -*-
"""Página de login e área segura."""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    USUARIO = (By.ID, "username")
    SENHA = (By.ID, "password")
    ENTRAR = (By.CSS_SELECTOR, "button[type='submit']")
    MENSAGEM = (By.ID, "flash")
    SAIR = (By.CSS_SELECTOR, "a.button.secondary")

    def abrir_login(self) -> None:
        self.abrir("/login")

    def entrar(self, usuario: str, senha: str) -> None:
        self.digitar(self.USUARIO, usuario)
        self.digitar(self.SENHA, senha)
        self.clicar(self.ENTRAR)

    def sair(self) -> None:
        self.clicar(self.SAIR)

    def mensagem(self) -> str:
        """Texto do aviso, sem o "×" do botão de fechar que vem junto."""
        return self.texto_de(self.MENSAGEM).splitlines()[0].strip()
