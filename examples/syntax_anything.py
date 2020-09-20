from vbml import Patcher
from vbml import Pattern

patcher = Patcher()
pattern = Pattern("abc<1>")

print(patcher.check(pattern, "abcd"), patcher.check(pattern, "abc"))  # {} False
