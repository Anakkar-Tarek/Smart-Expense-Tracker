# Smart Expense Tracker

## 📁 Project Structure


smart-expense-tracker/
├── .github/
│   └── workflows/
│       └── ci.yml                  # CI pipeline (tests & checks)
│
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI app entry point
│   │   ├── config.py               # Environment & database configuration
│   │   ├── database.py             # SQLAlchemy engine & session
│   │   ├── models.py               # Database models
│   │   ├── schemas.py              # Pydantic request/response schemas
│   │   ├── routers/                # API route definitions
│   │   │   ├── expenses.py
│   │   │   ├── categories.py
│   │   │   └── analytics.py
│   │   ├── services/               # Business logic layer
│   │   │   └── analytics_service.py
│   │   └── tests/                  # Backend unit & integration tests
│   │
│   ├── Dockerfile                  # Backend container definition
│   │   └── requirements.txt        # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/             # Reusable UI components
│   │   │   └── charts/             # Data visualization components
│   │   ├── services/               # Centralized API calls
│   │   ├── types/                  # Shared TypeScript types
│   │   ├── tests/                  # Frontend tests
│   │   └── main.tsx
│   │
│   ├── public/
│   ├── Dockerfile                  # Frontend container definition
│   └── package.json
│
├── docker-compose.yml               # Full system orchestration
├── README.md                        # Project documentation
└── .env.example                     # Environment variable template

📌 Problem Description
Managing personal expenses is often fragmented across spreadsheets, notes, or basic mobile apps that provide little insight into spending behavior. Users struggle to understand where their money goes, identify spending patterns, and make informed financial decisions.

Smart Expense Tracker is a full-stack web application designed to help users:

Record and categorize daily expenses

Store data persistently in a relational database

Analyze spending trends over time

Visualize expenses through charts and summaries

The system provides a clean user interface backed by a structured REST API and database, enabling reliable tracking and analysis of personal finances.

🤖 AI-Assisted System Development (Tools, Workflow, MCP)
This project was developed using AI-assisted programming workflows to accelerate development and improve code quality.

AI Tools Used
ChatGPT as a development assistant for:

Designing FastAPI endpoints

Structuring SQLAlchemy models and schemas

Debugging Docker, database, and import issues

Improving system architecture and documentation

Development Workflow
High-level feature planning and API design

Backend scaffolding with FastAPI and SQLAlchemy

Database integration and startup initialization

Frontend development with a centralized API layer

Containerization using Docker and docker-compose

Iterative debugging and refinement using AI feedback

MCP (Model Context Protocol)
No external MCP server is deployed. However, context-driven prompting was used to maintain consistency across:

API contracts

Database models

Frontend data expectations

This ensured alignment between frontend requirements and backend implementation.

🏗️ Technologies & System Architecture
Frontend
React with TypeScript

Vite for development and bundling

Recharts for data visualization

Centralized API communication layer (services/)

Backend
FastAPI for REST API development

SQLAlchemy ORM

Pydantic schemas for validation

Modular router-based architecture

Database
PostgreSQL as the primary database

SQLAlchemy abstracts the database layer

Architecture supports alternative databases (e.g., SQLite) with minimal changes

Containerization
Docker for frontend and backend services

docker-compose orchestrates:

Frontend

Backend

PostgreSQL database

CI/CD
GitHub Actions

Automated tests and checks on push

🎨 Frontend Implementation
Fully functional React frontend

Clean and modular component structure

Backend communication centralized in frontend/src/services

Charts and analytics implemented as reusable components

Frontend tests cover core logic and API integration

📜 API Contract (OpenAPI)
FastAPI automatically generates OpenAPI / Swagger documentation

Available at:

bash
Copy code
http://localhost:8000/docs
The OpenAPI specification serves as the contract between frontend and backend

Endpoints are designed to reflect frontend data requirements precisely

⚙️ Backend Implementation
Well-structured FastAPI application

Clear separation of concerns:

Routers (API layer)

Services (business logic)

Models (database layer)

Schemas (validation layer)

Backend follows the OpenAPI contract

Includes startup database initialization and default data insertion

Backend tests cover core functionality

🗄️ Database Integration
PostgreSQL database with persistent Docker volumes

SQLAlchemy ORM manages all database interactions

Database initialization runs automatically on startup

Designed to support multiple environments (development and production)

🐳 Containerization
The entire system runs using docker-compose.

Start the system
bash
Copy code
docker-compose up --build
Services
Frontend: http://localhost:5173

Backend API: http://localhost:8000

Database: PostgreSQL (port 5432)

No manual setup steps are required beyond Docker.

🧪 Testing & Validation
Backend Testing
Unit and integration tests included

Database-dependent workflows are tested

Tests are isolated from application logic

Frontend Testing
UI and service-level tests included

Focus on API interaction and core logic

Testing Tips for Reviewers
Ensure all containers are running before testing

Verify database tables are created on startup

Check /docs endpoint for API availability

Confirm frontend charts update after adding expenses

🚀 Deployment
Fully containerized and deployment-ready

Can be deployed to any Docker-compatible environment

Reproducible build process using docker-compose

🔁 CI/CD Pipeline
GitHub Actions workflow included

Automatically runs tests on push

Prevents broken builds from being merged

♻️ Reproducibility
Requirements
Docker

Docker Compose

Steps
bash
Copy code
git clone <repository-url>
cd smart-expense-tracker
docker-compose up --build
On startup:

Database is initialized

Default categories are inserted

Frontend and backend become immediately usable
