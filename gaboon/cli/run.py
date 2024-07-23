from typing import List, Any
import sys
from pathlib import Path
from gaboon.project.project_class import Project
import importlib.util
from gaboon.logging import logger
import boa


def main(args: List[Any]) -> int:
    run_script(args.project_root, args.script_name_or_path)
    return 0


def run_script(root: Path | str, script_name_or_path: Path | str):
    project = Project(root)
    script_path: Path = get_script_path(project, script_name_or_path)

    # Set up the environment (add necessary paths to sys.path, etc.)
    sys.path.insert(0, str(root)) if root not in sys.path else None
    sys.path.insert(0, str(root / project.src)) if (
        root / project.src
    ) not in sys.path else None

    # We give the user's script the module name "deploy_script"
    spec = importlib.util.spec_from_file_location("deploy_script", script_path)
    module = importlib.util.module_from_spec(spec)
    module.__dict__["boa"] = boa
    spec.loader.exec_module(module)

    if hasattr(module, "main") and callable(module.main):
        module.main()
    else:
        logger.info("No main() function found. Executing script as is...")


def get_script_path(project: Project, script_name_or_path: Path | str) -> Path:
    script_path = ""
    if not str(script_name_or_path).endswith(".py"):
        if project.script in str(script_name_or_path):
            if project.root in str(script_name_or_path):
                script_path = Path(f"{script_name_or_path}.py")
            else:
                script_name_or_path = project.root / f"{script_name_or_path}.py"
        else:
            script_path = project.root / project.script / f"{script_name_or_path}.py"
    else:
        if project.root in str(script_name_or_path):
            if project.script in str(script_name_or_path):
                script_path = Path(script_name_or_path)
            else:
                logger.error(f"{script_name_or_path} not found")
        else:
            if project.script in str(script_name_or_path):
                script_path = project.root / Path(script_name_or_path)
            else:
                script_path = project.root / project.script / Path(script_name_or_path)

    if not script_path.exists():
        logger.error(f"{script_path} not found")
    return script_path
