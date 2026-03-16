# Dental Clinic — 3 рівні архітектура

```
dental_clinic/
├── data_access/          ← Рівень 1: БД, ORM, репозиторії
│   ├── database.py       # підключення, session, init_db
│   ├── models.py        # Patient, Dentist, Appointment, Visit, ...
│   └── repositories.py  # PatientRepository, DentistRepository, ...
│
├── business/             ← Рівень 2: бізнес-логіка
│   └── services.py      # імпорт CSV, валідація, збереження
│
├── presentation/          ← Рівень 3: API та контролери
│   ├── controllers.py   # приймає запит → викликає business → відповідь
│   └── api.py           # FastAPI, Swagger /docs
│
├── data/
│   └── dental_data.csv
├── main.py               # точка входу (CLI або uvicorn main:app)
└── requirements.txt
```

## Запуск

```bash
cd dental_clinic
pip install -r requirements.txt

python main.py              # імпорт CSV
uvicorn main:app --reload   # API + Swagger: http://127.0.0.1:8000/docs
```

## Потік даних

**Запит → Presentation (controllers/api) → Business (services) → Data Access (repositories) → БД**


first step - python3 scripts/generate_csv.py - generate data

sec step - python3 main.py - create db

test orm logic - python3 main.py - echo true

Swagger / API endpoints
        │
        ▼
Presentation Layer
(controllers / routes)
        │
        ▼
Business Logic Layer
(services)
        │
        ▼
Data Access Layer
(repositories + ORM)
        │
        ▼
Database

сенс розділення проєкту на рівні це про зручне читання і подальше маштабування, презентешн це про експіріенс з юзером, бізнес де загальна логіка проєкту, дата леєр це про використання базиданих

sqlalchemy це про викориснна зрозумілих логічних запитів в проєкті замістт іспорт селект і тд
