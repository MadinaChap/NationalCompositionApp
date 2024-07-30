import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def grafic4(geografic_position, year):
    data = pd.read_excel('python.xlsx')
    novosibirsk = data[(data["географическое положение"] == geografic_position) & (data["год"] == year)]
    colors = plt.cm.tab20.colors
    plt.figure(figsize=(8, 8))
    wedges, texts = plt.pie(novosibirsk["доля населения"], colors=colors, startangle=140)
    plt.axis('equal') 
    plt.title(f"Круговая диаграмма национальностей по численности за {year} год")
    plt.legend(wedges, novosibirsk["национальности"], title="Национальности", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    
    plt.show()

geografic_position = input("Enter the geographic position: ")
year1 = int(input("Enter the first year: "))
grafic4(geografic_position,year1)
