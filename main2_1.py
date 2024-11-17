
import PyQt5.QtCore
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.uic as uic
import json
import clr
import sys
import os
from typing import List, Dict
from slpp import slpp as lua
from System import DBNull


#Defining global Variables
title_List = []
stars_List = []
productType_List = []
rating_List = []
genres_List = []
availibleKeys = []

titleIndx = 0
addNewFlag = False
firstBootFlag = 0

json_config = "app.config"
json_config_data =[]
vistaDB_DLL = ""
redboxDLL = ""
prof_file_path = ""
inv_file_path = ""
cover_directory = ""
image_file = ""
db_file = ""
start_SN = 0
end_SN = 0

#Defining a add New Template
product_Template = {
    "product_id": 20000,
    "stars": 1,
    "running_time": "4:20",
    "starring": {"JandaJanda", "Mordanthanus", "Viper33802"},
    "product_type_id": 1,
    "rating_id": 19,
    "long_name": "Redbox Tinkering",
    "sort_name": "Redbox Tinkering",
    "image_file": "rbtinker_title_logo.jpg",
    "description": (
        "In a world where DVDs once ruled the night, a group of tech enthusiasts and nostalgic movie buffs "
        "join forces to unravel the mysteries behind Redbox kiosks. Our mission? To decode the hardware secrets "
        "and crack the software enigmas that made these scarlet sentinels of cinema tick!\n\n"
        "Rating Pending for having fun."
    ),
    "genres": {1014: True, 1093: True},
    "release_date": "20241001000000",
    "sell_thru": True,
    "sell_thru_new": False,
    "box_office_gross": 1,
    "directors": set(),
    "coming_soon_days": 14,
    "sort_date": "20240702055300",
    "national_street_date": "20241001000000",
    "closed_captioned": False,
    "merchandise_date": "20241001000000",
    "sellthru_price": 1.00,
    "redbox_plus_eligible_date": "20241001000000",
    "studio": "Hacked"
}


# Attempt to open the JSON file and load data
with open("app.config", "r") as file:
    data = json.load(file)
                
json_config_data = data
# Access specific values from the JSON data
print("pre get data")
vistaDB_DLL = data.get("vistaDB_DLL", "")
redboxDLL = data.get("redboxDLL", "")




class NameListEditor(qtw.QWidget):
    def __init__(self, list):
        super().__init__()

        # If no list is passed, initialize as an empty list
        self.name_list = list if list else []

        self.setWindowTitle("Star Editor")
        self.resize(300, 400)

        # Set up main layout
        layout = qtw.QVBoxLayout()

        # Create QLineEdit for entering names
        self.name_input = qtw.QLineEdit(self)
        self.name_input.setPlaceholderText("Enter name")
        layout.addWidget(self.name_input)

        # Create Add button
        self.add_button = qtw.QPushButton("Add", self)
        self.add_button.clicked.connect(self.add_name)
        layout.addWidget(self.add_button)

        # Create QListView to display names
        self.list_view = qtw.QListView(self)
        self.list_model = qtc.QStringListModel()
        self.list_view.setModel(self.list_model)
        layout.addWidget(self.list_view)

        # Create Delete button
        self.delete_button = qtw.QPushButton("Delete", self)
        self.delete_button.clicked.connect(self.delete_name)
        layout.addWidget(self.delete_button)

        # Create Save button
        self.save_button = qtw.QPushButton("Save", self)
        self.save_button.clicked.connect(self.save)
        layout.addWidget(self.save_button)

        # Set up the central widget
        self.setLayout(layout)

        # Initialize the list view with the passed list
        print("list: ", self.name_list)
        self.update_list_view()


    def update_list_view(self):
        self.list_model.setStringList(self.name_list)

    def add_name(self):
        """Add the text from QLineEdit to the list view."""
        name = self.name_input.text().strip()
        if name:  # Ensure it's not empty
            current_list = self.list_model.stringList()
            current_list.append(name)
            self.list_model.setStringList(current_list)
            self.name_input.clear()
        else:
            qtw.QMessageBox.warning(self, "Input Error", "Please enter a name.")

    def delete_name(self):
        """Delete the selected name from the list view."""
        selected_index = self.list_view.selectedIndexes()
        if selected_index:
            selected_index = selected_index[0]
            name_to_delete = selected_index.data()
            current_list = self.list_model.stringList()
            current_list.remove(name_to_delete)
            self.list_model.setStringList(current_list)
        else:
            qtw.QMessageBox.warning(self, "Selection Error", "Please select a name to delete.")

    def save(self):
        global stars_List
        stars_List = self.list_model.stringList()
        print("new star list: ", stars_List)
        self.close()

class ConfigEditor(qtw.QWidget):
    def __init__(self, json_path):
        super().__init__()
        self.json_path = json_path
        self.config_data = {}
        
        # Load initial data from JSON
        self.load_config()

        # Set up main window
        self.setWindowTitle("Configuration Editor")
        self.resize(700, 700)
        
        # Create main layout
        layout = qtw.QVBoxLayout()
        
        # Create table widget
        self.table = qtw.QTableWidget(self)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Name", "Value"])
        self.table.setRowCount(len(self.config_data))
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 450)
        self.populate_table()
        layout.addWidget(self.table)
        
        # Create OK button
        self.ok_button = qtw.QPushButton("OK", self)
        self.ok_button.clicked.connect(self.save_config)
        layout.addWidget(self.ok_button)
        
        self.setLayout(layout)

    def load_config(self):
        """Load configuration data from JSON file."""
        try:
            with open(self.json_path, 'r') as f:
                self.config_data = json.load(f)
        except Exception as e:
            qtw.QMessageBox.critical(self, "Error", f"Failed to load config: {e}")
            self.config_data = {}

    def populate_table(self):
        """Populate the table with the configuration data."""
        for row, (key, value) in enumerate(self.config_data.items()):
            self.table.setItem(row, 0, qtw.QTableWidgetItem(key))
            value_item = qtw.QTableWidgetItem(str(value))
            value_item.setFlags(qtc.Qt.ItemIsSelectable | qtc.Qt.ItemIsEnabled | qtc.Qt.ItemIsEditable)
            self.table.setItem(row, 1, value_item)

    def save_config(self):
        """Save updated configuration data to JSON file."""
        # Update config_data with edited values
        for row in range(self.table.rowCount()):
            key = self.table.item(row, 0).text()
            value = self.table.item(row, 1).text()
            try:
                # Attempt to convert to number if possible
                if value.isdigit():
                    value = int(value)
                elif '.' in value:
                    value = float(value)
            except ValueError:
                pass  # Leave as string if conversion fails
            self.config_data[key] = value
        
        # Write updated data back to JSON
        try:
            with open(self.json_path, 'w') as f:
                json.dump(self.config_data, f, indent=4)
            qtw.QMessageBox.information(self, "Success", "Configuration saved successfully.")
            self.close()
        except Exception as e:
            qtw.QMessageBox.critical(self, "Error", f"Failed to save config: {e}")

class SearchWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set up layout
        layout = qtw.QVBoxLayout()

        # Create line edit for input
        self.input_line = qtw.QLineEdit(self)
        self.input_line.setPlaceholderText("Enter a Disk SN")

        # Create search button
        self.search_button = qtw.QPushButton("Search", self)
        self.search_button.clicked.connect(self.search)

        # Create text edit to display results
        self.result_text = qtw.QTextEdit(self)
        self.result_text.setReadOnly(True)  # Make the result box read-only

        # Add widgets to the layout
        layout.addWidget(self.input_line)
        layout.addWidget(self.search_button)
        layout.addWidget(self.result_text)

        # Set the layout for the main widget
        self.setLayout(layout)
        self.setWindowTitle("Search by Disk SN")
        self.setGeometry(300, 300, 400, 300)

    def search(self):
        # Get the text from the input line
        search_input = self.input_line.text()

        connection = Archive(inv_file_path, True)
        inventory = connection.Find(str(search_input))
        print("Checking SN: ", search_input)
        try:
            value = inventory.get_TitleId()
            print("Title ID: ", value)
        except AttributeError:
            print("SN does not exist in the Database")
            connection.Dispose()
        connection.Dispose()

        getQuery = "SELECT * FROM ProductCatalog WHERE [Key] = " + str(value)

        try:
            connection_string = f"Data Source={prof_file_path}"
            connection = VistaDBConnection(connection_string)
            # Open the database connection
            connection.Open()
            command = connection.CreateCommand()
            command.CommandText = getQuery
        
            # Execute the query and read the results
            reader = command.ExecuteReader()
        
            # Read each row in the result and convert to JSON and append to a list
            while reader.Read():
                # Fetch the value of the 'Value' column
                value_string = str(reader["Value"])
                #decode LUA to JSON
                value_str_json = lua.decode(value_string)
    
        except Exception as e:
            # Print any errors that occur
            print(f"Error: {e}")
    
        finally:
            # Clean up resources
            if reader:
                reader.Close()
            if connection.State == 'Open':
                connection.Close()

        # Display result in the text edit
        self.result_text.setText(value_string)

class setupDialog(qtw.QWidget):
    def __init__(self):
        super(setupDialog, self).__init__()
        uic.loadUi('setupDialog.ui', self)

        #ASSIGN BUTTONS TO OBJECTS
        self.selectProf = self.findChild(qtw.QPushButton, 'selectProf') # Find the button
        self.selectInv = self.findChild(qtw.QPushButton, 'selectInv') # Find the button
        self.selectCover = self.findChild(qtw.QPushButton, 'selectCoverDirect') # Find the button
        self.save = self.findChild(qtw.QPushButton, 'done') # Find the button

        #INSERT HANDLERS FOR BUTTONS
        self.selectProf.clicked.connect(lambda: self.open_file_dialog('profileFileLocation','Select the profile data file'))
        self.selectInv.clicked.connect(lambda: self.open_file_dialog('inventoryFileLocation','Select the inventory data file'))
        self.selectCover.clicked.connect(lambda: self.open_directory_dialog('movieCoverDirectLocation','Select the new movie cover directory'))
        self.save.clicked.connect(self.saveSettings)

        #ASSIGN LINE EDITS TO OBJECTS
        self.ProfFile = self.findChild(qtw.QLineEdit, 'profLoc') 
        self.InvFile = self.findChild(qtw.QLineEdit, 'invLoc') 
        self.coverDir = self.findChild(qtw.QLineEdit, 'coverLoc') 


    def open_file_dialog(self, jsonLocation: str, fileSelectionMsg: str):
        # Open a file dialog with a filter for .data files
        options = qtw.QFileDialog.Options()
        file_path, _ = qtw.QFileDialog.getOpenFileName(
            self,
            fileSelectionMsg,
            "",
            "Data Files (*.data);;All Files (*)",
            options=options
        )
        
        # If a file was selected, display its path in the textbox
        if file_path:
            if jsonLocation == 'profileFileLocation':
                self.ProfFile.setText(file_path)
                self.write_to_json(jsonLocation, file_path)

            if jsonLocation == 'inventoryFileLocation':
                self.InvFile.setText(file_path)
                inv_file_path = file_path
                self.write_to_json(jsonLocation, file_path)

    def open_directory_dialog(self, jsonLocation: str, SelectionMsg: str):
        """
        Opens a directory select dialog with specified JSON variable and dialog title text.

        Parameters:
        json_var (str): The JSON variable name or value to be used in the function.
        dialog_title (str): The title text for the dialog window.

        Returns:
        str: The selected directory path, or None if no selection was made.
        """
        # Open a QFileDialog for selecting a directory
        directory = qtw.QFileDialog.getExistingDirectory(
            None,          # No parent widget
            SelectionMsg  # Title of the dialog window
        )

        directory = directory + "/"
        self.coverDir.setText(directory)
        self.write_to_json(jsonLocation, directory)

    def write_to_json(self, variable_name, value):
        # Load the existing data
        try:
            with open("app.config", "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # Start with an empty dictionary if the file doesn't exist or is corrupted
            data = {}

        # Update or add the specified variable
        data[variable_name] = value

        # Write the updated data back to the JSON file
        with open("app.config", "w") as file:
            json.dump(data, file, indent=4)

    def saveSettings(self):

        #SETUP TEMP STORAGE VARIABLES
        profFile = ""
        invFile = ""
        coverDir = ""

        #GET VALUES
        profFile = self.ProfFile.text()
        invFile = self.InvFile.text()
        coverDir = self.coverDir.text()

        print("Profile: ", profFile)
        print("Inv: ", invFile)
        print("Cover: ", coverDir)

        if profFile and invFile and coverDir:
            self.write_to_json("firstBoot", 0)
            with open(profFile, 'rb') as fsrc, open(profFile+'.bak', 'wb') as fdst:
                # Read the source file and write to the destination
                while chunk := fsrc.read(1024):  # Read 1024 bytes at a time
                    fdst.write(chunk)

            with open(invFile, 'rb') as fsrc, open(invFile+'.bak', 'wb') as fdst:
                # Read the source file and write to the destination
                while chunk := fsrc.read(1024):  # Read 1024 bytes at a time
                    fdst.write(chunk)
            Ui.show_message_box(Ui, "Setting Saved! Restart the application to load the main window.")
            sys.exit()
        else:
            Ui.show_message_box(Ui, "Please fill in all the required boxes")


class ContentTypeDialog(qtw.QDialog):
    def __init__(self):
        super().__init__()

        self.selection = 0

        # Set up the dialog window
        self.setWindowTitle("Select Content Type")
        self.setGeometry(100, 100, 300, 150)
        self.center()

        # Create layout
        layout = qtw.QVBoxLayout()

        # Add label with message
        label = qtw.QLabel("Select the content type to add.")
        layout.addWidget(label)

        # Add buttons for DVD, Blu-Ray, and 4K
        dvd_button = qtw.QPushButton("DVD")
        blu_ray_button = qtw.QPushButton("Blu-Ray")
        k4_button = qtw.QPushButton("4K")

        # Connect buttons to methods
        dvd_button.clicked.connect(self.handle_dvd)
        blu_ray_button.clicked.connect(self.handle_blu_ray)
        k4_button.clicked.connect(self.handle_4k)

        # Add buttons to layout
        layout.addWidget(dvd_button)
        layout.addWidget(blu_ray_button)
        layout.addWidget(k4_button)

        # Set dialog layout
        self.setLayout(layout)

    # Define actions for each button
    def handle_dvd(self):
        self.selection = 1
        self.accept()  # Close the dialog after selection

    def handle_blu_ray(self):
        self.selection = 2
        self.accept()  # Close the dialog after selection

    def handle_4k(self):
        self.selection = 3
        self.accept()  # Close the dialog after selection

    def center(self):
        """Center the window on the screen."""
        # Get the screen's rectangle
        screen_rect = qtw.QDesktopWidget().availableGeometry()
        # Get the rectangle of the dialog itself
        window_rect = self.frameGeometry()
        # Calculate the center point of the screen
        center_point = screen_rect.center()
        # Move the window to the center
        window_rect.moveCenter(center_point)
        # Apply the calculated geometry to the window
        self.move(window_rect.topLeft())


class Ui(qtw.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('mainV1_2.ui', self)

        #ASSIGN BUTTONS TO OBJECTS
        self.addToInvButton = self.findChild(qtw.QPushButton, 'addToInventory') # Find the button
        self.searchTitleBtn = self.findChild(qtw.QPushButton, 'searchLongNameBtn') # Find the button
        self.saveBtn = self.findChild(qtw.QPushButton, 'saveBtn') # Find the button
        self.addNew = self.findChild(qtw.QPushButton, 'addNew') # Find the button
        self.resetBtn = self.findChild(qtw.QPushButton, 'resetBtn') # Find the button
        self.starBtn = self.findChild(qtw.QPushButton, 'addStar') # Find the button
        self.loadCover = self.findChild(qtw.QPushButton, 'loadImgBtn') # Find the button
        self.viewDiskSN = self.findChild(qtw.QPushButton, 'viewDiskSN') # Find the button
        self.genLabel = self.findChild(qtw.QPushButton, 'generateLabelsBtn') # Find the button
        self.printPrevLabel = self.findChild(qtw.QPushButton, 'printPreviewBtn') # Find the button
        self.printLabel = self.findChild(qtw.QPushButton, 'printLabelBtn') # Find the button

        #INSERT HANDLERS FOR BUTTONS
        self.loadCover.clicked.connect(lambda: self.open_image_file_dialog('Select the new movie cover image'))
        self.addToInvButton.clicked.connect(self.add_to_inv)
        self.searchTitleBtn.clicked.connect(self.searchTitle)
        self.saveBtn.clicked.connect(self.saveProfile)
        self.resetBtn.clicked.connect(self.resetInputs)
        self.viewDiskSN.clicked.connect(self.getSNList)
        self.starBtn.clicked.connect(self.configNameListEditor)
        self.addNew.clicked.connect(self.on_add_new)
        self.genLabel.clicked.connect(lambda: self.show_message_box("Feature Coming Soon!"))
        self.printPrevLabel.clicked.connect(lambda: self.show_message_box("Feature Coming Soon!"))
        self.printLabel.clicked.connect(lambda: self.show_message_box("Feature Coming Soon!"))
        

        #ASSIGN LINE EDITS TO OBJECTS
        self.nextSNTextBox = self.findChild(qtw.QLineEdit, 'nextSNDisplay')
        self.titleTextBox = self.findChild(qtw.QLineEdit, 'ProductID')
        self.productIDdb = self.findChild(qtw.QLineEdit, 'productIDdb')
        self.runTime = self.findChild(qtw.QLineEdit, 'runTime')
        self.studio = self.findChild(qtw.QLineEdit, 'studio')
        self.sortName = self.findChild(qtw.QLineEdit, 'sortName')
        self.longNameTextBox = self.findChild(qtw.QLineEdit, 'longName')

        #ASSIGN COMBO BOX TO OBJECTS
        self.productType = self.findChild(qtw.QComboBox, 'typeComboBox')
        self.ratingID = self.findChild(qtw.QComboBox, 'ratingComboBox')
        self.genres = self.findChild(qtw.QComboBox, 'genresComboBox')

        #ASSIGN SPIN BOX TO OBJECTS
        self.addQTYBox = self.findChild(qtw.QSpinBox, 'addQTY')
        
        #ASSIGN TEXT EDITS TO OBJECTS
        self.descriptiondb = self.findChild(qtw.QTextEdit, 'description')

        #ASSIGN LIST TO OBJECTS
        self.profileList = self.findChild(qtw.QListWidget, 'profileList')

        #INSERT HANDLERS FOR LISTS
        self.profileList.itemClicked.connect(self.on_item_selected)

        #ASSIGN LABELS TO OBJECTS
        self.coverImage = self.findChild(qtw.QLabel, 'coverImage')

        #INSERT HANDLERS FOR RETURNS
        self.longNameTextBox.returnPressed.connect(self.searchTitle)

        #APPLY PROPERTIES TO OBJECTS
        self.longNameTextBox.setFocus()
        self.titleTextBox.setValidator(qtg.QIntValidator())
        self.titleTextBox.setMaxLength(9)

        #ASSIGN ACTIONS TO OBJECTS
        self.configBTN = self.findChild(qtw.QAction, 'actionConfig')
        self.exit = self.findChild(qtw.QAction, 'actionExit')
        self.githubLink = self.findChild(qtw.QAction, 'actionGithub')
        self.insertDiskSN = self.findChild(qtw.QAction, 'actionInsert_Disk_SN')
        self.searchDiskSN = self.findChild(qtw.QAction, 'actionSearch_By_Disk_SN')
        self.about = self.findChild(qtw.QAction, 'actionAbout')

        #INSERT HANDLERS FOR TRIGGERED ACTIONS
        self.ConfigEditor = ConfigEditor(json_config)
        self.configBTN.triggered.connect(self.ConfigEditor.show)
        self.exit.triggered.connect(self.close)
        self.insertDiskSN.triggered.connect(lambda: self.show_message_box("Feature Coming Soon!"))
        self.githubLink.triggered.connect(lambda: self.show_message_box("Feature Coming Soon!"))
        self.about.triggered.connect(lambda: self.show_message_box("Feature Coming Soon!"))
        self.searchDiskSNWindow = SearchWindow()
        self.searchDiskSN.triggered.connect(self.searchDiskSNWindow.show)

        self.selectType = ContentTypeDialog()


        #INSERT HANDLERS
        self.on_startup()
        
    def on_startup(self):
        self.start_long_task()
        self.load_json_data()

        current_directory = os.getcwd()
        current_directory = current_directory.replace('\\', '/')
        print("Direct: ", current_directory)

        try:
            global Archive
            clr.AddReference(current_directory+redboxDLL)
            from Redbox.ProductLookupCatalog import Archive
        
        except:
            self.show_message_box("Error Loading Redbox Product Lookup Catalog DLL")
            sys.exit()

        try:
            global VistaDBConnection
            # Load the VistaDB DLL
            clr.AddReference(current_directory+vistaDB_DLL)

            # Import the VistaDB namespaces
            from VistaDB.Provider import VistaDBConnection
        
        except:
            self.show_message_box("Error Loading VistaDB DLL")
            sys.exit()



        
        if inv_file_path != "":
            self.load_inv_data()

        self.getGenres()
        self.getRating()
        self.getProductType()
        self.progress_dialog.close()

    def resetInputs(self):
        global addNewFlag
        addNewFlag = False
        self.profileList.clear()
        self.saveBtn.setEnabled(False)
        self.loadCover.setEnabled(False)
        self.addNew.setEnabled(True)
        self.productIDdb.clear()
        self.runTime.clear()
        self.sortName.clear()
        self.studio.clear()
        self.descriptiondb.clear()
        self.coverImage.clear()
        self.coverImage.setText("Image")

        self.productType.setCurrentText("DVD")
        self.ratingID.setCurrentText("Not Rated")
        self.reset_genres()

    def configNameListEditor(self):
        global stars_List
        print("Stars: ", stars_List)
        self.NameListEditor = NameListEditor(stars_List)
        self.NameListEditor.show()

    def getSNList(self):
        snList = []
        productID = title_List[titleIndx].get("product_id")
        #self.find_bytes_in_file(inv_file_path, int(productID), 4)


    def getGenres(self):
        global genres_List
        genres_List = self.get_value("SELECT Value FROM Genres",prof_file_path, genres_List)
        genres_List_temp = genres_List
        model = qtg.QStandardItemModel(self.genres)
        for item_text in genres_List_temp:
            genres_List_temp = qtg.QStandardItem(item_text.get("genre_name"))
            genres_List_temp.setCheckable(True)  # Make item checkable
            genres_List_temp.setSelectable(False)  # Ensure the item is not selectable to focus on checkbox
            model.appendRow(genres_List_temp)
        self.genres.setModel(model)

    def getRating(self):
        global rating_List
        rating_List = []
        rating_List = self.get_value("SELECT Value FROM ProductRating",prof_file_path, rating_List)
        for item_text in rating_List:
            self.ratingID.addItem(item_text.get("name"))

    def getProductType(self):
        global productType_List
        productType_List = self.get_value("SELECT Value FROM ProductType",prof_file_path, productType_List)
        for item_text in productType_List:
            self.productType.addItem(item_text.get("product_type_name"))


    def handle_item_pressed(self, index):
        # Toggle the check state of the clicked item
        item = self.comboBox.model().itemFromIndex(index)
        if item.checkState() == qtc.Qt.Checked:
            item.setCheckState(qtc.Qt.Unchecked)
        else:
            item.setCheckState(qtc.Qt.Checked)

    def saveProfile(self):
        global addNewFlag
        index = titleIndx
        #print("unencoded: ", title_List[titleIndx])
        tempTitle = product_Template.copy()

        tempTitle["product_id"] = self.productIDdb.text()
        tempTitle["stars"] = json_config_data.get("starsDefault",1)
        tempTitle["running_time"] = self.runTime.text()
        tempTitle["long_name"] = self.longNameTextBox.text()
        tempTitle["sort_name"] = self.sortName.text()
        tempTitle["studio"] = self.studio.text()
        tempTitle["starring"] = stars_List
        tempTitle["image_file"] = image_file
        tempTitle["description"] = self.descriptiondb.toPlainText()
        tempTitle["release_date"] = json_config_data.get("release_date_Default",20241010000000)
        tempTitle["box_office_gross"] = json_config_data.get("box_office_gross_Default",0.0)
        tempTitle["coming_soon_days"] = json_config_data.get("coming_soon_days_Default",1)
        tempTitle["sort_date"] = json_config_data.get("sort_date_Default",20240702055300)
        tempTitle["national_street_date"] = json_config_data.get("national_street_date_Default",20241001000000)
        tempTitle["merchandise_date"] = json_config_data.get("merchandise_date_Default", 20241010000000)
        tempTitle["redbox_plus_eligible_date"] = json_config_data.get("redbox_plus_eligible_date_Default", 20241010000000)

        genreIDs = self.get_checked_items()
        tempTitle["genres"].clear()
        for genre_id in genreIDs:
            tempTitle["genres"][genre_id] = True

        for i in range(len(rating_List)):
            nameScan = rating_List[i].get("name")
            selectedName = self.ratingID.currentText()
            if selectedName == nameScan:
                tempTitle["rating_id"] = int(rating_List[i].get("rating_id"))
                break

        for i in range(len(productType_List)):
            nameScan = productType_List[i].get("product_type_name")
            selectedName = self.productType.currentText()
            if selectedName == nameScan:
                tempTitle["product_type_id"] = int(productType_List[i].get("product_type_id"))
                break

        part1 = str(lua.encode(tempTitle))
        part1 = part1.replace('\'', '\'\'') #Sometimes the description has a single ' and causes issues with the SQL Query so replacing with '' to fix it
        part1 = part1.replace('[\"', '') #Getting rid of brackets and quotes around variable names
        part1 = part1.replace('\"]', '') #Getting rid of brackets and quotes around variable names
        part1 = part1.replace("\n", "").replace("\r", "") #Getting rid of the new line and carriage returns
        part1 = part1.replace('\t\t', ' ') #getting rid of the double tabs and replaceing with space
        part1 = part1.replace('\t', ' ') #getting rid of the tabs and replaceing with space

        if addNewFlag == False:
            part1Q = "UPDATE ProductCatalog SET Value = \'"
            part2Q = part1
            part3Q = "\' WHERE [Key] = "
            part4Q = str(tempTitle["product_id"])
            listTest = []
            print("Query: ", part1Q+part2Q+part3Q+part4Q)
            command = part1Q+part2Q+part3Q+part4Q
        elif addNewFlag == True:
            part1Q = "INSERT INTO ProductCatalog (Key, Value) VALUES (\'"
            part2Q = str(tempTitle["product_id"])
            part3Q = "\', \'"
            part4Q = part1
            part5Q = "\')"
            listTest = []
            print("Query: ", part1Q+part2Q+part3Q+part4Q+part5Q)
            command = part1Q+part2Q+part3Q+part4Q+part5Q
            addNewFlag = False

        listTest2 = 0
        try:
            listTest2 = self.put_value(command,prof_file_path, listTest)
        except:
            #print("Profile Updating Failed. Please close the app and try again")
            #self.show_message_box("Profile Updating Failed. Please close the app and try again")
            self.show_message_box("Profile Updating Failed. Make sure the Product ID is Unique")
            sys.exit()


        self.titleTextBox.setText(self.productIDdb.text())

        if listTest2 == 1:
            self.show_message_box("Profile Updated")


        self.resetInputs()
        self.profileList.clear()



    def get_checked_items(self):
        checked_items = []
        checked_itemsID = []
        global genres_List
        # Loop through all items in the model and check their state
        for i in range(self.genres.model().rowCount()):
            item = self.genres.model().item(i)
            if item.checkState() == qtc.Qt.Checked:
                checked_items.append(item.text())
        
        # Print or return the checked items
        print("Checked items:", checked_items)
        for x in checked_items:
            for y in genres_List:
                if x == y.get("genre_name"):
                    checked_itemsID.append(y.get("genre_id"))
                    break
        print("Checked itemsID:", checked_itemsID)


        return checked_itemsID

    def reset_genres(self):
        for i in range(self.genres.model().rowCount()):
            itemg = self.genres.model().item(i)
            itemg.setCheckState(qtc.Qt.Unchecked)

    def on_item_selected(self, item):
        global genres_List
        global stars_List
        global titleIndx
        global image_file
        self.reset_genres()
        self.getRating()
        # Get the index of the selected item
        index = self.profileList.row(item)
        titleIndx = index

        self.productIDdb.setText(str(title_List[index].get("product_id")))

        stars_List = title_List[index].get("starring")
        image_file = title_List[index].get("image_file")
        print("Stars: ", stars_List)
        self.runTime.setText(str(title_List[index].get("running_time")))

        self.longName.setText(str(title_List[index].get("long_name")))
        self.sortName.setText(str(title_List[index].get("sort_name")))
        self.studio.setText(str(title_List[index].get("studio")))
        self.descriptiondb.setText(title_List[index].get("description"))
        movieCoverFile = str(title_List[index].get("image_file"))
        coverLocation = cover_directory + movieCoverFile
        print(coverLocation)
        pixmap = qtg.QPixmap(coverLocation)
        scaled_pixmap = pixmap.scaled(self.coverImage.size(), qtc.Qt.KeepAspectRatio, qtc.Qt.SmoothTransformation)
        self.coverImage.setPixmap(scaled_pixmap)


        for i in title_List[index].get("genres"):
            for j in range(self.genres.model().rowCount()):

                itemg = self.genres.model().item(j)
                item = genres_List[j].get("genre_id")
                if item == i:
                    itemg.setCheckState(qtc.Qt.Checked)
                    break
                else:
                    print("FAIL")



        print("Result: ", title_List[index])
        print("prod type: ", str(title_List[index].get("product_type_id")))
        for i in range(len(productType_List)):
            currentID = productType_List[i].get("product_type_id")
            print("prod type in list: ", currentID)
            if currentID == title_List[index].get("product_type_id"):
                self.productType.setCurrentText(productType_List[i].get("product_type_name"))
                print("prod type in list(name): ", productType_List[i].get("product_type_name"))
                break

        print("rating: ", str(title_List[index].get("rating_id")))
        for i in range(len(rating_List)):
            currentID = int(rating_List[i].get("rating_id"))
            print("rating in list: ", currentID)
            if currentID == title_List[index].get("rating_id"):
                self.ratingID.setCurrentText(rating_List[i].get("name"))
                print("rating in list(name): ", rating_List[i].get("name"))
                break

        self.saveBtn.setEnabled(True)
        self.loadCover.setEnabled(True)
        self.addNew.setEnabled(False)


    def on_add_new(self, item):
        global genres_List
        global stars_List
        global image_file
        global addNewFlag
        print("Flag coming in:", addNewFlag)
        addNewFlag = True

        self.show_message_box("Please update the Product ID with an unused value otherwise the program will be unable to insert the value. Automatic value selection is in work")

        #self.find_available_product_keys(prof_file_path)

        #self.selectType.exec_()
        #print("selection: ", self.selectType.selection)
        #if self.selectType.selection == 1:
        #    print("selection: DVD")
        #    print("Key: ", availibleKeys)
        #    self.productIDdb.setText(str())

        #elif self.selectType.selection == 2:
        #    print("selection: BR")
        #    self.productIDdb.setText(str())

        #elif self.selectType.selection == 3:
        #    print("selection: 4K")
        #    self.productIDdb.setText(str())

        #else:
        #    return

        print("product Template Curently: ", product_Template)
        self.reset_genres()
        self.getRating()

        self.productIDdb.setText(str(product_Template["product_id"]))
        stars_List = product_Template["starring"]
        image_file = product_Template["image_file"]
        print("Stars: ", stars_List)
        self.runTime.setText(str(product_Template["running_time"]))

        self.longName.setText(str(product_Template["long_name"]))
        self.sortName.setText(str(product_Template["sort_name"]))
        self.studio.setText(str(product_Template["studio"]))
        self.descriptiondb.setText(product_Template["description"])
        movieCoverFile = str(product_Template["image_file"])
        coverLocation = cover_directory + movieCoverFile
        print(coverLocation)
        pixmap = qtg.QPixmap(coverLocation)
        scaled_pixmap = pixmap.scaled(self.coverImage.size(), qtc.Qt.KeepAspectRatio, qtc.Qt.SmoothTransformation)
        self.coverImage.setPixmap(scaled_pixmap)


        for i in product_Template["starring"]:
            for j in range(self.genres.model().rowCount()):

                itemg = self.genres.model().item(j)
                item = genres_List[j].get("genre_id")
                if item == i:
                    itemg.setCheckState(qtc.Qt.Checked)
                    break
                else:
                    print("FAIL")



        #print("Result: ", product_Template["starring"])
        #print("prod type: ", str(title_List[index].get("product_type_id")))
        for i in range(len(productType_List)):
            currentID = productType_List[i].get("product_type_id")
            print("prod type in list: ", currentID)
            if currentID == product_Template["product_type_id"]:
                self.productType.setCurrentText(productType_List[i].get("product_type_name"))
                print("prod type in list(name): ", productType_List[i].get("product_type_name"))
                break

        #print("rating: ", str(title_List[index].get("rating_id")))
        for i in range(len(rating_List)):
            currentID = int(rating_List[i].get("rating_id"))
            print("rating in list: ", currentID)
            if currentID == product_Template["rating_id"]:
                self.ratingID.setCurrentText(rating_List[i].get("name"))
                print("rating in list(name): ", rating_List[i].get("name"))
                break

        self.saveBtn.setEnabled(True)
        self.loadCover.setEnabled(True)
        self.addNew.setEnabled(False)
            

    def put_value(self, query, db_file, list: list):
        try:
            connection_string = f"Data Source={db_file}"
            connection = VistaDBConnection(connection_string)
        
            # Open the database connection
            connection.Open()
            command = connection.CreateCommand()
            command.CommandText = query
        
            # Execute the query and read the results
            reader = command.ExecuteNonQuery()
            print(f"Result: {reader}")
        
    
        except Exception as e:
            # Print any errors that occur
            print(f"Error: {e}")
    
        finally:
            # Clean up resources
            if connection.State == 'Open':
                connection.Close()
        return reader

    def get_value(self, query, db_file, list: list):
        try:
            connection_string = f"Data Source={db_file}"
            connection = VistaDBConnection(connection_string)
            # Open the database connection
            connection.Open()
            command = connection.CreateCommand()
            command.CommandText = query
        
            # Execute the query and read the results
            reader = command.ExecuteReader()
        
            # Read each row in the result and convert to JSON and append to a list
            while reader.Read():
                # Fetch the value of the 'Value' column
                value_string = str(reader["Value"])
                #decode LUA to JSON
                value_str_json = lua.decode(value_string)
                #Append to List
                list.append(value_str_json)
    
        except Exception as e:
            # Print any errors that occur
            print(f"Error: {e}")
    
        finally:
            # Clean up resources
            if reader:
                reader.Close()
            if connection.State == 'Open':
                connection.Close()
        return list

    def searchTitle(self):
        self.start_long_task()
        self.resetInputs()
        global title_List
        title_List = []
        self.profileList.clear()
        titleSearchValue = self.longNameTextBox.text()
        profileDB = prof_file_path
        preQuery = "SELECT * FROM ProductCatalog WHERE LOWER(value) LIKE LOWER(\'%long_name%"
        postQuery = "%sort_name%\');"
        getQuery = preQuery + titleSearchValue + postQuery

        title_List = self.get_value(getQuery, profileDB, title_List)

        for x in title_List:
            self.profileList.addItem(x.get("long_name"))
        self.progress_dialog.close()


    def find_bytes_in_file(self, file_path, search_bytes, byteNum: int, chunk_size=4096):
        """
        Search for the first occurrence of a specific byte sequence in a large file.
    
        Parameters:
            file_path (str): Path to the file to search.
            search_bytes (bytes): Byte sequence to search for.
            chunk_size (int): Size of chunks to read at a time (default is 4096 bytes).
        
        Returns:
            int: The index position of the first occurrence of search_bytes, or -1 if not found.
        """
        # Validate that search_bytes is exactly 8 bytes
        if len(search_bytes) != byteNum:
            raise ValueError("The search bytes did not match the provided requirement.")

        # Track the current position in the file
        position = 0
    
        with open(file_path, 'rb') as file:
            while chunk := file.read(chunk_size):
                # Check if the search_bytes are in this chunk
                found_at = chunk.find(search_bytes)
                if found_at != -1:
                    # Return the exact position in the file
                    file.close()
                    return position + found_at
            
                # Update position to reflect the start of the next chunk
                position += len(chunk)
    
        # If we reach this point, the search_bytes were not found
        file.close()
        return -1
    
    def find_SN_in_file(self, file_path, search_bytes, snList: list, chunk_size=4096):
        """
        Search for the first occurrence of a specific byte sequence in a large file.
    
        Parameters:
            file_path (str): Path to the file to search.
            search_bytes (bytes): Byte sequence to search for.
            chunk_size (int): Size of chunks to read at a time (default is 4096 bytes).
        
        Returns:
            int: The index position of the first occurrence of search_bytes, or -1 if not found.
        """
        # Validate that search_bytes is exactly 8 bytes
        if len(search_bytes) != 4:
            raise ValueError("The search bytes did not match the provided requirement.")

        # Track the current position in the file
        position = 0
    
        with open(file_path, 'rb') as file:
            while chunk := file.read(chunk_size):
                # Check if the search_bytes are in this chunk
                found_at = chunk.find(search_bytes)
                if found_at != -1:
                    # Return the exact position in the file

                    return position + found_at
            
                # Update position to reflect the start of the next chunk
                position += len(chunk)
    
        # If we reach this point, the search_bytes were not found
        file.close()
        return -1
    


    def insert_bytes_in_file(self, file_path, insert_position, bytes_to_insert, chunk_size=4096):
        # Check if bytes_to_insert is exactly 18 bytes
        if len(bytes_to_insert) != 18:
            raise ValueError("The bytes to insert must be exactly 18 bytes.")
    
        temp_file_path = file_path + ".tmp"
        with open(file_path, 'rb') as original_file, open(temp_file_path, 'wb') as temp_file:
            # Step 1: Copy up to the insertion position
            current_position = 0
            while current_position < insert_position:
                # Determine how much to read in this chunk
                read_size = min(chunk_size, insert_position - current_position)
                temp_file.write(original_file.read(read_size))
                current_position += read_size

            # Step 2: Write the new bytes at the insertion position
            temp_file.write(bytes_to_insert)

            # Step 3: Copy the rest of the file after the insertion point
            while chunk := original_file.read(chunk_size):
                temp_file.write(chunk)

        # Step 4: Replace the original file with the modified one
        original_file.close()
        temp_file.close()
        os.replace(temp_file_path, file_path)  

    def start_long_task(self):
        # Create and configure the progress dialog
        self.progress_dialog = qtw.QProgressDialog("Processing...", None, 0, 0, self)
        self.progress_dialog.setWindowModality(qtc.Qt.WindowModal)
        self.progress_dialog.setCancelButton(None)
        self.progress_dialog.setWindowTitle("Please Wait")
        self.progress_dialog.setValue(50)
        # Simulate a long-running task
        self.progress_dialog.show()


    def find_index_for_entry(self,  inv_file_path: str, snValue: str):
        snValueInt = int(snValue)
        while True:
            findSN_Hex = snValueInt.to_bytes(8, 'little')
            print("Checking if this SN is availible: ", findSN_Hex.hex())
            position = self.find_bytes_in_file(inv_file_path, findSN_Hex, 8)
            if position == -1:
                x = snValueInt - 1
                findSN_Hex = x.to_bytes(8, 'little')
                position = self.find_bytes_in_file(inv_file_path, findSN_Hex, 8)
                break
            else:
                i += 1
        print("Index Position: ", position+18)
        return position+18



    def add_to_inv(self):
        self.start_long_task()
        print(inv_file_path)
        addValue = self.addQTYBox.value()
        productIDValue = self.titleTextBox.text()
        snValue = self.nextSNTextBox.text()
        if addValue and productIDValue and snValue:
            for x in range (0, addValue):
                hexLine = self.createInventoryEntry(int(snValue)+x, int(productIDValue), 0,0)
                
                insert_position = self.find_index_for_entry(inv_file_path, snValue)

                self.insert_bytes_in_file(inv_file_path, insert_position, hexLine)
        else:
            print("Missing Value(s)")

        self.load_inv_data()
        self.progress_dialog.close()
        self.show_message_box("add to inventory complete")

    

    def load_inv_data(self):
        i = start_SN
        connection = Archive(inv_file_path, True)

        while i < end_SN:
            inventory = connection.Find(str(i))
            print("Checking SN: ", i)
            try:
                value = inventory.get_TitleId()
                print("Title ID: ", value)
                i += 1
            except AttributeError:
                print("SN not yet used")
                self.nextSNTextBox.setText(str(i))
                connection.Dispose()
                break
        connection.Dispose()



    def load_json_data(self):
        global start_SN
        global end_SN
        global inv_file_path
        global prof_file_path
        global cover_directory
        global json_config_data
        global vistaDB_DLL
        global redboxDLL
        global firstBootFlag
        try:
            # Attempt to open the JSON file and load data
            with open("app.config", "r") as file:
                data = json.load(file)
                
            json_config_data = data
            # Access specific values from the JSON data
            print("pre get data")
            vistaDB_DLL = data.get("vistaDB_DLL", "")
            redboxDLL = data.get("redboxDLL", "")
            inv_file_path = data.get("inventoryFileLocation", "")
            prof_file_path = data.get("profileFileLocation", "")
            cover_directory = data.get("movieCoverDirectLocation", "")
            firstBootFlag = data.get("firstBoot", 1)
            print("post get data")
            start_SN = data.get("startSerialNumber", 0)
            end_SN = data.get("endSerialNumber", 0)
            print("File Location: ", inv_file_path)
            print("Start SN: ", start_SN)
            print("End SN : ", end_SN)
            print("JSON config Data: ", json_config_data)
            
        except (FileNotFoundError, json.JSONDecodeError):
            self.show_message_box("Error Loading JSON config file: Does app.config Exist?")
            sys.exit()

    def write_to_json(self, variable_name, value):
        # Load the existing data
        try:
            with open("app.config", "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # Start with an empty dictionary if the file doesn't exist or is corrupted
            data = {}

        # Update or add the specified variable
        data[variable_name] = value

        # Write the updated data back to the JSON file
        with open("app.config", "w") as file:
            json.dump(data, file, indent=4)

    def open_image_file_dialog(self, fileSelectionMsg: str):
        # Open a file dialog with a filter for .data files
        global image_file
        options = qtw.QFileDialog.Options()

        try:
            file_path, _ = qtw.QFileDialog.getOpenFileName(
                self,
                fileSelectionMsg,
                cover_directory,
                "jpg Image (*.jpg);;All Files (*)",
                options=options
            )
        except:
            print("Closed the file dialog")

        # If a file was selected, display its path in the textbox
        if file_path:
            file_name_only = os.path.basename(file_path)
            image_file = file_name_only
            pixmap = qtg.QPixmap(file_path)
            scaled_pixmap = pixmap.scaled(self.coverImage.size(), qtc.Qt.KeepAspectRatio, qtc.Qt.SmoothTransformation)
            self.coverImage.setPixmap(scaled_pixmap)
            return file_name_only



    def open_file_dialog(self, jsonLocation: str, fileSelectionMsg: str):
        # Open a file dialog with a filter for .data files
        options = qtw.QFileDialog.Options()
        file_path, _ = qtw.QFileDialog.getOpenFileName(
            self,
            fileSelectionMsg,
            "",
            "Data Files (*.data);;All Files (*)",
            options=options
        )
        
        # If a file was selected, display its path in the textbox
        if file_path:
            if jsonLocation == 'profileFileLocation':
                self.profileFileTextBox.setText(file_path)
                prof_file_path = file_path
                self.write_to_json(jsonLocation, file_path)

            if jsonLocation == 'inventoryFileLocation':
                self.invFileTextBox.setText(file_path)
                inv_file_path = file_path
                self.load_inv_data()
                self.write_to_json(jsonLocation, file_path)

    def open_directory_dialog(self, jsonLocation: str, SelectionMsg: str):
        """
        Opens a directory select dialog with specified JSON variable and dialog title text.

        Parameters:
        json_var (str): The JSON variable name or value to be used in the function.
        dialog_title (str): The title text for the dialog window.

        Returns:
        str: The selected directory path, or None if no selection was made.
        """
        # Open a QFileDialog for selecting a directory
        directory = qtw.QFileDialog.getExistingDirectory(
            None,          # No parent widget
            SelectionMsg  # Title of the dialog window
        )

        self.coverDirectory.setText(directory)
        cover_directory = directory
        self.write_to_json(jsonLocation, directory)
    

    def createInventoryEntry(self, newSN, titleID, statusCode, rentalCount):
        newSN_Hex = newSN.to_bytes(8, 'little')
        titleID_Hex = titleID.to_bytes(4, 'little')
        statusCode_Hex = statusCode.to_bytes(1, 'little')
        rentalCount_Hex = rentalCount.to_bytes(5, 'little')

        appInv = newSN_Hex + titleID_Hex + statusCode_Hex + rentalCount_Hex

        return appInv
    
    def find_available_product_keys(seldf, db_file ,product_group_table="ProductGroup", product_catalog_table="ProductCatalog"):
        global availibleKeys
        print("DB File: ", db_file)

        try:
            # Open the database connection
            connection_string = f"Data Source={db_file}"
            connection = VistaDBConnection(connection_string)
            connection.Open()
            print("post connection open")

            # Query used keys from ProductGroup table
            usedgroup_keys = []
            command = connection.CreateCommand()
            command.CommandText = f"SELECT [Key] FROM {product_group_table}"
            reader = command.ExecuteReader()
        
            while reader.Read():
                key = int(reader["Key"])
                if 200000 <= key <= 299999:
                    usedgroup_keys.append(key)
            reader.Close()

            # Query used keys from ProductCatalog table
            usedproduct_keys = []
            command.CommandText = f"SELECT [Key] FROM {product_catalog_table}"
            reader = command.ExecuteReader()
        
            while reader.Read():
                key_value = reader["Key"]
                # Handle null values if necessary
                if key_value != DBNull.Value:
                    usedproduct_keys.append(int(key_value))
            reader.Close()
            

            # Separate used product keys into different ranges
            usedproduct_keys_range1 = [k for k in usedproduct_keys if 300000 <= k <= 399999]
            usedproduct_keys_range2 = [k for k in usedproduct_keys if 400000 <= k <= 499999]
            usedproduct_keys_range3 = [k for k in usedproduct_keys if 900000 <= k <= 999999]
            

            # Find available keys
            for key in range(200000, 300000):
                if key not in usedgroup_keys:
                    suffix = key % 1000
                    print(key)

                    # Check if suffix exists in any product ranges
                    matching_range1 = [k for k in usedproduct_keys_range1 if k % 1000 == suffix]
                    matching_range2 = [k for k in usedproduct_keys_range2 if k % 1000 == suffix]
                    matching_range3 = [k for k in usedproduct_keys_range3 if k % 1000 == suffix]
                    

                    # If no matching keys in ranges, return the available key set
                    if not matching_range1 and not matching_range2 and not matching_range3:
                        result = {
                            "ProductGroupID": key,
                            "DVDProductID": 300000 + suffix,
                            "BRProductID": 400000 + suffix,
                            "4KProductID": 900000 + suffix,
                        }
                    availibleKeys = result
                    print(result)

            print("No available keys found.")
    
        except Exception as e:
            print(f"Error: {e}")
    
        finally:
            if connection.State == 1:  # 1 corresponds to ConnectionState.Open
                connection.Close()

    def show_message_box(self, msgString):
        # Create a message box
        msg = qtw.QMessageBox()
        msg.setIcon(qtw.QMessageBox.Information)
        msg.setText(msgString)
        msg.setWindowTitle("Information")
        msg.setStandardButtons(qtw.QMessageBox.Ok)
        msg.exec_()
    
    

app = qtw.QApplication(sys.argv)
setupDialog = setupDialog()
Ui.load_json_data(Ui)
if firstBootFlag:
    setupDialog.show()
else:
    window = Ui()
    window.show()
app.exec_()
