# Pattern

## What pattern is for

### Purposes

The main purpose of `Pattern` is to make a regex schema based on VBML syntax (partly translate vbml to regex) and parse it.

### Syntax

Frames for vbml arguments are `<` and `>`. Everything inside frames is what vbml read and avoid escaping.

```python
from vbml import Pattern
pattern = Pattern("define <qwerty>")
```

This is a pattern with argument called `qwerty`

Distance between 2 arguments should be not less than one symbol because otherwise VBML will not be able to find a boundaries for these arguments:  
:-1: `<arg1><arg2>`  
:+1: `<arg1> <arg2>`  

## Matching pattern with text

### Matching

Lets match this pattern with some text:

```python
# Match pattern with text
result = pattern.parse("define hello")
print(result) # True
```

`True` means that the matching was succeed.

### Take your data

After pattern matching with text, matching save as pregmatch value in it, pregmatch can be received by the `pattern.dict()`.  
Text is escaped from these symbols: `\.*+?()[]|^${}`. 

That's how matching data can be taken after pattern was successfully matched with text (result is `True`, otherwise the exception will be thrown):
```python
print(pattern.dict()) # {"qwerty": "hello"}
```

## Pattern options

**text** - VBML-syntax pattern  
**regex** - outside regex wrapper. `{}` is automatically replaced with vbml-generated regex  
**lazy** - change mode of arguments:  

If `lazy` is `True` - `Pattern("I am <name> <surname>")` with text `I am Kate Isobelle Furler` will be matched with dict `{"name": "Kate", "surname": "Isobelle Furler"}` _(default)_

If `lazy` is `False` - `Pattern("I am <name> <surname>")` with text `I am Kate Isobelle Furler` will be matched with dict `{"name": "Kate Isobelle", "surname": "Furler"}`
