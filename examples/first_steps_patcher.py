from vbml import Patcher, Pattern

patcher = Patcher()
pattern = Pattern("i am <age:int> years old")

result = patcher.check(pattern, "i am 9 years old")

print("Match succeed", result not in (False, None))
print("Match data", pattern.dict())
