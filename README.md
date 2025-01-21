# FastAPI Base Project 🚀

A FastAPI base project template for building modern and scalable APIs.

## 🌟 Features

- Modern API structure based on FastAPI
- Database integration with SQLAlchemy
- Automatic database migrations with Alembic
- Robust data validation with Pydantic
- Base classes for CRUD operations
- Modular and scalable project structure

## 🛠️ Technologies

- Python 3.11+
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- PostgreSQL

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- PostgreSQL
- pip

### Installation

1. Clone the project:
```bash
git clone https://github.com/yourusername/fastapi-base.git
cd fastapi-base
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env file with your settings
```

5. Run database migrations:
```bash
alembic upgrade head
```

6. Start the application:
```bash
uvicorn app.main:app --reload
```

## 📁 Project Structure

```
fastapi-base/
├── app/
│   ├── core/          # Core configurations and helper functions
│   ├── crud/          # CRUD operations
│   ├── models/        # SQLAlchemy models
│   ├── schemas/       # Pydantic models
│   ├── services/      # Business logic services
│   └── main.py        # Application entry point
├── migrations/        # Alembic migrations
├── .env              # Environment variables
├── alembic.ini       # Alembic configuration
└── requirements.txt   # Project dependencies
```

## 🔗 API Documentation

Access the API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👏 Contributors

Special thanks to: Cursor and Claude 