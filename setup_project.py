
from pathlib import Path

# Create the project structure in the current directory.
project_root = Path(__file__).parent

directories = [
    "app",
    "tests",
]

files = [
    "app/__init__.py",
    "app/config.py",
    "app/github_client.py",
    "app/routes.py",
    "app/main.py",
    "tests/__init__.py",
    "tests/test_api.py",
    ".env",
    ".env.example",
    ".gitignore",
    ".dockerignore",
    "requirements.txt",
    "Dockerfile",
    "README.md",
]

# Create directories.
for directory in directories:
    (project_root / directory).mkdir(parents=True, exist_ok=True)

# Create empty files without overwriting existing content.
for file in files:
    file_path = project_root / file
    file_path.parent.mkdir(parents=True, exist_ok=True)

    if not file_path.exists():
        file_path.touch()
        print(f"Created: {file}")
    else:
        print(f"Already exists: {file}")

print("\nProject structure created successfully!")
