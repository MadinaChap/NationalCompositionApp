import pandas as pd

pd.set_option('display.max_rows',None)

df = pd.read_excel('python.xlsx')
kol = int(input("Введите значение: "))
nationalities = input("Введите национаьность: ")
# Отчет 1: Вывод данных для определенной национальности

def chisl(df: pd.DataFrame, cndname: str, cndval: str, intname: str, intval: int) -> pd.DataFrame:
    """ Функция генерации отчетов о численности для одного строкового
    и одного целочисленного (макс.) критериев
    Parameters
    ----------
    df : pd.DataFrame - исходная таблица с данными об национальностях
    cndname : str - атрибут критерия
    cndval : str - значение критерия
    intname : str - атрибут критерия
    intval : int - максимальное значение критерия
    Returns
    -------
    filtered_df : pd.DataFrame - отчет.
    """
    new_df = df[(df[cndname] == cndval) & (df[intname].astype(int) < intval)][['численность', 'национальности', 'географическое положение', 'год']]
    return new_df


# Пример использования функции
print('Текстовый отчет №1')
print('Функция генерации отчетов о численности (>50000) для национальности')
print(chisl(df, 'национальности', nationalities, 'численность', kol))