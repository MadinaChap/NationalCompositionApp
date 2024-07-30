import sys
import pandas as pd
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QComboBox, QPushButton, QAbstractItemView
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt6.QtCore import QAbstractTableModel, QVariant, QModelIndex
from PyQt6.uic import loadUi

class PandasModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent=QModelIndex()):
        return len(self._data.index)

    def columnCount(self, parent=QModelIndex()):
        return len(self._data.columns)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            return str(self._data.iloc[index.row(), index.column()])
        return QVariant()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)  # Добавьте эту строку
        loadUi("grafiks/krug.ui", self)

        self.df = pd.read_excel("python.xlsx")

        self.items1 = sorted(self.df["географическое положение"].astype(str).unique().tolist())
        self.comboBox.addItems(self.items1)

        self.pushButton.clicked.connect(self.create_report)
        self.pushButton.clicked.connect(self.create_report_1)

        self.comboBox.currentIndexChanged.connect(self.update_items2)  

        self.kol = None
        self.update_items2() 

        self.model = PandasModel(pd.DataFrame(columns=['национальности', 'численность']))  # Создаем модель для отчета
        self.tableView.setModel(self.model)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)

        self.toolbar = NavigationToolbar(self.canvas, self)  
        layout.addWidget(self.toolbar)

        self.graphicsView.setLayout(layout)

    def update_items2(self):
        geografic_position = self.comboBox.currentText()
        df = pd.read_excel("python.xlsx")
        filtered_df = df[df["географическое положение"] == geografic_position]
        self.items2 = sorted(filtered_df["год"].unique().astype(str).tolist())  
        self.comboBox_2.clear()
        self.comboBox_2.addItems(self.items2)

        self.model = PandasModel(pd.DataFrame(columns=['национальности', 'численность', ]))  
        self.tableView.setModel(self.model)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.figure.clear()  # Очищаем старый график
        self.canvas.draw()

    def create_report(self):
        # Функция для создания отчета, вызывает функцию grafic4 для построения круговой диаграммы
        print("Функция create_report вызвана")
        geografic_position = self.comboBox.currentText()
        year = int(self.comboBox_2.currentText())  # Преобразуем год из строки в число
        self.grafic4(geografic_position, year)

    def grafic4(self, geografic_position, year):
        """
        Функция для построения круговой диаграммы на основе отфильтрованных данных
        :param geografic_position: выбранное географическое положение
        :param year: выбранный год
        """
        data = self.df
        # Фильтрация данных по географическому положению и году
        filtered_data = data[(data["географическое положение"] == geografic_position) & (data["год"] == year)]
        
        colors = plt.cm.tab20b.colors
        self.figure.clear() 
        ax = self.figure.add_subplot(111)
        # Построение круговой диаграммы
        wedges, texts = ax.pie(filtered_data["доля населения"], colors=colors, startangle=140)
        
        ax.axis('equal') 
        ax.set_title(f"Круговая диаграмма национальностей по численности за {year} год")
        # Добавление легенды к диаграмме
        ax.legend(wedges, filtered_data["национальности"], title="Национальности", loc="upper right", bbox_to_anchor=(1.05, 1))
        
        self.canvas.draw()

    ##### Отчет
    def create_report_1(self):
        # Функция для создания отчета 1, отображает данные в виде табличного представления
        # Использует выбранное географическое положение и год для формирования отчета
        geografic_position = self.comboBox.currentText()
        year = int(self.comboBox_2.currentText())
        filtered_data = self.df[(self.df["географическое положение"] == geografic_position) & (self.df["год"] == year)]
        report_df = filtered_data[["национальности", "доля населения"]].copy()
        report_df["доля населения"] = report_df["доля населения"].apply(lambda x: "{:.2%}".format((x/100)*100))
        report_df.rename(columns={"доля населения": "численность"}, inplace=True)
        self.model = PandasModel(report_df)
        self.tableView.setModel(self.model)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())