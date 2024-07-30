import sys
import pandas as pd
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableView, QHeaderView
from PyQt6.uic import loadUi
from PyQt6.QtCore import QAbstractTableModel, Qt, QVariant

from PyQt6.QtGui import QColor

class PandasModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent):
        return self._data.shape[0]

    def columnCount(self, parent):
        return self._data.shape[1]

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            if pd.isna(value):
                return ('')
            else:
                return str(value)
        elif role == Qt.ItemDataRole.BackgroundRole:
            value = self._data.iloc[index.row(), index.column()]
            if pd.isna(value):
                return QColor('red')
            else:
                return QColor('white')

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return QVariant(str(self._data.columns[section]))
            elif orientation == Qt.Orientation.Vertical:
                return QVariant(str(self._data.index[section]))


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        
        # Загрузка пользовательского интерфейса из фа
        # йла svodntable.ui
        loadUi("otcheti\svodntable.ui", self)
        
        # Чтение данных из файла Excel 'python.xlsx'
        df = pd.read_excel("python.xlsx")
        
        # Преобразование столбцов 'численность' и 'год' в числовой формат
        df['численность'] = pd.to_numeric(df['численность'], errors='coerce').fillna(0).astype(int)
        df['год'] = pd.to_numeric(df['год'], errors='coerce').fillna(0).astype(int)
        
        # Создание сводной таблицы на основе данных DataFrame
        pivot_table = pd.pivot_table(df, values='численность', index='национальности', columns='год', aggfunc='sum')
        
        # Создание модели данных PandasModel на основе сводной таблицы
        model = PandasModel(pivot_table)
        
        # Установка модели данных для отображения в tableView
        self.tableView.setModel(model)
        
        # Установка режима изменения размеров колонок таблицы по содержимому
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())