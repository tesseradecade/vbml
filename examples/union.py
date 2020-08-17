from vbml import Pattern

pattern = Pattern("i love <(, )*items>")
result = pattern.parse("i love icecream, watermelon, you")

print("Match succeed", result)
print("Match data", pattern.dict())
