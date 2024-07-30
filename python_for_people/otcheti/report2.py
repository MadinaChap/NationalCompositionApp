import sys
import pandas as pd
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTableView, QTableWidgetItem, QHeaderView
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMessageBox, QTableView
from PyQt6.QtCore import QAbstractTableModel, Qt

number_to_word = {
    0: "Национальность",
    1: "Год",
    2: "Субъект",
    3: "Численность"
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
        loadUi("otcheti\otchet2.ui", self)

        df = pd.read_excel("python.xlsx")
        self.items1 = sorted(df["географическое положение"].unique().tolist())
        self.comboBox.addItems(self.items1)

        self.comboBox.currentIndexChanged.connect(self.update_items2) 
        self.pushButton.clicked.connect(self.create_report)  

        self.kol = None
        self.update_items2() 

    def update_items2(self):
        selected_subject = self.comboBox.currentText()
        df = pd.read_excel("python.xlsx")
        filtered_df = df[df["географическое положение"] == selected_subject]
        self.items2 = sorted(filtered_df["год"].unique().astype(str).tolist())  
        self.comboBox_2.clear()
        self.comboBox_2.addItems(self.items2)

    def create_report(self):
        position = self.comboBox.currentText()
        year = self.comboBox_2.currentText()

        df = pd.read_excel('python.xlsx')
        report_df = self.chisl(df, 'географическое положение', position, 'год', year)

        model = PandasModel(report_df)
        self.tableView.setModel(model)

    def chisl(self, df: pd.DataFrame, cndname_1: str, cndval_1: str, cndname_2: str, cndval_2: str) -> pd.DataFrame:
        """
        Функция фильтрует данные DataFrame по двум заданным условиям и возвращает новый DataFrame.

        Параметры:
        - df: pd.DataFrame - исходный DataFrame с данными
        - cndname_1: str - название первого столбца для условия фильтрации
        - cndval_1: str - значение первого условия фильтрации
        - cndname_2: str - название второго столбца для условия фильтрации
        - cndval_2: str - значение второго условия фильтрации

        Возвращает:
        - new_df: pd.DataFrame - новый DataFrame после фильтрации
        """
        
        # Фильтрация данных по двум заданным условиям
        new_df = df[(df[cndname_1] == cndval_1) & (df[cndname_2].astype(str) == cndval_2)][['национальности', 'год', 'географическое положение', 'численность']]
        
        # Возврат нового DataFrame после фильтрации
        return new_df



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())