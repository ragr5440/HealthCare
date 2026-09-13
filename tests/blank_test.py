import inspect

from autogen_core.models import (
    ChatCompletionClient,
)

print(
    ChatCompletionClient.__abstractmethods__
)