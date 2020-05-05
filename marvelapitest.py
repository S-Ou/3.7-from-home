import sys  # Importing everyting
import asyncio
import math
import PyQt5
from functools import partial
import urllib, io, aiohttp
import copy
import marvel  # pip install git+https://github.com/Rocked03/PyMarvel-Asyncronous.git
from PyQt5.QtWidgets import QWidget, QMainWindow, QDesktopWidget, QApplication, QToolTip, QPushButton, QLabel, QLineEdit, QGridLayout, QVBoxLayout, QHBoxLayout, QAbstractButton
from PyQt5.QtGui import QFont, QPixmap, QPainter, QImage, QColor, QPalette
from PyQt5 import QtCore
from marvel.marvel import Marvel

pub = 'c308e081bf8a6f8347e89da166b8be55'
pri = '13f8386ead310c3da88b68be2b5088034dbfa60b'
m = Marvel(pub, pri)  # Initialising Marvel API session


class PicButton(QAbstractButton):
    """Picture button Object - code from https://stackoverflow.com/questions/2711033/how-code-a-image-button-in-pyqt"""
    def __init__(self, pixmap, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def size(self):
        return self.pixmap.size()


class Base(QMainWindow):
    """Main Window Base"""
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Marvel API Search Test')  # Window Title

        self.setAutoFillBackground(True)
        p = self.palette()
        # p.setColor(self.backgroundRole(), QtCore.Qt.darkGray)
        self.setPalette(p)

        layout = QVBoxLayout()  # Allows multiple layouts to be added and layed out vertically

        layout.addWidget(Main())
        layout.addWidget(Infobox())

        wid = QWidget()
        wid.setLayout(layout)

        # self.setFont(QFont("Beyno", 14))

        self.setCentralWidget(wid)

class WorkerThread(QtCore.QObject):
    """Signal thing that allows variables to be passed from 1 class to another"""
    # global searchclick
    searchclick = QtCore.pyqtSignal(PyQt5.QtWidgets.QLineEdit)
    line = ''
 
    def __init__(self, parent=None):
        super(WorkerThread, self).__init__(parent)


    # @QtCore.pyqtSlot()
    def run(self):
        self.searchclick.connect(Infobox.clickmethod)
        self.searchclick.emit(self.line)

    


class Main(QWidget):
    """Main window"""
    def __init__(self):
        super().__init__()

        self.worker = aworker  # Signal thing
       
        self.setMaximumHeight(150)  # Height of box

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.open())
        loop.close()

    @QtCore.pyqtSlot()  # Makes the signal thing work
    async def open(self):
        """All the stuff in the box"""

        self.setAutoFillBackground(True)
        p = self.palette()
        # p.setColor(self.backgroundRole(), QtCore.Qt.darkRed)
        self.setPalette(p)

        # print(self.height())

        screen = app.primaryScreen()
        size = screen.availableGeometry()

        # self.nameLabel = QLabel(self)  # "Search" before the search bpx
        # self.nameLabel.setText('Search:')
        # # self.nameLabel.setStyleSheet("QLabel { color : white; font-weight: bold; }")
        # self.nameLabel.setStyleSheet("QLabel { font-weight: bold; }")
        self.line = QLineEdit(self)  # Search box
        # self.line.returnPressed.connect(Infobox.wrapclickmethod())
        self.line.returnPressed.connect(self.runwrapper)  # On Enter


        # self.line.move(80, 20)  # Positioning
        self.line.resize(1000, 80)
        self.line.move(int(size.width() / 2 - 500), 50)
        # self.nameLabel.move(20, 20)

        self.title = QLabel(self)
        self.title.setText('Marvel API search    ')
        self.title.setStyleSheet("QLabel { font-weight: bold; font-size: 30px; }")
        self.title.move(int(size.width() / 2 - self.title.width()), 20)

        # pybutton = QPushButton('OK', self)  # OK button
        # # pybutton.clicked.connect(Infobox.wrapclickmethod())
        # # pybutton.clicked.connect(self.runwrapper)
        # pybutton.clicked.connect(self.runwrapper)  # On Click
        # pybutton.resize(200,32)
        # pybutton.move(80, 60)

    def runwrapper(self):
        """Wrapper"""
        self.worker.line = self.line
        self.worker.run()

    def filler(self):
        pass


class Infobox(QWidget):
    """Box with all the info"""
    def __init__(self):
        super().__init__()

        self.worker = aworker  # Signal stuff
        self.workerThread = QtCore.QThread()
        self.worker.searchclick.connect(self.wrapclickmethod)
        self.worker.moveToThread(self.workerThread)
        self.workerThread.start()


        self.grid_layout = QGridLayout()
        self.grid_layout.setHorizontalSpacing(5)
        self.setLayout(self.grid_layout)


        loopc = asyncio.new_event_loop()
        loopc.run_until_complete(self.setup())
        loopc.close()

    async def setup(self):
        """All the stuff in the box"""
        self.info = QLabel(self)  # Where the comic info goes
        # self.info.setText('a\nb\nc')
        self.info.setText('Comic info displayed here')  # Placeholder
        self.info.move(20, 0)
        self.info.resize(1000, 50)


        # for x in range(3):
        #     for y in range(3):
        #         button = QPushButton(str(str(3*x+y)))
        #         self.grid_layout.addWidget(button, x, y)


    def wrapclickmethod(self, line):
        """Runs the asyncronous function through a non-asyncronous function"""
        self.line = line
        loopb = asyncio.new_event_loop()
        loopb.run_until_complete(self.clickmethod())
        loopb.close()

    async def clickmethod(self):
        """Search thing on click"""
        for i in reversed(range(self.grid_layout.count())):  # Clear grid
            self.grid_layout.itemAt(i).widget().deleteLater()


        # self.info.setText(await self.searchapi(self.line.text()))

        output = await self.searchapi(self.line.text())  # Get search text, and search it

        screen = app.primaryScreen()
        size = screen.availableGeometry()

        widthsize = 200
        width = math.floor((size.width() - 50) / widthsize)
        height = math.ceil(len(output) / width)
        newwidthsize = math.floor(((size.width() - 50) - ((width - 1) * 5)) / width)  # Get sizing and grid layout based on window size


        # width = 1
        # height = len(output)

        i = 0
        for x in range(width):  # For each button
            for y in range(height):
                if i == len(output): break
                button = QPushButton()  # Create the button
                button.clicked.connect(partial(self.wrapseriesinfo, output, int(i)))  # Show info on click
                button.setMinimumHeight(350)  # Size
                button.setMaximumWidth(newwidthsize)
                buttontxt = QLabel(self)  # Text inside button
                buttontxt.setText(output[i].title)
                buttontxt.setWordWrap(True)
                buttontxt.setAlignment(QtCore.Qt.AlignCenter)
                buttonlayout = QHBoxLayout(button)
                buttonlayout.addWidget(buttontxt, 0, QtCore.Qt.AlignCenter)

                self.grid_layout.addWidget(button, y, x)  # Add button to grid

                i += 1

        i = 0
        for x in range(width):  # This puts pictures on the buttons

            break  # But it's a bit broken so the break just skips over it for now

            for y in range(height):
                if i == len(output): break
                # thumb = output[i].thumbnail
                try:
                    thumb = (await m.get_comic(output[i].comics.items[-1].resourceURI.split('/')[-1])).data.results[0].images[0]
                except IndexError:
                    thumb = output[i].thumbnail
                thumbnail = thumb.path + '/portrait_incredible.' + thumb.extension
                # thumbnail = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/1200px-Google_%22G%22_Logo.svg.png"

                async with aiohttp.ClientSession() as cs:
                    async with cs.get(thumbnail) as r:
                        image_file = await r.read()
                final_image = QImage()
                final_image.loadFromData(image_file)
                img = QPixmap(final_image)
                print(type(img))
                button = PicButton(img)
                button.resize(216, 324)
                button.move(0, 0)

                self.grid_layout.addWidget(button, y, x)
                print(self.grid_layout.count())
                i += 1


    def wrapseriesinfo(self, output, i):
        """Runs the asyncronous function through a non-asyncronous function"""
        loops = asyncio.new_event_loop()
        loops.run_until_complete(self.seriesinfo(output[i]))
        loops.close()

    async def seriesinfo(self, series):
        """Turns raw info into a nice String"""
        # print(series.description)
        desc = series.description if series.description else 'No description'
        textlist = [series.title, desc, ', '.join([i.name for i in series.creators.items if i.role == 'writer'])]
        text = '\n'.join(textlist)
        self.info.setText(text)



    async def searchapi(self, x):
        """Searches API from query"""
        # character_data_wrapper = await m.get_characters(orderBy="name,-modified", limit="5", offset="15")
        # x = ', '.join([character.name for character in character_data_wrapper.data.results])

        # comics = await m.get_series(titleStartsWith=x, orderBy='-startYear,title', limit='20')
        # y = ', '.join([z.title for z in comics.data.results])

        # return y


        comicfull = await m.get_series(titleStartsWith = x, limit = '100', orderBy = "-startYear")  # Searches
        comiccoll = await m.get_series(titleStartsWith = x, limit = '100', orderBy = "-startYear", seriesType = 'collection')  # Searches, but only for collections

        try: comicfullt = comicfull.data.dict['total']
        except KeyError: comicfullt = 0
        try: comiccollt = comiccoll.data.dict['total']
        except KeyError: comiccollt = 0

        limit = 20

        print(comicfullt, comiccollt)
        ntotal = comicfullt - comiccollt
        nresults = []
        oresults = [i.dict for i in comiccoll.data.results]
        x = 0
        for i in comicfull.data.results:  # Compares full list with collection list, and removes any collections
            if i.dict not in oresults: 
                nresults.append(i.dict)
                x += 1
            if x >= limit: break

        nwrapper = comicfull.dict
        nwrapper['data']['total'] = ntotal
        nwrapper['data']['count'] = len(nresults)
        nwrapper['data']['results'] = nresults

        comicraw = marvel.series.SeriesDataWrapper(m, nwrapper)  # Creates new list without collections (stupid API thing doesn't have in-built option for this, so it had to be done manually)

        return comicraw.data.results


if __name__ == '__main__':
    """get it to run"""
    app = QApplication(sys.argv)

    global aworker  # The only global variable in the whole code. This is necessary so that all the classes can access the same instance of WorkerThread(), and therefore emit and receive signals (send search query on click)
    aworker = WorkerThread()

    w = Base()
    w.showMaximized()  # Full-screen

    sys.exit(app.exec_())
