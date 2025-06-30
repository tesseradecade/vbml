from vbml import Patcher, Pattern

patcher = Patcher()
pattern = Pattern("abc<1>")

print(patcher.check(pattern, "abcd"), patcher.check(pattern, "abc"))  # {} False
