import json
import platform
from shutil import copyfileobj, unpack_archive
from tempfile import NamedTemporaryFile
from urllib.request import urlopen

from PyQt5.QtCore import QStandardPaths


class WinDlLily(QDialog):

    def __init__(self, parent):
    super(InfoDialog, self).__init__(parent)
    self.setWindowModality(Qt.WindowModal)

    """Combo box """
    combobox = QComboBox()
    combobox.addItems(result)# add list result here
    """"""
    layout = QVBoxLayout()
    layout.addWidget(combobox)
    layout.setSpacing(10)
    self.setLayout(layout)
    
    b.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    b.accepted.connect(self.accept)
    b.rejected.connect(self.reject)
    userguide.addButton(b, "prefs_lilypond")
    app.translateUI(self)
    qutil.saveDialogSize(self, "/preferences/lilypond/lilypondinfo/dialog/size")


    #def translateUI(self):
        #super(InfoList, self).translateUI()
        #WinRealises.setWindowTitle(_translate("WinRealises", "Get my Lilypond"))

        #self.label.setText(_translate("WinRealises", "Lilypond :"))
        #self.label_2.setText(_translate("WinRealises", "<html><head/><body><p><span style=\" font-weight:600;\">Select the desired version and click on ok </span></p></body></html>"))
        
 




    def get_all_lilypond_versions():
        '''Open and read the .json'''
        # TODO: handle "no network" case
        url = "https://gitlab.com/api/v4/projects/18695663/releases"
        response = urlopen(url)
        content = response.read()
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
            result.append(version)#ajouter une fonction sort())
        result.sort()
        return result

    def download_lilypond(version):
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
            unpack_archive(tfile.name, dest) # error: unknown archive format

    download_lilypond((2, 25, 5))