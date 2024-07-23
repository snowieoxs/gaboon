import importlib
import sys
from pathlib import Path
from gaboon.logging import logger, set_log_level
import tomllib
import argparse
from gaboon.project import Project

GAB_VERSION_STRING = "Gaboon v{}"


def main(argv: list) -> int:
    if "--version" in argv or "version" in argv:
        return get_version()

    main_parser = argparse.ArgumentParser(
        prog="Gaboon",
        description="🐍 Pythonic Smart Contract Development Framework",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    main_parser.add_argument(
        "-d", "--debug", action="store_true", help="Run in debug mode"
    )
    main_parser.add_argument(
        "-q", "--quiet", action="store_true", help="Suppress all output except errors"
    )
    sub_parsers = main_parser.add_subparsers(dest="command")

    # Init command
    init_parser = sub_parsers.add_parser(
        "init",
        help="Initialize a new project.",
        description="""
This will create a basic directory structure at the path you specific, which looks like:
.
├── README.md
├── gaboon.toml
├── script/
├── src/
│   └── Counter.vy
└── tests/
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    init_parser.add_argument(
        "path",
        help="Path of the new project, defaults to current directory.",
        type=Path,
        nargs="?",
        default=Path("."),
    )
    init_parser.add_argument(
        "-f",
        "--force",
        required=False,
        help="Overwrite existing project.",
        action="store_true",
    )

    # Compile command
    sub_parsers.add_parser(
        "compile",
        help="Compiles the project.",
        description="""Compiles all Vyper contracts in the project. \n
This command will:
1. Find all .vy files in the src/ directory
2. Compile each file using the Vyper compiler
3. Output the compiled artifacts to the out/ directory

Use this command to prepare your contracts for deployment or testing.""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        aliases=["build"],
    )

    # Run command
    run_parser = sub_parsers.add_parser(
        "run",
        help="Runs a script with the project's context.",
        description="Runs a script with the project's context.",
    )
    run_parser.add_argument(
        "script_name_or_path",
        help="Name of the script in the script folder, or the path to your script.",
        type=str,
        default="./script/deploy.py",
    )
    run_parser.add_argument(
        "--rpc-url",
        help="RPC of the EVM network you'd like to deploy this code to.",
        type=str,
        nargs="?",
    )

    # Parsing starts
    if len(argv) == 0 or (len(argv) == 1 and (argv[0] == "-h" or argv[0] == "--help")):
        main_parser.print_help()
        return 0
    args = main_parser.parse_args(argv)

    set_log_level(quiet=args.quiet, debug=args.debug)

    try:
        project_root: Path = Project.find_project_root()
    except FileNotFoundError:
        if args.command != "init":
            logger.error(
                "Not in a Gaboon project (or any of the parent directories).\nTry to create a gaboon.toml file with `gab init` "
            )
            return 1
        project_root = Path.cwd()

    # Alias overrides
    if args.command == "build":
        args.command = "compile"

    # Add project_root and config to args
    args.project_root = project_root
    logger.info(f"Running {args.command} command...")
    if args.command:
        importlib.import_module(f"gaboon.cli.{args.command}").main(args)
    else:
        main_parser.print_help()
    return 0


def get_version() -> int:
    with open(
        Path(__file__).resolve().parent.parent.parent.joinpath("pyproject.toml"), "rb"
    ) as f:
        gaboon_data = tomllib.load(f)
        logger.info(GAB_VERSION_STRING.format(gaboon_data["project"]["version"]))
        return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
