from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow,  QDialog, QPushButton, QVBoxLayout, QLineEdit, QLabel
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys

Form, Window = uic.loadUiType("pril.ui")
GraficsForm, GraficsWindow = uic.loadUiType("grafics.ui")
ReportsForm, ReportsWindow = uic.loadUiType("reports.ui")

app = QApplication([])

window = Window()
form = Form()
form.setupUi(window)

grafics_window = None
reports_window = None
python_path = sys.executable
script_path = "grafiks/new.py"
script_path1 = "grafiks/Box.py"
script_path2 = "grafiks/krugv.py"
script_path3 = "grafiks/rass.py"
script_path4 = "grafiks/kategor_gist.py"
################################################################################################################################################################################################
path_report1 = "otcheti/report1.py"
path_report2 = "otcheti/report2.py"
path_report3 = "otcheti/report3.py"
path_svod = "otcheti/svodn.py"
path_svod2 = "otcheti/svod2.py"

########################################################################################################################################################################################################################

##################################################################################################################################################################################################################
def create_second_window():
    global reports_window
    reports_window = ReportsWindow()
    reports_form = ReportsForm()
    reports_form.setupUi(reports_window)

    button11 = QPushButton("Отчет о численности для национальности")
    button11.setObjectName("pushbutton_report1")
    button11.clicked.connect(opeт_first_report)

    button12 = QPushButton("Отчет о национальном составе региона в определенный год")
    button12.setObjectName("pushbutton_report2")
    button12.clicked.connect(opeт_second_report)

    button13 = QPushButton("Численный состав национальности в пределах")
    button13.setObjectName("pushbutton_report3")
    button13.clicked.connect(opeт_3_report)

    button14 = QPushButton("Сводная таблица национального состава РФ")
    button14.setObjectName("pushbutton_report4")
    button14.clicked.connect(opeт_4_report)

    button15 = QPushButton("Сводная таблица количества населения субъектов РФ")
    button15.setObjectName("pushbutton_report5")
    button15.clicked.connect(opeт_5_report)

    layout = reports_form.verticalLayout
    layout.addWidget(button11)
    layout.addWidget(button12)
    layout.addWidget(button13)
    layout.addWidget(button14)
    layout.addWidget(button15)

    reports_window.show()

def opeт_first_report():
    import subprocess
    subprocess.Popen([python_path, path_report1])

def opeт_second_report():
    import subprocess
    subprocess.Popen([python_path, path_report2])

def opeт_3_report():
    import subprocess
    subprocess.Popen([python_path, path_report3])

def opeт_4_report():
    import subprocess
    subprocess.Popen([python_path, path_svod])

def opeт_5_report():
    import subprocess
    subprocess.Popen([python_path, path_svod2])

###################################################################################################################################################################################################################

def create_new_window():
    global grafics_window
    grafics_window = GraficsWindow()
    grafics_form = GraficsForm()
    grafics_form.setupUi(grafics_window)

    button0 = QPushButton("Линейный график")
    button0.setObjectName("pushButton_line")
    button0.clicked.connect(open_new_window)
    
    button1 = QPushButton("График Bow-and-Whisker")
    button1.setObjectName("pushButton_line0")
    button1.clicked.connect(open_new_window_1)

    button22 = QPushButton("Круговая диаграмма")
    button22.setObjectName("pushButton_grafic1")
    button22.clicked.connect(open_new_window_2)

    button3 = QPushButton("Категоризированная диаграмма рассеивания")
    button3.setObjectName("pushButton_grafic2")
    button3.clicked.connect(open_new_window_3)
    
    button2 = QPushButton("Категоризированная гистограмма")
    button2.setObjectName("pushButton_grafic1")
    button2.clicked.connect(open_new_window_4)


    layout = grafics_form.verticalLayout
    layout.addWidget(button0)
    layout.addWidget(button1)
    layout.addWidget(button22)
    layout.addWidget(button3)
    layout.addWidget(button2)

    
    grafics_window.show()

def open_new_window():
    import subprocess
    subprocess.Popen([python_path, script_path])
def open_new_window_1():
    import subprocess
    subprocess.Popen([python_path, script_path1])
def open_new_window_2():
    import subprocess
    subprocess.Popen([python_path, script_path2])
def open_new_window_3():
    import subprocess
    subprocess.Popen([python_path, script_path3])
def open_new_window_4():
    import subprocess
    subprocess.Popen([python_path, script_path4])

form.pushButton.clicked.connect(create_new_window)
form.toolButton_2.clicked.connect(create_second_window)
window.show()
app.exec()