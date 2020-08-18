from vbml import Patcher
from vbml import Pattern
from re import compile


patcher = Patcher()
URL_REGEX = compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")

@patcher.validator("url")
def url_validator(value: str, *args):
    if URL_REGEX.match(value):
        return value


pattern = Pattern("New video <video_url:url> on my youtube channel")
result = patcher.check(pattern, "New video https://youtu.be/RJVFkzLqXP8 on my youtube channel")

print("Match succeed", result)
print("Match data", pattern.dict())
