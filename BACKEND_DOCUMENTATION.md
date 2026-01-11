# DragonOps Backend Documentation

## 1. Executive Summary
This document outlines the backend architecture, data flow, and implementation details for the **DragonOps** DevOps SaaS platform. The system is designed to provide a robust, scalable, and responsive API to support the React-based frontend, handling complex data relationships for clients, projects, environments, and server infrastructure.

## 2. Technology Stack

*   **Core Framework**: FastAPI (Python 3.10+)
    *   *Why*: High performance (async), automatic OpenAPI documentation, strict type validation (Pydantic).
*   **Database**: PostgreSQL (via Supabase)
    *   *Why*: Robust relational data model, built-in Auth, Real-time capabilities, and row-level security.
*   **ORM/Data Access**: `supabase-py` client (Postgrest)
    *   *Why*: Seamless integration with Supabase, clean query syntax.
*   **Authentication**: Supabase Auth (JWT)
    *   *Why*: Secure, handled entirely by Supabase, easy RBAC implementation.

## 3. System Architecture

The application follows a **Service-Oriented Architecture (SOA)** within a monolithic codebase for ease of development, structured as follows:

```mermaid
graph TD
    Client[React Frontend] -->|REST API (JSON)| API[FastAPI Backend]
    API -->|Auth Check| Middleware[CORSMiddleware]
    
    subgraph "FastAPI Application"
        Router[API Routers]
        Logic[Business Logic]
        Models[Pydantic Models]
        
        Router --> Logic
        Logic --> Models
    end
    
    API -->|Query| DB[(Supabase PostgreSQL)]
    DB -->|Auth Events| Triggers[DB Triggers]
```

## 4. Data Flow & Business Logic

### 4.1 Authentication Flow
1.  **User Action**: User logs in on Frontend.
2.  **Supabase Auth**: Returns a JWT (Access Token).
3.  **API Requests**: Frontend attaches `Authorization: Bearer <token>` to all requests.
4.  **Backend Verification**: (Future) Middleware validates the JWT signature.
5.  **User Profile**: A Database Trigger (`on_auth_user_created`) automatically copies new users from `auth.users` to the public `profiles` table to assign roles (Admin/User).

### 4.2 Dashboard & Analytics Flow
*   **Endpoint**: `GET /api/stats/dashboard`
*   **Logic**: 
    *   Performs highly optimized `COUNT` queries across `clients`, `projects`, and `servers` tables.
    *   Aggregates health scores from the `monitors` table.
*   **Response**: Returns a lightweight JSON object with summary metrics, ensuring the Dashboard loads instantly without fetching heavy detailed lists.

### 4.3 Hierarchy Data Flow (The "DragonOps Core")
The core value of DragonOps is managing the infrastructure hierarchy. The data flows top-down:

1.  **Clients** (`/api/clients`)
    *   Root entity. Represents a paying customer.
2.  **Projects** (`/api/projects`)
    *   Belong to a Client. backend fetches relationship via `clientId`.
3.  **Environments** (`/api/environments`)
    *   Belong to a Project (e.g., `Production`, `Staging`).
    *   Stores `resource_usage` JSON (CPU/RAM stats).
4.  **Servers** (`/api/servers`)
    *   The physical/virtual compute units running inside an Environment.

**Data Access Strategy**: 
*   Heavy reliance on **Foreign Keys** and **Joins** via Supabase.
*   Example: `supabase.table("projects").select("*, environments(*)")` allows fetching a project and all its environments in a single HTTP request, preventing "N+1 query" performance issues on the frontend.

### 4.4 Real-Time Monitoring Flow
*   **Endpoint**: `GET /api/monitoring`
*   **Simulation**:
    *   The backend retrieves uptime records from the `monitors` table.
    *   *Production Flow*: A background worker (Celery/Redis Queue) would ping target URLs every 60 seconds and update the `status` and `response_time` columns in the DB. The API simply reads this latest state.

### 4.5 AI Infrastructure Assistant
*   **Endpoint**: `POST /api/ai/generate`
*   **Input**: Natural language prompt (e.g., "Create an Nginx config for a React app").
*   **Process**:
    1.  Sanitizes input.
    2.  Matches keywords or sends context to an LLM (OpenAI/Gemini).
    3.  Formats the output code block.
*   **Output**: Returns JSON with `code` (string) and `explanation` (string).

## 5. Database Schema (ERD)

| Entity | Primary Key | Foreign Key | Key Fields |
| :--- | :--- | :--- | :--- |
| **Clients** | `id` | - | `name`, `status`, `projectCount` |
| **Projects** | `id` | `clientId` | `name`, `status`, `technology[]` |
| **Environments**| `id` | `projectId` | `name`, `url`, `resources (JSON)` |
| **Servers** | `id` | `environmentId`| `type`, `status`, `privateIp` |
| **Monitors** | `id` | - | `url`, `uptime`, `incidents` |
| **Secrets** | `id` | - | `key`, `value` (encrypted), `env` |
| **Settings** | `id` | - | `key`, `value` |

## 6. Directory Structure Mapping
```
app/
├── core/           # Configuration & Settings (Env vars)
├── db/             # Database connection & client instantiation
├── routes/         # API Endpoints (Controllers)
│   ├── clients.py
│   ├── projects.py
│   ├── ai.py
│   └── ...
├── schemas/        # Pydantic Models (Request/Response validation)
└── main.py         # App Entrypoint & CORS setup
```

## 7. Scalability & Future Considerations
*   **Caching**: Implement Redis caching for `/api/dashboard` stats to reduce DB load.
*   **Websockets**: Switch `/api/servers` to a WebSocket endpoint for live CPU/Memory usage streaming.
*   **Task Queue**: Move Server Actions (Restart/Stop) to a Celery task queue to handle long-running cloud operations asynchronously.
