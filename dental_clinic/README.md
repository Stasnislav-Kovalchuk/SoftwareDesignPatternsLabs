# Dental Clinic Management System — Лабораторна 3 (MVC) + 3‑рівнева архітектура

## Мета роботи

Створити веб‑додаток за шаблоном **MVC**, який за запитом користувача **візуалізує дані предметної області** “Стоматологічна клініка” (з ЛР1), та підтримує **CRUD** (додавання/редагування/видалення).

Архітектурно застосовано **3 рівні**:
- **Presentation Layer** — взаємодія з користувачем (HTML/HTTP контролери)
- **Business Logic Layer** — прикладна логіка (сервіси)
- **Data Access Layer** — ORM/репозиторії/SQLite

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

## Лабораторна 3 (MVC веб‑додаток)

### Основна сутність

**Patient** (Пацієнт) — основна сутність предметної області для демонстрації CRUD.

### MVC відповідність

- **Model**: `data_access/` (ORM + репозиторії) + бізнес‑сервіс `business/patient_service.py`
- **View**: `presentation/templates/*.html` (HTML сторінки)
- **Controller**: `presentation/api.py` (маршрути, що викликають бізнес‑логіку)

### CRUD (HTML)

- Список: `GET /ui/patients`
- Додати: `GET /ui/patients/new` + `POST /ui/patients/new`
- Редагувати: `GET /ui/patients/{id}/edit` + `POST /ui/patients/{id}/edit`
- Видалити: `POST /ui/patients/{id}/delete`

## Як це працює (логіка MVC)

1) **View (HTML)** відображає дані й відправляє форми (POST) на контролер.  
2) **Controller** (`presentation/api.py`) приймає запит і викликає **бізнес‑сервіс** `PatientService`.  
3) **Business** (`business/patient_service.py`) виконує логіку CRUD і працює з даними через **репозиторій**.  
4) **Repository** (`data_access/repositories.py`) виконує операції з БД через `Session`.  
5) **ORM/SQLite** (`data_access/models.py`, `data_access/database.py`) зберігає та повертає дані.

Таке розділення підвищує читабельність, тестованість і спрощує масштабування.

## Запуск

```bash
cd dental_clinic
pip install -r requirements.txt

python main.py              # імпорт CSV
uvicorn main:app --reload   # API + Swagger: http://127.0.0.1:8000/docs
```

## Рекомендований сценарій демонстрації

1) (Опціонально) Згенерувати тестовий CSV (1000+ рядків):

```bash
python3 scripts/generate_csv.py
```

2) Імпортувати CSV у SQLite (створить/оновить `dental_clinic.db`):

```bash
python main.py
```

3) Запустити веб‑додаток:

```bash
uvicorn main:app --reload
```

4) Відкрити в браузері:
- **MVC HTML (візуалізація + CRUD)**: `http://127.0.0.1:8000/ui/patients`
- **Swagger (API)**: `http://127.0.0.1:8000/docs`

## Потік даних (3 рівні)

```
Browser (HTML View) / Swagger
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
SQLite Database
```

## Чому SQLAlchemy ORM

SQLAlchemy дозволяє працювати з даними як з **об’єктами Python (ORM)**, а не писати SQL‑запити в контролерах. Це зменшує зв’язність коду та спрощує підтримку.
