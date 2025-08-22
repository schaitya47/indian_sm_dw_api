# Indian Stock Market Data Warehouse API

A FastAPI application providing access to Indian stock market data.

## Quick Start with Docker

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd indian_sm_dw_api
```

### 2. Create environment file
```bash
cp .env.example .env
# Edit .env with your database details
```

### 3. Start the application
```bash
docker compose up -d
```

### 4. Test the API
```bash
curl http://localhost:8000/db-test
curl http://localhost:8000/docs
```

## Environment Variables

Update `.env` file with your database details:

```bash
DATABASE_URL=postgresql+asyncpg://postgres:your-password@your-db-host:5432/indian_sm_dw
PORT=8000
DEBUG=false
```

## API Endpoints

- `GET /` - API documentation
- `GET /db-test` - Database connectivity test
- `GET /stocks-list` - List available stocks
- `GET /stock-info/{symbol}` - Get stock information
- `GET /stock-ohlcv` - Get OHLCV data
- And more...

## Management Commands

```bash
# Start
docker compose up -d

# Stop
docker compose down

# View logs
docker compose logs -f

# Rebuild
docker compose up --build -d
```

## Development

For local development without Docker:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
