"""test_analysis_of_developer_performance.py"""
import pytest

from analysis_of_developer_performance import build_arg_parser, get_report, main
from base_report import PerformanceReport, ReportError


def test_build_arg_parser_parses_arguments(csv_file_path):
    """Проверяем, что build_arg_parser создаёт парсер"""

    parser = build_arg_parser()
    argv = ["--files", str(csv_file_path), "--report", "performance"]
    args = parser.parse_args(argv)
    assert args.files == [str(csv_file_path)]
    assert args.report == "performance"


def test_get_report_returns_performance_report():
    """Проверяем, что get_report возвращает экземпляр PerformanceReport"""

    report = get_report("performance")
    assert isinstance(report, PerformanceReport)


def test_get_report_raises_on_unknown_report():
    """Проверяем, что get_report выбрасывает ReportError"""

    with pytest.raises(ReportError):
        get_report("unknown")


def test_main_integration_success(tmp_path):
    """Создаем временный файл csv, запускаем main"""

    csv_content = (
        "name,position,completed_tasks,performance,skills,team,experience_years\n"
        "Oleg Sorokin,Backend Developer,45,4.8,"
        "\"Python, Django, PostgreSQL, Docker\",API Team,5\n"
        "Maria Petrova,Frontend Developer,38,4.7,"
        "\"React, TypeScript, Redux, CSS\",Web Team,4\n"
    )

    csv_path = tmp_path / "data.csv"
    csv_path.write_text(csv_content, encoding="utf-8")
    argv = ["--files", str(csv_path), "--report", "performance"]
    exit_code = main(argv)
    assert exit_code == 0
