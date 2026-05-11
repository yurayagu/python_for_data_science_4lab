import time
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

# Рядок підключення відповідає змінним середовища з docker-compose
DB_URL = "mysql+mysqlconnector://myuser:mypassword@localhost:3306/my_database"


def fetch_titanic_data():
    engine = create_engine(DB_URL)
    max_retries = 10
    retry_delay = 10  # секунд

    for attempt in range(1, max_retries + 1):
        try:
            print(f"Спроба підключення до БД {attempt}/{max_retries}...")
            # Якщо підключення успішне, виконуємо запит
            df = pd.read_sql("SELECT * FROM titanic", con=engine)
            print("Підключення успішне! Дані завантажено.\n")
            return df

        except OperationalError as e:
            print(f"База ще не готова. Очікування {retry_delay} секунд...")
            if attempt == max_retries:
                print("Помилка: Не вдалося підключитися до бази даних після 10 спроб.")
                raise e
            time.sleep(retry_delay)


if __name__ == "__main__":
    df = fetch_titanic_data()

    # Виводимо результат
    pd.set_option('display.max_columns', None)  # Щоб консоль не обрізала колонки
    print(df.head())  # Друкуємо перші 5 рядків
    print(f"\nОчікуваний результат: {df.shape[0]} рядків і {df.shape[1]} колонок.")