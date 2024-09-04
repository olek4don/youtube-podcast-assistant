## **Prepare environment**

1) ```conda create -n <name> python=3.12```
2) ```conda activate <name>```
3) ```conda env create -f environment.yaml```
\* If conda is not available, use ```pip install -r requirements.txt```

## Ingest transcripts

## Chunking transcripts into logical sentences

## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── README.md          <- The top-level README for developers using this project
├── data
│   ├── external       <- Data from third-party sources (e.g., transcripts from YouTube podcasts)
│   ├── interim        <- Intermediate data that has been transformed
│   ├── processed      <- The final, canonical data sets for modeling
│   └── raw            <- The original, immutable data dump
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── Dockerfile         <- Dockerfile to build the Docker image
├── docker-compose.yml <- Docker Compose file for orchestrating multi-container Docker applications
│
└── src                         <- Source code for this project
    │
    ├── __init__.py             <- Makes src a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download, clean, or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── inference.py            <- Code to run model inference with trained models (consider renaming `predict.py` to `inference.py`)
    │
    ├── train.py                <- Code to train models
    │
    ├── plots.py                <- Code to create visualizations
    │
    ├── ingestion_pipeline      <- Scripts or pipelines for data ingestion
    │   ├── __init__.py 
    │   └── pipeline.py         <- Define the data ingestion pipeline (e.g., Mage, Airflow, Prefect)
    │
    ├── monitoring              <- Scripts and configurations for monitoring (e.g., Grafana, Dash)
    │   ├── __init__.py
    │   ├── grafana_dashboard.json <- Example Grafana dashboard configuration
    │   └── metrics.py          <- Scripts to log and visualize metrics
    │
    ├── services                <- Service classes to connect with external platforms, tools, or APIs
    │   ├── __init__.py 
    │   ├── llm_service.py      <- Code to interface with LLMs like OpenAI, Ollama, etc.
    │   └── database_service.py <- Code to interface with the knowledge base (e.g., PostgreSQL)
    │
    └── api                     <- API layer (FastAPI)
        ├── __init__.py
        ├── main.py             <- FastAPI entry point
        └── routes.py           <- API route definitions

```
