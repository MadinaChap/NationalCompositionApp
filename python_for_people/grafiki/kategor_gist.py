import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def grafic1(geografic_position, year1, year2):
    data = pd.read_excel('python.xlsx')
    df = pd.DataFrame(data)
    df = df[df['географическое положение'] == geografic_position]
    df = df[(df['национальности'] != 'Русские')]
    df_year1 = df[df['год'] == year1]
    df_year2 = df[df['год'] == year2]

    # Объединяем данные по национальностям
    nationalities = set(df_year1['национальности']).union(set(df_year2['национальности']))

    df_combined = pd.DataFrame({'национальности': list(nationalities)})
    df_combined = df_combined.merge(df_year1, on='национальности', how='left')
    df_combined = df_combined.merge(df_year2, on='национальности', how='left')

    bar_width = 0.35
    index = np.arange(len(df_combined['национальности']))
    plt.figure(figsize=(12, 6))
    
    plt.bar(index, df_combined['численность_x'].fillna(0), bar_width, color='blue', label=str(year1))
    plt.bar(index + bar_width, df_combined['численность_y'].fillna(0), bar_width, color='red', label=str(year2))
    
    plt.xlabel('Национальности')
    plt.ylabel('Численность')
    plt.title(f'Численность самых крупных национальностей в {year1} и {year2} годах')
    plt.xticks(index + bar_width / 2, df_combined['национальности'], rotation=45)
    plt.legend()
    plt.show()

geografic_position = input("Enter the geographic position: ")
year1 = int(input("Enter the first year: "))
year2 = int(input("Enter the second year: "))
grafic1(geografic_position, year1, year2)
