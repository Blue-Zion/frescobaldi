import json
import platform
from shutil import copyfileobj, unpack_archive
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
import os
from PyQt5.QtCore import QStandardPaths
from PyQt5.QtCore import QSettings, Qt
from PyQt5.QtWidgets import (QAbstractItemView, QDialog, QDialogButtonBox,
 QFileDialog,QGridLayout, QHBoxLayout, QLabel, QLineEdit, QListWidgetItem,
 QPushButton,QComboBox, QVBoxLayout, QWidget)



#def settings():
    #s = QSettings()
    #s.beginGroup("lilypond_settings")
    #return s

#class WinDlLily(QDialog):

    #def __init__(self, parent):
    #super(InfoDialog, self).__init__(parent)
    #self.setWindowModality(Qt.WindowModal)




    """Combo box """
    #combobox = QComboBox()
    #combobox.addItems(result)# add list result here
    """"""
    #layout = QVBoxLayout()
    #layout.addWidget(combobox)
    #layout.setSpacing(10)
    #self.setLayout(layout)
    #b = self.buttons = QDialogButtonBox(self)
    #layout.addWidget(b)

    #b.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    #b.accepted.connect(self.accept)
    #b.rejected.connect(self.reject)
    #userguide.addButton(b, "prefs_lilypond")
    #app.translateUI(self)
    #qutil.saveDialogSize(self, "/preferences/lilypond/lilypondinfo/dialog/size")


    #def translateUI(self):
        #self.setWindowTitle(app.caption(_("LilyPond")))
        #super(InfoList, self).translateUI()
        #WinRealises.setWindowTitle(_translate("WinRealises", "Get my Lilypond"))

       
 


    def get_all_lilypond_versions():
        '''Open and read the .json'''
        # TODO: handle "no network" case
        url = "https://gitlab.com/api/v4/projects/18695663/releases"
        response = urlopen(url)
        content = response.read()
        if response.getcode() == 200 :#The status code 200 means that the response is OK.
            json_decode = json.loads(content.decode("utf8"))
        result = []

        '''Put what we have find from a specific directory in the .json into a dictionary '''
        '''Then we filetre it to have a proper material to use'''

        for item in json_decode:
            tag = item ['tag_name']
            if tag == "release/2.22.2-1" :
                continue
            tag = tag.lstrip("v") # We just want numbers , so we erase the "v"
            tag_split = tag.split(".") # Split each number (tuplet)
            version = [int(v) for v in tag_split] # Conversion into integer
            result.append(version)
        result.sort() # We sort the result 
        return result

    def download_lilypond(version):
        ''' Download according to the operating system user'''
        major, minor, micro = version
        if platform.system() == 'Darwin':
            archive = f"lilypond-{major}.{minor}.{micro}-darwin-x86_64.tar.gz"
            lily_url = f"https://gitlab.com/lilypond/lilypond/-/releases/v{major}.{minor}.{micro}/downloads/{archive}"
        elif platform.system() == 'Linux':
            archive = f"lilypond-{major}.{minor}.{micro}-linux-x86_64.tar.gz"
            lily_url = f"https://gitlab.com/lilypond/lilypond/-/releases/v{major}.{minor}.{micro}/downloads/{archive}"
        elif platform.system() == 'Windows':
            archive = f"lilypond-{major}.{minor}.{micro}-mingw-x86_64.zip"
            lily_url = f"https://gitlab.com/lilypond/lilypond/-/releases/v{major}.{minor}.{micro}/downloads/{archive}"

        # We download the compressed file in a tempory file and copy it
        # to the destination
        with urlopen(lily_url) as response, NamedTemporaryFile() as tfile:
            copyfileobj(response, tfile)
            dest = QStandardPaths.writableLocation(QStandardPaths.DataLocation)
            print(dest)
            if platform.system() == 'Windows' :
                try : 
                    unpack_archive(tfile.name, dest,format="zip") # faire un try pour windows
                except:
                    print("unrecognized archive format for the download")
            elif platform.system() != 'Windows':
                try :
                    unpack_archive(tfile.name, dest,format="gztar") # faire un try pour linux et darwin
                except:
                    print("unrecognized archive format for the download")

    download_lilypond((2, 25, 5))
  
                    if platform.system() == 'Linux' :
                        try:
                            os.system('sudo apt install -y <package_name>')
                        except:
                            exit("Failed to install Lilypond")
                    elif platform.system() == 'Windows' :
                        try:
                            os.system('winget install<Software_name>')
                        except:
                            exit("Failed to install Lilypond <Software_name>")
                    elif platform.system() == 'Darwin' :
                        try:
                            os.system('<Software_name>')#A finir
                        except:
                            exit("Failed to install Lilypond <Software_name>")    
    #
    #
    #
    #
    #
    #
    #uninstall software windows:
    #os.system(f'wmic product where description = (name software) unistall
    #
