import math
import sys
import os
import dcs
import RotorOpsMission as ROps
import RotorOpsUtils


from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox
)
from PyQt5 import QtGui
from MissionGeneratorUI import Ui_MainWindow

scenarios = []
red_forces_files = []
blue_forces_files = []

class Window(QMainWindow, Ui_MainWindow):


    def __init__(self, parent=None):
        super().__init__(parent)
        self.m = ROps.RotorOpsMission()
        self.setupUi(self)
        self.connectSignalsSlots()
        self.populateScenarios()
        self.populateForces("red", self.redforces_comboBox, red_forces_files)
        self.populateForces("blue", self.blueforces_comboBox, blue_forces_files)
        self.populateSlotSelection()

        self.background_label.setPixmap(QtGui.QPixmap(self.m.assets_dir + "/background.PNG"))
        self.statusbar.setStyleSheet(
            "QStatusBar{padding-left:5px;color:black;font-weight:bold;}")


    def connectSignalsSlots(self):
        # self.action_Exit.triggered.connect(self.close)
        # self.action_Find_Replace.triggered.connect(self.findAndReplace)
        # self.action_About.triggered.connect(self.about)
        self.action_generateMission.triggered.connect(self.generateMissionAction)
        self.action_scenarioSelected.triggered.connect(self.scenarioChanged)

    def populateScenarios(self):
        os.chdir(self.m.scenarios_dir)
        path = os.getcwd()
        dir_list = os.listdir(path)
        print("Looking for mission files in '", path, "' :")

        for filename in dir_list:
            if filename.endswith(".miz"):
                scenarios.append(filename)
                self.scenario_comboBox.addItem(filename.removesuffix('.miz'))

    def populateForces(self, side, combobox, files_list):
        os.chdir(self.m.home_dir)
        os.chdir(self.m.forces_dir + "/" + side)
        path = os.getcwd()
        dir_list = os.listdir(path)
        print("Looking for " + side + " Forces files in '", os.getcwd(), "' :")

        for filename in dir_list:
            if filename.endswith(".miz"):
                files_list.append(filename)
                combobox.addItem(filename.removesuffix('.miz'))

    def populateSlotSelection(self):
        for type in ROps.RotorOpsMission.client_helos:
            self.slot_template_comboBox.addItem(type.id)


    def scenarioChanged(self):
        try:
            os.chdir(self.m.scenarios_dir)
            filename = scenarios[self.scenario_comboBox.currentIndex()]
            source_mission = dcs.mission.Mission()
            source_mission.load_file(filename)
            zones = source_mission.triggers.zones()
            conflict_zones = 0
            staging_zones = 0
            conflict_zone_size_sum = 0
            conflict_zone_distance_sum = 0
            spawn_zones = 0
            conflict_zone_positions = []
            for zone in zones:
                if zone.name == "STAGING":
                    staging_zones += 1
                if zone.name == "ALPHA" or zone.name == "BRAVO" or zone.name == "CHARLIE" or zone.name == "DELTA":
                    conflict_zones += 1
                    conflict_zone_size_sum += zone.radius
                    conflict_zone_positions.append(zone.position)
                if zone.name.rfind("_SPAWN") > 0:
                    spawn_zones += 1
            if conflict_zones > 1:
                for index, position in enumerate(conflict_zone_positions):
                    if index > 0:
                        conflict_zone_distance_sum += RotorOpsUtils.getDistance(conflict_zone_positions[index], conflict_zone_positions[index - 1])

            if conflict_zones and staging_zones :
                average_zone_size = conflict_zone_size_sum / conflict_zones
                self.description_textBrowser.setText(
                    "Map: " + source_mission.terrain.name + "\n" +
                    "Conflict Zones: " + str(conflict_zones) + "\n" +
                    "Average Zone Size " + str(math.floor(average_zone_size)) + "m \n" +
                    "Infantry Spawn Zones: " + str(spawn_zones) + "\n" +
                    "Approx Distance: " + str(math.floor(RotorOpsUtils.convertMeterToNM(conflict_zone_distance_sum))) + "nm \n"
                )
        except:
            self.description_textBrowser.setText("File error occured.")


    def generateMissionAction(self):
        red_forces_filename = red_forces_files[self.redforces_comboBox.currentIndex()]
        blue_forces_filename = blue_forces_files[self.blueforces_comboBox.currentIndex()]
        scenario_filename = scenarios[self.scenario_comboBox.currentIndex()]
        data = {
                "scenario_filename": scenario_filename,
                "red_forces_filename": red_forces_filename,
                "blue_forces_filename": blue_forces_filename,
                "red_quantity": self.redqty_spinBox.value(),
                "blue_quantity": self.blueqty_spinBox.value(),
                "inf_spawn_qty": self.inf_spawn_spinBox.value(),
                "apc_spawns_inf": self.apcs_spawn_checkBox.isChecked(),
                "e_transport": self.enemy_transport_checkBox.isChecked(),
                "e_attack_helos": self.enemy_attack_helos_checkBox.isChecked(),
                "e_fighters": self.enemy_fighters_checkBox.isChecked(),
                "e_attack_planes": self.enemy_attack_planes_checkBox.isChecked(),
                "crates": self.logistics_crates_checkBox.isChecked(),
                "f_awacs": self.awacs_checkBox.isChecked(),
                "f_tankers": self.tankers_checkBox.isChecked(),
                "smoke_zone": self.smoke_checkBox.isChecked(),
                "voiceovers": self.voiceovers_checkBox.isChecked(),
                "force_offroad": self.force_offroad_checkBox.isChecked(),
                "game_display": self.game_status_checkBox.isChecked(),
                "defense": self.defense_checkBox.isChecked(),
                }
        #n = ROps.RotorOpsMission()
        #result = n.generateMission(data)
        print("Generating mission with options:")
        print(str(data))
        result = self.m.generateMission(data)
        if result["success"]:
            print(result["filename"] + "'  successfully generated in " + result["directory"])
            self.statusbar.showMessage(result["filename"] + "'  successfully generated in " + result["directory"], 10000)
        msg = QMessageBox()
        msg.setWindowTitle("Mission Generated")
        msg.setText("Awesome, your mission is ready! It's located in this directory: \n" +
                    self.m.output_dir + "\n" +
                    "\n" +
                    "Next, you should use the DCS Mission Editor to fine tune unit placements.  Don't be afraid to edit the missions that this generator produces. \n" +
                    "\n" +
                    "There are no hidden script changes, everything is visible in the ME.  Triggers have been created to help you to add your own actions based on active zone and game status. \n" +
                    "\n" +
                    "Units can be changed or moved without issue.  Player slots can be changed or moved without issue. \n" +
                    "\n" +
                    "Don't forget, you can also create your own templates that can include any mission options, objects, or even scripts. \n" +
                    "\n" +
                    "Have fun! \n"
                    )
        x = msg.exec_()  # this will show our messagebox


    # def findAndReplace(self):
    #     dialog = FindReplaceDialog(self)
    #     dialog.exec()
    #
    # def about(self):
    #     QMessageBox.about(
    #         self,
    #         "About Sample Editor",
    #         "<p>A sample text editor app built with:</p>"
    #         "<p>- PyQt</p>"
    #         "<p>- Qt Designer</p>"
    #         "<p>- Python</p>",
    #     )

# class FindReplaceDialog(QDialog):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         loadUi("ui/find_replace.ui", self)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())



