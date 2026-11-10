# IHSG Market Insight

An automated Indonesian stock market reporting system built with Python and FastAPI. It collects market data, analyzes stock performance, and generates structured daily market insights.

The project integrates with n8n for scheduled report delivery to Discord.

## Setup

### Requirements

- Python 3.11+
- Git
- Docker Desktop

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
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | API health check |
| GET | `/market/summary` | IHSG market summary |
| GET | `/market/closing-insight` | Complete closing market insight |
| GET | `/market/closing-insight/discord` | Discord-formatted closing report |

## Discord Integration

Discord is used as the notification platform for automated market reports.

### 1. Create a Discord Webhook

1. Open your Discord server.
2. Navigate to the target channel (e.g. `#general`).
3. Open **Edit Channel → Integrations**.
4. Select **Webhooks**.
5. Click **New Webhook**.
6. Configure the webhook name and target channel.
7. Copy the webhook URL.

**Important:** Keep the webhook URL private. Anyone with access to it can send messages to your Discord channel.

## n8n Setup

n8n handles workflow scheduling and report delivery. In this project, n8n runs locally using Docker Desktop.

### 1. Install Docker Desktop

Download and install Docker Desktop:

https://www.docker.com/products/docker-desktop/

Make sure Docker Desktop is running before proceeding.

### 2. Create Persistent Storage

Create a Docker volume to store n8n data:

```bash
docker volume create n8n_data
```

This volume preserves n8n configurations, credentials, and workflows when the container is recreated.

### 3. Download the n8n Image

```bash
docker pull n8nio/n8n:latest
```

### 4. Run n8n

Start the n8n container:

```bash
docker run -d \
  --name n8n \
  --restart unless-stopped \
  -p 5678:5678 \
  -e GENERIC_TIMEZONE=Asia/Jakarta \
  -e TZ=Asia/Jakarta \
  -v n8n_data:/home/node/.n8n \
  n8nio/n8n:latest
```

Access the n8n editor:

```text
http://localhost:5678
```

Create an owner account during the initial setup.

### 5. Configure the Workflow

Create a new workflow named:

`IHSG Closing Insight - Discord`

The workflow consists of three nodes:

**Schedule Trigger**

Configure the schedule:

- Trigger Interval: Weeks
- Weeks Between Triggers: 1
- Trigger on Weekdays: Monday–Friday
- Trigger at Hour: 5 PM
- Trigger at Minute: 0

**HTTP Request — Get Market Report**

Configure the first HTTP Request node:

| Field | Value |
|---|---|
| Method | GET |
| URL | `http://host.docker.internal:8000/market/closing-insight/discord` |
| Authentication | None |

This endpoint retrieves the generated closing market report from FastAPI.

**HTTP Request — Send to Discord**

Configure the second HTTP Request node:

| Field | Value |
|---|---|
| Method | POST |
| URL | Your Discord Webhook URL |
| Authentication | None |
| Body Content Type | JSON |
| Specify Body | Using JSON |

Enable the JSON Body expression and use:

```javascript
{{ { content: $json.message } }}
```

This sends the formatted market report to the configured Discord channel.

**Security:** Store your Discord webhook URL securely in n8n. Never commit it to the repository or expose it in public documentation.

### 6. Publish the Workflow

1. Save the workflow.
2. Click **Publish**.
3. Confirm that the workflow is published and active.

The workflow is now configured to send the closing market report automatically every weekday at 17:00 WIB.

### 7. Runtime Requirements

Because n8n is running locally, the following services must remain available for scheduled execution:

- MacBook must be powered on.
- Docker Desktop and the n8n container must be running.
- FastAPI must be running.
- Internet connection must be available.

For continuous 24/7 automation, consider deploying n8n to a VPS or cloud server.

## Data Source

Market data is currently retrieved from Yahoo Finance using `yfinance`.

**Note:** Yahoo Finance is an unofficial data source and does not provide complete IDX market coverage or foreign investor flow data.
