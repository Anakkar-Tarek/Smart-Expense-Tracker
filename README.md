# Smart Expense Tracker with Receipt OCR

## Problem Description

**The Challenge:**
Tracking personal expenses is tedious and time-consuming. People accumulate receipts but rarely log them consistently. By month's end, they've lost track of spending patterns, making budgeting and financial planning difficult. Existing solutions are either too complex (enterprise accounting software) or too basic (spreadsheets that require manual data entry).

**The Solution:**
A web application that simplifies expense tracking by:
- **Automating data entry**: Upload receipt photos and automatically extract merchant, amount, date, and items using free OCR technology
- **Manual entry option**: Quick form for expenses without receipts
- **Smart categorization**: Organize expenses into categories (food, transport, utilities, entertainment, etc.)
- **Visual analytics**: Interactive charts showing spending patterns by category and time
- **Budget tracking**: Set monthly budgets and receive visual alerts when approaching limits
- **Export capability**: Download expense data as CSV for tax purposes or further analysis

**Target Users:**
- Individuals tracking personal finances
- Freelancers managing business expenses
- Anyone wanting to understand their spending habits

## System Architecture

### Frontend
- **React 18** with TypeScript for type safety
- **Tailwind CSS** for responsive, modern UI
- **Recharts** for data visualization (pie charts, trend graphs)
- **Axios** with centralized API service layer
- **Vite** for fast development and building

### Backend
- **FastAPI** (Python 3.11+) - Modern, fast web framework with automatic OpenAPI docs
- **Tesseract OCR** - Free, open-source OCR engine for receipt text extraction
- **Pillow** - Image preprocessing for better OCR accuracy
- **SQLAlchemy** - ORM for database operations
- **Pydantic** - Data validation matching OpenAPI schema

### Database
- **PostgreSQL** for production (robust, reliable)
- **SQLite** for development/testing (zero configuration)
- Environment-based configuration for seamless switching

### Infrastructure & DevOps
- **Docker & Docker Compose** - Full containerization of all services
- **GitHub Actions** - CI/CD pipeline for automated testing and deployment
- **Render/Railway** - Free tier cloud deployment
- **pytest** - Backend testing with >80% coverage
- **Vitest/React Testing Library** - Frontend component and integration testing

## Features

### Core Functionality
1. ✅ **Receipt OCR Processing**
   - Upload JPG/PNG receipt images
   - Automatic extraction of merchant name, total amount, date
   - Confidence scoring for OCR results
   - Manual editing of extracted data

2. ✅ **Manual Expense Entry**
   - Quick form with merchant, amount, category, date
   - Optional notes field
   - Date picker with default to today

3. ✅ **Expense Management**
   - View all expenses in a sortable, filterable table
   - Search by merchant name or notes
   - Filter by date range, category, amount
   - Edit or delete individual expenses

4. ✅ **Analytics Dashboard**
   - Spending by category (pie chart)
   - Monthly spending trends (line chart)
   - Category comparison (bar chart)
   - Total spending summary

5. ✅ **Data Export**
   - Export filtered expenses to CSV
   - Includes all expense details
   - Useful for tax records or external analysis

### Technical Features
- RESTful API following OpenAPI 3.0 specification
- Comprehensive error handling and validation
- Responsive design (mobile, tablet, desktop)
- Database migrations for schema versioning
- Environment-based configuration
- Structured logging
- Health check endpoints

## Project Structure

```
expense-tracker/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI application entry point
│   │   ├── config.py                # Environment configuration
│   │   ├── database.py              # Database connection & session
│   │   ├── models.py                # SQLAlchemy ORM models
│   │   ├── schemas.py               # Pydantic schemas (validation)
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── expenses.py          # Expense CRUD endpoints
│   │   │   ├── categories.py        # Category endpoints
│   │   │   └── analytics.py         # Analytics & reporting
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── ocr_service.py       # Tesseract OCR integration
│   │   └── tests/
│   │       ├── __init__.py
│   │       ├── conftest.py          # pytest fixtures
│   │       ├── test_expenses.py     # Expense endpoint tests
│   │       ├── test_categories.py   # Category tests
│   │       ├── test_analytics.py    # Analytics tests
│   │       └── test_ocr.py          # OCR service tests
│   ├── uploads/                      # Receipt image storage
│   ├── requirements.txt              # Python dependencies
│   ├── Dockerfile                    # Backend container
│   ├── pytest.ini                    # pytest configuration
│   └── alembic/                      # Database migrations
│       ├── versions/
│       └── env.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ExpenseForm.tsx      # Manual entry form
│   │   │   ├── ExpenseList.tsx      # Expense table
│   │   │   ├── ReceiptUpload.tsx    # OCR upload component
│   │   │   ├── Dashboard.tsx        # Analytics dashboard
│   │   │   ├── CategoryFilter.tsx   # Filter controls
│   │   │   └── charts/
│   │   │       ├── PieChart.tsx
│   │   │       ├── TrendChart.tsx
│   │   │       └── BarChart.tsx
│   │   ├── services/
│   │   │   └── api.ts               # Centralized API client
│   │   ├── types/
│   │   │   └── index.ts             # TypeScript interfaces
│   │   ├── App.tsx                  # Main application
│   │   ├── main.tsx                 # Entry point
│   │   └── tests/
│   │       ├── ExpenseForm.test.tsx
│   │       ├── Dashboard.test.tsx
│   │       └── api.test.ts
│   ├── public/
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── Dockerfile
├── docker-compose.yml                # Multi-container orchestration
├── .github/
│   └── workflows/
│       └── ci-cd.yml                 # CI/CD pipeline
├── openapi.yaml                      # API contract specification
├── README.md                         # This file
├── AGENTS.md                         # AI development workflow
└── .env.example                      # Environment variables template
```

## Prerequisites

- **Docker** & **Docker Compose** (recommended for easiest setup)
- OR manually install:
  - Python 3.11+
  - Node.js 18+
  - PostgreSQL 14+ (or use SQLite for development)
  - Tesseract OCR

## Quick Start with Docker (Recommended)

```bash
# 1. Clone the repository
git clone <repository-url>
cd expense-tracker

# 2. Create environment file
cp .env.example .env
# Edit .env if needed (defaults work for Docker setup)

# 3. Build and start all services
docker-compose up --build

# 4. Access the application
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

That's it! The application is now running with PostgreSQL database.

## Manual Setup (Without Docker)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Tesseract OCR
# Ubuntu/Debian: sudo apt-get install tesseract-ocr
# macOS: brew install tesseract
# Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki

# Set environment variables
export DATABASE_URL=sqlite:///./expenses.db
export UPLOAD_DIR=./uploads

# Run database migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set API URL
echo "VITE_API_URL=http://localhost:8000" > .env

# Start development server
npm run dev
```

## Running Tests

### Backend Tests

```bash
cd backend
pytest --cov=app --cov-report=html
# View coverage report: open htmlcov/index.html
```

### Frontend Tests

```bash
cd frontend
npm test
npm run test:coverage
```

### Integration Tests

```bash
# With Docker Compose running
docker-compose exec backend pytest tests/test_integration.py
```

## Deployment

### Prerequisites
- GitHub account
- Render.com or Railway.app account (both offer free tiers)

### Steps

1. **Push code to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

2. **Deploy Backend (Render)**
   - Connect GitHub repository
   - Select "Web Service"
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Add environment variables (DATABASE_URL will be auto-provided)

3. **Deploy Frontend (Render)**
   - Select "Static Site"
   - Build command: `npm install && npm run build`
   - Publish directory: `dist`
   - Add environment variable: `VITE_API_URL=<backend-url>`

4. **Automated Deployment**
   - GitHub Actions workflow automatically runs tests on push
   - Deployment triggers on successful test completion

## API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

The API follows the OpenAPI 3.0 specification defined in `openapi.yaml`.

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost:5432/expenses
# Or for development: sqlite:///./expenses.db
UPLOAD_DIR=./uploads
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000
```

## Technology Decisions

### Why Tesseract OCR?
- **Free & Open Source**: No API costs or usage limits
- **Local Processing**: Privacy-friendly, no data sent to third parties
- **Mature**: Industry standard with 30+ years of development
- **Good Accuracy**: 85-95% accuracy on printed receipts with proper preprocessing

### Why FastAPI?
- **Modern Python**: Async support, type hints, automatic validation
- **Auto-Documentation**: OpenAPI/Swagger docs generated automatically
- **Fast**: Performance comparable to Node.js and Go
- **Easy Testing**: Built-in test client

### Why PostgreSQL?
- **Production-Ready**: ACID compliance, robust
- **Free**: Open source with no licensing costs
- **SQLAlchemy Support**: Excellent ORM integration
- **Scalable**: Can handle growth from prototype to production

### Why React + TypeScript?
- **Type Safety**: Catch errors at compile time
- **Component Reusability**: Modular, maintainable code
- **Large Ecosystem**: Libraries for charts, forms, etc.
- **Developer Experience**: Fast refresh, excellent tooling

## Development Workflow

See [AGENTS.md](AGENTS.md) for detailed information about:
- How AI tools (Claude) were used in development
- MCP (Model Context Protocol) integration
- Prompt engineering strategies
- Code generation workflows

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests for your changes
4. Ensure all tests pass (`pytest` and `npm test`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check existing documentation
- Review API docs at `/docs` endpoint

## Roadmap

Future enhancements:
- [ ] Mobile app (React Native)
- [ ] Multi-user support with authentication
- [ ] Recurring expense templates
- [ ] Budget alerts via email/SMS
- [ ] Receipt storage in cloud (S3/Cloudinary)
- [ ] Advanced OCR with item-level extraction
- [ ] Multiple currency support
- [ ] Bank statement import
- [ ] Expense sharing/splitting

---

**Built with ❤️ using modern web technologies and AI-assisted development**
