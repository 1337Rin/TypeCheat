#from PySide6.QtCore import QFileInfo
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QCheckBox,
    QApplication,
    QDialog,
    QTabWidget,
    QLineEdit,
    QDialogButtonBox,
    QFrame,
    QListWidget,
    QGroupBox,
    QGridLayout,
    QSpinBox,
    QTextEdit, 
    QPushButton, 
    QMessageBox, 
    QListWidget,
    QVBoxLayout, 
    QFileDialog,
)

from PySide6 import QtCore
from PySide6.QtCore import Qt

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from PIL import Image
from pytesseract import pytesseract

import time
import tempfile
import os
import sys
import subprocess

#driver = webdriver.Firefox()
#driver.get("https://play.typeracer.com/")
#actions = ActionChains(driver)

#practice xPaths
raceTextS = "/html/body/div[1]/div/div[1]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/div/div[1]/table/tbody/tr[3]/td/div/div/table/tbody/tr[2]/td[3]/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table"
inputTextS = "/html/body/div[1]/div/div[1]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/div/div[1]/table/tbody/tr[3]/td/div/div/table/tbody/tr[2]/td[3]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/input"

#multiplyer xpaths
raceTextM = "/html/body/div[1]/div/div[1]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/div/div[1]/div/table/tbody/tr[2]/td[3]/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div"
inputTextM = "/html/body/div[1]/div/div[1]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/div/div[1]/div/table/tbody/tr[2]/td[3]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/input"

#sign in button
signXPATH = "/html/body/div[1]/div/div[1]/table/tbody/tr/td[3]/div/div[2]/div[2]/div[1]/a[2]"
signXPATH2 = "/html/body/div[4]/div/div/div[3]/div/div[1]/div/table[1]/tbody/tr[2]/td/div/table/tbody/tr[4]/td[2]/table/tbody/tr/td[1]/button"
usernameXPATH = "/html/body/div[4]/div/div/div[3]/div/div[1]/div/table[1]/tbody/tr[2]/td/div/table/tbody/tr[1]/td[2]/input"
passwordXPATH = "/html/body/div[4]/div/div/div[3]/div/div[1]/div/table[1]/tbody/tr[2]/td/div/table/tbody/tr[2]/td[2]/table/tbody/tr[1]/td/input"

#text to image stuff
path_to_tesseract = r"/usr/bin/tesseract"
imagePath = f"{tempfile.gettempdir()}/foo.png"
pytesseract.tesseract_cmd = path_to_tesseract

def xpathExists(xpath):
    try:
        driver.find_element(By.XPATH, xpath)
        return True
    except NoSuchElementException:
        return False

class TabDialog(QDialog):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        tab_widget = QTabWidget()
        tab_widget.addTab(CheatTab(self), "Cheat")
        tab_widget.addTab(SettingsTab(self), "Settings")
        tab_widget.addTab(About(self), "About")

        main_layout = QVBoxLayout()
        main_layout.addWidget(tab_widget)
        self.setLayout(main_layout)
        self.setWindowTitle("TypeCheater")

class CheatTab(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.btn = QPushButton("Get text")
        self.btn.clicked.connect(self.getText)

        self.btn2 = QPushButton("Start typing")
        self.btn2.clicked.connect(self.startRace)

        self.wpmLabel = QLabel("WPM:")
        self.wpm = QSpinBox()
        self.wpm.setValue(50)
        self.wpm.setMaximum(999)

        self.textLabel = QLabel("Selected text: ")
        self.txtDisplay = QTextBrowser()

        button_layout_1 = QVBoxLayout()
        button_layout_1.addWidget(self.btn)
        button_layout_1.addWidget(self.btn2)
        button_layout_1.addStretch()

        main_layout = QGridLayout()
        main_layout.addWidget(self.wpmLabel, 0, 0)
        main_layout.addWidget(self.wpm, 0, 1)
        main_layout.addLayout(button_layout_1, 1, 1)
        main_layout.addWidget(self.textLabel, 2, 0)
        main_layout.addWidget(self.txtDisplay, 2, 1)

        self.setLayout(main_layout)

    def getText(self):
        if xpathExists(raceTextS) == True:
            raceText = raceTextS
        elif xpathExists(raceTextM) == True:
            raceText = raceTextM
        else:
            Print("cant find xpath")

        self.txtDisplay.clear()
        global text
        text = driver.find_element(By.XPATH, raceText)
        text.screenshot(imagePath)

        img = Image.open(rf"{imagePath}")
        text = pytesseract.image_to_string(img)
        text = text.replace("\n", " ", -1)
        text = text.replace(" change display format", "", -1)
        text = text.replace("|", "I", -1)
        self.txtDisplay.append(text[:-1])

    def startRace(self):
        if xpathExists(inputTextS) == True:
            inputText = inputTextS
        elif xpathExists(inputTextM) == True:
            inputText = inputTextM
        else:
            print("cant find xpath")

        interval = ((60 / len(text[:-1])) * (len(text[:-1]) / (self.wpm.value() * 5)))
        inputfield = driver.find_element(By.XPATH, inputText)
        for i in text[:-1]:
            time.sleep(interval)
            inputfield.send_keys(i)

        if os.path.exists(imagePath):
            os.remove(imagePath)

class SettingsTab(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.launchLabal = QLabel("launch browser:")
        self.relaunch = QPushButton("relaunch")
        self.relaunch.clicked.connect(self.newdriver)

        self.tesseractLabel = QLabel("tesseract path:")
        self.tesseractInput = QLineEdit()
        self.tesseractInput.setText(path_to_tesseract)

        self.setpath = QPushButton("set")
        self.setpath.clicked.connect(self.setTesseractPath)

        self.credLabel = QLabel("login credentials (optional)")
        self.userLabel = QLabel("username:")
        self.passLabel = QLabel("password:")
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)

        self.login = QCheckBox("Login")

        main_layout = QGridLayout()
        main_layout.addWidget(self.relaunch, 0, 1)
        main_layout.addWidget(self.launchLabal, 0, 0)
        main_layout.addWidget(self.tesseractLabel, 1, 0)
        main_layout.addWidget(self.tesseractInput, 1, 1)
        main_layout.addWidget(self.setpath, 1, 2)
        main_layout.addWidget(self.credLabel, 2, 0)
        main_layout.addWidget(self.userLabel, 3, 0)
        main_layout.addWidget(self.username, 3, 1)
        main_layout.addWidget(self.passLabel, 4, 0, Qt.AlignTop)
        main_layout.addWidget(self.password, 4, 1, Qt.AlignTop)
        main_layout.addWidget(self.login, 5, 0, Qt.AlignTop)
        self.setLayout(main_layout)

    def newdriver(self):
        global driver
        global actions
        driver = webdriver.Firefox()
        driver.get("https://play.typeracer.com/")
        actions = ActionChains(driver)

        if self.login.isChecked() and self.username.text() != "" and self.password.text() != "":
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, signXPATH)))
            signIn = driver.find_element(By.XPATH, signXPATH)
            signIn.click()

            usernameInput = driver.find_element(By.XPATH, usernameXPATH)
            passwordInput = driver.find_element(By.XPATH, passwordXPATH)
            signIn2 = driver.find_element(By.XPATH, signXPATH2)

            usernameInput.send_keys(self.username.text())
            passwordInput.send_keys(self.password.text())
            signIn2.click()

            popUpXpath = "/html/body/div[5]/div/div/div[1]"
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, popUpXpath)))
            popUp = driver.find_element(By.XPATH, popUpXpath)
            popUp.click()

        else:
            pass

    def setTesseractPath(self):
        path_to_tesseract = rf"{self.tesseractInput.text()}"
        pytesseract.tesseract_cmd = path_to_tesseract
        self.tesseractInput.setText(path_to_tesseract)

class About(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tab_dialog = TabDialog()
    tab_dialog.show()
    sys.exit(app.exec())
