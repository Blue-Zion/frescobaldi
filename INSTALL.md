Installation instructions for Frescobaldi
=========================================

You can run Frescobaldi without installing. Just unpack and then run:

    python3 frescobaldi

See below for the required dependencies.

The Frescobaldi package is based on distutils. No build process is needed as
Frescobaldi is fully written in the interpreted Python language. To install in
the default locations:

    sudo python3 setup.py install    # install to /usr/local
    python3 setup.py install --user  # install to ~/.local

To run Frescobaldi, then simply type

    frescobaldi

If you want to install into /usr instead of /usr/local:

    sudo python3 setup.py install --prefix=/usr

If you have a Debian-based system such as Ubuntu, and you get the error
message "ImportError: No module named frescobaldi_app.main", try:

    python3 setup.py install --install-layout=deb

If you checked out Frescobaldi from Git, generate the message object files in
frescobaldi_app/i18n using:

    make -C i18n

Those message object (*.mo) files contain the translated texts in Frescobaldi's
GUI and built-in user guide.

You should also generate the desktop and AppStream metainfo files, as the
repository contains only the template without translations:

    make -C linux

The setup.cfg file contains a few default install options.
It ensures that some important files (icon, desktop, appstream, man page)
are installed in the install prefix. It also generates a file listing all
the installed files, which is useful to uninstall:

    cat installed.txt | xargs rm

See the distutils documentation for more install options.

NOTE: Since 2.18, Frescobaldi depends on the python-ly module, which needs to
      be installed separately (see below). Previously, this Python module
      (named 'ly') was part of Frescobaldi. When installing Frescobaldi, be
      sure that old remnants of previous Frescobaldi installations are removed,
      otherwise Frescobaldi will use the old 'ly' module instead, resulting in
      various error messages.


Dependencies
============

Frescobaldi is written in Python and depends on Qt >= 5.4 and PyQt >= 5.4, and
uses the python-poppler-qt5 binding to Poppler for the built-in PDF preview.

For MIDI the PortMidi library is used, either via importing 'pypm',
'pyportmidi._pyportmidi', or, if that is not available, loading the pygame.pypm
module from pygame; or, as a last resort, embedding the PortMidi C-library via
ctypes. MIDI is optional.

Required:
    Python (>= 3.8):
        http://www.python.org/
    Qt5 (>= 5.9):
        http://qt.io/
        Qt modules used by Frescobaldi:
            QtCore, QtGui, QtNetwork, QtPrintSupport, QtSvg, QtWebChannel,
            QtWebEngineWidgets, QtWidgets
    PyQt5 (>= 5.9):
        http://www.riverbankcomputing.co.uk/software/pyqt/
    python-ly (>= 0.9.5):
        https://pypi.python.org/pypi/python-ly
    Poppler (>= 0.82.0):
        http://poppler.freedesktop.org/
    python-poppler-qt5:
        https://github.com/frescobaldi/python-poppler-qt5
    qpageview:
        https://github.com/frescobaldi/qpageview

Optional but recommended:
    PortMidi: (for MIDI input and playback)
        http://portmedia.sourceforge.net/portmidi/
    pycups: (on UNIX, for printing to a local CUPS server)
        https://pypi.org/project/pycups/

Suggested:
    LilyPond:
        http://www.lilypond.org/

Of course, PyQt5, python-poppler-qt5, python-ly, and pypm or pyportmidi need
to be installed for the same Python version as Frescobaldi itself.

LilyPond is not a dependency of Frescobaldi, but of course you'll need to
install one or more versions of LilyPond to make sensible use of Frescobaldi!


"Freeze" installer
==================

The freeze.py script can create a self-contained Windows-installer, bundling all
of Python, PyQt5, popplerqt5 and pypm (from pygame) when used on MS Windows.
To use the script you need cx_Freeze and Inno Setup.


Mac OS X application bundle
===========================

The macosx/mac-app.py script can build an application bundle on Mac OS X.
To see the usage notes, run:

    python macosx/mac-app.py -h

The application bundle will be created inside a 'dist' folder in the current
working directory.
The script can build both a non-standalone system-dependent launcher and an
**almost** standalone self-contained application bundle (the script will print
instructions on the further steps needed to get a **fully** standalone
self-contained application bundle).
To use the script you need argparse (included in Python >= 2.7) and py2app.

A macosx/build-dmg.sh script is provided to build the **fully** standalone
application bundle and wrap it in a distributable DMG disk image along with
the README and COPYING files.
The script assumes a specific system configuration (for details run the script
with the '-h' option), but can be easily adapted to other configurations.


For Linux distribution packagers
================================

See the section Dependencies for the dependencies that need to be installed.
Be sure that all python packages belong to the same Python version Frescobaldi
uses.

Frescobaldi contains some files by default which are also available in other
packages often used in Linux distributions. It is possible to remove those
files after installing/packaging and make Frescobaldi depend on the package
containing those files. This makes the filesystem less cluttered, and copyright
files simpler.

Icons:
You can remove the frescobaldi_app/icons/Tango directory, and make Frescobaldi
depend on the tango-icon-theme package instead.

Hyphenation dictionaries:
You can remove the hyph_*.dic files from frescobaldi_app/hyphdicts, and make
Frescobaldi depend on a package that installs hyphenation dictionaries in
/usr/share/hyphen/ (or another dictionary listed by default in frescobaldi_app/
hyphendialog.py). Do not remove the hyphdicts directory entirely.
