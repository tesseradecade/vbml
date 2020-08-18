from vbml import Patcher
from vbml import Pattern

patcher = Patcher()
pattern = Pattern("solve <a:int> <(+-/*)^operand> <b:int>")

result = patcher.check(pattern, "solve 5 + 10")

if not result:
    exit("The problem is invalid")

print("Solution is", eval(f"{result['a']} {result['operand']} {result['b']}"))
