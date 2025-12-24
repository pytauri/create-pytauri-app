from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

from .prompting import Choice, ask, choose, select


@dataclass
class Answer:
    project_name: str
    identifier: str
    frontend_lang: Literal["js", "py"]
    frontend_flavor: Literal["ts", "js"] | None
    frontend_template: str
    use_rust: bool

    @property
    def package_name(self) -> str:
        return self.project_name.replace("-", "_")

    @property
    def frontend_template_full(self):
        frontend_template = self.frontend_template
        if self.frontend_lang == "js":
            frontend_template += "-ts" if self.frontend_flavor == "ts" else ""
        return frontend_template

    def to_dict(self):
        return {k: str(v) for k, v in asdict(self).items()}


def ask_info() -> Answer:
    project_name = ask("Project name", "pytauri-app")
    user = Path.home().name.lower()
    identifier = ask("Identifier", f"com.{user}.{project_name}")

    frontend_langs = [
        Choice(label="Python", value="py", meta="uv"),
        Choice(
            label="TypeScript / JavaScript", value="js", meta="pnpm, yarn, npm, bun"
        ),
    ]

    frontend_lang = select(
        "Choose which language to use for your frontend", frontend_langs
    )

    match frontend_lang:
        case "js":
            frontend_frameworks = [
                Choice(value="vanilla"),
                Choice(value="vue", meta="https://vuejs.org/"),
                Choice(value="svelte", meta="https://svelte.dev/"),
                Choice(value="react", meta="https://react.dev/"),
            ]
        case _:
            frontend_frameworks = [
                Choice(label="NiceGUI", value="nicegui", meta="https://nicegui.io/"),
            ]

    frontend_template = select("Choose your UI template", frontend_frameworks)

    frontend_flavor = None
    if frontend_lang == "js":
        frontend_flavors = [
            Choice(label="TypeScript", value="ts"),
            Choice(label="JavaScript", value="js"),
        ]
        frontend_flavor = select("Choose your UI flavor", frontend_flavors)

    use_rust = choose("Choose if you want to use Rust")

    if frontend_template == "nicegui":
        raise NotImplementedError("No template is available for NiceGUI yet!")

    return Answer(
        project_name=project_name,
        identifier=identifier,
        frontend_lang=frontend_lang,
        frontend_flavor=frontend_flavor,
        frontend_template=frontend_template,
        use_rust=use_rust,
    )
