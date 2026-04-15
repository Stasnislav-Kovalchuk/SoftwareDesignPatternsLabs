"""
Generate data/dental_data.csv with 1000+ rows.
Run from dental_clinic/: python scripts/generate_csv.py
"""
import csv
import random
from pathlib import Path
from datetime import datetime, timedelta

OUTPUT_PATH = Path(__file__).resolve().parent.parent / "data" / "dental_data.csv"
NUM_ROWS = 1050

FIRST_NAMES = [
    "Олександр", "Дмитро", "Андрій", "Максим", "Сергій", "Олег", "Іван", "Михайло",
    "Володимир", "Василь", "Ігор", "Юрій", "Петро", "Микола", "Богдан", "Роман",
    "Марія", "Олена", "Анна", "Катерина", "Наталія", "Ірина", "Тетяна", "Юлія",
    "Вікторія", "Софія", "Дарія", "Валерія", "Оксана", "Людмила", "Світлана", "Галина",
]
LAST_NAMES = [
    "Коваленко", "Бондаренко", "Шевченко", "Мельник", "Кравченко", "Козак", "Ткаченко",
    "Олійник", "Савченко", "Петренко", "Коваль", "Бойко", "Гончаренко", "Лисенко",
    "Сердюк", "Поліщук", "Руденко", "Марченко", "Клименко", "Павленко", "Захарченко",
    "Іваненко", "Тарасенко", "Семененко", "Левченко", "Гриценко", "Федоренко", "Кравчук",
]
DENTISTS = [
    ("Др. Іваненко О.В.", "Терапевт"),
    ("Др. Петренко М.І.", "Ортодонт"),
    ("Др. Коваленко С.П.", "Хірург"),
    ("Др. Шевченко Л.М.", "Педіатр"),
    ("Др. Мельник В.К.", "Імплантолог"),
    ("Др. Кравченко А.С.", "Пародонтолог"),
    ("Др. Бондаренко Т.О.", "Терапевт"),
    ("Др. Ткаченко Р.В.", "Ортопед"),
]
DIAGNOSES = [
    "Карієс", "Пульпіт", "Пародонтит", "Гінгівіт", "Стоматит", "Періодонтит",
    "Киста зуба", "Абсцес", "Знос емалі", "Гіперчутливість", "Неправильний прикус",
    "Відсутній зуб", "Ускладнення після екстракції", "Травма зуба",
]
TREATMENT_PLANS = [
    "Пломбування", "Ендодонтичне лікування", "Профілактична чистка", "Видалення зуба",
    "Імплантація", "Встановлення коронки", "Лікування ясен", "Відбілювання",
    "Ортодонтичне лікування", "Рентген та спостереження", "Медикаментозне лікування",
]
PROCEDURES = [
    ("Консультація", 200),
    ("Профілактична чистка", 800),
    ("Пломбування", 600),
    ("Ендодонтичне лікування", 1500),
    ("Видалення зуба", 500),
    ("Рентген", 150),
    ("Відбілювання", 2500),
    ("Коронка", 3500),
    ("Імплант", 12000),
    ("Лікування ясен", 400),
    ("Анестезія", 100),
]


def random_phone():
    return f"+380{random.randint(50, 99)}{random.randint(100, 999)}{random.randint(10, 99)}{random.randint(10, 99)}"


def random_email(first: str, last: str, n: int):
    base = f"{first.lower()}.{last.lower()}".replace("'", "")
    return f"{base}{n}@example.com"


def random_date():
    start = datetime(2022, 1, 1)
    end = datetime(2024, 12, 31)
    delta = (end - start).days
    d = start + timedelta(days=random.randint(0, delta))
    return d.strftime("%Y-%m-%d")


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    columns = [
        "patient_first_name", "patient_last_name", "patient_phone", "patient_email",
        "dentist_name", "appointment_date", "diagnosis", "treatment_plan",
        "procedure_name", "procedure_cost", "payment_amount",
    ]
    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for i in range(NUM_ROWS):
            first = random.choice(FIRST_NAMES)
            last = random.choice(LAST_NAMES)
            dentist_name, _ = random.choice(DENTISTS)
            diag = random.choice(DIAGNOSES)
            plan = random.choice(TREATMENT_PLANS)
            proc_name, proc_cost = random.choice(PROCEDURES)
            payment = proc_cost + random.randint(-50, 200)
            payment = max(0, payment)
            writer.writerow({
                "patient_first_name": first,
                "patient_last_name": last,
                "patient_phone": random_phone(),
                "patient_email": random_email(first, last, i),
                "dentist_name": dentist_name,
                "appointment_date": random_date(),
                "diagnosis": diag,
                "treatment_plan": plan,
                "procedure_name": proc_name,
                "procedure_cost": proc_cost,
                "payment_amount": payment,
            })
    print(f"Generated {NUM_ROWS} rows at {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
