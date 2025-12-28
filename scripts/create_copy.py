from create_pytauri_app import _main
from create_pytauri_app.questionnaire import Answer
from create_pytauri_app.utils import get_project_root

if __name__ == "__main__":
    answer = Answer(
        project_name="pytauri-app",
        identifier="com.username.pytauri-app",
        frontend_lang="js",
        frontend_flavor="ts",
        frontend_template="vue",
        use_rust=True,
    )
    output_dir = get_project_root() / ".generated_template"
    _main(output_dir, answer)
