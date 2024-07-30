import sys
import pandas as pd
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTableView, QTableWidgetItem, QHeaderView
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
        
        


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("otcheti\otcheti3.ui", self)

        df = pd.read_excel("python.xlsx")
        df['численность'] = pd.to_numeric(df['численность'], errors='coerce') 
        df = df.dropna(subset=['численность'])  
        self.items1 = sorted(df['численность'].astype(int).unique().tolist())

        self.comboBox.addItems([str(x) for x in self.items1])
        self.comboBox_2.addItems([str(x) for x in self.items1])
        self.pushButton.clicked.connect(self.create_report) 

    def create_report(self):
        try:
            # Попытка преобразовать текущий текст из выпадающего списка в целое число для минимальной и максимальной численности населения
            min_population = int(self.comboBox.currentText())
            max_population = int(self.comboBox_2.currentText())
            
            # Проверка, что минимальное значение населения не больше максимального
            if min_population > max_population:
                # Вывод предупреждения об ошибке, если условие не выполняется
                QMessageBox.warning(self, "Ошибка", "Минимальное значение не может быть больше Максимального")
                return
        except ValueError:
            # В случае исключения ValueError (некорректные данные) выводится предупреждение
            QMessageBox.warning(self, "Выберите корректные данные")
            return
        
        df = pd.read_excel('python.xlsx')
        df['численность'] = pd.to_numeric(df['численность'], errors= 'coerce').fillna(0).astype(int)
        df['год'] = pd.to_numeric(df['год'], errors= 'coerce').fillna(0).astype(int)
        
        df.sort_values(by = 'численность', inplace=True)
        
        report_df = self.report4(df, 'численность', min_population, 'численность', max_population)

        model = PandasModel(report_df)
        self.tableView.setModel(model)

    def report4(self, df: pd.DataFrame, cndname_1: str, intname: int, cndname_2: str, cndval_2: int) -> pd.DataFrame:
        """
        Функция формирует отчет на основе данных DataFrame, фильтруя их по заданным условиям.

        Параметры:
        - df: pd.DataFrame - исходный DataFrame с данными
        - cndname_1: str - название первого столбца для фильтрации по значению больше или равно intname
        - intname: int - числовое значение для фильтрации по cndname_1
        - cndname_2: str - название второго столбца для фильтрации по значению меньше или равно cndval_2
        - cndval_2: int - числовое значение для фильтрации по cndname_2

        Возвращает:
        - new_df: pd.DataFrame - новый DataFrame после применения фильтрации
        """
        
        # Фильтрация данных по заданным условиям
        new_df = df[(df[cndname_1] >= intname) & (df[cndname_2] <= int(cndval_2))][['численность', 'национальности', 'географическое положение', 'год']]
        
        # Возврат нового DataFrame после фильтрации для формирования отчета
        return new_df



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())