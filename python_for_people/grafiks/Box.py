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

# Класс для модели данных Pandas
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

# Главное окно приложения
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("grafiks/Box.ui", self)  # Загрузка пользовательского интерфейса

        self.df = pd.read_excel("python.xlsx")  # Загрузка данных из Excel файла

        # Добавление уникальных значений географического положения в комбо-бокс
        self.items1 = sorted(self.df["географическое положение"].astype(str).unique().tolist())
        self.comboBox.addItems(self.items1)

        # Подключение кнопок к соответствующим методам
        self.pushButton.clicked.connect(self.create_report)
        self.pushButton_2.clicked.connect(self.remove_nationality)
        self.pushButton_3.clicked.connect(self.remove_nationality_2)

        # Создание модели данных для отчета и привязка к таблице
        self.model = PandasModel(pd.DataFrame(columns=['национальности', 'численность']))
        self.tableView.setModel(self.model)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        # Создание графического окна и добавление элементов
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.toolbar)
        self.graphicsView.setLayout(layout)

    # Метод для удаления строки с выбранной национальностью из таблицы и обновления графика
    def remove_nationality(self):
        selected_rows = self.tableView.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            nationality = self.model._data.iloc[row]['национальности']
            self.model._data = self.model._data[self.model._data['национальности'] != nationality]
            self.model.layoutChanged.emit()
            self.update_plot()

    # Метод для выбора строк для построения графика
    def remove_nationality_2(self):
        selected_rows = self.tableView.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            nationality = self.model._data.iloc[row]['национальности']
            self.model._data = self.model._data[self.model._data['национальности'] != nationality]
            self.model.layoutChanged.emit()
            self.update_plot_2()

    def update_plot_2(self):
        # Очистка фигуры перед построением нового графика
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Получение выбранных национальностей из таблицы
        selected_nationalities = [index.data() for index in self.tableView.selectionModel().selectedRows(column=0)]
        
        if selected_nationalities:
            # Построение Box-and-Whiskers графика для выбранных национальностей
            ax.boxplot([self.df[(self.df['географическое положение'] == self.comboBox.currentText()) & (self.df['национальности'] == nationality)]['численность'] for nationality in selected_nationalities], patch_artist=True, widths=0.7)
            ax.set_xlabel('Национальность')
            ax.set_ylabel('Численность')
            ax.set_title(f'Box-and-Whiskers график для города {self.comboBox.currentText()}')
            ax.set_xticks(range(1, len(selected_nationalities) + 1))
            ax.set_xticklabels(selected_nationalities, rotation=90)
            ax.grid(True)
            self.canvas.draw()
        else:
            # В случае отсутствия выбранных национальностей выводим сообщение
            ax.axis('off')
            ax.text(0.5, 0.5, "Выберите национальность в таблице", horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
            self.canvas.draw()

    def update_plot(self):
        # Очистка фигуры перед построением нового графика
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # Сортировка данных по национальностям
        sorted_data = self.model._data.sort_values(by='национальности')

        # Построение Box-and-Whiskers графика для всех национальностей
        ax.boxplot([self.df[(self.df['географическое положение'] == self.comboBox.currentText()) & (self.df['национальности'] == nationality)]['численность'] for nationality in sorted_data['национальности']], patch_artist=True, widths=0.7)
        ax.set_xlabel('Национальность')
        ax.set_ylabel('Численность')
        ax.set_title(f'Box-and-Whiskers график для города {self.comboBox.currentText()}')
        ax.set_xticks(range(1, len(sorted_data) + 1))
        ax.set_xticklabels(sorted_data['национальности'], rotation=90)
        ax.grid(True)
        self.canvas.draw()

    def create_report(self):
        # Получаем текущее географическое положение из выпадающего списка
        geografic_position = self.comboBox.currentText()
        
        # Фильтруем данные по выбранному географическому положению
        data = self.df[self.df['географическое положение'] == geografic_position]
        
        # Группируем данные по национальностям и суммируем численность
        report_df = data.groupby('национальности')['численность'].sum().reset_index()
        
        # Сортируем данные по национальностям
        report_df = report_df.sort_values(by='национальности')
        
        # Обновляем данные в модели для отображения в таблице
        self.model._data = report_df
        self.model.layoutChanged.emit()

        # Очищаем фигуру перед построением нового графика
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Строим Box-and-Whiskers график для данных по национальностям
        ax.boxplot([data[data['национальности'] == nationality]['численность'] for nationality in report_df['национальности']], patch_artist=True, widths=0.7)
        ax.set_xlabel('Национальность')
        ax.set_ylabel('Численность')
        ax.set_title(f'Box-and-Whiskers график для города {geografic_position}.')
        ax.set_xticks(range(1, len(report_df) + 1))
        ax.set_xticklabels(report_df['национальности'], rotation=90)
        ax.grid(True)
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())