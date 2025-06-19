import argparse
import shutil
from pathlib import Path
import zipfile
import os
import subprocess
import importlib.util
import sys

SYNTAX = {
    "name": "pack",
    "description": "Export or import CPTD commands as ZIP archives",
    "usage": "cptd pack --export --output <folder> | --import --from <folder> [--replace] [--skip-existing] [--allow-insecure]",
    "arguments": [
        {"name": "--export", "required": False, "help": "Export all installed commands to ZIPs"},
        {"name": "--import", "required": False, "help": "Import commands from a folder of ZIPs"},
        {"name": "--output", "required": False, "help": "Folder to export ZIPs to"},
        {"name": "--from", "required": False, "help": "Folder to import ZIPs from"},
        {"name": "--replace", "required": False, "help": "Delete existing commands before import"},
        {"name": "--skip-existing", "required": False, "help": "Skip commands already installed"},
        {"name": "--allow-insecure", "required": False, "help": "Allow commands with insecure code (e.g., pip install)"}
    ],
    "examples": [
        "cptd pack --export --output ./my_exports",
        "cptd pack --import --from ./shared",
        "cptd pack --import --from ./shared --replace",
        "cptd pack --import --from ./shared --allow-insecure"
    ]
}


def print_help(syntax):
    print(f"\n[ℹ] {syntax['description']}")
    print(f"Usage: {syntax['usage']}\n")
    print("Arguments:")
    for arg in syntax['arguments']:
        print(f"  {arg['name']:20} {arg['help']}")
    print("\nExamples:")
    for example in syntax['examples']:
        print(f"  {example}")
    print()


def run(argv):
    if "--help" in argv or "-h" in argv:
        print_help(SYNTAX)
        return

    parser = argparse.ArgumentParser()
    parser.add_argument("--export", action="store_true")
    parser.add_argument("--import", dest="import_", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--from", dest="from_", type=Path)
    parser.add_argument("--replace", action="store_true")
    parser.add_argument("--skip-existing", action="store_true")
    parser.add_argument("--allow-insecure", action="store_true")
    args = parser.parse_args(argv)

    spec = importlib.util.find_spec("cptd_tools")
    if not spec or not spec.submodule_search_locations:
        print("[!] Could not locate cptd_tools installation directory")
        return

    command_dir = Path(spec.submodule_search_locations[0]) / "commands"

    # ---------- EXPORT ----------
    if args.export:
        if not args.output:
            print("[!] --output folder is not specified")
            return
        args.output.mkdir(parents=True, exist_ok=True)
        for cmd in command_dir.iterdir():
            if not cmd.is_dir():
                continue
            if cmd.name in ("__pycache__", "command", "pack"):
                continue
            zip_path = args.output / f"{cmd.name}.zip"
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                for file in cmd.rglob("*"):
                    if '__pycache__' in file.parts or file.name.endswith('.pyc'):
                        continue
                    zf.write(file, file.relative_to(cmd))
            print(f"[✔] Exported: {zip_path}")

    # ---------- IMPORT ----------
    elif args.import_:
        if not args.from_:
            print("[!] --from folder is not specified")
            return
        if not args.from_.exists():
            print(f"[!] Import directory does not exist: {args.from_}")
            return

        if args.replace:
            for cmd in command_dir.iterdir():
                if cmd.is_dir() and cmd.name not in ("command", "pack"):
                    shutil.rmtree(cmd)
            print("[ℹ] Existing commands removed")

        for zip_file in sorted(args.from_.glob("*.zip")):
            cmd_name = zip_file.stem
            dest = command_dir / cmd_name

            if dest.exists() and args.skip_existing:
                print(f"[↷] Skipped (exists): {cmd_name}")
                continue
            if dest.exists():
                try:
                    shutil.rmtree(dest)
                except PermissionError:
                    print(f"[🚫] Cannot remove existing command '{cmd_name}': it is being used by another process.")
                    continue
                except Exception as e:
                    print(f"[⚠] Failed to remove existing command '{cmd_name}': {e}")
                    continue


            cmd = ["cptd", "command", "--add", str(zip_file)]
            if args.allow_insecure:
                cmd.append("--allow-insecure")

            print(f"[→] Installing via: {' '.join(cmd)}")
            try:
                subprocess.run(cmd, check=True)
            except subprocess.CalledProcessError as e:
                print(f"[⛔] Failed to install {zip_file.name}: {e}")

    else:
        print("[!] Either --export or --import must be specified")
        print_help(SYNTAX)
