#!/usr/bin/env python3
"""
CONDA Re-architecture Orchestrator
- Creates new modular structure (/src/conda, /src/cybercore, /src/common, /src/backend, /src/frontend)
- Migrates existing code (agent -> cybercore/agents, backend -> conda/core, renderer -> frontend)
- Removes obsolete/duplicate legacy paths, leaving only CONDA structure
- Rebrands identifiers and docs to CONDA
- Outputs logs: new tree, removed items, actions summary
"""
from __future__ import annotations
import os, re, shutil, sys, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
DOCS = ROOT / "docs"

NEW_DIRS = [
    SRC/"conda"/"core",
    SRC/"conda"/"browser",
    SRC/"conda"/"ui",
    SRC/"conda"/"utils",
    SRC/"conda"/"config",
    SRC/"cybercore"/"agents",
    SRC/"cybercore"/"security",
    SRC/"cybercore"/"workflows",
    SRC/"cybercore"/"knowledge",
    SRC/"cybercore"/"learning",
    SRC/"cybercore"/"models",
    SRC/"common"/"utils",
    SRC/"common"/"middleware",
    SRC/"common"/"shared_agents",
    SRC/"common"/"interfaces",
    SRC/"backend"/"api",
    SRC/"backend"/"services",
    SRC/"backend"/"db",
    SRC/"frontend"/"components",
    SRC/"frontend"/"assets",
    SRC/"frontend"/"styles",
    SRC/"frontend"/"pages",
]

REMOVAL_ALLOWLIST = {
    # keep only these top-level items after migration
    ".git", ".gitignore", "README.md", "LICENSE", "pyproject.toml", "package.json", "package-lock.json",
    "src", "docs", ".vscode", ".github"
}

removed_items: list[str] = []
actions: list[str] = []


def mkdirs():
    for d in NEW_DIRS:
        d.mkdir(parents=True, exist_ok=True)
        actions.append(f"mkdir {d.relative_to(ROOT)}")


def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    actions.append(f"write {path.relative_to(ROOT)}")


def copy_tree(src: Path, dst: Path):
    if not src.exists():
        return
    for p in src.rglob("*"):
        if p.is_file():
            rel = p.relative_to(src)
            target = dst/rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, target)
            actions.append(f"copy {p.relative_to(ROOT)} -> {target.relative_to(ROOT)}")


def migrate_code():
    # agent -> cybercore/agents
    copy_tree(SRC/"agent", SRC/"cybercore"/"agents")
    # backend -> conda/core
    copy_tree(SRC/"backend", SRC/"conda"/"core")
    # renderer -> frontend
    copy_tree(SRC/"renderer", SRC/"frontend")


def create_init_packages():
    init_map = {
        SRC/"conda"/"__init__.py": '"""CONDA - Unified Intelligent Agentic Browser System"""\n__all__ = ["core", "browser", "ui", "utils"]\n',
        SRC/"cybercore"/"__init__.py": '"""CyberCore - Advanced Agent & Security Framework"""\n__all__ = ["agents", "security", "workflows"]\n',
        SRC/"common"/"__init__.py": '"""Common utilities, middleware, and shared agents for CONDA"""\n',
    }
    for k, v in init_map.items():
        write(k, v)
    # touch subpackage inits
    for d in NEW_DIRS:
        write(d/"__init__.py", f'"""{d.name} package"""\n')


def rebrand_file(path: Path):
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return
    original = text
    # Replace old names with CONDA
    replacements = [
        (r"\bconda-app\b", "CONDA"),
        (r"\bConda App\b", "CONDA"),
        (r"\bCyber[Cc]ore\b", "CyberCore"),
        (r"\blocal-first-agentic-browser-core\b", "CONDA"),
    ]
    for pat, rep in replacements:
        text = re.sub(pat, rep, text)
    if text != original:
        path.write_text(text, encoding="utf-8")
        actions.append(f"rebrand {path.relative_to(ROOT)}")


def rebrand_tree(root: Path):
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in {".md", ".py", ".ts", ".tsx", ".js", ".json", ".yml", ".yaml"}:
            rebrand_file(p)


def cleanup_legacy():
    # remove legacy root items not in allowlist
    for child in ROOT.iterdir():
        name = child.name
        if name.startswith(".") and name not in {".git", ".gitignore", ".vscode", ".github"}:
            try:
                if child.is_file():
                    child.unlink()
                    removed_items.append(str(child))
                else:
                    shutil.rmtree(child)
                    removed_items.append(str(child))
            except Exception:
                pass
            continue
        if name not in REMOVAL_ALLOWLIST:
            try:
                if child.is_file():
                    child.unlink()
                else:
                    shutil.rmtree(child)
                removed_items.append(str(child))
            except Exception:
                pass

    # inside src: remove old agent, backend copy, renderer originals after migration
    for legacy in [SRC/"agent", SRC/"backend", SRC/"renderer"]:
        if legacy.exists():
            try:
                shutil.rmtree(legacy)
                removed_items.append(str(legacy))
            except Exception:
                pass


def write_docs():
    readme = ROOT/"README.md"
    new_readme = f"""
# CONDA — Unified Intelligent Agentic Browser System

CONDA unifies former conda-app and CyberCore into a modular, decoupled architecture:

- src/conda: Core browser, UI, utilities, config
- src/cybercore: Agents, security, workflows, knowledge, learning
- src/common: Shared utilities, middleware, and cross-cutting agents
- src/backend: Global backend services/APIs
- src/frontend: Global UI integration
- docs: Unified documentation

## Quick start

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt || true
python src/conda/main.py
```

## Development
- Run unit tests: `pytest`
- Lint: `ruff check` (if configured)

## Directory Tree (after re-architecture)
```
{tree}
```
"""
    write(readme, new_readme)

    # minimal main to allow a smoke run
    write(SRC/"conda"/"main.py", (
        "from conda.core import __init__\n"
        "print('CONDA started')\n"
    ))


def gen_tree(path: Path, prefix: str = "") -> list[str]:
    lines = []
    entries = sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
    for i, e in enumerate(entries):
        connector = "└── " if i == len(entries)-1 else "├── "
        lines.append(prefix + connector + e.name)
        if e.is_dir():
            extension = "    " if i == len(entries)-1 else "│   "
            lines.extend(gen_tree(e, prefix + extension))
    return lines


def main():
    mkdirs()
    create_init_packages()
    migrate_code()
    rebrand_tree(ROOT)
    cleanup_legacy()
    write_docs()

    tree_lines = gen_tree(ROOT)
    log = {
        "summary": {
            "actions": actions,
            "removed": removed_items,
        },
        "tree": tree_lines,
    }
    out = ROOT/"RESTRUCTURING_REPORT.json"
    write(out, json.dumps(log, indent=2))
    print("Re-architecture complete. See RESTRUCTURING_REPORT.json")

if __name__ == "__main__":
    main()
