# eairt-kb

**Enterprise Artificial Intelligence Runtime Knowledge Store**

A lightweight, production-ready REST API for storing, retrieving, and semantically searching structured knowledge entries for use at AI runtime.

## Features

- **CRUD** operations for knowledge entries (create, read, update, delete)
- **Full-text search** over entry content and metadata
- **Tagging and categorization** of entries
- **Versioning** of entry content
- **Health** endpoint
- **OpenAPI** documentation (Swagger UI at `/docs`)

## Quick Start

### Prerequisites

- Python 3.11+
- `pip`

### Install

```bash
pip install -r requirements.txt
```

### Run

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

### Docker

```bash
docker build -t eairt-kb .
docker run -p 8000:8000 eairt-kb
```

## Configuration

Environment variables (all optional):

| Variable | Default | Description |
|----------|---------|-------------|
| `EAIRT_KB_HOST` | `0.0.0.0` | Bind host |
| `EAIRT_KB_PORT` | `8000` | Bind port |
| `EAIRT_KB_LOG_LEVEL` | `info` | Log level |
| `EAIRT_KB_DB_URL` | `sqlite:///./eairt_kb.db` | SQLAlchemy database URL |

## API Overview

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/entries` | List entries (with optional search/filter) |
| `POST` | `/entries` | Create a new entry |
| `GET` | `/entries/{id}` | Get entry by ID |
| `PUT` | `/entries/{id}` | Update an entry |
| `DELETE` | `/entries/{id}` | Delete an entry |
| `GET` | `/entries/{id}/history` | Get version history of an entry |
| `GET` | `/tags` | List all tags |

## Development

```bash
pip install -r requirements-dev.txt
pytest
```

## License

Apache 2.0