"""Обчислення кількості секунд у кожному місяці заданого року."""

import calendar


MONTH_NAMES = (
    "Січень", "Лютий", "Березень", "Квітень", "Травень", "Червень",
    "Липень", "Серпень", "Вересень", "Жовтень", "Листопад", "Грудень",
)


def seconds_in_month(month: int, year: int) -> int:
    """Повертає кількість секунд у вказаному місяці року."""
    days = calendar.monthrange(year, month)[1]
    return days * 24 * 60 * 60


def main() -> None:
    while True:
        value = input("Введіть рік: ").strip()
        try:
            year = int(value)
            if year < 1:
                raise ValueError
            break
        except ValueError:
            print("Помилка: введіть цілий додатний номер року.")

    print(f"Кількість секунд у місяцях {year} року:")
    for month in range(1, 13):
        name = MONTH_NAMES[month - 1]
        print(f"{month:02d}. {name}: {seconds_in_month(month, year):,} с".replace(",", " "))


if __name__ == "__main__":
    main()
