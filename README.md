# 🤖 AI SQL Analytics Agent

> Transform natural language into SQL queries and generate AI-powered business insights from your database.

---

# 📖 Overview

AI SQL Analytics Agent is an intelligent analytics platform that allows users to interact with SQL databases using plain English instead of writing SQL queries manually.

The system uses Large Language Models (LLMs) to understand user questions, generate optimized SQL queries, execute them safely on the connected database, and return meaningful results with visualizations and AI-generated insights.

Instead of asking:

```sql
SELECT department, SUM(salary)
FROM employees
GROUP BY department;
```

Users can simply ask:

> "Show me total salary department wise."

or

> "Which products generated the highest revenue this month?"

The AI handles everything automatically.

---

# 🎯 Project Goals

The objective of this project is to build an AI-powered analytics assistant that can:

- Convert Natural Language → SQL
- Execute SQL safely
- Explain generated SQL
- Generate charts automatically
- Summarize results using AI
- Maintain conversation context
- Support multiple databases
- Provide enterprise-level security

---

# 🚀 Features

## 1. Natural Language to SQL

Users can ask questions in plain English.

Example:

```
Show top 10 customers by revenue.
```

Generated SQL

```sql
SELECT customer_name,
SUM(total_amount) AS revenue
FROM orders
GROUP BY customer_name
ORDER BY revenue DESC
LIMIT 10;
```

---

## 2. AI Query Explanation

Every generated SQL query is explained in simple language.

Example

> This query groups all orders by customer, calculates total revenue for each customer, sorts them in descending order, and returns the top 10 customers.

---

## 3. Database Execution

Execute generated SQL directly on the connected database.

Supported databases:

- MySQL
- PostgreSQL
- SQLite
- SQL Server (future)
- Oracle (future)

---

## 4. AI Insights

Instead of showing only rows, AI summarizes the results.

Example

```
Sales increased by 23% compared to last month.

North Region contributed 48% of total revenue.

Product X generated the highest sales.
```

---

## 5. Automatic Charts

Based on the query result, the AI automatically chooses the best visualization.

Supported charts:

- Bar Chart
- Line Chart
- Pie Chart
- Scatter Plot
- Area Chart
- Histogram

---

## 6. Conversational Analytics

The assistant remembers previous questions.

Example

User:

```
Show total sales.
```

Then

```
Now only for Delhi.
```

Then

```
Compare with Mumbai.
```

The agent understands the conversation without repeating the context.

---

## 7. Schema Understanding

The AI automatically understands:

- Tables
- Columns
- Primary Keys
- Foreign Keys
- Relationships

No manual SQL writing is required.

---

## 8. Safe SQL Execution

Only safe SQL statements are executed.

Allowed

- SELECT
- WITH (CTE)
- SHOW
- DESCRIBE
- EXPLAIN

Blocked

- DELETE
- DROP
- UPDATE
- INSERT
- ALTER
- TRUNCATE

This prevents accidental database modifications.

---

## 9. Query Validation

Before execution the SQL is validated for:

- Syntax
- Existing tables
- Existing columns
- SQL injection
- Dangerous operations

---

## 10. Query History

Maintain history of:

- User Questions
- Generated SQL
- Results
- Execution Time

---

## 11. Export Results

Users can export results as:

- CSV
- Excel
- JSON
- PDF (Future)

---

## 12. Authentication

Secure authentication using JWT.

Roles:

- Admin
- Analyst
- Viewer

---

## 🏗️ Project Architecture

```
                 User
                  │
                  ▼
        FastAPI REST API
                  │
                  ▼
          LangChain Agent
                  │
      ┌───────────┴───────────┐
      │                       │
      ▼                       ▼
 OpenAI LLM             SQL Toolkit
      │                       │
      └───────────┬───────────┘
                  ▼
          SQL Generator
                  │
                  ▼
         SQL Validator
                  │
                  ▼
        SQLAlchemy Engine
                  │
                  ▼
             MySQL Database
                  │
                  ▼
          Query Results
                  │
                  ▼
      AI Summary + Charts
                  │
                  ▼
               Response
```

---

# 📂 Project Structure

```
ai-sql-analytics-agent/

│
├── app/
│
├── api/
│   ├── routes/
│   └── dependencies/
│
├── core/
│   ├── config.py
│   ├── database.py
│   └── security.py
│
├── services/
│   ├── llm_service.py
│   ├── sql_service.py
│   ├── chart_service.py
│   ├── analytics_service.py
│   └── memory_service.py
│
├── prompts/
│   ├── sql_prompt.py
│   ├── summary_prompt.py
│   └── chart_prompt.py
│
├── models/
│
├── schemas/
│
├── repositories/
│
├── utils/
│
├── tests/
│
├── .env
├── requirements.txt
├── README.md
└── main.py
```

---

# ⚙️ Tech Stack

## Backend

- Python 3.12+
- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn

---

## AI

- OpenAI GPT-4.1 / GPT-5
- LangChain
- LangGraph (Future)

---

## Database

- MySQL
- PostgreSQL
- SQLite

---

## Data Processing

- Pandas
- NumPy

---

## Visualization

- Matplotlib
- Plotly

---

## Security

- JWT Authentication
- Environment Variables
- SQL Validation

---

## Testing

- Pytest

---

# 🔄 Workflow

```
User Question
      │
      ▼
Understand User Intent
      │
      ▼
Load Database Schema
      │
      ▼
Generate SQL using AI
      │
      ▼
Validate SQL
      │
      ▼
Execute Query
      │
      ▼
Fetch Result
      │
      ▼
Generate Charts
      │
      ▼
Generate AI Summary
      │
      ▼
Return Final Response
```

---

# 📊 Example

## User Question

```
Which employees earned more than 1 lakh this year?
```

### Generated SQL

```sql
SELECT employee_name,
SUM(salary) AS total_salary
FROM salaries
WHERE YEAR(payment_date)=YEAR(CURDATE())
GROUP BY employee_name
HAVING total_salary > 100000;
```

---

### AI Summary

```
15 employees earned more than ₹1,00,000 this year.

The highest-paid employee earned ₹8,75,000.

Engineering department contributed the majority of high-income employees.
```

---

# 🔒 Security

The system is designed with security as a priority.

Implemented safeguards include:

- Read-only SQL execution
- SQL injection prevention
- Query validation
- Parameterized queries
- Connection pooling
- Environment-based configuration
- JWT authentication
- Error handling without exposing database details

---

# 🚧 Future Enhancements

- Multi-database connections
- Dashboard creation using prompts
- Scheduled reports
- Email report delivery
- Voice-based analytics
- Role-based permissions
- Vector database for schema memory
- LangGraph multi-agent workflow
- MCP integration
- Business KPI recommendation engine
- Natural language dashboard builder

---

# 🎯 Use Cases

- Business Intelligence
- Finance Analytics
- HR Analytics
- Sales Reporting
- Inventory Analysis
- Customer Analytics
- Operations Dashboard
- Executive Reporting

---

# 👨‍💻 Development Roadmap

### Phase 1
- Project setup
- Database connection
- Schema extraction
- LLM integration

### Phase 2
- Natural language to SQL
- SQL validation
- Query execution

### Phase 3
- AI-generated summaries
- Chart generation
- Conversation memory

### Phase 4
- Authentication
- Query history
- Export functionality

### Phase 5
- Multi-database support
- Dashboard generation
- Agent orchestration
- Production deployment

---

# 🌟 Vision

Our goal is to build an AI-powered SQL Analytics Agent that enables anyone—regardless of SQL expertise—to explore and understand data through natural language. By combining large language models, database intelligence, and automated visualizations, the platform aims to make business analytics faster, more accessible, and more insightful.

Ultimately, the project aspires to evolve into a comprehensive AI analytics assistant capable of answering complex business questions, generating reports, recommending insights, and serving as a conversational interface for enterprise data.


Developed by Baibhav varshney