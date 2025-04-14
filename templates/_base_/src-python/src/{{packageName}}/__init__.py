import sys

from anyio.from_thread import start_blocking_portal
from pydantic import BaseModel, RootModel
from pytauri import (
    BuilderArgs,
    builder_factory,
    context_factory, Commands,
)

commands: Commands = Commands()


class Person(BaseModel):
    name: str


@commands.command()
async def greet(body: Person) -> RootModel[str]:
    return RootModel[str](f"Hello {body.name}! You've been greeted from Python {sys.winver}!")


with start_blocking_portal("asyncio") as portal:
    builder = builder_factory()
    app = builder.build(
        BuilderArgs(
            context_factory(),
            # 👇
            invoke_handler=commands.generate_handler(portal),
        )
    )
    app.run()
