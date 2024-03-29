#!/usr/bin/env python3
import argparse
from pathlib import Path
import subprocess
from urllib.request import urlopen

DOCKERFILE_CONTENT = """
FROM python:3.12-slim-bullseye

RUN useradd --create-home --home-dir /app --shell /bin/bash app
WORKDIR /app

COPY requirements ./requirements
RUN pip install --disable-pip-version-check --no-cache-dir -r requirements/{}.txt

COPY . .
USER app
"""

DOCKERIGNORE_SOURCE = 'https://raw.githubusercontent.com/GoogleCloudPlatform/getting-started-python/main/optional-kubernetes-engine/.dockerignore'  # noqa: E501

DEV_REQUIREMENTS_CONTENT = """
-r base.txt
flake8
flake8-print
flake8-multiline-containers
flake8-builtins
flake8-import-order
flake8-commas
flake8-quotes
"""

FLAKE8_CONTENT = """
[flake8]
max-line-length = 100
import-order-style = google
application-import-names = code
exclude = venv
"""

GITIGNORE_SOURCE = 'https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore'

GIT_BRANCH = 'develop'

GIT_COMMIT = 'initial commit'


def main() -> None:
    parser = argparse.ArgumentParser(description='Create project directory structure')
    parser.add_argument('project_name', type=str, help='Name of the project')
    args = parser.parse_args()

    project_dir = Path(args.project_name)

    _create_project(project_dir)
    _create_code_dir(project_dir)
    _create_requirements_dir(project_dir)
    _create_docker_dir(project_dir)
    _create_dockerignore(project_dir)
    _create_flake8_config(project_dir)
    _create_gitignore(project_dir)
    _init_git(project_dir)


def _create_project(project_dir: Path) -> None:
    project_dir.mkdir()


def _create_code_dir(project_dir: Path) -> None:
    code_dir = project_dir / 'code'
    code_dir.mkdir()

    (code_dir / '__init__.py').touch()
    (code_dir / 'main.py').touch()


def _create_requirements_dir(project_dir: Path) -> None:
    requirements_dir = project_dir / 'requirements'
    requirements_dir.mkdir()

    (requirements_dir / 'base.txt').touch()

    with open(requirements_dir / 'dev.txt', 'w') as file:
        file.write(DEV_REQUIREMENTS_CONTENT.lstrip())


def _create_docker_dir(project_dir: Path) -> None:
    docker_dir = project_dir / 'docker'
    docker_dir.mkdir()

    with open(docker_dir / 'Dockerfile', 'w') as file:
        file.write(DOCKERFILE_CONTENT.format('base').lstrip())

    with open(docker_dir / 'Dockerfile.dev', 'w') as file:
        file.write(DOCKERFILE_CONTENT.format('dev').lstrip())


def _create_dockerignore(project_dir: Path) -> None:
    with urlopen(DOCKERIGNORE_SOURCE) as response:
        gitignore_content = response.read().decode('utf-8')

    with open(project_dir / '.dockerignore', 'w') as file:
        file.write(gitignore_content)


def _create_flake8_config(project_dir: Path) -> None:
    with open(project_dir / '.flake8', 'w') as file:
        file.write(FLAKE8_CONTENT)


def _create_gitignore(project_dir: Path) -> None:
    with urlopen(GITIGNORE_SOURCE) as response:
        gitignore_content = response.read().decode('utf-8')

    with open(project_dir / '.gitignore', 'w') as file:
        file.write(gitignore_content)


def _init_git(project_dir: Path) -> None:
    subprocess.run(['git', 'init', project_dir, '--initial-branch', GIT_BRANCH])
    subprocess.run(['git', '-C', project_dir, 'add', '.'])
    subprocess.run(['git', '-C', project_dir, 'commit', '-m', GIT_COMMIT])


if __name__ == '__main__':
    main()
