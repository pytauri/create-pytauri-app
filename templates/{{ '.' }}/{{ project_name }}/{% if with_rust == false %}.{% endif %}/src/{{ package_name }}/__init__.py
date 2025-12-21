import sys
from os import environ
from pathlib import Path

from anyio.from_thread import start_blocking_portal
from pydantic import BaseModel
from pytauri import Commands
from pytauri_wheel.lib import builder_factory, context_factory

SRC_TAURI_DIR = Path(__file__).parent.parent.parent.absolute()


# If the DEV_SERVER env. variable is set, use that server for development (allows hot-reloading). Otherwise, use the built assets to serve the frontend.
DEV_SERVER = environ.get("DEV_SERVER")  # Default: http://localhost:1420

if DEV_SERVER is not None:
    tauri_config = {
        "build": {
            "frontendDist": DEV_SERVER,
        },
    }
else:
    tauri_config = None


class Person(BaseModel):
    name: str


commands: Commands = Commands()


@commands.command()
async def greet(body: Person) -> str:
    return f"Hello, {body.name}! You've been greeted from Python {sys.version}!"


def main() -> int:
    with start_blocking_portal("asyncio") as portal:
        app = builder_factory().build(
            context=context_factory(SRC_TAURI_DIR, tauri_config=tauri_config),
            invoke_handler=commands.generate_handler(portal),
            plugins=[],
        )
        exit_code = app.run_return()
        return exit_code
