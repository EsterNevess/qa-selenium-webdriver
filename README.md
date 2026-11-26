# Automação Web com Selenium WebDriver

[![Testes Selenium](https://github.com/EsterNevess/qa-selenium-webdriver/actions/workflows/ci.yml/badge.svg)](https://github.com/EsterNevess/qa-selenium-webdriver/actions/workflows/ci.yml)
[![Relatório Allure](https://img.shields.io/badge/Relat%C3%B3rio-Allure-FF5722?logo=qase&logoColor=white)](https://esternevess.github.io/qa-selenium-webdriver/)

Suíte de **35 testes automatizados** com **Selenium WebDriver** (Python) sobre o
[the-internet.herokuapp.com](https://the-internet.herokuapp.com), um site feito para praticar automação.

Eu já automatizo interfaces com Playwright nos outros repositórios. Este projeto existe para mostrar
o **Selenium** em uso real, e por isso o site é outro: ele traz justamente os casos em que o
Selenium exige técnica própria, como alertas JavaScript, quadros aninhados, abas, espera de
elementos que aparecem depois e upload de arquivo.

| | |
|---|---|
| Testes | 35 (login, elementos de formulário e tabela, alertas, frames, janelas, espera dinâmica, upload, autenticação, menu de contexto) |
| Tempo de execução | ~3 min 40 s na minha máquina, com um navegador novo por teste |
| Stack | Python · Selenium 4 · pytest · Page Object Model · Allure · pytest-html · GitHub Actions |
| Alvo | https://the-internet.herokuapp.com |

## O que está coberto

| Arquivo | Testes | O que verifica |
|---|---|---|
| `tests/test_login.py` | 5 | login válido, três tipos de credencial inválida (incluindo campos vazios) e logout |
| `tests/test_elementos.py` | 16 | lista suspensa, caixas de marcar, hover, ordenação de tabela, teclas, adicionar e remover elementos |
| `tests/test_interacoes.py` | 14 | alertas JS (alerta, confirmação, pergunta), frames aninhados, nova aba, carregamento dinâmico, upload, autenticação básica, clique com o botão direito |

A ordenação da tabela compara a **lista inteira** contra `sorted()`, nas duas direções, porque uma
ordenação pode acertar o topo e errar o meio.

## Decisões de projeto

- **Esperas explícitas, nenhuma implícita e nenhum `sleep`.** Cada ação espera uma condição concreta
  (visível, clicável, alerta aberto, número de abas). É isso que evita o teste que passa na minha
  máquina e falha no CI. O `pages/base_page.py` concentra essas esperas.
- **Um navegador novo por teste.** Nenhum teste herda cookie, aba ou alerta aberto de outro. Custa
  tempo de execução, e eu aceito o custo em troca de testes que não dependem da ordem.
- **Page Object Model.** O teste diz **o que** se espera; a página diz **como** chegar lá. Quando um
  seletor muda, muda em um lugar só.
- **Selenium Manager.** O chromedriver certo para o Chrome instalado é baixado pelo próprio Selenium 4,
  então não há driver para versionar nem caminho para configurar.
- **Headless por padrão**, com `HEADED=1` para ver o navegador abrindo.

## Evidência de falha

Quando um teste falha, o `tests/conftest.py` anexa ao próprio teste no relatório Allure o **print da
tela**, a **URL** e o **HTML da página** naquele instante. O print também é salvo em `evidencias/`,
para quem roda localmente. Verifiquei esse caminho provocando uma falha de propósito e conferindo os
três anexos no resultado.

## O que não está coberto, e por quê

| Caso | Motivo |
|---|---|
| Teclar **ENTER** no campo de teclas | O campo está dentro de um formulário: o Enter o envia e a página recarrega sem o resultado. Os outros três tipos de tecla estão testados. |
| Corpo da resposta **401** da autenticação básica | O Chrome mostra uma página vazia depois de recusar o diálogo de login, então o Selenium não enxerga o texto "Not authorized". O teste confere o **status 401** por HTTP direto, e isso é dito no código. |
| **Arrastar e soltar** (`/drag_and_drop`) | O arrastar HTML5 não é simulado de forma confiável pelo Selenium; ficou de fora em vez de entrar instável. |
| Download de arquivo | Depende de configuração de pasta do navegador que difere entre a máquina local e o CI; não entrou. |

Também vale saber: o alvo é um **site público de terceiros**. Se ele ficar fora do ar, os testes
falham por isso, e não por defeito de quem os escreveu.

## Como rodar

```bash
python -m venv venv
venv\Scripts\activate          # no Linux e no macOS: source venv/bin/activate
pip install -r requirements.txt
pytest                          # rodada completa, com relatórios
pytest tests/test_login.py      # só um arquivo
HEADED=1 pytest tests/test_login.py   # com o navegador visível
```

Precisa do **Google Chrome** instalado. O relatório simples sai em `relatorio.html`; os dados do
Allure saem em `allure-results/`. Para ver o relatório Allure localmente: `allure serve allure-results`.

## Estrutura

```
pages/             Page Object Model (base, login, elementos, interações)
tests/             testes e fixtures (driver, evidência de falha)
.github/workflows/ execução automática a cada push, com relatório Allure
```

## Integração contínua

A cada push o GitHub Actions roda a suíte em `ubuntu-24.04` com o Chrome do próprio runner, gera o
relatório Allure com o histórico das execuções anteriores e o publica no GitHub Pages. O resultado
real dos testes volta para o job: se um teste falha, o selo do README fica vermelho, mesmo com o
relatório publicado.
