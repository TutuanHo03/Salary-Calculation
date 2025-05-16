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
- [CI/CD Pipeline](#ci/cd-pipeline)

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

### Docker Deployment Setup

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

# Upload Excel file for bulk processing
curl -X POST http://localhost:8000/api/salary/upload \
  -F "file=@Salary-Calculation/test/data/data_test_gross_net.xlsx" \
  -H "Content-Type: multipart/form-data"
```

## CI/CD Pipeline

### Workflow Configuration

The GitHub Actions workflow is defined in `.github/workflows/github-actions.yaml` and performs the following steps:

1. **Trigger conditions**:
   - On push to the `main` branch
   - On pull requests to the `main` branch
   - Manual trigger via workflow_dispatch

2. **Testing**:
   - Sets up Python environment
   - Installs dependencies
   - Runs pytest with coverage report
   - Uploads coverage reports as artifacts

3. **Building and Pushing Docker Images**:
   - Builds backend and frontend Docker images
   - Tags images with commit SHA and 'latest'
   - Pushes images to Docker Hub
   - (Only runs on successful merges to main)

4. **Deployment**:
   - Triggers Render.com deployment webhook
   - Waits for deployment completion
   - Runs basic health checks on deployed services

### Setting Up the CI/CD Pipeline

1. **Configure GitHub repository secrets**:
   - `DOCKER_USERNAME`: Your Docker Hub username
   - `DOCKER_PASSWORD`: Your Docker Hub access token
   - `RENDER_WEBHOOK`: Render.com deployment webhook URL

2. **Enable GitHub Actions**:
   - Go to your repository → Actions tab
   - Enable workflows

3. **Deploy on Render.com**:
   - Create a new Web Service in your Render dashboard
   - Select "Container Registry" as deployment type
   - Configure container settings:
     - Registry: `Docker Hub`
     - Image: `yourusername/python_api-backend:latest`
     - Port: `8000`
   - Configure environment variables:
     - `PYTHONPATH`: `/app`
     - `PORT`: `8000`
   - Repeat the process for the frontend service:
     - Image: `yourusername/python_api-frontend:latest`
     - Port: `8501`
     - Environment variables:
       - `API_URL`: `https://your-backend-service.onrender.com`

4. **Verify deployment**:
   - Backend: Visit `https://your-backend-service.onrender.com/docs`
   - Frontend: Visit `https://your-frontend-service.onrender.com`

5. **Set up Render webhook**:
   - In Render.com dashboard, go to your service
   - Navigate to Settings → Deploy Hooks
   - Create a new deploy hook and copy the URL
   - Add this URL as the `RENDER_WEBHOOK` secret in GitHub

### Troubleshooting Deployment

- **Container fails to start**:
  - Check logs in Render dashboard
  - Verify environment variables are correctly set
  - Try building and running containers locally first

- **Services can't communicate**:
  - Check network settings in Docker Compose
  - Verify API_URL is correctly set for frontend service
  - Check for CORS issues in backend logs

- **CI/CD pipeline failures**:
  - Check GitHub Actions logs for detailed error messages
  - Verify Docker Hub credentials are correct
  - Check if tests are passing locally






