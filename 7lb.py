import csv
import time
from datetime import datetime
import re

def is_float(value):
    # Проверяет, является ли строка числом с плавающей точкой 
    try:
        # Заменяем запятую на точку и пытаемся преобразовать в float
        float(value.replace(',', '.'))
        return True
    except ValueError:
        return False


def modify_csv(input_file, output_file):

    start_time = time.time()
    total_errors = 0

    data = []
    try:
        with open(input_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                data.append(row)

    except FileNotFoundError:
        print(f"Ошибка: Файл '{input_file}' не найден.")
        return
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
        return


    for i in range(2, len(data)):
        original_row = data[i].copy()
        row_errors = 0

        for j in range(1, len(data[i])):
            value = data[i][j].strip()

            if value == '':
                data[i][j] = '0.0'
                if row_errors == 0:
                    print(f"Строка {i+1}: Пропущено значение в столбце {j+1}. Заменено на 0.0")
                row_errors += 1
                total_errors += 1


            else:
                # Шаг 1: Удаляем все символы, кроме цифр, точек и запятых
                cleaned_value = re.sub(r'[^\d\.,]', '', value)

                # Шаг 2: Заменяем запятую на точку 
                if ',' in cleaned_value:
                    cleaned_value = cleaned_value.replace(',', '.')

                # Шаг 3: Проверяем, является ли результатом числом
                if is_float(cleaned_value):
                    try:
                        data[i][j] = str(float(cleaned_value))  # Приводим к float и обратно к str 
                    except ValueError:
                        data[i][j] = '0.0'
                        print(f"Строка {i+1}: Ошибка преобразования '{value}' в число. Заменено на 0.0")
                        row_errors += 1
                        total_errors += 1

                else: # если даже после обработки результат не число, ставим 0.0
                    data[i][j] = '0.0'
                    print(f"Строка {i+1}: Некорректное значение '{value}' в столбце {j+1}. Заменено на 0.0")
                    row_errors += 1
                    total_errors += 1


        # Проверка и корректировка формата Datetime
        try:
            datetime.strptime(data[i][0], '%m/%d/%Y %H:%M')
        except ValueError:
            print(f"Строка {i+1}: Некорректный формат Datetime. Заменено на текущую дату и время.")
            data[i][0] = datetime.now().strftime('%m/%d/%Y %H:%M')
            row_errors += 1
            total_errors += 1

        if row_errors > 0:
            print(f"Строка {i+1}: Исходная - {original_row}, \n Исправленная - {data[i]}")


    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)
        print(f"Модифицированный набор данных сохранен в файл: {output_file}")

    except Exception as e:
        print(f"Произошла ошибка при записи в файл: {e}")
        return

    end_time = time.time()
    print(f"Время выполнения: {end_time - start_time:.4f} секунд")
    print(f"Общее количество ошибок: {total_errors}")


# Пример использования:
input_csv_file = r'C:\Users\mitra\OneDrive\Рабочий стол\протодьяконов\it2abs.csv'
output_csv_file = r'C:\Users\mitra\OneDrive\Рабочий стол\протодьяконов\1403Отчет2abs.csv'
modify_csv(input_csv_file, output_csv_file)