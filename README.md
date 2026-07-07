# 🤖 AI SQL Analytics Agent

> Transform natural language into SQL queries and generate AI-powered business insights from any SQL database using AI.

---

# 📖 Overview

AI SQL Analytics Agent is an intelligent analytics platform that enables users to query SQL databases using natural language instead of writing SQL manually.

Users simply connect their database, ask questions in plain English, and the platform automatically:

* Understands the database schema
* Generates optimized SQL
* Validates queries for security
* Executes SQL safely
* Produces AI-generated insights
* Recommends visualizations
* Maintains conversation context

The goal is to make business analytics accessible to everyone, regardless of SQL expertise.

---

# 🚀 Features

## 🔐 Authentication

* JWT Authentication
* Secure Login & Registration
* Password Hashing
* Protected APIs
* User-based Database Connections

---

## 🗄️ Database Connectivity

Supports multiple databases:

* MySQL
* PostgreSQL
* SQLite
* SQL Server (Planned)
* Oracle (Planned)

Each user securely stores their own encrypted database connection.

---

## 🧠 Automatic Schema Understanding

The agent automatically extracts:

* Tables
* Columns
* Data Types
* Primary Keys
* Foreign Keys
* Indexes
* Views
* Relationships

The extracted schema is converted into an AI-friendly context and cached for faster future queries.

---

## 💬 Natural Language to SQL

Ask questions like:

> Show top 10 customers by revenue.

> Compare sales between Delhi and Mumbai.

> Which department has the highest salary expense?

The AI automatically generates optimized SQL.

---

## 🛡 SQL Validation

Every generated query passes through a security layer.

Allowed:

* SELECT
* WITH (CTE)
* SHOW
* DESCRIBE
* EXPLAIN

Blocked:

* INSERT
* UPDATE
* DELETE
* DROP
* ALTER
* TRUNCATE
* Multiple Statements

This ensures the connected database remains read-only.

---

## ⚡ SQL Execution

Validated SQL is executed using SQLAlchemy.

The platform returns:

* Columns
* Rows
* Execution Time
* Total Records

---

## 📊 AI Business Insights

Instead of returning only raw rows, the AI explains:

* Important findings
* Trends
* Patterns
* Business insights
* Recommendations

---

## 📈 Smart Chart Recommendations

Based on query results, the system recommends:

* Bar Chart
* Line Chart
* Pie Chart
* Scatter Plot
* Area Chart
* Histogram

The frontend renders the visualization dynamically.

---

## 🧠 Conversation Memory

The assistant remembers previous questions.

Example:

User:

Show total sales.

User:

Only for Delhi.

User:

Compare with Mumbai.

The agent understands the previous conversation automatically.

---

## 📜 Query History

Every interaction stores:

* User Question
* Generated SQL
* Execution Time
* Results
* Timestamp

---

# 🏗️ System Architecture

```
                    User
                      │
             Login / Register
                      │
                JWT Authentication
                      │
               User Dashboard
                      │
           Connect Database
       (MySQL / PostgreSQL / SQLite)
                      │
           Test Database Connection
                      │
       Encrypt & Save Credentials
                      │
          Create SQLAlchemy Engine
                      │
              Schema Extraction
                      │
      Tables │ Columns │ PK │ FK │ Indexes │ Views
                      │
          Build Schema Context
                      │
            Cache Schema (Redis)
                      │
────────────────────────────────────────────
             User asks a question
────────────────────────────────────────────
                      │
        Conversation Memory Service
                      │
       Retrieve Previous Conversation
                      │
             Prompt Builder
      (Schema + History + User Prompt)
                      │
                 OpenAI LLM
                      │
             Generate SQL Query
                      │
            SQL Validation Layer
      ✓ SELECT only
      ✓ Single statement
      ✓ No UPDATE / DELETE / DROP
                      │
            SQL Execution Service
                      │
              Database Results
                      │
         Analytics / Insight Service
                      │
      ┌───────────────┼───────────────┐
      │               │               │
      ▼               ▼               ▼
AI Summary      Chart Generator   Recommendations
      │               │               │
      └───────────────┼───────────────┘
                      │
              Save Query History
                      │
                  API Response
                      │
              Frontend Dashboard
```

---

# 🏛️ Project Structure

```
ai-sql-analytics-agent/
│
├── backend/                       # FastAPI application
│   ├── main.py
│   ├── api/
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── database.py
│   │   │   └── ai.py
│   │   └── dependencies/
│   │       └── auth.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── db/
│   │   ├── database.py
│   │   ├── models.py
│   │   └── session.py
│   ├── ai/
│   │   ├── agent.py
│   │   ├── llm.py
│   │   └── tools/
│   │       ├── schema_tool.py
│   │       ├── execute_sql_tool.py
│   │       ├── chart_tool.py
│   │       └── recommendation_tool.py
│   ├── services/
│   │   ├── database_service.py
│   │   ├── schema_service.py
│   │   ├── sql_service.py
│   │   ├── sql_validator.py
│   │   ├── chart_service.py
│   │   ├── recommendation_service.py
│   │   ├── prompt_service.py
│   │   └── redis_service.py
│   ├── prompts/
│   │   ├── sql_prompt.py
│   │   └── recommendation_prompt.py
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── database.py
│   │   ├── schema.py
│   │   └── ai.py
│   └── utils/
│
├── frontend/                      # Vite + React + TypeScript SPA
│   ├── src/
│   │   ├── api/client.ts
│   │   ├── auth/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── public/
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   └── vite.config.ts
│
├── docker/
│   └── entrypoint.sh
├── tests/
├── sql_query/
├── Dockerfile                     # Backend image
├── docker-compose.yml             # db + redis + backend + frontend
├── requirements.txt
├── create_tables.py
├── run.py
├── .env.example
└── README.md
```

---

# ⚙️ Technology Stack

## Backend

* FastAPI
* SQLAlchemy
* Pydantic
* Uvicorn

## AI

* OpenAI GPT-5 / GPT-4.1
* LangChain (Optional)
* LangGraph (Future)

## Database

* MySQL
* PostgreSQL
* SQLite

## Data Processing

* Pandas
* NumPy

## Visualization

* Plotly
* Matplotlib

## Security

* JWT Authentication
* Password Hashing
* Encrypted Database Credentials
* SQL Validation
* Environment Variables

## Caching

* Redis (Production)
* In-Memory Cache (Development)

---

# 🔄 Complete Workflow

1. User authenticates using JWT.
2. User connects a SQL database.
3. Connection credentials are validated and encrypted.
4. SQLAlchemy creates a database engine.
5. Schema Service extracts tables, columns, keys, indexes, views, and relationships.
6. Schema context is cached.
7. User submits a natural language question.
8. Conversation memory is retrieved.
9. Prompt Builder combines:

   * Database schema
   * Conversation history
   * User question
10. OpenAI generates SQL.
11. SQL Validator verifies the query is safe.
12. SQL Execution Service runs the query.
13. Analytics Service generates business insights.
14. Chart Service recommends the best visualization.
15. Recommendations are generated.
16. Query history is stored.
17. API returns SQL, results, insights, charts, and recommendations to the frontend.

---

# 📦 Example Response

```json
{
  "question": "Show top 5 customers by revenue",
  "generated_sql": "SELECT ...",
  "execution_time": "0.18 sec",
  "columns": [
    "customer_name",
    "revenue"
  ],
  "rows": [
    {
      "customer_name": "ABC Ltd",
      "revenue": 250000
    }
  ],
  "summary": "ABC Ltd generated the highest revenue this year.",
  "insights": [
    "Top 5 customers contributed 72% of total revenue.",
    "Revenue is concentrated among a few customers."
  ],
  "recommendations": [
    "Focus retention efforts on high-value customers.",
    "Investigate opportunities to diversify revenue."
  ],
  "chart": {
    "type": "bar",
    "x": "customer_name",
    "y": "revenue"
  }
}
```

---

# 🚀 Development Roadmap

## Phase 1

* Authentication
* Database Connection
* Schema Extraction
* Schema Cache

## Phase 2

* Prompt Builder
* LLM Integration
* SQL Generation
* SQL Validation
* SQL Execution

## Phase 3

* AI Insights
* Chart Recommendation
* Conversation Memory
* Query History

## Phase 4

* Saved Reports
* Export (CSV / Excel / PDF)
* Dashboard Builder
* Scheduled Reports

## Phase 5

* Multi-Agent Workflow
* Multi-Database Analytics
* MCP Integration
* KPI Recommendation Engine
* AI Dashboard Generation

---

# 🌟 Vision

AI SQL Analytics Agent aims to become an enterprise-grade conversational analytics platform where users can securely connect their databases, ask questions in natural language, and instantly receive accurate SQL queries, business insights, visualizations, and actionable recommendations.

The long-term vision is to evolve beyond SQL generation into a complete AI-powered business intelligence platform capable of building dashboards, generating reports, monitoring KPIs, and acting as an intelligent data analyst for organizations.

---

Developed by **Baibhav Varshney**
