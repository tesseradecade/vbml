<p align="center">
  <a href="https://github.com/tesseradecade/vbml">
    <img src="docs/logo.jpeg" width="200px" style="display: inline-block;">
  </a>
</p>

<h1>
  vbml
</h1>

<p>
— markup language that compiles to regex.
</p>

<p align="center">
  <img alt="Code Style" src="https://img.shields.io/badge/code_style-Ruff-D7FF64?logo=ruff&logoColor=fff&style=flat-square&labelColor=black"></img>
  <img alt="Type Checker" src="https://img.shields.io/badge/types-basedpyright-black?logo=python&color=%23FBCA04&logoColor=edb641&labelColor=black&style=flat-square"></img>
  <img alt="Python version" src="https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2Ftesseradecade%2Fvbml%2Frefs%2Fheads%2Fmaster%2Fpyproject.toml&query=%24.project.requires-python&style=flat-square&logo=python&logoColor=fff&label=python&labelColor=black"></img>
</p>

<p align="center">
  <img alt="GitHub License" src="https://img.shields.io/github/license/tesseradecade/vbml.svg?color=lightGreen&labelColor=black&style=flat-square"></img>
  <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dw/vbml?color=lightGreen&labelColor=black&style=flat-square"></img>
  <img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/tesseradecade/vbml?labelColor=black&style=flat-square"></img>
  <img alt="GitHub issues by-label" src="https://img.shields.io/github/issues/tesseradecade/vbml/bug?labelColor=black&style=flat-square"></img>
</p>

## Features

* Clean `regex`-based parser
* Easy-to-understand validators / Custom validators
* Lots of features out-of-box

`I am <name>, i am <age:int> years old` + `I am Steven, i am 20 years old` = `{"name": "Steven", "age": 20}`

## Installation

Install with pip, poetry or uv:

```shell script
pip install vbml
poetry add vbml
uv add vbml
```

## Run tests

Clone repo from git:

```shell script
git clone https://github.com/tesseradecade/vbml.git
```

Go to repository and run tests with `uv`:

```shell script
cd vbml
uv sync
uv run pytest tests
```

## :book: Documentation

Full documentation contents are available in [docs/index.md](/docs/index.md)

## Simple example

```python
from vbml import Patcher, Pattern

patcher = Patcher()
pattern = Pattern("I have <amount:int> apples. They are <adj>")

result1 = patcher.check(pattern, "I have 3 apples. They are green")
result2 = patcher.check(pattern, "I have three apples. They are green")
result3 = patcher.check(pattern, "Something irrelevant")

result1 # {"amount": 3, "adj": "green"}
result2 # None
result3 # None
```
