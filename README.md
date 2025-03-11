# Multi-disease Forecasting Platform

## Overview
The **Multi-disease Forecasting Platform** is an end-to-end platform for forecasting multiple diseases using historical disease data and weather data. The application allows users to log in, upload disease datasets, retrieve relevant weather data dynamically, and generate forecasts. The system is containerized with Docker and deployed using Kubernetes, ensuring scalability and reliability.

## Features
- **User Authentication** (JWT/OAuth2-based secure login)
- **Dynamic Disease Data Upload** (via API or CSV/XLSX)
- **Automated Weather Data Retrieval** (via CDS API - ERA5 climate data)
- **AI-driven Disease Forecasting** (Machine Learning Models)
- **Interactive Dashboard** (Built with React.js)
- **API for Data Access & Model Predictions**
- **Logging & Monitoring** (ELK/EFK stack integration)
- **CI/CD Pipeline** (GitHub Actions/Jenkins for automated deployment)
- **Secure Secrets Management** (Kubernetes Secrets)
- **Scalable Deployment** (Docker & Kubernetes)

---

## Directory Structure
```
forecast_app/
├── .github/workflows/ci-cd.yml    # CI/CD pipeline configuration
├── Dockerfile                     # Containerization of the backend
├── app.py                          # Main Flask/FastAPI app entry point
├── cds_downloader/                 # Weather data retrieval module
│   ├── __init__.py
│   ├── country_utils.py            # Utility functions for country selection
│   ├── downloader.py                # Fetching ERA5 climate data
│   ├── process_grib.py              # Processing weather data files
├── dashboard/                      # React.js frontend for visualization
│   ├── package.json
│   ├── public/
│   │   ├── favicon.ico
│   │   ├── index.html
│   ├── src/
│   │   ├── App.js
│   │   ├── index.js
│   │   ├── components/
│   │   │   ├── Dashboard.js         # Main dashboard UI
│   │   │   ├── Login.js             # User authentication UI
│   │   ├── services/api.js          # API interaction service
│   │   ├── styles/main.css          # Stylesheets
├── deployment.yaml                 # Kubernetes deployment configuration
├── disease_processor.py            # Processing uploaded disease datasets
├── modeller/                        # AI/ML forecasting module
│   ├── __init__.py
│   ├── predict.py                   # Prediction logic
│   ├── train.py                     # Model training
│   ├── utils.py                     # Helper functions
├── pvc.yaml                         # Persistent volume configuration
├── requirements.txt                 # Python dependencies
├── secret.yaml                      # Kubernetes secrets for secure API keys
├── service.yaml                     # Kubernetes service configuration
```

---

## Setup & Installation
### **1. Clone the Repository**
```sh
git clone https://github.com/drkaushiksarkar/forecast_app.git
cd forecast_app
```

### **2. Set Up a Virtual Environment & Install Dependencies**
```sh
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### **3. Configure Environment Variables**
Create a `.env` file and add:
```env
SECRET_KEY=your_secret_key
CDS_API_KEY=your_cds_api_key
DATABASE_URL=your_database_url
```

### **4. Run the Backend Application**
```sh
python app.py
```
The API will be available at `http://127.0.0.1:5000`

### **5. Set Up the Frontend**
```sh
cd dashboard
npm install
npm start
```
The React dashboard will be available at `http://localhost:3000`

### **6. Run the Application with Docker**
#### **Build & Run the Docker Container**
```sh
docker build -t forecast_app .
docker run -p 5000:5000 forecast_app
```

### **7. Deploy with Kubernetes**
```sh
kubectl apply -f pvc.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

---

## API Endpoints
### **Authentication**
- `POST /auth/login` → User login
- `POST /auth/register` → User registration

### **Disease Data Handling**
- `POST /upload` → Upload disease data (CSV/XLSX)
- `GET /data` → Fetch stored disease data

### **Weather Data Retrieval**
- `GET /weather` → Fetch ERA5 weather data dynamically

### **Forecasting Model**
- `POST /predict` → Get disease forecast based on historical data

---

## Deployment & CI/CD
- **GitHub Actions** automates testing & deployment.
- **Docker** containers ensure portability.
- **Kubernetes** handles scaling & service orchestration.

---

## Security Measures
- **JWT Authentication** for API access.
- **Kubernetes Secrets** for storing sensitive credentials.
- **HTTPS Enforcement** in production environments.
- **Role-Based Access Control (RBAC)** for users.

---

## Future Enhancements
- Add more disease forecasting models.
- Improve UI/UX of the dashboard.
- Implement real-time notifications for new forecasts.

---

## Contributors
- **Chief Scientist & Lead Architect – Dr. Kaushik Sarkar
- **Contributors** - Malembe Sandrine Ebama, Maquines Sewe
- **Partner Organization** - Task Force for Global Health
- **Funding** - The Global Fund
- **Project** - Early Warning Surveillance

---

## License
This project is licensed under the **MIT License**.

---

## Contact
For any queries or contributions, reach out via [GitHub Issues](https://github.com/drkaushiksarkar/forecast_app/issues).
