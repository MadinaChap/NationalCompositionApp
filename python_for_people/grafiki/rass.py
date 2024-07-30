import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def grafic4(geografic_position):
    data = pd.read_excel('python.xlsx')
    novosibirsk = data[data["географическое положение"] == geografic_position]

    plt.scatter(novosibirsk["доля населения"], novosibirsk["национальности"], c=novosibirsk["год"])
    plt.xlabel("Доля населения")
    plt.ylabel("Национальности")
    plt.colorbar(label="год")
    plt.xticks(rotation=75)

    plt.title("Категоризированная диаграмма рассеивания")
    plt.show()

geografic_position = input("Enter the geographic position: ")
grafic4(geografic_position)
