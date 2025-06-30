from vbml import Patcher, Pattern


def test_start_patcher():
    patcher = Patcher()

    assert patcher.check(Pattern(".<description>-<integer:int>/<floating:float>"), ".awesome-30/8.33") == {
        "description": "awesome",
        "integer": 30,
        "floating": 8.33,
    }
    assert not patcher.check(Pattern("//<integer:int>//<floating:float>"), "//eee//1")
