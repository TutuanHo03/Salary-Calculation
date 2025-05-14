# Salary Calculation System

A full-stack web application for calculating net salary from gross salary, with support for both individual calculations and bulk processing through Excel uploads.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Deployment](#deployment)
- [License](#license)

## Features

- **Single Salary Calculation**: Convert gross salary to net salary with personalized deduction options
- **Bulk Processing**: Upload Excel files with employee data for mass salary calculations
- **Excel Integration**: Download templates and results as Excel files
- **Modern UI**: Clean and responsive interface built with Streamlit
- **Dockerized**: Easy deployment with Docker containers

## Tech Stack

### Backend
- **FastAPI**: High-performance API framework
- **Pydantic**: Data validation and settings management
- **Pandas**: Data manipulation and Excel file processing
- **pytest**: Comprehensive testing

### Frontend
- **Streamlit**: Interactive data application framework
- **Pandas**: Data processing and Excel integration
- **Requests**: API communication

### DevOps
- **Docker & Docker Compose**: Containerization and multi-container orchestration
- **GitHub Actions**: Continuous Integration and Testing
- **Render**: Cloud deployment

##  Project Structure

```
Salary-Calculation/
│
├── app/                     # Backend API
│   ├── api/                 # API routes
│   │   └── routes/          # Endpoint definitions
│   ├── models/              # Data models and schemas
│   ├── services/            # Business logic
│   ├── main.py              # Application entrypoint
│   ├── Dockerfile           # Backend container definition
│   └── requirements.txt     # Python dependencies
│
├── frontend/                # Streamlit web application
│   ├── app.py               # Frontend application code
│   ├── Dockerfile           # Frontend container definition
│   └── requirements.txt     # Frontend dependencies
│
├── test/                    # Test directory
│   ├── test_salary_service.py  # Service tests
│   └── test_salary_routes.py   # API route tests
│
├── .github/workflows/       # CI/CD workflows
├── compose.yaml             # Docker Compose configuration
└── README.md                # Documentation
```

##  Getting Started

### Prerequisites

- Python 3.8+
- Docker and Docker Compose (for containerized deployment)
- Git

### Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Salary-Calculation.git
   cd Salary-Calculation
   ```

2. Set up virtual environments and install dependencies:
   ```bash
   # Backend
   cd app
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cd ..

   # Frontend
   cd frontend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cd ..
   ```

3. Run the backend:
   ```bash
   cd app
   uvicorn main:app --reload
   ```

4. Run the frontend (in a new terminal):
   ```bash
   cd frontend
   streamlit run app.py
   ```

### Docker Setup

For a containerized setup with Docker Compose:

```bash
docker compose up -d
```

This will start both the backend and frontend services.

##  Usage

### Single Salary Calculation

1. Navigate to the "Single Calculation" tab in the application
2. Enter the gross salary amount
3. Specify the number of dependents
4. Click "Calculate" to see the results

### Bulk Salary Calculation

1. Navigate to the "Bulk Upload" tab
2. Download the Excel template
3. Fill in employee information (ID, name, gross salary, and number of dependents)
4. Upload the completed template
5. Click "Process Salaries" to calculate results for all employees
6. Download the results as an Excel file

## API Documentation

When running the backend, API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Key Endpoints

- `POST /api/salary/calculate`: Calculate net salary for a single gross salary
- `POST /api/salary/upload`: Process an Excel file and calculate net salaries for multiple employees

## Testing

Run the test suite with pytest:

```bash
python -m pytest test/
```

### Manual Testing

You can also use curl or Postman to test the API endpoints:

```bash
# Calculate single salary
curl -X POST http://localhost:8000/api/salary/calculate \
  -H "Content-Type: application/json" \
  -d '{"gross_salary": 15000000, "number_of_dependents": 2}'
```

##  Deployment

### Deploying with Docker Registry

1. Build and push Docker images:
   ```bash
   docker build -t yourusername/python_api-backend:latest ./app
   docker build -t yourusername/python_api-frontend:latest ./frontend
   
   docker push yourusername/python_api-backend:latest
   docker push yourusername/python_api-frontend:latest
   ```

2. Deploy on Render:
   - Create a new Web Service
   - Use the Container Registry option
   - Configure environment variables:
     - For backend: `PYTHONPATH=/app`
     - For frontend: `API_URL=https://your-backend-service.onrender.com`

### Continuous Deployment

The project uses GitHub Actions for CI/CD:
- Runs tests on every push to master
- Builds and pushes Docker images
- Triggers deployment on Render via webhooks


