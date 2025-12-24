from create_pytauri_app.utils import get_project_root
import shutil
from pathlib import Path

from copier import run_copy

from create_pytauri_app.prompting import ask, choose
from create_pytauri_app.questionnaire import Answer, ask_info


def get_info(ask: bool = False) -> Answer:
    info = (
        ask_info()
        if ask
        else Answer(
            project_name="pytauri-app",
            identifier="com.username.pytauri-app",
            frontend_lang="js",
            frontend_flavor="ts",
            frontend_template="vue",
            use_rust=True,
        )
    )

    return info


def main():
    TEMPLATE_DIR = get_project_root() / "templates"
    OUTPUT_DIR = get_project_root() / ".generated_template"

    info = get_info()

    project_dir = OUTPUT_DIR / info.project_name
    print(project_dir)

    # Clean up old templates to ensure a new, clean one.
    if project_dir.exists() and choose("Directory is not empty, delete?"):
        shutil.rmtree(project_dir)

    project_dir.mkdir()

    frontend_dir = TEMPLATE_DIR / f"template-{info.frontend_template_full}"
    tauri_dir = TEMPLATE_DIR / "_base_" / "src-tauri"

    # Copy over frontend
    run_copy(
        str(frontend_dir),
        str(project_dir),
        vcs_ref="HEAD",
        data=info.to_dict(),
        quiet=True,
    )

    # Copy over src-tauri
    run_copy(
        str(tauri_dir),
        str(project_dir / "src-tauri"),
        vcs_ref="HEAD",
        data=info.to_dict(),
        quiet=True,
    )

    # Copy over assets
    # ...
