# IHSG Market Insight

An automated Indonesian stock market reporting system built with Python and FastAPI. It collects market data, analyzes stock performance, and generates structured daily market insights.

The project is designed to integrate with n8n for scheduled report delivery to Discord.

## Setup

### Requirements

- Python 3.11+
- Git

### Installation

Clone the repository:

```bash
git clone https://github.com/naufalsutrisna/ihsg-market-insight.git
cd ihsg-market-insight
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Run the API

Start the FastAPI development server:

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | API health check |
| GET | `/market/summary` | IHSG market summary |
| GET | `/market/closing-insight` | Complete closing market insight |
| GET | `/market/closing-insight/discord` | Discord-formatted closing report |

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## Data Source

Market data is currently retrieved from Yahoo Finance using `yfinance`.

**Note:** Yahoo Finance is an unofficial data source and does not provide complete IDX market coverage or foreign investor flow data.
