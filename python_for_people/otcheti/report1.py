import sys
import pandas as pd
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTableView, QTableWidgetItem, QHeaderView
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMessageBox, QTableView
from PyQt6.QtCore import QAbstractTableModel, Qt

number_to_word = {
    0: "Численность",
    1: "Национальность",
    2: "Субъект",
    3: "Год"
}

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
            if isinstance(value, int) and value in number_to_word:
                return number_to_word[value]
            else:
                return str(value)
    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                if section in number_to_word:
                    return number_to_word[section]
                else:
                    return str(self._data.columns[section])
            elif orientation == Qt.Orientation.Vertical:
                return str(section + 1)
        return None 
        


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("otcheti\otchet1.ui", self)

        df = pd.read_excel("python.xlsx")
        self.items1 = sorted([str(x) for x in df["национальности"].unique()])

        self.comboBox.addItems(self.items1)

        self.pushButton.clicked.connect(self.create_report)
        self.lineEdit.textChanged.connect(self.update_kol)

        self.kol = None

    def update_kol(self):
        text = self.lineEdit.text()
        try:
            self.kol = int(text)  
        except ValueError:
            self.kol = None 

    def create_report(self):
        # Получение выбранной национальности из комбо-бокса
        nationalities = self.comboBox.currentText()
        
        # Проверка на пустое значение выбранной национальности
        if nationalities == "nan":
            # Вывод предупреждения, если национальность не выбрана
            QMessageBox.warning(self, "Предупреждение", "Выберите национальность")
            return
        
        # Проверка на наличие корректного значения для количества
        if self.kol is None:
            # Вывод предупреждения, если количества нет или некорректное
            QMessageBox.warning(self, "Предупреждение", "Введите корректное значение для количества")
            return

        # Загрузка данных из Excel файла 'python.xlsx' в DataFrame
        df = pd.read_excel('python.xlsx')
        
        # Преобразование столбцов 'численность' и 'год' в числовой формат
        df['численность'] = pd.to_numeric(df['численность'], errors='coerce').fillna(0).astype(int)
        df['год'] = pd.to_numeric(df['год'], errors='coerce').fillna(0).astype(int)
        
        # Сортировка данных по столбцу 'численность'
        df.sort_values(by='численность', inplace=True)
        
        # Вызов функции self.chisl для создания отчета по выбранной национальности и количеству
        report_df = self.chisl(df, 'национальности', nationalities, 'численность', self.kol)

        # Создание модели данных PandasModel на основе отчета report_df
        model = PandasModel(report_df)
        
        # Установка созданной модели данных в таблицу для отображения
        self.tableView.setModel(model)

    def chisl(self, df: pd.DataFrame, cndname: str, cndval: str, intname: str, intval: int) -> pd.DataFrame:
        """
        Функция фильтрует данные DataFrame по заданным условиям и возвращает новый DataFrame.

        Параметры:
        - df: pd.DataFrame - исходный DataFrame с данными
        - cndname: str - название столбца для условия фильтрации
        - cndval: str - значение условия фильтрации
        - intname: str - название столбца для сравнения с числовым значением
        - intval: int - числовое значение для фильтрации

        Возвращает:
        - new_df: pd.DataFrame - новый DataFrame после фильтрации
        """
        
        # Фильтрация данных по заданным условиям
        new_df = df[(df[cndname] == cndval) & (df[intname] < intval)][['численность', 'национальности', 'географическое положение', 'год']]
        
        # Возврат нового DataFrame после фильтрации
        return new_df

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())