import pandas as pd
pd.set_option('display.max_rows', None)
df = pd.read_excel('python.xlsx')

min_population = int(input())
max_population = int(input())

def report4(df: pd.DataFrame, cndname_1: str, intname: int, cndname_2: str, cndval_2: int) -> pd.DataFrame:
    """
    Функция формирует отчет на основе данных DataFrame, фильтруя их по заданным условиям.

    Параметры:
    - df: pd.DataFrame - исходный DataFrame с данными
    - cndname_1: str - название первого столбца для фильтрации по значению больше или равно intname
    - intname: int - числовое значение для фильтрации по cndname_1
    - cndname_2: str - название второго столбца для фильтрации по значению меньше или равно cndval_2
    - cndval_2: int - числовое значение для фильтрации по cndname_2

    Возвращает:
     - new_df: pd.DataFrame - новый DataFrame после применения фильтрации
    """
    new_df = df[(df[cndname_1] >= intname) & (df[cndname_2] <= int(cndval_2))][['численность', 'национальности', 'географическое положение', 'год']]
    return new_df

print('Текстовый отчет №4')
print('Функция генерации отчетов национальном составе по численности')
print(report4(df, 'численность', min_population, 'численность', max_population))
