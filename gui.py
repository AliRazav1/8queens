from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor

def find_all_possibilities(lst,i):
  if (i>u) or (len(lst) == o) :
    possibilities.append(lst)
    return
  if (i not in [_[0] for _ in lst]):
   for myitem in range(1,u+1):
    if (myitem not in [_[1] for _ in lst]):
     if len([0 for p in lst if abs(p[0]-i) == abs(p[1]-myitem)])==0:
       find_all_possibilities(lst+[[i,myitem]],i+1)

def start(n,k):
  global possibilities , u,o
  u = n
  o = k
  possibilities = []
  find_all_possibilities([],1)
  return possibilities

class Pawn(QtWidgets.QWidget):
    def __init__(self,color):
        super().__init__()
        if color == 1:
         self.image = QtGui.QPixmap('bq.png')
        else:
         self.image = QtGui.QPixmap('wq.png')
        self.setMinimumSize(30, 30)
    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        size = min(self.width(), self.height())
        qp.drawPixmap(0, 0, self.image.scaled(
            size, size, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))

class process(QtWidgets.QWidget):
    def __init__(self , brd):
        super().__init__()
        layout = QtWidgets.QGridLayout(self)
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)
        self.myboard = brd
        self.number_of_all_possibilities = QtWidgets.QLabel()
        self.number_of_all_possibilities.setAlignment(Qt.AlignCenter)
        self.default_color = 1
        self.button = QtWidgets.QPushButton('Click me')
        self.button.setFixedWidth(120)
        self.next = QtWidgets.QPushButton('Next')
        self.next.setFixedWidth(120)
        self.previous = QtWidgets.QPushButton('Previous')
        self.black_mode = QtWidgets.QRadioButton()
        self.white_mode = QtWidgets.QRadioButton()
        self.black_mode.setChecked(True)
        self.black_mode.setText("Black Mode")
        self.white_mode.setText("White Mode")
        self.black_mode.toggled.connect(self.black_selected)
        self.white_mode.toggled.connect(self.white_selected)
        self.previous.setFixedWidth(120)
        self.previous.setEnabled(False)
        self.next.setEnabled(False)
        self.lst = None
        self.button.clicked.connect(lambda: self.draw_queens(8))
        self.button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.next.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.previous.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.black_mode.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.white_mode.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.next.clicked.connect(self.next_draw)
        self.previous.clicked.connect(self.previous_draw)
        layout.addWidget(self.number_of_all_possibilities)
        layout.addWidget(self.black_mode)
        layout.addWidget(self.white_mode)
        layout.addWidget(self.button)
        layout.addWidget(self.previous)
        layout.addWidget(self.next)
    def black_selected(self,selected):
        if selected:
            self.default_color = 1
            if self.lst != None:
                self.myboard.clear_widgets()
                self.myboard.drawing(self.lst[default_index],self.default_color)

    def white_selected(self,selected):
        if selected:
            self.default_color = 0
            if self.lst != None:
                self.myboard.clear_widgets()
                self.myboard.drawing(self.lst[default_index],self.default_color)

    def next_draw(self):
        global default_index
        default_index += 1
        self.myboard.clear_widgets()
        self.previous.setEnabled(True)
        if default_index == len(self.lst)-1:
            self.next.setEnabled(False)
        self.myboard.drawing(self.lst[default_index],self.default_color)
    def previous_draw(self):
        global default_index
        default_index -= 1
        self.myboard.clear_widgets()
        self.next.setEnabled(True)
        if default_index == 0:
            self.previous.setEnabled(False)
        self.myboard.drawing(self.lst[default_index],self.default_color)
    def draw_queens(self,t):
        global default_index
        self.lst = start(8,t)
        self.next.setEnabled(True)
        self.number_of_all_possibilities.setText("ALL : "+str(len(self.lst)))
        self.number_of_all_possibilities.adjustSize()
        self.myboard.drawing(self.lst[default_index],self.default_color)
        self.button.setEnabled(False)

class Board(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QGridLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.background = QtGui.QPixmap('photo.jpg')
        self.mylayout = layout
    
    def clear_widgets(self):
        for i in reversed(range(self.mylayout.count())): 
            self.mylayout.itemAt(i).widget().setParent(None)

    def drawing(self,l,c):
      for item in l:
       self.mylayout.addWidget(Pawn(c), item[0]-1, item[1]-1)

    def minimumSizeHint(self):
        return QtCore.QSize(500, 500)

    def sizesHint(self):
        return QtCore.QSize(1000, 1000)

    def resizeEvent(self, event):
        size = min(self.width(), self.height())
        rect = QtCore.QRect(0, 0, size, size)
        rect.moveCenter(self.rect().center())
        self.layout().setGeometry(rect)

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        rect = self.layout().geometry()
        qp.drawPixmap(rect, self.background.scaled(rect.size(), 
            QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
    

class ChessGame(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Chess Game')
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignCenter)
        self.board = Board()
        layout.addWidget(self.board)
        self.process = process(self.board)
        layout.addWidget(self.process)

import sys
default_index = 0
app = QtWidgets.QApplication(sys.argv)
game = ChessGame()
game.show()
sys.exit(app.exec_())