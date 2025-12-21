import os
from pathlib import Path
from copier import run_copy

if __name__ == "__main__":
    TEMPLATE_DIR = Path(__file__).parent.parent
    OUTPUT_DIR = Path(__file__).parent.parent / ".generated_template" / "pytauri-app"

    kwargs = {
        "project_name": "pytauri-app",
        "identifier": "com.username.pytauri-app",
        "template": "vue"
    }

    if OUTPUT_DIR.exists():
        os.remove(OUTPUT_DIR)

    run_copy(str(TEMPLATE_DIR), str(OUTPUT_DIR), kwargs)
