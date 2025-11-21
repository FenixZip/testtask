"""conftest.py"""
import pytest


@pytest.fixture
def sample_rows():
    """Возвращаем список словарей, имитирующих строки CSV-файла"""

    return [
        # Первая строка для позиции Backend Developer
        {
            "name": "Alex Ivanov",
            "position": "Backend Developer",
            "completed_tasks": "45",
            "performance": "4.8",
            "skills": "Python, Django, PostgreSQL, Docker",
            "team": "API Team",
            "experience_years": "5",
        },

        {
            "name": "John Smith",
            "position": "Backend Developer",
            "completed_tasks": "30",
            "performance": "4.2",
            "skills": "Python, FastAPI",
            "team": "API Team",
            "experience_years": "3",
        },

        {
            "name": "Maria Petrova",
            "position": "Frontend Developer",
            "completed_tasks": "38",
            "performance": "4.7",
            "skills": "React, TypeScript, Redux, CSS",
            "team": "Web Team",
            "experience_years": "4",
        },
    ]


@pytest.fixture
def csv_file_path(tmp_path):
    """Создаёт временный CSV-файл с одной строкой данных и
    возвращает путь к этому файлу
    """

    csv_content = (
        "name,position,completed_tasks,performance,skills,team,experience_years\n"
        "Oleg Sorokin,Backend Developer,45,4.8,"
        "\"Python, Django, PostgreSQL, Docker\",API Team,5\n"
    )

    path = tmp_path / "data.csv"
    path.write_text(csv_content, encoding="utf-8")
    return path
