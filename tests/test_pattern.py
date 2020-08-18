from vbml import Pattern

def test_start_pattern():
    pattern = Pattern("i am <name>")
    result = pattern.parse("i am vbml")

    assert result
    assert pattern.dict() == {"name": "vbml"}

    result2 = pattern.parse("wrong text")
    assert not result2


def test_pattern_ignore_validators():
    pattern = Pattern("my name <name> age <age:int>")
    result = pattern.parse("my name vbml age 1")
    assert result
    assert pattern.dict() == {"name": "vbml", "age": "1"}


def test_pattern_representation():
    pattern = Pattern("test <a> test <b>,<c>")
    assert pattern.representation == "test ? test ?,?"


def test_pattern_lazy():
    pattern = Pattern("i am <name> <surname>", lazy=True)
    pattern.parse("i am Kate Isobelle Furler")

    pattern2 = Pattern("i am <name> <surname>", lazy=False)
    pattern2.parse("i am Kate Isobelle Furler")

    assert pattern.dict() == {"name": "Kate", "surname": "Isobelle Furler"}
    assert pattern2.dict() == {"name": "Kate Isobelle", "surname": "Furler"}

def test_pattern_escape():
    pattern = Pattern("$%^/\\[]<(/\\)^char>")
    assert pattern.parse("$%^/\\[]\\")
    assert pattern.dict() == {"char": "\\"}
