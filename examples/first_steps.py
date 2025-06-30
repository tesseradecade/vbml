from vbml import Pattern

pattern = Pattern("i am <name> i love <item>")
result = pattern.parse("i am vasya i love icecream")

print("Match succeed", result not in (False, None))
print("Match data", pattern.dict())
