import pandas as pd
import matplotlib.pyplot as plt

def create_linear_plot(oblasts):

    data = pd.read_excel('python.xlsx')
    df = pd.DataFrame(data)

    plt.figure()

    for oblast in oblasts:
        df_oblast = df[df['субъекты'] == oblast]
        df_oblast['население'] = pd.to_numeric(df_oblast['население'], errors= 'coerce')
        plt.plot(df_oblast['период'], df_oblast['население'], label = oblast)

    plt.xlabel('Год')
    plt.ylabel('Количество населения')
    plt.title('Сравнение двух областей по количеству населения')
    
    plt.ticklabel_format(style='plain')  
    plt.legend()
    plt.show()


kol = int(input('Введите количесвто областей, которые вы хотите сравнить: '))
oblasts = []
for i in range(kol):
    oblast = input(f"Введите область {i + 1}: ")
    oblasts.append(oblast)

create_linear_plot(oblasts)


from PyQt6.uic import loadUi
