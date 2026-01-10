# DragonOps Backend

This is the backend for DragonOps, a DevOps SaaS application.

## Setup

1.  **Clone the repository** (if you haven't already).
2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure Environment**:
    *   Rename `.env.example` to `.env`.
    *   Fill in your `SUPABASE_URL` and `SUPABASE_KEY` (Anon Key).
5.  **Setup Database**:
    *   Run the SQL commands in `database.sql` in your Supabase SQL Editor to set up the tables and mock data.

## Running the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

## API Routes

*   `/api/health`: Health check
*   `/clients`: Client management
*   `/projects`: Project management
*   `/environments`: Environment management
*   `/servers`: Server management
*   `/monitoring`: Monitoring data
*   `/stats`: Dashboard statistics
*   `/ai`: AI generation (Mock)

## Stack

*   **FastAPI**: Web framework
*   **Supabase**: Database & Auth
*   **Pydantic**: Data validation
