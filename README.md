# SoftwareDesignPatternsLabs lab3
Dental Clinic — 3 рівні архітектура
<img width="1680" height="1050" alt="Знімок екрана 2026-04-07 о 15 45 06" src="https://github.com/user-attachments/assets/1629b0a5-7254-4ef4-a925-dcdb976f941f" />
<img width="1680" height="1050" alt="Знімок екрана 2026-04-07 о 15 45 18" src="https://github.com/user-attachments/assets/1a93a963-8f9b-4264-8e4f-b0755d713ea0" />
<img width="1680" height="1050" alt="Знімок екрана 2026-04-07 о 15 45 32" src="https://github.com/user-attachments/assets/10168c29-2295-4f80-9a58-d9c1716f4fd5" />

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
Запуск

cd dental_clinic
pip install -r requirements.txt

python main.py              # імпорт CSV
uvicorn main:app --reload   # API + Swagger: http://127.0.0.1:8000/docs
Потік даних

Запит → Presentation (controllers/api) → Business (services) → Data Access (repositories) → БД

first step - python3 scripts/generate_csv.py - generate data

sec step - python3 main.py - create db

test orm logic - python3 main.py - echo true

Swagger / API endpoints │ ▼ Presentation Layer (controllers / routes) │ ▼ Business Logic Layer (services) │ ▼ Data Access Layer (repositories + ORM) │ ▼ Database

сенс розділення проєкту на рівні це про зручне читання і подальше маштабування, презентешн це про експіріенс з юзером, бізнес де загальна логіка проєкту, дата леєр це про використання базиданих

sqlalchemy це про викориснна зрозумілих логічних запитів в проєкті замістт іспорт селект і тд
