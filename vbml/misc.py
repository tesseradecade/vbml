import typing
from collections import deque
from collections.abc import Iterable

type IterableData[T] = Iterable[T | IterableData[T]]


def flatten[T](data: IterableData[T], /) -> list[T]:
    result = list[typing.Any]()
    stack = deque[typing.Any]([iter(data)])

    while stack:
        try:
            item = next(stack[-1])

            if isinstance(item, Iterable) and not isinstance(item, str | bytes | bytearray):
                stack.append(iter(item))  # type: ignore[UnknownArgumentType]
            else:
                result.append(item)
        except StopIteration:
            stack.pop()

    return result


__all__ = ("flatten",)
