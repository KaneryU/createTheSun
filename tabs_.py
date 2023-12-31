#from PyQt6.QtCore import
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
#from PyQt6.QtGui import 
import sys
import save
import tabs.maintab as maintab
import tabs.automationtab as automationtab
import tabs.settingstab as settingstab
saveModule = save # I don't know if importing save from main.py will cause a circular import, but this feels safer for now.
class mainTab(QWidget):
    def updateDisplay(self):
        self.tabContent.updateDisplay()
    def updateInternal(self):
        pass
    def __init__(self):
        super().__init__()
        self.layout_ = QVBoxLayout()
        self.tabContent = maintab.content()
        self.layout_.addWidget(self.tabContent)
        self.setLayout(self.layout_)
         
    def name(): #type: ignore
        return "Main Tab"

class upgradeTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout_ = QVBoxLayout()
        self.layout_.addWidget(QLabel("Upgrade Tab"))
        self.setLayout(self.layout_)
        
    def updateDisplay(self):
        return 0
    
    def name(): #type: ignore
        return "Upgrades"

class automationTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout_ = QVBoxLayout()
        self.tabContent = automationtab.content()
        self.layout_.addWidget(self.tabContent)
        self.setLayout(self.layout_)
        
    def updateDisplay(self):
        self.tabContent.updateDisplay()
        
    def updateInternal(self):
        self.tabContent.updateInternal()
        
    def updateEverything(self):
        self.tabContent.updateEverything()
    
    def name(): #type: ignore
        return "Automation"
        
class settingsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout_ = QVBoxLayout()
        self.tabContent = settingstab.content()
        self.layout_.addWidget(self.tabContent)
        self.setLayout(self.layout_)
        
    def updateDisplay(self):
        return 0
    
    def name(): #type: ignore
        return "Settings"
    
class achievementsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout_ = QVBoxLayout()
        self.layout_.addWidget(QLabel("Achievements Tab"))
        self.setLayout(self.layout_)
    def updateDisplay(self):
        return 0
    
    def name(): #type: ignore
        return "Achevements"

tabs = [mainTab, automationTab, settingsTab]