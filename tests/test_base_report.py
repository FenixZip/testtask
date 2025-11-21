"""conftest.py"""
import pytest

from base_report import PerformanceReport, ReportError, REPORT_REGISTRY, reading_csv_files


def test_performance_report_calculates_average(sample_rows):
    """Корректно считает среднюю эффективность"""

    report = PerformanceReport()
    headers, table_data = report.generate_report(sample_rows)
    assert headers == ["position", "average_performance"]
    result_by_position = {row[0]: row[1] for row in table_data}
    assert result_by_position["Backend Developer"] == 4.5
    assert result_by_position["Frontend Developer"] == 4.7


def test_performance_report_skips_invalid_performance():
    """Проверяем, что пропускаются строки с некорректным  значениями"""

    rows = [
        {
            "name": "Oleg Sorokin",
            "position": "Backend Developer",
            "completed_tasks": "45",
            "performance": "4.8",
            "skills": "Python, Django, PostgreSQL, Docker",
            "team": "API Team",
            "experience_years": "5",
        },

        {
            "name": "Invalid Person",
            "position": "Backend Developer",
            "completed_tasks": "10",
            "performance": "N/A",
            "skills": "None",
            "team": "API Team",
            "experience_years": "1",
        },
    ]

    report = PerformanceReport()
    headers, table_data = report.generate_report(rows)
    assert headers == ["position", "average_performance"]
    assert len(table_data) == 1
    assert table_data[0][1] == 4.8


def test_performance_report_missing_column_raises():
    """Проверяем, что при отсутствии обязательной колонки возникает исключение ReportError"""

    rows = [
        {
            "name": "Alex Ivanov",
            "position": "Backend Developer",
            "completed_tasks": "45",
            "skills": "Python, Django, PostgreSQL, Docker",
            "team": "API Team",
            "experience_years": "5",
        },
    ]

    report = PerformanceReport()
    with pytest.raises(ReportError):
        report.generate_report(rows)


def test_report_registry_contains_performance():
    """Проверяем, что отчёт 'performance' зарегистрирован в REPORT_REGISTRY"""

    assert "performance" in REPORT_REGISTRY
    assert REPORT_REGISTRY["performance"] is PerformanceReport


def test_read_csv_files_success(csv_file_path):
    """Проверяем, что reading_csv_files корректно читает строки"""

    rows = list(reading_csv_files([csv_file_path]))
    assert len(rows) == 1
    assert rows[0]["name"] == "Oleg Sorokin"
    assert rows[0]["position"] == "Backend Developer"


def test_read_csv_files_file_not_found():
    """Проверяем, что файл отсуствует и выбрасывается исключенгие"""

    missing_path = "fake_files.csv"
    with pytest.raises(ReportError):
        list(reading_csv_files([missing_path]))
