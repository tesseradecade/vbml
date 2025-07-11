import sys

from vbml import Patcher, Pattern

patcher = Patcher()
pattern = Pattern("solve <a:int> <(+-/*)^operand> <b:int>")

result = patcher.check(pattern, "solve 5 + 10")

if not result:
    sys.exit("The problem is invalid")

print("Solution is", eval(f"{result['a']} {result['operand']} {result['b']}"))
