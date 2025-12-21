import shutil
from pathlib import Path

from copier import run_copy

if __name__ == "__main__":
    TEMPLATE_DIR = Path(__file__).parent.parent
    OUTPUT_DIR = Path(__file__).parent.parent / ".generated_template" / "pytauri-app"

    kwargs = {
        "project_name": "pytauri-app",
        "identifier": "com.username.pytauri-app",
        "template": "vue",
        "with_rust": "false",
    }

    # Clean up old templates to ensure a new, clean one.
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)

    run_copy(str(TEMPLATE_DIR), str(OUTPUT_DIR), vcs_ref="HEAD", data=kwargs)
