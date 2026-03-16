"""
Простий тест для перевірки репозиторію пацієнтів.
Запускати з каталогу dental_clinic:
    python3 test_repository.py
"""
from data_access.database import get_session
from data_access.repositories import PatientRepository


def main() -> None:
    session = get_session()
    repo = PatientRepository(session)
    patients = repo.get_all()
    print("Patients:", len(patients))
    session.close()


if __name__ == "__main__":
    main()