import sys
from PyQt4 import QtGui, Qt
from audio_folder import AudioFolder
from meta_modifier import MetaDataModifier


class Gui(QtGui.QWidget):

    def __init__(self):
        super(Gui, self).__init__()

        self.init_ui()
        self.file_path = None
        self.add_track_number = True
        self.cleanup_title = True
        self.ai_metadata = False

    def init_ui(self):
        self.setGeometry(300, 300, 800, 500)
        self.setWindowTitle('Auto Metadata Modifier')
        self.setWindowIcon(QtGui.QIcon('gui_resources/icon1.png'))

        self.chooseBtn = QtGui.QPushButton('Choose Folder', self)
        self.chooseBtn.move(300, 20)
        self.chooseBtn.clicked.connect(self.show_dialog)

        self.goBtn = QtGui.QPushButton('Go!', self)
        self.goBtn.move(350, 400)
        self.goBtn.clicked.connect(self.edit_meta_data)

        self.filePathLabel = QtGui.QLabel(self)
        self.filePathLabel.move(100, 80)
        self.filePathLabel.setText("Click Choose Folder to select songs to edit.")
        self.filePathLabel.setStyleSheet("QLabel {font: 18pt}")
        self.filePathLabel.setAlignment(Qt.Qt.AlignCenter)

        checkBoxAddTrackNumber = QtGui.QCheckBox('Add track number', self)
        checkBoxAddTrackNumber.move(100, 200)
        checkBoxAddTrackNumber.toggle()
        checkBoxAddTrackNumber.stateChanged.connect(self.change_add_track_number_state)

        checkCleanupTitle = QtGui.QCheckBox('Clean up title', self)
        checkCleanupTitle.move(100, 250)
        checkCleanupTitle.toggle()
        checkCleanupTitle.stateChanged.connect(self.change_cleanup_title_state)

        checkCleanupTitle = QtGui.QCheckBox('Search for file metadata intelligently', self)
        checkCleanupTitle.move(100, 300)
        checkCleanupTitle.stateChanged.connect(self.change_ai_metadata_state)

        self.setStyleSheet("QWidget {font: 24pt}")

        self.show()

    def show_dialog(self):
        # Get filename using QFileDialog
        self.file_path = QtGui.QFileDialog.getExistingDirectory(self, 'Open File', '/')
        if self.file_path:
            self.filePathLabel.setText("Selected folder: " + str(MetaDataModifier.extract_filename(self.file_path)))

    def edit_meta_data(self):
        audio_folder = AudioFolder(self.file_path)
        path_list = audio_folder.get_file_paths()

        for path in path_list:
            MetaDataModifier(path).set_meta_data(self.add_track_number, self.cleanup_title)

        self.filePathLabel.setText("Processed " + str(len(path_list)) + " files")

    def change_add_track_number_state(self):
        if self.add_track_number:
            self.add_track_number = False
        else:
            self.add_track_number = True

    def change_cleanup_title_state(self):
        if self.add_track_number:
            self.add_track_number = False
        else:
            self.add_track_number = True

    def change_ai_metadata_state(self):
        if self.add_track_number:
            self.add_track_number = False
        else:
            self.add_track_number = True

def run_gui():
    app = QtGui.QApplication(sys.argv)
    ex = Gui()
    sys.exit(app.exec_())
