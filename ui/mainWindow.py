from PyQt5.QtCore import Qt, pyqtSignal, QEasingCurve
from PyQt5.QtWidgets import QFrame, QLabel, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QIcon
from qfluentwidgets import (
    setTheme,
    theme,
    Theme,
    LineEdit,
    BodyLabel,
    NavigationBar,
    FluentIcon,
    FlowLayout,
    PushButton,
    NavigationInterface,
    NavigationItemPosition,
    OpacityAniStackedWidget,
    PopUpAniStackedWidget,
    FolderListDialog,
)
from qframelesswindow import FramelessWindow, TitleBar
from .parseInterface import ParseInterface
from .trainInterface import TrainInterface
from .infoInterface import InfoInterface

# import darkdetect


class StackedWidget(QFrame):
    """Stacked widget"""

    currentChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.view = PopUpAniStackedWidget(self)

        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.view)

        self.view.currentChanged.connect(self.currentChanged)

    def addWidget(self, widget):
        """add widget to view"""
        self.view.addWidget(widget)

    def widget(self, index: int):
        return self.view.widget(index)

    def setCurrentWidget(self, widget, popOut=False):
        if not popOut:
            self.view.setCurrentWidget(widget, duration=300)
        else:
            self.view.setCurrentWidget(widget, True, False, 200, QEasingCurve.InQuad)

    def setCurrentIndex(self, index, popOut=False):
        self.setCurrentWidget(self.view.widget(index), popOut)


class MyTitleBar(TitleBar):
    """Title bar with icon and title"""

    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedHeight(48)
        self.hBoxLayout.removeWidget(self.minBtn)
        self.hBoxLayout.removeWidget(self.maxBtn)
        self.hBoxLayout.removeWidget(self.closeBtn)
        # add window icon
        self.iconLabel = QLabel(self)
        self.iconLabel.setFixedSize(18, 18)
        self.iconLabel.setPixmap(QIcon("rsc/img/icon.png").pixmap(18, 18))

        # add title label
        self.titleLabel = BodyLabel(self)
        self.titleLabel.setText("Music Trainer")

        self.vBoxLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setSpacing(0)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout.setAlignment(Qt.AlignTop)
        self.buttonLayout.addWidget(self.minBtn)
        self.buttonLayout.addWidget(self.maxBtn)
        self.buttonLayout.addWidget(self.closeBtn)
        self.vBoxLayout.addLayout(self.buttonLayout)
        self.vBoxLayout.addStretch(1)

        self.hBoxLayout.setStretch(0, 0)
        self.hBoxLayout.addSpacing(16)
        self.hBoxLayout.addWidget(self.iconLabel)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.titleLabel)
        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addLayout(self.vBoxLayout, 0)


class MainWindow(FramelessWindow):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.setTitleBar(MyTitleBar(self))
        self.titleBar.setAttribute(Qt.WA_StyledBackground)
        # self.setQss()

        self.hBoxLayout = QHBoxLayout(self)
        self.navigationBar = NavigationBar(self)
        self.stackWidget = StackedWidget(self)

        self.trainInterface = TrainInterface(self)
        self.parseInterface = ParseInterface(self)
        self.infoInterface = InfoInterface(self)

        self.initLayout()
        self.initNavigation()

    def initLayout(self):
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 48, 0, 0)
        self.hBoxLayout.addWidget(self.navigationBar)
        self.hBoxLayout.addWidget(self.stackWidget)
        self.hBoxLayout.setStretchFactor(self.stackWidget, 1)

    def initNavigation(self):
        self.addSubInterface(self.trainInterface, FluentIcon.SEND, "训练")
        self.addSubInterface(self.parseInterface, FluentIcon.MUSIC_FOLDER, "解析")
        self.addSubInterface(self.infoInterface, FluentIcon.INFO, "关于")

        self.stackWidget.currentChanged.connect(self.onCurrentInterfaceChanged)
        self.navigationBar.setCurrentItem(self.trainInterface.objectName())

    def addSubInterface(
        self,
        interface,
        icon,
        text: str,
        position=NavigationItemPosition.TOP,
        selectedIcon=None,
    ):
        self.stackWidget.addWidget(interface)
        self.navigationBar.addItem(
            routeKey=interface.objectName(),
            icon=icon,
            text=text,
            onClick=lambda: self.stackWidget.setCurrentWidget(interface),
            selectedIcon=selectedIcon,
            position=position,
        )

    def onCurrentInterfaceChanged(self, index):
        widget = self.stackWidget.widget(index)
        self.navigationBar.setCurrentItem(widget.objectName())

    # def setQss(self):
    #     isDark = darkdetect.isDark()
    #     if isDark:
    #         setTheme(Theme.DARK)
    #     color = "dark" if isDark else "light"
    #     with open(f"ui/resource/{color}.qss", encoding='utf-8') as f:
    #         self.setStyleSheet(f.read())
