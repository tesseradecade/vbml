# Patcher

Patcher is active validation controller.

## What validators are for

Validators are needed to check if argument value is what it should be. Like price value should be numeric or city argument value should be possessed in the worldwide city list

## Making validators

Firstly patcher should be created:

```python
from vbml import Patcher
patcher = Patcher()
```

### Making validators with ABCValidator

Here is the example:

```python
from vbml import Patcher, ABCValidator
import typing
import string

patcher = Patcher()

@patcher.validator("latin")
class NamePassValidator(ABCValidator):
    def check(self, value: str, *args) -> typing.Optional[typing.Any]:
        if not value.strip(string.ascii_letters):
            return value
```

Validator with name `latin` is ready!  
If implemented `check` method returns anything except `None` the validation request is approved

### Making validators with FuncBaseValidator

Here is the example:

```python
from vbml import Patcher
import typing
import string

patcher = Patcher()

@patcher.validator("latin")
def namepass_validator(value: str) -> typing.Optional[typing.Any]:
    if not value.strip(string.ascii_letters):
        return value
```

Validator with name `latin` is ready!  
If implemented function returns anything except `None` the validation request is approved

## Matching and validating patterns with text

Now custom validator `latin` is ready and can be used with current patcher:

```python
# ...
from vbml import Pattern

pattern = Pattern("my name is <name:latin>")
patcher.check(pattern, "my name is серый") # None
patcher.check(pattern, "my name is john") # {"name": "john"}
```

