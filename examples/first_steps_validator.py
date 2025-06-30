from re import compile

from vbml import Patcher, Pattern

URL_REGEX = compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")

patcher = Patcher()


@patcher.validator("url")
def url_validator(value: str) -> str | None:
    return value if URL_REGEX.match(value) else None


pattern = Pattern("Nice repository base layer <gh_repo_url:url>")
result = patcher.check(pattern, "Nice repository base layer https://github.com/flaunysagh/repositorybaselayer")


print("Match succeed", result not in (False, None))
print("Match data", pattern.dict())
