import sys

from anyio.from_thread import start_blocking_portal
from pydantic import BaseModel, RootModel
from pytauri import (
    BuilderArgs,
    Commands,
    builder_factory,
    context_factory,
)

commands: Commands = Commands()


class Person(BaseModel):
    name: str


Greeting = RootModel[str]


@commands.command()
async def greet(body: Person) -> Greeting:
    return Greeting(
        f"Hello, {body.name}! You've been greeted from Python {sys.version}!"
    )


def main() -> int:
    with start_blocking_portal("asyncio") as portal:  # or `trio`
        app = builder_factory().build(
            context=context_factory(),
            invoke_handler=commands.generate_handler(portal),
        )
        exit_code = app.run_return()
        return exit_code
