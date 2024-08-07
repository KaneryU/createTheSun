import json
import sys
import time
from copy import deepcopy

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QVBoxLayout, QWidget

from .. import gamedefine, observerModel, urbanistFont
from ..gameLogic import itemGameLogic, numberLogic
from . import unlockTab


class purchaseStrip(QWidget):
    def __init__(self, name):
        super().__init__()
        self.layout_ = QHBoxLayout()
        self.layout_.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.name = name

        if not gamedefine.gamedefine.itemVisualDefine[name] == None:
            self.internalItem = gamedefine.gamedefine.itemInternalDefine[name]
            self.visualItem = gamedefine.gamedefine.itemVisualDefine[name]
        else:
            self.item = gamedefine.gamedefine.itemInternalDefine["proton"]
            self.visualItem = gamedefine.gamedefine.itemVisualDefine["proton"]
            name = "proton"
            print(f"error importing item '{name}' from gamedefine.gamedefine")

        self.setToolTip(gamedefine.gamedefine.itemVisualDefine[name]["description"])
        self.setToolTipDuration(5000)

        self.label = QLabel(
            f"You have {numberLogic.humanReadableNumber(gamedefine.gamedefine.amounts[name])} {self.visualItem['visualName'].lower()}"
        )

        self.layout_.addWidget(self.label)
        if not name == "quarks":
            self.purchaseButton = QPushButton("")
        else:
            self.purchaseButton = QPushButton("Free")
        self.purchaseButton.clicked.connect(self.purchase)
        self.layout_.addWidget(self.purchaseButton)

        self.setLayout(self.layout_)

    def purchase(self):
        observerModel.callEvent(
            observerModel.Observable.ITEM_OBSERVABLE, observerModel.ObservableCallType.GAINED, self.name
        )
        if self.name == "quarks":
            itemGameLogic.purchase("quarks")
            return 0

        if itemGameLogic.canAfford(self.name):
            itemGameLogic.purchase(self.name, True)

    def updateTab(self):
        """
        Updates the tab with the current information.

        This method updates the label text to display the amount of a specific item the player has.
        It also updates the purchase button text to display the cost of the item.
        If the item is "quarks", the purchase button text is set to "Free".
        """
        self.label.setText(
            f"You have {numberLogic.humanReadableNumber(gamedefine.gamedefine.amounts[self.name])} {self.visualItem['visualName'].lower()}"
        )

        if not self.internalItem["whatItCosts"][0]["amount"] == -1:
            self.purchaseButton.setText(itemGameLogic.parseCost(self.name))
            if not itemGameLogic.canAfford(self.name):
                self.purchaseButton.setDisabled(True)
            else:
                self.purchaseButton.setDisabled(False)
        else:
            self.purchaseButton.setText("Free")


class header(QWidget):
    def __init__(self):
        super().__init__()
        self.layout_ = QHBoxLayout()
        self.layout_.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.label = QLabel("Buy x")
        self.textEdit = QLineEdit("1")

        self.textEdit.setValidator(QIntValidator())
        self.textEdit.textChanged.connect(self.updateBuyMultiple)

        self.spacer = QSpacerItem(10, 0)

        self.maxAllButton = QPushButton("Max All")
        self.maxAllButton.clicked.connect(itemGameLogic.maxAll)

        self.layout_.addWidget(self.label)
        self.layout_.addWidget(self.textEdit)
        self.layout_.addItem(self.spacer)
        self.layout_.addWidget(self.maxAllButton)
        self.setLayout(self.layout_)
        self.setMaximumWidth(500)

    def updateBuyMultiple(self):
        try:
            if not int(self.textEdit.text()) == 0:
                if not int(self.textEdit.text()) < 0:
                    gamedefine.gamedefine.mainTabBuyMultiple = int(self.textEdit.text())
                else:
                    gamedefine.gamedefine.mainTabBuyMultiple = 1
            else:
                gamedefine.gamedefine.mainTabBuyMultiple = 1
        except:
            gamedefine.gamedefine.mainTabBuyMultiple = 1


class footer(QWidget):
    def __init__(self):
        super().__init__()
        self.layout_ = QVBoxLayout()
        self.layout_.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.content = unlockTab.unlockStrip("hydrogenUnlock", maintab=True)
        self.content.mouseReleaseEvent = self.mReleaseEvent
        self.layout_.addWidget(self.content)

        self.setLayout(self.layout_)

    def mReleaseEvent(self, event):
        for i in range(gamedefine.theTabWidget.count()):
            if gamedefine.theTabWidget.widget(i).objectName() == "unlockTab":
                gamedefine.theTabWidget.setCurrentIndex(i)
                break

    def updateDisplay(self):
        self.content.updateTab()


class content(QWidget):
    resetSignal = Signal()

    def __init__(self):
        super().__init__()
        self.resetObserver = observerModel.registerObserver(
            self.reset_,
            observerModel.Observable.RESET_OBSERVABLE,
            observerModel.ObservableCallType.ALL,
            observerModel.ObservableCheckType.TYPE,
            "mainTab",
        )
        self.resetSignal.connect(self.reset)
        self.topLevelLayout = QVBoxLayout()
        self.topLevelLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.header_ = header()
        self.topLevelLayout.addWidget(self.header_)

        self.purchaseStripsContainer = QWidget()
        self.purchaseStripsLayout = QVBoxLayout()
        self.purchaseStripsLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.purchaseStripsContainer.setLayout(self.purchaseStripsLayout)

        self.purchaseStrips: list[purchaseStrip] = []
        for i in gamedefine.gamedefine.purchaseToCreate:
            if not i == "electrons":
                print("Creating " + str(i))
                self.purchaseStrips.append(purchaseStrip(i))
                self.purchaseStripsLayout.addWidget(self.purchaseStrips[-1])

        self.topLevelLayout.addWidget(self.purchaseStripsContainer)

        self.footer_ = footer()
        self.topLevelLayout.addWidget(self.footer_)
        self.setLayout(self.topLevelLayout)

    def updateDisplay(self):
        for i in self.purchaseStrips:
            i.updateTab()

        if not len(self.purchaseStrips) == len(gamedefine.gamedefine.purchaseToCreate):
            self.reset()

        self.footer_.updateDisplay()

    def reset(self):
        print("reseting")
        for i in reversed(range(len(self.purchaseStrips))):
            widget = self.purchaseStrips[i]
            self.purchaseStripsLayout.removeWidget(widget)
            widget.setParent(None)
            widget.deleteLater()
            self.purchaseStrips.pop(i)

        for i in gamedefine.gamedefine.purchaseToCreate:
            print("Creating " + str(i))
            self.purchaseStrips.append(purchaseStrip(i))
            self.purchaseStripsLayout.addWidget(self.purchaseStrips[-1])

        self.setLayout(self.topLevelLayout)

    def reset_(self, event):
        self.resetSignal.emit()
