import csv


def write_to_csv_file(file_name: str, fieldnames: list[str], data: list[dict]) -> None:
    with open(file_name, mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row)
