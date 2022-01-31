# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MissionGeneratorUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1140, 826)
        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("assets/icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setWindowOpacity(4.0)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: white;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.scenario_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.scenario_comboBox.setGeometry(QtCore.QRect(270, 40, 361, 31))
        self.scenario_comboBox.setToolTip("")
        self.scenario_comboBox.setToolTipDuration(-1)
        self.scenario_comboBox.setWhatsThis("")
        self.scenario_comboBox.setObjectName("scenario_comboBox")
        self.scenario_label = QtWidgets.QLabel(self.centralwidget)
        self.scenario_label.setGeometry(QtCore.QRect(60, 30, 181, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.scenario_label.setFont(font)
        self.scenario_label.setObjectName("scenario_label")
        self.generateButton = QtWidgets.QPushButton(self.centralwidget)
        self.generateButton.setGeometry(QtCore.QRect(940, 720, 141, 41))
        self.generateButton.setStyleSheet("background-color: white;\n"
"border-style: outset;\n"
"border-width: 2px;\n"
"border-radius: 15px;\n"
"border-color: black;\n"
"padding: 4px;")
        self.generateButton.setObjectName("generateButton")
        self.description_textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.description_textBrowser.setGeometry(QtCore.QRect(710, 20, 331, 131))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.description_textBrowser.setFont(font)
        self.description_textBrowser.setStyleSheet("border-radius: 5px; color: gray")
        self.description_textBrowser.setObjectName("description_textBrowser")
        self.blueforces_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.blueforces_comboBox.setGeometry(QtCore.QRect(790, 230, 291, 31))
        self.blueforces_comboBox.setObjectName("blueforces_comboBox")
        self.scenario_label_2 = QtWidgets.QLabel(self.centralwidget)
        self.scenario_label_2.setGeometry(QtCore.QRect(690, 180, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.scenario_label_2.setFont(font)
        self.scenario_label_2.setObjectName("scenario_label_2")
        self.scenario_label_3 = QtWidgets.QLabel(self.centralwidget)
        self.scenario_label_3.setGeometry(QtCore.QRect(60, 180, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.scenario_label_3.setFont(font)
        self.scenario_label_3.setObjectName("scenario_label_3")
        self.redforces_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.redforces_comboBox.setGeometry(QtCore.QRect(170, 230, 291, 31))
        self.redforces_comboBox.setObjectName("redforces_comboBox")
        self.background_label = QtWidgets.QLabel(self.centralwidget)
        self.background_label.setGeometry(QtCore.QRect(10, 430, 801, 371))
        self.background_label.setAutoFillBackground(False)
        self.background_label.setStyleSheet("")
        self.background_label.setText("")
        self.background_label.setPixmap(QtGui.QPixmap("assets/background.PNG"))
        self.background_label.setObjectName("background_label")
        self.scenario_hint_label = QtWidgets.QLabel(self.centralwidget)
        self.scenario_hint_label.setGeometry(QtCore.QRect(250, 80, 381, 16))
        self.scenario_hint_label.setAlignment(QtCore.Qt.AlignCenter)
        self.scenario_hint_label.setObjectName("scenario_hint_label")
        self.forces_hint_label = QtWidgets.QLabel(self.centralwidget)
        self.forces_hint_label.setGeometry(QtCore.QRect(130, 270, 381, 16))
        self.forces_hint_label.setAlignment(QtCore.Qt.AlignCenter)
        self.forces_hint_label.setObjectName("forces_hint_label")
        self.blueqty_spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.blueqty_spinBox.setGeometry(QtCore.QRect(690, 230, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.blueqty_spinBox.setFont(font)
        self.blueqty_spinBox.setMinimum(0)
        self.blueqty_spinBox.setMaximum(50)
        self.blueqty_spinBox.setProperty("value", 3)
        self.blueqty_spinBox.setObjectName("blueqty_spinBox")
        self.redqty_spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.redqty_spinBox.setGeometry(QtCore.QRect(70, 230, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.redqty_spinBox.setFont(font)
        self.redqty_spinBox.setMinimum(0)
        self.redqty_spinBox.setMaximum(50)
        self.redqty_spinBox.setProperty("value", 2)
        self.redqty_spinBox.setObjectName("redqty_spinBox")
        self.scenario_label_4 = QtWidgets.QLabel(self.centralwidget)
        self.scenario_label_4.setGeometry(QtCore.QRect(670, 260, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.scenario_label_4.setFont(font)
        self.scenario_label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.scenario_label_4.setObjectName("scenario_label_4")
        self.game_status_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.game_status_checkBox.setGeometry(QtCore.QRect(910, 510, 191, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.game_status_checkBox.setFont(font)
        self.game_status_checkBox.setChecked(True)
        self.game_status_checkBox.setTristate(False)
        self.game_status_checkBox.setObjectName("game_status_checkBox")
        self.voiceovers_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.voiceovers_checkBox.setGeometry(QtCore.QRect(910, 570, 191, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.voiceovers_checkBox.setFont(font)
        self.voiceovers_checkBox.setChecked(True)
        self.voiceovers_checkBox.setObjectName("voiceovers_checkBox")
        self.logistics_crates_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.logistics_crates_checkBox.setGeometry(QtCore.QRect(910, 320, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.logistics_crates_checkBox.setFont(font)
        self.logistics_crates_checkBox.setObjectName("logistics_crates_checkBox")
        self.awacs_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.awacs_checkBox.setGeometry(QtCore.QRect(910, 350, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.awacs_checkBox.setFont(font)
        self.awacs_checkBox.setStatusTip("")
        self.awacs_checkBox.setObjectName("awacs_checkBox")
        self.tankers_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.tankers_checkBox.setGeometry(QtCore.QRect(910, 380, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.tankers_checkBox.setFont(font)
        self.tankers_checkBox.setObjectName("tankers_checkBox")
        self.apcs_spawn_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.apcs_spawn_checkBox.setGeometry(QtCore.QRect(470, 400, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.apcs_spawn_checkBox.setFont(font)
        self.apcs_spawn_checkBox.setObjectName("apcs_spawn_checkBox")
        self.enemy_transport_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.enemy_transport_checkBox.setEnabled(False)
        self.enemy_transport_checkBox.setGeometry(QtCore.QRect(70, 320, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.enemy_transport_checkBox.setFont(font)
        self.enemy_transport_checkBox.setObjectName("enemy_transport_checkBox")
        self.enemy_attack_helos_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.enemy_attack_helos_checkBox.setEnabled(True)
        self.enemy_attack_helos_checkBox.setGeometry(QtCore.QRect(70, 350, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.enemy_attack_helos_checkBox.setFont(font)
        self.enemy_attack_helos_checkBox.setObjectName("enemy_attack_helos_checkBox")
        self.enemy_fighters_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.enemy_fighters_checkBox.setEnabled(False)
        self.enemy_fighters_checkBox.setGeometry(QtCore.QRect(70, 380, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.enemy_fighters_checkBox.setFont(font)
        self.enemy_fighters_checkBox.setObjectName("enemy_fighters_checkBox")
        self.enemy_attack_planes_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.enemy_attack_planes_checkBox.setEnabled(True)
        self.enemy_attack_planes_checkBox.setGeometry(QtCore.QRect(70, 410, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.enemy_attack_planes_checkBox.setFont(font)
        self.enemy_attack_planes_checkBox.setObjectName("enemy_attack_planes_checkBox")
        self.inf_spawn_spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.inf_spawn_spinBox.setGeometry(QtCore.QRect(680, 360, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.inf_spawn_spinBox.setFont(font)
        self.inf_spawn_spinBox.setMinimum(0)
        self.inf_spawn_spinBox.setMaximum(50)
        self.inf_spawn_spinBox.setProperty("value", 2)
        self.inf_spawn_spinBox.setObjectName("inf_spawn_spinBox")
        self.smoke_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.smoke_checkBox.setGeometry(QtCore.QRect(910, 540, 191, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.smoke_checkBox.setFont(font)
        self.smoke_checkBox.setChecked(True)
        self.smoke_checkBox.setObjectName("smoke_checkBox")
        self.scenario_label_5 = QtWidgets.QLabel(self.centralwidget)
        self.scenario_label_5.setGeometry(QtCore.QRect(50, 260, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.scenario_label_5.setFont(font)
        self.scenario_label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.scenario_label_5.setObjectName("scenario_label_5")
        self.forces_hint_label_2 = QtWidgets.QLabel(self.centralwidget)
        self.forces_hint_label_2.setGeometry(QtCore.QRect(790, 270, 311, 20))
        self.forces_hint_label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.forces_hint_label_2.setObjectName("forces_hint_label_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(470, 360, 191, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.slot_template_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.slot_template_comboBox.setGeometry(QtCore.QRect(790, 630, 291, 31))
        self.slot_template_comboBox.setObjectName("slot_template_comboBox")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(650, 630, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.scenario_label_6 = QtWidgets.QLabel(self.centralwidget)
        self.scenario_label_6.setGeometry(QtCore.QRect(470, 320, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.scenario_label_6.setFont(font)
        self.scenario_label_6.setObjectName("scenario_label_6")
        self.force_offroad_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.force_offroad_checkBox.setGeometry(QtCore.QRect(910, 480, 191, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.force_offroad_checkBox.setFont(font)
        self.force_offroad_checkBox.setChecked(False)
        self.force_offroad_checkBox.setTristate(False)
        self.force_offroad_checkBox.setObjectName("force_offroad_checkBox")
        self.defense_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.defense_checkBox.setGeometry(QtCore.QRect(60, 90, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.defense_checkBox.setFont(font)
        self.defense_checkBox.setObjectName("defense_checkBox")
        self.background_label.raise_()
        self.scenario_comboBox.raise_()
        self.scenario_label.raise_()
        self.generateButton.raise_()
        self.description_textBrowser.raise_()
        self.blueforces_comboBox.raise_()
        self.scenario_label_2.raise_()
        self.scenario_label_3.raise_()
        self.redforces_comboBox.raise_()
        self.scenario_hint_label.raise_()
        self.forces_hint_label.raise_()
        self.blueqty_spinBox.raise_()
        self.redqty_spinBox.raise_()
        self.scenario_label_4.raise_()
        self.game_status_checkBox.raise_()
        self.voiceovers_checkBox.raise_()
        self.logistics_crates_checkBox.raise_()
        self.awacs_checkBox.raise_()
        self.tankers_checkBox.raise_()
        self.apcs_spawn_checkBox.raise_()
        self.enemy_transport_checkBox.raise_()
        self.enemy_attack_helos_checkBox.raise_()
        self.enemy_fighters_checkBox.raise_()
        self.enemy_attack_planes_checkBox.raise_()
        self.inf_spawn_spinBox.raise_()
        self.smoke_checkBox.raise_()
        self.scenario_label_5.raise_()
        self.forces_hint_label_2.raise_()
        self.label.raise_()
        self.slot_template_comboBox.raise_()
        self.label_2.raise_()
        self.scenario_label_6.raise_()
        self.force_offroad_checkBox.raise_()
        self.defense_checkBox.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1140, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setAcceptDrops(False)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_generateMission = QtWidgets.QAction(MainWindow)
        self.action_generateMission.setObjectName("action_generateMission")
        self.action_scenarioSelected = QtWidgets.QAction(MainWindow)
        self.action_scenarioSelected.setObjectName("action_scenarioSelected")
        self.action_blueforcesSelected = QtWidgets.QAction(MainWindow)
        self.action_blueforcesSelected.setObjectName("action_blueforcesSelected")
        self.action_redforcesSelected = QtWidgets.QAction(MainWindow)
        self.action_redforcesSelected.setObjectName("action_redforcesSelected")

        self.retranslateUi(MainWindow)
        self.generateButton.clicked.connect(self.action_generateMission.trigger)
        self.scenario_comboBox.currentIndexChanged['int'].connect(self.action_scenarioSelected.trigger)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RotorOps Mission Generator"))
        self.scenario_comboBox.setStatusTip(_translate("MainWindow", "Tip: You can create your own templates that include mission options like kneeboards, briefings, weather, static units, triggers, scripts, etc."))
        self.scenario_label.setText(_translate("MainWindow", "Scenario Template:"))
        self.generateButton.setText(_translate("MainWindow", "Generate Mission"))
        self.description_textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Provide close air support for our convoys as we take back Las Vegas from the enemy!</span></p></body></html>"))
        self.blueforces_comboBox.setStatusTip(_translate("MainWindow", "Tip: You can create your own custom ground forces groups to be automatically generated."))
        self.scenario_label_2.setText(_translate("MainWindow", "Friendly Forces:"))
        self.scenario_label_3.setText(_translate("MainWindow", "Enemy Forces:"))
        self.redforces_comboBox.setStatusTip(_translate("MainWindow", "Tip: You can create your own custom ground forces groups to be automatically generated."))
        self.scenario_hint_label.setText(_translate("MainWindow", "Scenario templates are .miz files in \'Generator/Scenarios\'"))
        self.forces_hint_label.setText(_translate("MainWindow", "Forces templates are .miz files in \'Generator/Forces\'"))
        self.blueqty_spinBox.setStatusTip(_translate("MainWindow", "How many groups should we generate?"))
        self.redqty_spinBox.setStatusTip(_translate("MainWindow", "How many groups should we generate?"))
        self.scenario_label_4.setText(_translate("MainWindow", "Groups Per Zone"))
        self.game_status_checkBox.setStatusTip(_translate("MainWindow", "Enable an onscreen zone status display.  This helps keep focus on the active conflict zone."))
        self.game_status_checkBox.setText(_translate("MainWindow", "Game Status Display"))
        self.voiceovers_checkBox.setStatusTip(_translate("MainWindow", "Voiceovers from the ground commander. Helps keep focus on the active zone."))
        self.voiceovers_checkBox.setText(_translate("MainWindow", "Voiceovers"))
        self.logistics_crates_checkBox.setStatusTip(_translate("MainWindow", "Enable CTLD logistics crates for building ground units and air defenses."))
        self.logistics_crates_checkBox.setText(_translate("MainWindow", "Logistics Crates"))
        self.awacs_checkBox.setText(_translate("MainWindow", "Friendly AWACS"))
        self.tankers_checkBox.setText(_translate("MainWindow", "Friendly Tankers"))
        self.apcs_spawn_checkBox.setStatusTip(_translate("MainWindow", "Friendly/enemy APCs will drop infantry when reaching a new conflict zone."))
        self.apcs_spawn_checkBox.setText(_translate("MainWindow", "APCs Spawn Infantry"))
        self.enemy_transport_checkBox.setStatusTip(_translate("MainWindow", "Not yet implemented."))
        self.enemy_transport_checkBox.setText(_translate("MainWindow", "Enemy Transport Helicopters"))
        self.enemy_attack_helos_checkBox.setStatusTip(_translate("MainWindow", "Not yet implemented."))
        self.enemy_attack_helos_checkBox.setText(_translate("MainWindow", "Enemy Attack Helicopters"))
        self.enemy_fighters_checkBox.setStatusTip(_translate("MainWindow", "Not yet implemented."))
        self.enemy_fighters_checkBox.setText(_translate("MainWindow", "Enemy Fighter Planes"))
        self.enemy_attack_planes_checkBox.setStatusTip(_translate("MainWindow", "Not yet implemented."))
        self.enemy_attack_planes_checkBox.setText(_translate("MainWindow", "Enemy Ground Attack Planes"))
        self.inf_spawn_spinBox.setStatusTip(_translate("MainWindow", "This value is multiplied by the number of spawn zones in the mission template."))
        self.smoke_checkBox.setStatusTip(_translate("MainWindow", "Not yet implemented."))
        self.smoke_checkBox.setText(_translate("MainWindow", "Smoke Active Zone"))
        self.scenario_label_5.setText(_translate("MainWindow", "Groups Per Zone"))
        self.forces_hint_label_2.setText(_translate("MainWindow", "Forces templates are .miz files in \'Generator/Forces\'"))
        self.label.setText(_translate("MainWindow", "Infantry Groups per zone:"))
        self.slot_template_comboBox.setStatusTip(_translate("MainWindow", "Default player/client spawn locations at a friendly airport."))
        self.label_2.setText(_translate("MainWindow", "Player Slots"))
        self.scenario_label_6.setText(_translate("MainWindow", "Infantry Spawns:"))
        self.force_offroad_checkBox.setStatusTip(_translate("MainWindow", "May help prevent long travel times or pathfinding issues.  Tip: You can change this dynamically from mission triggers."))
        self.force_offroad_checkBox.setText(_translate("MainWindow", "Force Offroad"))
        self.defense_checkBox.setText(_translate("MainWindow", "Defensive Mode"))
        self.action_generateMission.setText(_translate("MainWindow", "_generateMission"))
        self.action_scenarioSelected.setText(_translate("MainWindow", "_scenarioSelected"))
        self.action_blueforcesSelected.setText(_translate("MainWindow", "_blueforcesSelected"))
        self.action_redforcesSelected.setText(_translate("MainWindow", "_redforcesSelected"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
