from vbml import Pattern

pattern = Pattern("My sentence: <!><( )#last_word>.")
result = pattern.parse("My sentence: Please take you seats and dont scream.")

print("Match succeed", result)
print("Match data", pattern.dict())  # {"last_word": "scream"}
