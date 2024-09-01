# %%
import os

# List of directories to create
directories = [
    "LICENSE",
    "README.md",
    "data/external",
    "data/interim",
    "data/processed",
    "data/raw",
    "models",
    "notebooks",
    "references",
    "reports/figures",
    "src",
    "src/ingestion_pipeline",
    "src/monitoring",
    "src/services",
    "src/api",
]

# List of files to create
files = [
    "requirements.txt",
    "Dockerfile",
    "docker-compose.yml",
    "src/__init__.py",
    "src/config.py",
    "src/dataset.py",
    "src/features.py",
    "src/inference.py",
    "src/train.py",
    "src/plots.py",
    "src/ingestion_pipeline/__init__.py",
    "src/ingestion_pipeline/pipeline.py",
    "src/monitoring/__init__.py",
    "src/monitoring/grafana_dashboard.json",
    "src/monitoring/metrics.py",
    "src/services/__init__.py",
    "src/services/llm_service.py",
    "src/services/database_service.py",
    "src/api/__init__.py",
    "src/api/main.py",
    "src/api/routes.py",
]

# Create directories if they don't exist
for directory in directories:
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")
    else:
        print(f"Directory already exists: {directory}")

# Create files if they don't exist
for file in files:
    if not os.path.exists(file):
        with open(file, "a"):
            os.utime(
                file, None
            )  # Updates timestamp, creating the file if it doesn't exist
        print(f"Created file: {file}")
    else:
        print(f"File already exists: {file}")
