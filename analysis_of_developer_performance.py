"""analysis_of_developer_performance.py"""
import argparse
from tabulate import tabulate

from base_report import REPORT_REGISTRY, ReportError, reading_csv_files


def build_arg_parser():
    """Returns command line arguments"""

    parser = argparse.ArgumentParser(
        description="Анализ  отчета"
    )

    parser.add_argument(
        "--files",
        nargs="+",
        type=str,
        required=True,
    )

    parser.add_argument(
        "--report",
        type=str,
        default="performance",
    )

    return parser


def get_report(report_name):
    """Returns the report"""

    report_class = REPORT_REGISTRY.get(report_name)
    if report_class is None:
        raise ReportError(f"Неизвестный тип отчёта: {report_name}")
    return report_class()


def main(argv=None):
    """Точка входа в рпиложение"""

    parser = build_arg_parser()
    args = parser.parse_args(argv)
    try:
        report = get_report(args.report)
        rows = list(reading_csv_files(args.files))
        headers, table_data = report.generate_report(rows)
        table_str = tabulate(table_data, headers=headers, tablefmt="github")
        print(table_str)
        return 0
    except ReportError as error:
        print(f"Ошибка при формировании отчёта: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
