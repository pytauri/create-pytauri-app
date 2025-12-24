import shutil
from pathlib import Path

from copier import run_copy

from create_pytauri_app.prompting import choose
from create_pytauri_app.questionnaire import ask_info
from create_pytauri_app.utils import construct_finish_msg, get_project_root


def main():
    output_dir = Path(".")

    template_dir = get_project_root() / "templates"
    tauri_dir = template_dir / "_base_" / "src-tauri"

    info = ask_info()

    project_dir = output_dir / info.project_name

    # Clean up old templates to ensure a new, clean one.
    if project_dir.exists() and choose("Directory is not empty, delete?"):
        shutil.rmtree(project_dir)

    project_dir.mkdir()

    frontend_template_dir = template_dir / f"template-{info.frontend_template_full}"

    # Copy over frontend
    run_copy(
        str(frontend_template_dir),
        str(project_dir),
        vcs_ref="HEAD",
        data=info.model_dump(),
        quiet=True,
    )

    # Copy over src-tauri
    run_copy(
        str(tauri_dir),
        str(project_dir / "src-tauri"),
        vcs_ref="HEAD",
        quiet=True,
        data=info.model_dump(),
    )

    # Copy over assets
    asset_dir = "static" if info.frontend_template == "svelte" else "public"
    run_copy(str(template_dir / "_assets_"), str(project_dir / asset_dir), quiet=True)

    print(construct_finish_msg(info))
