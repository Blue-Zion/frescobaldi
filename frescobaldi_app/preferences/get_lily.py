import json
import platform
from shutil import copyfileobj, unpack_archive
from tempfile import NamedTemporaryFile
from urllib.request import urlopen

from PyQt5.QtCore import QStandardPaths



class get_my_lily :


    def get_all_lilypond_versions():
        '''Open and read the .json'''
        
        url = "https://gitlab.com/api/v4/projects/18695663/releases"
        response = urlopen(url)
        content = response.read()
        if response.getcode() == 200 :#The status code 200 means that the response is OK.
            json_decode = json.loads(content.decode("utf8"))
        else:
            print ("a problem occurred when attempting to reach the json file" )
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
                    unpack_archive(tfile.name, dest,format="zip") #Unpack for windows
                except:
                    print("unrecognized archive format for the .zip download")
            elif platform.system() != 'Windows':
                try :
                    unpack_archive(tfile.name, dest,format="gztar") # Unpack for linux et darwin
                except:
                    print("unrecognized archive format for the .tar download")
