from vbml import Pattern

pattern = Pattern(
    'Listen, my full name is <("<( )#first_name> <middle_name> <( )#second_name>")&full_name>, i am from <("<city>, <country>")&origin>'
)
result = pattern.parse("Listen, my full name is David Robert Joseph Beckham, i am from Leytonstone, England")

print("Match succeed", result)
print("Match data", pattern.dict())
