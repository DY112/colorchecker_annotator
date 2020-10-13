import sys,json,os
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *

JPG_FOLDER = '/Users/dykim/Desktop/colorchecker_bbox/jpg/'
EXT_TYPE = "JPG"

# connect UI file
form_class = uic.loadUiType("colorchecker_bbox.ui")[0]

# define class for GUI window
class WindowClass(QMainWindow, form_class) :
    def __init__(self, json_data, file_list) :
        super().__init__()
        self.setMouseTracking(False)
        self.setupUi(self)
        self.setWindowTitle("ColorChecker Box Annotation Tool")

        self.json_data = json_data
        self.file_list = file_list
        self.current_file_idx = 0
        self.current_box_idx = 0
        self.current_point_idx = 0
        self.top_left = [0,0]
        self.bottom_right = [0,0]
        self.top_left_ready = False
        self.bottom_right_ready = False

        # init qpixmap and show image
        self.qPixmapVar = QPixmap()
        self.reloadImage()

        # init qlistwidget
        self.updateList()

        # connect buttons with corresponding functions
        self.box_1.clicked.connect(self.boxoneFunction)
        self.box_2.clicked.connect(self.boxtwoFunction)
        self.box_3.clicked.connect(self.boxthreeFunction)
        self.box_4.clicked.connect(self.boxfourFunction)
        self.box_5.clicked.connect(self.boxfiveFunction)
        self.box_6.clicked.connect(self.boxsixFunction)
        self.next_file.clicked.connect(self.nextFileFunction)
        self.prev_file.clicked.connect(self.prevFileFunction)
        self.save_btn.clicked.connect(self.saveJson)

    def boxoneFunction(self):
        self.current_box_idx = 0
        self.top_left_ready = False
        self.bottom_right_ready = False
        self.mousecord.setText("Click top left corner of box 1")

    def boxtwoFunction(self):
        self.current_box_idx = 1
        self.top_left_ready = False
        self.bottom_right_ready = False
        self.mousecord.setText("Click top left corner of box 2")

    def boxthreeFunction(self):
        self.current_box_idx = 2
        self.top_left_ready = False
        self.bottom_right_ready = False
        self.mousecord.setText("Click top left corner of box 3")

    def boxfourFunction(self):
        self.current_box_idx = 3
        self.top_left_ready = False
        self.bottom_right_ready = False
        self.mousecord.setText("Click top left corner of box 4")

    def boxfiveFunction(self):
        self.current_box_idx = 4
        self.top_left_ready = False
        self.bottom_right_ready = False
        self.mousecord.setText("Click top left corner of box 5")

    def boxsixFunction(self):
        self.current_box_idx = 5
        self.top_left_ready = False
        self.bottom_right_ready = False
        self.mousecord.setText("Click top left corner of box 6")

    def boxFunction(self):
        self.top_left_ready = False
        self.bottom_right_ready = False
        

    def nextFileFunction(self):
        if self.current_file_idx+1 < len(self.file_list):
            self.current_file_idx += 1
        self.boxoneFunction()
        self.reloadImage()
        self.saveJson()

    def prevFileFunction(self):
        if self.current_file_idx > 0:
            self.current_file_idx -= 1
        self.boxoneFunction()
        self.reloadImage()
        self.saveJson()

    def mousePressEvent(self, event):
        if event.x() < 40 or event.x() > 1480 or event.y() < 50 or event.y() > 1010:
            return

        if self.top_left_ready == False:
            self.top_left = [(event.x()-40)*4, (event.y()-50)*4]
            self.top_left_ready = True
            msg = "box{0} top left pos : x={1} y={2}\nNow click the bottom right corner."\
                .format(self.current_box_idx+1, (event.x()-40)*4, (event.y()-50)*4)
            self.mousecord.setText(msg)

        elif self.bottom_right_ready == False:
            self.bottom_right = [(event.x()-40)*4, (event.y()-50)*4]
            self.bottom_right_ready = True
            msg = "box{0} bottom right pos : x={1} y={2}\nJson data updated."\
                .format(self.current_box_idx+1, (event.x()-40)*4, (event.y()-50)*4)
            
            # update json box coordinate
            if self.top_left_ready and self.bottom_right_ready:
                self.json_data[self.file_list[self.current_file_idx]]["box_"+str(self.current_box_idx)] = [self.top_left, self.bottom_right]
            
            # continue to next box
            if self.current_box_idx < 5:
                self.current_box_idx += 1
            self.top_left_ready = False
            self.bottom_right_ready = False
            self.mousecord.setText("Click top left corner of box "+str(self.current_box_idx+1))
        
        self.updateList()

    def reloadImage(self):
        # reload image
        self.filenamelabel.setText(str(self.file_list[self.current_file_idx]))
        self.qPixmapVar.load(os.path.join(JPG_FOLDER, self.file_list[self.current_file_idx]))
        self.qPixmapVar = self.qPixmapVar.scaledToWidth(1440)
        self.imagelabel.setPixmap(self.qPixmapVar)
        
        # update box list
        self.updateList()

    def updateList(self):
        # update box list view wrt current file
        current_filename = self.file_list[self.current_file_idx]
        self.boxlist.clear()
        self.boxlist.addItem(current_filename)
        for i in range(6):
            self.boxlist.addItem(str(self.json_data[current_filename]["box_"+str(i)]))

    def saveJson(self):
        with open('./annotation.json', 'w') as out_file:
            json.dump(self.json_data, out_file, indent=4)

def init_json(file_list):
    if os.path.exists('./annotation.json'):
    # if json file exists, read data
        with open('./annotation.json', 'r') as json_file:
            json_data = json.load(json_file)

        return json_data
    
    else:
    # if json file doesn't exist, create new one
        json_data = {}
        
        for filename in file_list:
            file_dict = {}
            for i in range(6):
                key = "box_" + str(i)
                value = [[0,0], [0,0]]
                file_dict[key] = value
            json_data[filename] = file_dict
        
        return json_data

if __name__ == "__main__" :
    # QApplication : Class that runs program
    app = QApplication(sys.argv)

    file_list = sorted(os.listdir(JPG_FOLDER))
    file_list = [f for f in file_list if f.endswith(EXT_TYPE)]
    json_data = init_json(file_list)

    # WindowClass Instanciation
    myWindow = WindowClass(json_data, file_list) 

    # Show program window
    myWindow.show()

    # App execution code
    app.exec_()