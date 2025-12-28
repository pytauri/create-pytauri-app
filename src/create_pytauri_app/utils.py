import platform
from pathlib import Path

from create_pytauri_app.questionnaire import Answer


def get_project_root():
    return Path(__file__).parent.parent.parent


def construct_finish_msg(info: Answer) -> str:
    msg = "\nTemplate created! To get started, run:\n"
    cmds = [
        f"cd {info.project_name}",
        "pnpm install",
    ]
    if info.use_rust:
        cmds.append(
            "uv --python-preference only-system",
        )
        if platform.system() == "Windows":
            cmds.append(r".venv\Scripts\activate")
        else:
            cmds.append(r"source .venv/bin/activate")

    else:
        cmds.append(
            "pnpm build",
        )

    cmds.append("uv sync")

    msg += "\n".join(f"   {cmd}" for cmd in cmds)

    if info.use_rust:
        dev_start_msg = "\nFor development, run:\n"
        dev_cmd = "   pnpm tauri dev"
    else:
        dev_start_msg = "\nFor development, run:\n"
        dev_cmd = f"   python -m {info.package_name}"

    msg += "\n" + dev_start_msg + dev_cmd

    return msg
