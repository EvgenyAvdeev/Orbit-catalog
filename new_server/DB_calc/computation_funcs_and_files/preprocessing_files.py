import glob
import os

import pandas as pd


def process_csv_files():
    """
    Обрабатывает CSV-файлы в указанной директории, удаляя строки с нулевым периодом

    Возвращает:
    ----------
    None
    """
    directory_path = "DB_calc/computation_funcs_and_files/computation_files"
    csv_files = glob.glob(os.path.join(directory_path, "*.csv"))
    for file_path in csv_files:
        try:
            df = pd.read_csv(file_path)
            if "t" in df.columns:
                original_count = len(df)
                df = df[df["t"] != 0]
                df.to_csv(file_path, index=False)
                print(
                    f"Обработан {os.path.basename(file_path)}: удалено {original_count - len(df)} строк"
                )
            else:
                print(f"Пропущен {os.path.basename(file_path)}: нет столбца 't'")

        except Exception as e:
            print(f"Ошибка в {file_path}: {e}")


if __name__ == "__main__":
    process_csv_files()
