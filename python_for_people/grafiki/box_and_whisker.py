import pandas as pd
import matplotlib.pyplot as plt
import numpy as np




def grafic3(geografic_position):

    data = pd.read_excel('python.xlsx')
    data_novosibirsk = data[data['географическое положение'] == geografic_position]

    plt.figure(figsize=(10,6))
    plt.boxplot([data_novosibirsk[data_novosibirsk['национальности'] == nationality]['численность'] for nationality in data_novosibirsk['национальности'].unique()], patch_artist=True, widths=0.7)
    plt.xlabel('Национальность')
    plt.ylabel('Численность')
    plt.title('Box-and-Whiskers график для города {geografic_position}')
    plt.xticks(range(1, len(data_novosibirsk['национальности'].unique())+1), data_novosibirsk['национальности'].unique(), rotation=45)
    plt.grid(True)
    plt.show()

geografic_position = input("Enter the geographic position: ")
grafic3(geografic_position)

