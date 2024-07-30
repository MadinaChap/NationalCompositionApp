import sys
import pandas as pd
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QComboBox, QPushButton, QAbstractItemView, QMessageBox
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
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        loadUi("grafiks/Kategor.ui", self)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.toolbar)
        self.graphicsView.setLayout(layout)

        self.df = pd.read_excel("python.xlsx")

        self.items1 = sorted(self.df["географическое положение"].astype(str).unique().tolist())
        self.comboBox.addItems(self.items1)

        self.comboBox.currentIndexChanged.connect(self.update_items2)  

        self.kol = None
        self.update_items2() 

        self.pushButton.clicked.connect(self.create_report)
        self.pushButton_2.clicked.connect(self.remove_nationality)
        self.pushButton_3.clicked.connect(self.remove_nationality_2)

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
            # Получение данных для выбранных национальностей
            geografic_position = self.comboBox.currentText()
            year1 = int(self.comboBox_2.currentText())
            year2 = int(self.comboBox_3.currentText())

            df = self.df[(self.df['географическое положение'] == geografic_position) & 
                         (self.df['национальности'].isin(selected_nationalities))]

            df_year1 = df[df['год'] == year1]
            df_year2 = df[df['год'] == year2]

            df_combined = pd.DataFrame({'национальности': selected_nationalities})
            df_combined = df_combined.merge(df_year1[['национальности', 'численность']], on='национальности', how='left', suffixes=('_x', '_y'))
            df_combined = df_combined.merge(df_year2[['национальности', 'численность']], on='национальности', how='left')

            df_combined = df_combined.sort_values(by='национальности')

            # Создание гистограммы
            bar_width = 0.35
            index = np.arange(len(df_combined['национальности']))

            ax.bar(index, df_combined['численность_x'].fillna(0), bar_width, color='blue', label=str(year1))
            ax.bar(index + bar_width, df_combined['численность_y'].fillna(0), bar_width, color='red', label=str(year2))

            ax.set_xlabel('Национальности')
            ax.set_ylabel('Численность')
            ax.set_title(f'Численность самых крупных национальностей в {year1} и {year2} годах')
            ax.set_xticks(index + bar_width / 2)
            ax.set_xticklabels(df_combined['национальности'], rotation=90)
            ax.legend()

            self.canvas.draw()
        else:
            # В случае отсутствия выбранных национальностей выводим сообщение
            ax.axis('off')
            ax.text(0.5, 0.5, "Выберите национальность в таблице", horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
            self.canvas.draw()


    # Метод для удаления строки с выбранной национальностью из таблицы и обновления графика
    def remove_nationality(self):
        selected_rows = self.tableView.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            nationality = self.model._data.iloc[row]['национальности']
            self.model._data = self.model._data[self.model._data['национальности'] != nationality]
            self.model.layoutChanged.emit()
            self.update_plot()

    def update_plot(self):
        # Очистка фигуры перед построением нового графика
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # Сортировка данных по национальностям
        sorted_data = self.model._data.sort_values(by='национальности')

        # Создание гистограммы
        bar_width = 0.35
        index = np.arange(len(sorted_data['национальности']))

        ax.bar(index, sorted_data['численность_x'].fillna(0), bar_width, color='blue', label=self.comboBox_2.currentText())
        ax.bar(index + bar_width, sorted_data['численность_y'].fillna(0), bar_width, color='red', label=self.comboBox_3.currentText())

        ax.set_xlabel('Национальности')
        ax.set_ylabel('Численность')
        ax.set_title(f'Численность самых крупных национальностей в {self.comboBox_2.currentText()} и {self.comboBox_3.currentText()} годах')
        ax.set_xticks(index + bar_width / 2)
        ax.set_xticklabels(sorted_data['национальности'], rotation=90)
        ax.legend()

        self.canvas.draw()
    

    def update_items2(self):
        geografic_position = self.comboBox.currentText()
        df = pd.read_excel("python.xlsx")
        filtered_df = df[df["географическое положение"] == geografic_position]
        self.items2 = sorted(filtered_df["год"].unique().astype(str).tolist())  
        self.comboBox_2.clear()
        self.comboBox_2.addItems(self.items2)
        self.comboBox_3.clear()
        self.comboBox_3.addItems(self.items2)

        self.model = PandasModel(pd.DataFrame(columns=['национальности', 'численность', ]))  
        self.tableView.setModel(self.model)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)


    def create_report(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        geografic_position = self.comboBox.currentText()
        year1_text = self.comboBox_2.currentText()
        year2_text = self.comboBox_3.currentText()
        
        if year1_text and year2_text:
            year1 = int(year1_text)
            year2 = int(year2_text)
            
            data = pd.read_excel('python.xlsx')
            df = pd.DataFrame(data)
            df = df[df['географическое положение'] == geografic_position]
            df_year1 = df[(df['год'] == year1)]
            df_year2 = df[(df['год'] == year2)]
            
            nationalities = set(df_year1['национальности']).union(set(df_year2['национальности']))
            
            df_combined = pd.DataFrame({'национальности': list(nationalities)})
            df_combined = df_combined.merge(df_year1[['национальности', 'численность']], on='национальности', how='left', suffixes=('_x', '_y'))
            df_combined = df_combined.merge(df_year2[['национальности', 'численность']], on='национальности', how='left')
            
            df_combined = df_combined.sort_values(by='национальности')
            
            self.model = PandasModel(df_combined[['национальности', 'численность_x', 'численность_y']])
            self.tableView.setModel(self.model)
            
            bar_width = 0.35
            index = np.arange(len(df_combined['национальности']))
            
            ax.bar(index, df_combined['численность_x'].fillna(0), bar_width, color='blue', label=str(year1))
            ax.bar(index + bar_width, df_combined['численность_y'].fillna(0), bar_width, color='red', label=str(year2))
            
            ax.set_xlabel('Национальности')
            ax.set_ylabel('Численность')
            ax.set_title(f'Численность самых крупных национальностей в {year1} и {year2} годах')
            ax.set_xticks(index + bar_width / 2)
            ax.set_xticklabels(df_combined['национальности'], rotation=90)
            ax.legend()
            
            self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
