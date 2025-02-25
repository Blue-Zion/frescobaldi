# This file is part of the Frescobaldi project, http://www.frescobaldi.org/
#
# Copyright (c) 2008 - 2014 by Wilbert Berendsen
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# See http://www.gnu.org/licenses/ for more information.

"""
Widgets to edit a list of items in a flexible way.
"""


from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QFileDialog, QGridLayout, QListWidget, QListWidgetItem, QPushButton,
    QWidget)

import app
import icons


class ListEdit(QWidget):
    """A widget to edit a list of items (e.g. a list of directories)."""

    # emitted when anything changed in the listbox.
    changed = pyqtSignal()

    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        layout = QGridLayout(self)#The new grid layout  is call layout
        self.setLayout(layout)#It Constructs a new grid layout.This layout divides the space into rows and columns.

        
        self.addButton = QPushButton(icons.get('list-add'), '')#It Provides an Add button
        self.editButton = QPushButton(icons.get('document-edit'), '')#It Provides an Edit button
        self.removeButton = QPushButton(icons.get('list-remove'), '')# It Provides a Remove button
        self.listBox = QListWidget()#It Provides a list view 

        """Add childs widget on layout ,and spacing and margins between each ones"""
        """                          v v v v v v v v                           """

        layout.setContentsMargins(1, 1, 1, 1)#SizeConstraint { SetDefaultConstraint, SetFixedSize, SetMinimumSize, SetMaximumSize, SetMinAndMaxSize, SetNoConstraint }
        layout.setSpacing(0)#
        layout.addWidget(self.listBox, 0, 0, 8, 1)#
        layout.addWidget(self.addButton, 1, 1)#first number is the up-bottom position , seconde number is the left-right position
        layout.addWidget(self.editButton, 2, 1)#first number is the up-bottom position , seconde number is the left-right position
        layout.addWidget(self.removeButton, 3, 1)#first number is the up-bottom position , seconde number is the left-right position

        """ The buttons are unable/able when the list is empty/not empty  """
        """                       v v v v                                 """
        self.changed.connect(self.updateSelection)
        self.listBox.itemSelectionChanged.connect(self.updateSelection)
        self.updateSelection()
        self.connectSlots()
        app.translateUI(self)
    
    
    def connectSlots(self):
        """Add action to buttons"""
        self.addButton.clicked.connect(self.addClicked)#Connect the add button to the fonction addClicked
        self.editButton.clicked.connect(self.editClicked)#Connect the edit button to the fonction editClicked
        self.removeButton.clicked.connect(self.removeClicked)#Connect the remove button to the fonction removeClicked
        self.listBox.itemDoubleClicked.connect(self.itemDoubleClicked)#Connect the listbox to the fonction itemDoubleClicked
        self.listBox.model().layoutChanged.connect(self.changed)

    

    def translateUI(self):
        """Add text  to buttons ,internationalization """
        self.addButton.setText(_("&Add..."))
        self.editButton.setText(_("&Edit..."))
        self.removeButton.setText(_("&Remove"))
    

     
    def addClicked(self, button):
        """ Fonction connected to button add """
        item = self.createItem()
        if self.openEditor(item):
            self.addItem(item)

    def editClicked(self, button):
        """ Fonction connected to button edit """
        item = self.listBox.currentItem()
        item and self.editItem(item)

    def removeClicked(self, button):
        """ Fonction connected to button remove """
        item = self.listBox.currentItem()
        if item:
            self.removeItem(item)

    def updateSelection(self):
        selected = bool(self.listBox.currentItem())
        self.editButton.setEnabled(selected)
        self.removeButton.setEnabled(selected)

    def itemDoubleClicked(self, item):
        item and self.editItem(item)

    def createItem(self):
        return QListWidgetItem()

    def addItem(self, item):
        self.listBox.addItem(item)
        self.itemChanged(item)
        self.changed.emit()

    def removeItem(self, item):
        self.listBox.takeItem(self.listBox.row(item))
        self.changed.emit()

    def editItem(self, item):
        if self.openEditor(item):
            self.itemChanged(item)
            self.changed.emit()

    def setCurrentItem(self, item):
        self.listBox.setCurrentItem(item)

    def setCurrentRow(self, row):
        self.listBox.setCurrentRow(row)

    def openEditor(self, item):
        """Opens an editor (dialog) for the item.

        Returns True if the dialog was accepted and the item edited.
        Returns False if the dialog was cancelled (the item must be left
        unedited).
        """
        pass

    def itemChanged(self, item):
        """Called after an item has been added or edited.

        Re-implement to do something at this moment if needed, e.g. alter the
        text or display of other items.
        """
        pass

    def setValue(self, strings):
        """Sets the listbox to a list of strings."""
        self.listBox.clear()
        self.listBox.addItems(strings)
        self.changed.emit()

    def value(self):
        """Returns the list of paths in the listbox."""
        return [self.listBox.item(i).text()
            for i in range(self.listBox.count())]

    def setItems(self, items):
        """Sets the listbox to a list of items."""
        self.listBox.clear()
        for item in items:
            self.listBox.addItem(item)
            self.itemChanged(item)
        self.changed.emit()

    def items(self):
        """Returns the list of items in the listbox."""
        return [self.listBox.item(i)
            for i in range(self.listBox.count())]

    def clear(self):
        """Clears the listbox."""
        self.listBox.clear()
        self.changed.emit()


class FilePathEdit(ListEdit):
    """
    A widget to edit a list of directories (e.g. a file path).
    """
    def __init__(self, *args, **kwargs):
        super(FilePathEdit, self).__init__(*args, **kwargs)

    def fileDialog(self):
        """The QFileDialog this widget is using."""
        try:
            return self._filedialog
        except AttributeError:
            self._filedialog = d = QFileDialog(self)
            d.setFileMode(QFileDialog.Directory)
            return d

    def openEditor(self, item):
        """Asks the user for an (existing) directory."""
        directory = item.text()
        dlg = self.fileDialog()
        dlg.selectFile(directory)
        if dlg.exec_():
            item.setText(dlg.selectedFiles()[0])
            return True
        return False

    def setFileMode(self, mode):
        modes = {
            'directory': QFileDialog.Directory,
            QFileDialog.Directory: QFileDialog.Directory,
            'file': QFileDialog.ExistingFile,
            QFileDialog.ExistingFile: QFileDialog.ExistingFile,
            'anyfile': QFileDialog.AnyFile,
            QFileDialog.AnyFile: QFileDialog.AnyFile
        }
        self.fileDialog().setFileMode(modes[mode])
