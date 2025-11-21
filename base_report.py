"""baseReport.py"""
import csv


class ReportError(Exception):
    """Logical errors when reading data and reducing reports"""


def reading_csv_files(file_paths):
    """Reading the data csv"""

    for path in file_paths:
        try:
            with open(path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                yield from reader
        except FileNotFoundError as error:
            raise ReportError(f"Файл не найден {path}") from error
        except csv.Error as error:
            raise ReportError(f"Ошибка чтения CSV-файла {path}: {error}") from error


class BaseReport: # pylint: disable=too-few-public-methods
    """Base class for all reports"""

    def generate_report(self, rows):
        """Generate report"""

        raise NotImplementedError("Метод generate_report должен быть реализован в подклассе.")


class PerformanceReport(BaseReport): # pylint: disable=too-few-public-methods
    """Average employee performance by position"""

    name = "performance"

    def generate_report(self, rows):
        """Average employee performance by position"""

        performance_sum_by_position = {}
        count_by_position = {}

        for row in rows:
            try:
                position = row["position"]
                performance_value = float(row["performance"])
            except KeyError as error:
                raise ReportError(f"Отсутствует колонка в данных: {error}") from error
            except ValueError:
                continue

            performance_sum_by_position[position] = (
                    performance_sum_by_position.get(position, 0.0) + performance_value
            )
            count_by_position[position] = count_by_position.get(position, 0) + 1

        table_data = []

        for position, total_performance in performance_sum_by_position.items():
            count = count_by_position[position]
            if count > 0:
                average_performance = total_performance / count
            else:
                average_performance = 0.0
            average_performance = round(average_performance, 2)
            table_data.append([position, average_performance])
        table_data.sort(key=lambda r: r[1], reverse=True)

        headers = ["position", "average_performance"]

        return headers, table_data


REPORT_REGISTRY = {
    PerformanceReport.name: PerformanceReport,
}
