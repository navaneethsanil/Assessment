# Assessment API

This repository contains the source code for the **Assessment API** built with FastAPI. Follow the steps below to set up and run the project locally.

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/navaneethsanil/Assessment.git
cd assessment
code .  # Open in VS Code
```

### 2. Set Up the Virtual Environment

```bash
python -m venv env
source env/Scripts/activate  # Use `source env/bin/activate` on Unix-based systems
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root and add the following:

```env
# API Keys
GEMINI_API_KEY=

# Database
DB_HOST=
DB_PORT=
DB_USER=
DB_PASS=
DB_NAME=

# JWT Configuration
SECRET_KEY=
ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Run the Development Server

```bash
uvicorn app.main:app --host localhost --port 8000 --reload
```

## 📬 API Testing
NOTE: Ensure your server is running locally before testing the API. You can start the server with the following command
```bash
uvicorn app.main:app --host localhost --port 8000 --reload
```
You can test the API endpoints using [Postman](https://me-only-7199.postman.co/workspace/Assessment~e0f6c62e-66f7-4452-abc1-ee0de57c34ff/collection/35122471-99c731f8-bdb9-4977-bfa0-2dfb060f490f?action=share&creator=35122471&active-environment=35122471-c6eca3a0-bdfe-4dd9-b40a-a644627923e6).
