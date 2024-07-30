import pandas as pd

def pivot_population_data(df: pd.DataFrame, index_col: str, columns_col: str, values_col: str) -> pd.DataFrame:
    """
    Создает сводную таблицу населения на основе указанных столбцов.

    Аргументы:
        df (pd.DataFrame): Входной DataFrame.
        index_col (str): Название столбца для индекса сводной таблицы.
        columns_col (str): Название столбца для столбцов сводной таблицы.
        values_col (str): Название столбца для значений сводной таблицы.

    Возвращает:
        pd.DataFrame: Результирующая сводная таблица.

    Пример:
        pivot_population_data(df, 'субъекты', 'период', 'население')
    """
    pivot_table = pd.pivot_table(df, values=values_col, index=index_col, columns=columns_col)
    return pivot_table

# Пример использования
df = pd.read_excel('python.xlsx', sheet_name=1)
df['население'] = pd.to_numeric(df['население'], errors='coerce').fillna(0).astype(int)
df['период'] = pd.to_numeric(df['период'], errors='coerce').fillna(0).astype(int)

print('Сводная таблица населения:')
print(pivot_population_data(df, 'субъекты', 'период', 'население'))
