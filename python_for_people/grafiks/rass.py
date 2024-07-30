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
        loadUi("grafiks/rass.ui", self)

        self.df = pd.read_excel("python.xlsx")

        self.items1 = sorted(self.df["географическое положение"].astype(str).unique().tolist())
        self.comboBox.addItems(self.items1)

        self.pushButton.clicked.connect(self.create_report)
        self.pushButton_2.clicked.connect(self.remove_nationality)
        self.pushButton_3.clicked.connect(self.remove_nationality_2)

        self.model = PandasModel(pd.DataFrame(columns=['национальности', 'численность']))  
        self.tableView.setModel(self.model)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)

        self.toolbar = NavigationToolbar(self.canvas, self)  
        layout.addWidget(self.toolbar)

        self.graphicsView.setLayout(layout)

    def remove_nationality(self):
        selected_rows = self.tableView.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            nationality = self.model._data.iloc[row]['национальности']
            self.model._data = self.model._data[self.model._data['национальности'] != nationality]
            self.model.layoutChanged.emit()
            self.update_plot()

    def remove_nationality_2(self):
        selected_rows = self.tableView.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            nationality = self.model._data.iloc[row]['национальности']
            self.model._data = self.model._data[self.model._data['национальности'] != nationality]
            self.model.layoutChanged.emit()
            self.update_plot_2()

    def update_plot_2(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        selected_nationalities = [index.data() for index in self.tableView.selectionModel().selectedRows(column=0)]
        if selected_nationalities:
            data = self.df[(self.df['географическое положение'] == self.comboBox.currentText()) & (self.df['национальности'].isin(selected_nationalities))]
            data = data.sort_values(by='доля населения')
            scatter = ax.scatter(data['доля населения'].apply(lambda x: "{:.2%}".format((x/1000))), data['национальности'], c=data['год']) 
            ax.set_xlabel('Доля населения')
            ax.set_ylabel('Национальность')
            ax.set_title('Категоризированная диаграмма рассеивания')
            ax.xaxis.set_tick_params(rotation=90)
            ax.grid(True)
            legend = ax.legend(*scatter.legend_elements(), title="Годы")
            ax.add_artist(legend)
            self.canvas.draw()
        else:
            ax.axis('off')
            ax.text(0.5, 0.5, "Выберите национальность в таблице", horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
            self.canvas.draw()

    def update_plot(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        sorted_data = self.model._data.sort_values(by='национальности')
        data = self.df[(self.df['географическое положение'] == self.comboBox.currentText()) & (self.df['национальности'].isin(sorted_data['национальности']))]
        data = data.sort_values(by='доля населения')
        scatter = ax.scatter(data['доля населения'].apply(lambda x: "{:.2%}".format((x/1000))), data['национальности'], c=data['год'])  
        ax.set_xlabel('Доля населения')
        ax.set_ylabel('Национальность')
        ax.set_title('Категоризированная диаграмма рассеивания')
        ax.xaxis.set_tick_params(rotation=90)
        ax.grid(True)
        legend = ax.legend(*scatter.legend_elements(), title="Годы")
        ax.add_artist(legend)
        self.canvas.draw()

    def create_report(self):
        # Получение выбранного географического положения из комбо-бокса
        geografic_position = self.comboBox.currentText()
        
        # Фильтрация данных по выбранному географическому положению
        data = self.df[self.df['географическое положение'] == geografic_position]
        
        # Группировка данных по национальности, доле населения и году, и подсчет суммы
        report_df = data.groupby(['национальности', 'доля населения', 'год']).sum().reset_index()
        
        # Преобразование столбца 'доля населения' в процентный формат
        report_df["доля населения"] = report_df["доля населения"].apply(lambda x: "{:.2%}".format((x/1000)))
        
        # Сортировка данных по национальности
        report_df = report_df.sort_values(by='национальности') 

        # Отображение данных с наибольшей долей населения
        report_df = report_df.sort_values(by='доля населения') 
        
        # Обновление модели данных для отображения в таблице
        self.model._data = report_df
        self.model.layoutChanged.emit()

        # Очистка текущего графика и добавление нового графика
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Построение диаграммы рассеивания
        scatter = ax.scatter(report_df['доля населения'], report_df['национальности'], c=report_df['год'])
        ax.set_xlabel('Доля населения')
        ax.set_ylabel('Национальность')
        ax.set_title('Категоризированная диаграмма рассеивания')
        ax.xaxis.set_tick_params(rotation=90)
        ax.grid(True)

        # Добавление легенды к графику
        legend = ax.legend(*scatter.legend_elements(), title="Годы")
        ax.add_artist(legend)

        # Скрытие лишних столбцов в таблице
        self.tableView.setColumnHidden(3, True)  
        self.tableView.setColumnHidden(4, True)
        self.tableView.setColumnHidden(5, True)
        self.tableView.setColumnHidden(6, True)
        self.tableView.setColumnHidden(7, True)
        
        # Обновление отображения графика
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())