import pandas as pd

pd.set_option('display.max_rows', None)

df = pd.read_excel('python.xlsx')

def analyze_population(df: pd.DataFrame, region: str) -> pd.DataFrame:
    """ Функция для анализа численности населения по географическому положению.
    
    Parameters
    ----------
    df : pd.DataFrame - исходная таблица с данными о численности населения
    region : str - географическое положение для анализа
    
    Returns
    -------
    analyzed_df : pd.DataFrame - отчет с анализом численности населения по географическому положению.
    """
    region_df = df[df['географическое положение'] == region]
    
    if region_df.empty:
        print(f"No data available for the region '{region}'.")
        return pd.DataFrame()  # Return an empty DataFrame
    
    years = region_df['год'].unique()
    common_nationalities = set(region_df[region_df['год'] == years[0]]['национальности'])
    for year in years[1:]:
        common_nationalities = common_nationalities.intersection(set(region_df[region_df['год'] == year]['национальности']))
    
    common_nationalities_df = region_df[region_df['национальности'].isin(common_nationalities)]
    common_nationalities_df['среднее значение'] = common_nationalities_df.groupby('национальности')['численность'].transform('mean')
    common_nationalities_df = common_nationalities_df[['национальности', 'среднее значение']]
    common_nationalities_df = common_nationalities_df.drop_duplicates(subset='национальности')
    return common_nationalities_df

# Пример использования функции
print('Текстовый отчет №4')
nat = input()
result_df = analyze_population(df, nat)
print(result_df)
