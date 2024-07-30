import sys
import pandas as pd
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.uic import loadUi


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=7.6, height=5.8, dpi=100):
        # Создание фигуры и осей для графика
        fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        super(MplCanvas, self).__init__(fig)
        self.setParent(parent)

    def plot_data(self, oblasts, sheet_name="Лист1"):
        # Очистка текущего графика
        self.ax.clear()
        # Загрузка данных из Excel файла
        data = pd.read_excel('python.xlsx', sheet_name=sheet_name)
        df = pd.DataFrame(data)

        # Построение графиков для выбранных регионов
        for oblast in oblasts:
            # Фильтрация данных по выбранному региону
            df_oblast = df[df['субъекты'] == oblast]
            # Преобразование столбца 'население' в числовой формат
            df_oblast['население'] = pd.to_numeric(df_oblast['население'], errors='coerce')
            # Удаление строк с отсутствующими значениями в столбце 'население'
            df_oblast = df_oblast.dropna(subset=['население'])
            # Построение графика населения по годам для выбранного региона
            self.ax.plot(df_oblast['период'], df_oblast['население'], label=oblast)

        # Настройка подписей осей и заголовка графика
        self.ax.set_xlabel('Год')
        self.ax.set_ylabel('Количество населения')
        self.ax.set_title('Сравнение регионов по населению')
        # Форматирование значений осей
        self.ax.ticklabel_format(style='plain')
        # Добавление легенды к графику
        self.ax.legend()
        # Обновление отображения графика
        self.figure.canvas.draw()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Загрузка интерфейса из файла .ui
        loadUi("grafiks/new.ui", self)

        # Загрузка данных из Excel файла и создание списка уникальных значений для комбо-боксов
        df = pd.read_excel("python.xlsx", sheet_name="Лист1")
        self.items1 = sorted(df["субъекты"].astype(str).unique().tolist())

        # Добавление уникальных значений в комбо-боксы для выбора
        self.comboBox_2.addItems(self.items1)
        self.comboBox_3.addItems(self.items1)
        self.comboBox_4.addItems(self.items1)
        self.comboBox_5.addItems(self.items1)
        self.comboBox_6.addItems(self.items1)
        self.comboBox_7.addItems(self.items1)
        self.comboBox_14.addItems(self.items1)
        self.comboBox_15.addItems(self.items1)
        self.comboBox_16.addItems(self.items1)
        self.comboBox_17.addItems(self.items1)

        # Подключение кнопки к функции создания графика
        self.pushButton.clicked.connect(self.create_plot)
        # Создание экземпляра класса MplCanvas для отображения графиков
        self.canvas = MplCanvas(self.graphicsView)
    
    def create_plot(self):
        # Получение выбранных значений из комбо-боксов
        oblasts = [
            self.comboBox_2.currentText(),
            self.comboBox_3.currentText(),
            self.comboBox_4.currentText(),
            self.comboBox_5.currentText(),
            self.comboBox_6.currentText(),
            self.comboBox_7.currentText(),
            self.comboBox_14.currentText(),
            self.comboBox_15.currentText(),
            self.comboBox_16.currentText(),
            self.comboBox_17.currentText(),
        ]
        # Фильтрация значений, исключение 'nan'
        oblasts = [oblast for oblast in oblasts if oblast != 'nan']
        
        # Передача отфильтрованных данных для построения графика
        self.canvas.plot_data(oblasts)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())