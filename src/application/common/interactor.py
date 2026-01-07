from typing import Generic, TypeVar

InputDto = TypeVar("InputDto")
OutputDto = TypeVar("OutputDto")


class Interactor(Generic[InputDto, OutputDto]):
    async def __call__(self, data: InputDto) -> OutputDto:
        raise NotImplementedError
