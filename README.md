# vbml - perfect pythonistic parser / string manipulator :sparkles:

## Features

* Fast `regex`-based parser
* Easy-to-understand validators / Custom validators
* Lots of features out-of-box

`I am <name>, i am <age:int> years old` + `I am Steven, i am 20 years old` = `{"name": "Steven", "age": 20}`

## Installation

Install with pip:

```shell script
pip install vbml
```

Or with poetry:

```shell script
poetry add vbml
```

## Run tests

Clone repo from git:

```shell script
git clone https://github.com/tesseradecade/vbml.git
```

Go to repository and run tests with `poetry`:

```shell script
cd vbml
poetry install
poetry run pytest
```

## Documentation

Full documentation is available in [docs/index.md](/docs/index.md)

## Simple example

```python
from vbml import Patcher, Pattern

patcher = Patcher()
pattern = Pattern("He is <description> like he has right just turned <age:int> years old")

result1 = patcher.check(pattern, "He is so spontaneous like he has right just turned 10 years old")
result2 = patcher.check(pattern, "He is silly like he has right just turned t3n years old")
result3 = patcher.check(pattern, "Haha regex go brrr")

result1 # {"description": "so spontaneous", "age": 10}
result2 # False
result3 # False
```

Made with :heart: by [timoniq](https://github.com/timoniq)