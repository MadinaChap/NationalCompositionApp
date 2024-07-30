import pandas as pd
#используем библиотеки pandas и openpyxl
#их необходимо установить

# Загрузка данных из файла Excel
df = pd.read_excel('python.xlsx')

year = int(input("Введите год: "))
position = input("субъект: ")

# Отчет 2: Вывод данных для определенного географического положения и года
def geografic_and_year(df: pd.DataFrame, cndname_1: str, cndval_1: str, cndname_2: str, cndval_2: str) -> pd.DataFrame:
    """ Функция генерации отчетов о сравнении географического положения и года
    Parameters
    ----------
    df : pd.DataFrame - исходная таблица с данными об игроках
    cndname_1 : str - атрибут критерия 1
    cndval_1 : str - значение критерия 1
    cndname_2 : str - атрибут критерия 2
    cndval_2 : str - значение критерия 2
    Returns
    -------
    filtered_df : pd.DataFrame - отчет.
    """
    new_df = df[(df[cndname_1] == cndval_1) & (df[cndname_2] == int(cndval_2))][['национальности', 'год', 'географическое положение']]
    return new_df
# Пример использования функции
print('Текстовый отчет №2')
print('Функция генерации отчетов о географическом положении и численности')
print(geografic_and_year(df, 'географическое положение', position, 'год', year))