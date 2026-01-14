# Smart Expense Tracker

## Overview

Smart Expense Tracker is a full-stack web application designed to record, store, and analyze personal expenses.  
The system allows users to create expense records, categorize them, persist data in a relational database, and visualize spending patterns through a web interface.

The project focuses on **clean system architecture**, **API-driven design**, **database integration**, and **containerized deployment**, following modern software engineering practices.

---

## Problem Statement

Many individuals struggle to track their daily expenses consistently and understand their spending behavior over time. Manual methods such as spreadsheets or note-taking are error-prone and provide limited analytical insight.

This project addresses the problem by providing:
- A structured backend API for expense management
- A frontend interface for interacting with expense data
- Persistent storage using a relational database
- Analytical endpoints to summarize and group spending data

---

## Technologies Used

### Backend
- **Python 3**
- **FastAPI** – REST API framework
- **SQLAlchemy** – ORM for database interaction
- **Pydantic** – request/response validation
- **PostgreSQL** – relational database
- **Uvicorn** – ASGI server

### Frontend
- **React**
- **TypeScript**
- **Vite** – frontend build tool
- **Recharts** – data visualization
- **Axios** – API communication

### Infrastructure
- **Docker**
- **Docker Compose**
- **GitHub Actions** – CI pipeline

---

## System Architecture

The system follows a **client–server architecture**:

- **Frontend** communicates with the backend via RESTful HTTP endpoints.
- **Backend** exposes API routes, handles business logic, and interacts with the database.
- **Database** stores expenses, categories, and related data.
- **Docker Compose** orchestrates all services for reproducible execution.

---

## Project Structure

```text
smart-expense-tracker/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application entry point
│   │   ├── config.py            # Environment and configuration
│   │   ├── database.py          # Database engine and session
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── routers/             # API routes
│   │   ├── services/            # Business logic
│   │   └── tests/               # Backend tests
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/          # UI components
│   │   ├── services/            # API service layer
│   │   ├── types/               # TypeScript types
│   │   └── tests/               # Frontend tests
│   ├── Dockerfile
│   └── package.json
│
├── docker-compose.yml            # Service orchestration
├── .env.example                  # Environment variable template
└── README.md
```
## Backend Implementation

### Architecture Overview

The backend is implemented as a **modular FastAPI application** with a clean and maintainable architecture.

The project follows a **clear separation of concerns**:

- **Routers** – API layer (HTTP endpoints)
- **Services** – Business logic
- **Models** – Database layer (ORM models)
- **Schemas** – Validation and serialization layer (Pydantic)

### Key Features

- Database tables are **created automatically on application startup**
- **Default categories** are inserted during initialization
- API documentation is **generated automatically via OpenAPI**
- Clean, scalable structure suitable for production-grade APIs

---

## Frontend Implementation

### Architecture Overview

The frontend is built using **React + TypeScript** with a focus on maintainability and clarity.

### Key Design Principles

- **Centralized API calls** through a dedicated service layer
- **Reusable chart components** for analytics and visualization
- Clear separation between:
  - UI components
  - Application logic
  - API communication
- The frontend communicates **exclusively through the backend API**
- No direct database access from the frontend

---

## API Documentation

Once the backend is running, API documentation is available at:

http://localhost:8000/docs

### Swagger UI Capabilities

Using the Swagger UI, testers can:

- Inspect all available endpoints
- Submit test requests directly from the browser
- Verify request and response schemas
- Validate API behavior without external tools

---

## Containerization

The entire application is **fully containerized**.

### Services Included

- Frontend
- Backend
- PostgreSQL database

All services are managed using **Docker Compose**, ensuring consistent behavior across environments.

---

## How to Run the Project

### Requirements

- Docker
- Docker Compose

### Steps

```bash
git clone <repository-url>
cd smart-expense-tracker
docker-compose up --build
```




