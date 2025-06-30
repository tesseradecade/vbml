from vbml import Patcher, Pattern

patcher = Patcher()

print(patcher.check(Pattern("a <(,)*any>"), "a a,b,c,d"))  # {'any': ['a', 'b', 'c', 'd']}
print(patcher.check(Pattern("a <(,)*integers:int>"), "a 1,2,3,4"))  # {'integers': [1, 2, 3, 4]}
print(patcher.check(Pattern("a <(,)*floatings:float>"), "a 1,3.14,9.5"))  # {'floatings': [1.0, 3.14, 9.5]}
