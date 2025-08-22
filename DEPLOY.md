# Simple Deployment to GCP Compute Engine

## Steps:

1. **SSH to your compute engine:**
   ```bash
   gcloud compute ssh your-instance-name --zone=your-zone
   ```

2. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/indian_sm_dw_api.git
   cd indian_sm_dw_api
   ```

3. **Create environment file:**
   ```bash
   cp .env.example .env
   nano .env  # Edit with your database details
   ```

4. **Start the API:**
   ```bash
   docker compose up -d
   ```

5. **Test:**
   ```bash
   curl http://localhost:8000/db-test
   ```

## Environment Configuration

Your `.env` file should look like:
```bash
DATABASE_URL=postgresql+asyncpg://postgres:your-password@localhost:5432/indian_sm_dw
PORT=8000
DEBUG=false
```

## Management Commands

- **Start:** `docker compose up -d`
- **Stop:** `docker compose down`
- **Logs:** `docker compose logs -f`
- **Rebuild:** `docker compose up --build -d`

That's it! 🚀
