#!/usr/bin/env python3
"""
CyberCore Installation Setup
Enhanced cross-platform setup with platform-specific dependencies
"""

import sys
import platform
from setuptools import setup, find_packages
from pathlib import Path

# Read requirements
def read_requirements(filename):
    """Read requirements from file"""
    req_path = Path(__file__).parent / filename
    if req_path.exists():
        with open(req_path) as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return []

# Platform detection
PLATFORM = platform.system().lower()
IS_WINDOWS = PLATFORM == "windows"
IS_MACOS = PLATFORM == "darwin"
IS_LINUX = PLATFORM == "linux"

# Base requirements
base_requirements = read_requirements("requirements.txt")

# Platform-specific dependencies
platform_deps = []
if IS_WINDOWS:
    platform_deps.extend([
        "pywin32>=305",
        "pywin32-ctypes>=0.2.0",
    ])
elif IS_MACOS:
    platform_deps.extend([
        "pyobjc-core>=9.0",
        "pyobjc-framework-Cocoa>=9.0",
    ])

# Development dependencies
dev_requirements = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "pytest-asyncio>=0.21.0",
    "black>=23.7.0",
    "flake8>=6.1.0",
    "mypy>=1.5.0",
    "isort>=5.12.0",
]

# Documentation dependencies
docs_requirements = [
    "sphinx>=7.1.0",
    "sphinx-rtd-theme>=1.3.0",
    "myst-parser>=2.0.0",
]

# Read long description
readme_path = Path(__file__).parent / "DOCKER_README.md"
if not readme_path.exists():
    readme_path = Path(__file__).parent / "README.md"
long_description = ""
if readme_path.exists():
    with open(readme_path, encoding="utf-8") as f:
        long_description = f.read()

setup(
    name="cybercore",
    version="6.0.0",
    author="CyberCore Team",
    author_email="team@cybercore.dev",
    description="Autonomous Security Testing Framework with DSPY Self-Improvement",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cybercore/cybercore",
    packages=find_packages(exclude=["tests", "tests.*"]),
    python_requires=">=3.11",
    install_requires=base_requirements + platform_deps,
    extras_require={
        "dev": dev_requirements,
        "docs": docs_requirements,
        "full": dev_requirements + docs_requirements + platform_deps,
    },
    entry_points={
        "console_scripts": [
            "cybercore=cybercore.cli.main:cli",
            "cybercore-api=cybercore.api.app:run_server",
            "cybercore-optimize=cybercore.dspy.optimizer:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Security",
        "Topic :: Software Development :: Testing",
        "Topic :: System :: Monitoring",
    ],
    keywords="security testing vapt stqa autonomous dspy machine-learning",
    project_urls={
        "Documentation": "https://cybercore.readthedocs.io",
        "Source": "https://github.com/cybercore/cybercore",
        "Tracker": "https://github.com/cybercore/cybercore/issues",
    },
    include_package_data=True,
    zip_safe=False,
)
