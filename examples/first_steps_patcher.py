from vbml import Patcher
from vbml import Pattern

patcher = Patcher()
pattern = Pattern("i am <age:int> years old")

result = patcher.check(pattern, "i am 9 years old")

print("Match succeed", result)
print("Match data", pattern.dict())
