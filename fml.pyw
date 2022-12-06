#!/usr/bin/python3

#Author Filip Malmberg

import keyring
import os
import pymysql
import subprocess
import sys

from datetime import datetime
from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore
from PyQt5.Qt import QApplication, QClipboard
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QColor


user = os.getlogin()
dbpw = keyring.get_password("172.28.88.47", "simdbuploader")
fspw = keyring.get_password("fs", "svc-supply-chain")

#C:\Program Files\glabels 3.99.0\bin>glabels-batch-qt.exe --printer Microsoft_Print_to_PDF --define sap=600001 C:\\Users\\filip\\Downloads\\R01.glabels

#C:\Program Files\glabels 3.99.0\bin>glabels-batch-qt.exe --output C:\\Users\\filip\\Documents\\a.pdf --define sap=600001 C:\\Users\\filip\\Downloads\\R01.glabels

#test

def sqlquery(query):
    try:
        db = pymysql.connect(host="172.28.88.47",user="simdbuploader",password=dbpw,database="simdb")
        cursor = db.cursor()
        cursor.execute(f"{query}")
    except Exception as e:
        print(e)
        warning_dialog('Unable to connect to database')
        return
    try:
        result = cursor.fetchone()[0]
    except Exception:
        result = False
    return(result)
    db.close()


def dbupload(cmd1, cmd2):
    db = pymysql.connect(host="172.28.88.47",user="simdbuploader",password=dbpw,database="simdb")
    cursor = db.cursor()
    #sql= "INSERT INTO simdb.racks (customerid, projectid, articlenumber, rackserial, routerserial, customerserialprefix, customerserial) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    #val = (serial, projectid, sap, simids['simid1'], sims['sim1'], simids['simid2'], sims['sim2'], simids['simid3'], sims['sim3'], simids['simid4'], sims['sim4'], simids['simid5'], sims['sim5'], simids['simid6'], sims['sim6'], simids['simid7'], sims['sim7'], simids['simid8'], sims['sim8'], simids['simid9'], sims['sim9'], simids['simid10'], sims['sim10'], simids['simid11'], sims['sim11'], simids['simid12'], sims['sim12'], simids['simid13'], sims['sim13'], simids['simid14'], sims['sim14'], simids['simid15'], sims['sim15'], simids['simid16'], sims['sim16'], firmwares['modemfirmware1'], firmwares['modemfirmware2'], firmwares['modemfirmware3'], firmwares['modemfirmware4'], firmwares['modemfirmware5'], firmwares['modemfirmware6'], imeis['imei1'], imeis['imei2'], imeis['imei3'], imeis['imei4'], imeis['imei5'], imeis['imei6'], modems['modem1'], modems['modem2'], modems['modem3'], modems['modem4'], modems['modem5'], modems['modem6'], wifis['wifi0'], wifis['wifi1'], mac, imp, mo)
    cursor.execute(cmd1, cmd2)
    db.commit()
    cursor.close()
    db.close()


def warning_dialog(message):
    dlg = QtWidgets.QMessageBox()
    dlg.setWindowTitle("Warning!")
    dlg.setText(message)
    dlg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    dlg.setIcon(QtWidgets.QMessageBox.Question)
    button = dlg.exec()


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('/usr/local/bin/g.ui', self)
        self.show()
        self.lineEdit.returnPressed.connect(self.classify_input)
        self.actionRegister_Filter_Rack.triggered.connect(self.Register_Filter_Rack)
        self.actionProduction_Label.triggered.connect(self.Production_Label)
        self.actionProject_Label.triggered.connect(self.Project_Label)
        self.actionRegister_Router_Rack.triggered.connect(self.Register_Router_Rack)
        self.pushButton.clicked.connect(self.print_label)
        self.checkBox.stateChanged.connect(self.resize_window)

    def resize_window(self):
        if self.frameGeometry().width() == 420:
            self.setFixedWidth(620)
        else:
            self.setFixedWidth(420)


    def reprint_label_dialog(self):
        dlg = QtWidgets.QMessageBox(self)
        dlg.setWindowTitle("Warning!")
        dlg.setText("Serial already exists in database.\n\nReprint label?")
        dlg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        dlg.setIcon(QtWidgets.QMessageBox.Question)
        button = dlg.exec()
        if button == QtWidgets.QMessageBox.Yes:
            return True
        else:
            return False

    def classify_input(self):
        user_input = str(self.lineEdit.text())
        self.textBrowser.append(user_input)

        if self.lineEdit_7.text() == 'Project Label':
            if len(user_input) == 6 and user_input[:2] == '60' or len(user_input) == 9 and user_input[:2] == '60' and '-' in user_input:
                self.lineEdit_2.setText(user_input)
                sap = self.lineEdit_2.text()
                serialcheck = sqlquery(f"SELECT serial FROM simdb.standardprojectglabels WHERE pn='{sap}'")
                if serialcheck == 'True':
                    if len(self.lineEdit_2.text()) >= 6 and len(self.lineEdit_3.text()) >= 1:
                        self.print_label()
                else:
                    self.print_label()
            else:
                self.lineEdit_3.setText(user_input)
                try:
                    sap = self.lineEdit_2.text()
                    serialcheck = sqlquery(f"SELECT serial FROM simdb.standardprojectglabels WHERE pn='{sap}'")
                    if serialcheck == 'True':
                        if len(self.lineEdit_2.text()) >= 6 and len(self.lineEdit_3.text()) >= 1:
                            self.print_label()
                except Exception:
                    pass

        elif self.lineEdit_7.text() == 'Register Router Rack' or self.lineEdit_7.text() == 'Production Label':
            if len(user_input) == 6 and user_input[:2] == '60' or len(user_input) == 9 and user_input[:2] == '60' and '-' in user_input:
                self.lineEdit_2.setText(user_input)
            else:
                self.lineEdit_3.setText(user_input)
            
            try:
                if len(self.lineEdit_2.text()) >= 6 and len(self.lineEdit_3.text()) >= 1:
                    self.print_label()
            except Exception:
                pass

        elif self.lineEdit_7.text() == 'Register Filter Rack':
            if len(user_input) == 6 and user_input[:2] == '60' or len(user_input) == 9 and user_input[:2] == '60' and '-' in user_input:
                self.lineEdit_2.setText(user_input)
                self.lineEdit_3.setText('')
                self.lineEdit_4.setText('')
                self.lineEdit_5.setText('')
                self.lineEdit_6.setText('')
            else:
                if len(self.lineEdit_3.text()) == 0 or len(self.lineEdit_3.text()) >= 1 and len(self.lineEdit_4.text()) >= 1 and len(self.lineEdit_5.text()) >= 1 and len(self.lineEdit_6.text()) >= 1 :
                    self.lineEdit_4.setText('')
                    self.lineEdit_5.setText('')
                    self.lineEdit_6.setText('')
                    print('serial1 is empty')
                    self.lineEdit_3.setText(user_input)
                else:
                    if len(self.lineEdit_4.text()) == 0:
                        print('serial2 is empty')
                        self.lineEdit_4.setText(user_input)
                    else:
                        if len(self.lineEdit_5.text()) == 0:
                            print('serial3 is empty')
                            self.lineEdit_5.setText(user_input)
                        else:
                            if len(self.lineEdit_6.text()) == 0:
                                print('serial4 is empty')
                                self.lineEdit_6.setText(user_input)
                                self.print_label()
        self.lineEdit.clear()

    def Register_Filter_Rack(self):
        self.lineEdit_7.setText('Register Filter Rack')
        self.pushButton.setEnabled(True)
        self.comboBox.setEnabled(True)
        self.comboBox_2.setEnabled(True)
        self.spinBox.setEnabled(True)
        self.spinBox_2.setEnabled(True)
        self.lineEdit.setEnabled(True)
        self.lineEdit_2.setEnabled(True)
        self.lineEdit_3.setEnabled(True)
        self.lineEdit_4.setEnabled(True)
        self.lineEdit_5.setEnabled(True)
        self.lineEdit_6.setEnabled(True)
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.lineEdit_5.clear()
        self.lineEdit_6.clear()

    def Production_Label(self):
        self.lineEdit_7.setText('Production Label')
        self.pushButton.setEnabled(True)
        self.comboBox.setEnabled(True)
        self.comboBox_2.setEnabled(True)
        self.spinBox.setEnabled(True)
        self.spinBox_2.setEnabled(True)
        self.lineEdit.setEnabled(True)
        self.lineEdit_2.setEnabled(True)
        self.lineEdit_3.setEnabled(True)
        self.lineEdit_4.setEnabled(False)
        self.lineEdit_5.setEnabled(False)
        self.lineEdit_6.setEnabled(False)
        self.spinBox.setEnabled(True)
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.lineEdit_5.clear()
        self.lineEdit_6.clear()

    def Project_Label(self):
        self.lineEdit_7.setText('Project Label')
        self.pushButton.setEnabled(True)
        self.comboBox.setEnabled(True)
        self.comboBox_2.setEnabled(True)
        self.spinBox.setEnabled(True)
        self.spinBox_2.setEnabled(True)
        self.lineEdit.setEnabled(True)
        self.lineEdit_2.setEnabled(True)
        self.lineEdit_3.setEnabled(True)
        self.lineEdit_4.setEnabled(False)
        self.lineEdit_5.setEnabled(False)
        self.lineEdit_6.setEnabled(False)
        self.spinBox.setEnabled(True)
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.lineEdit_5.clear()
        self.lineEdit_6.clear()

    def Register_Router_Rack(self):
        self.lineEdit_7.setText('Register Router Rack')
        self.pushButton.setEnabled(True)
        self.comboBox.setEnabled(True)
        self.comboBox_2.setEnabled(True)
        self.spinBox_2.setEnabled(True)
        self.lineEdit.setEnabled(True)
        self.lineEdit_2.setEnabled(True)
        self.lineEdit_3.setEnabled(True)
        self.lineEdit_4.setEnabled(False)
        self.lineEdit_5.setEnabled(False)
        self.lineEdit_6.setEnabled(False)
        self.spinBox.setEnabled(False)
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.lineEdit_5.clear()
        self.lineEdit_6.clear()

    def print_label(self):
        sap = self.lineEdit_2.text()
        printer = self.comboBox.currentText()
        labelsize = self.comboBox_2.currentText()
        increments = self.spinBox.value()
        copies = self.spinBox_2.value()

        if self.lineEdit_7.text() == 'Production Label':
            sapcheck = sqlquery(f"SELECT pn FROM simdb.product_label WHERE pn='{sap}'")
            if sapcheck == False:
                warning_dialog('SAP number does not exist in database')
                self.lineEdit_2.clear()
                return
            serial = int(self.lineEdit_3.text())
            typenumber = sqlquery(f"SELECT type FROM simdb.product_label WHERE pn='{sap}'")
            template = sqlquery(f"SELECT template FROM simdb.product_label WHERE pn='{sap}'")
            if labelsize == '101x152mm':
                template = template+'p'
            commands = []
            for i in range(increments):
                cmd = "glabels-batch-qt  "\
                        f"/mnt/fs/Icomera/Line/Supply Chain/Production/Glabels/Templates/{template}.glabels  "\
                        f"-D  serial={serial}  "\
                        f"-D  sap={sap}  "\
                        f"-D  type={typenumber}  "\
                        f"-o  /home/{user}/labelfiles/{serial}.pdf".split("  ")
                commands.append(f"-c /home/{user}/labelfiles/{serial}.pdf")
                try:
                    create_pdf = subprocess.run(cmd, capture_output=True)
                except Exception as e:
                    warning_dialog(str(e))
                    return
                if b'Printing 1 item on 1 page' not in create_pdf.stderr:
                    warning_dialog('Unable to find label template')
                    return
                serial = serial+1
            files_strings = " ".join(commands)
            cmd = f"lp -n {copies} {files_strings} -d {printer} -o media={labelsize}".split()
            subprocess.call(cmd)

        elif self.lineEdit_7.text() == 'Project Label':
            sapcheck = sqlquery(f"SELECT pn FROM simdb.standardprojectglabels WHERE pn='{sap}'")
            if sapcheck == False:
                warning_dialog('SAP number does not exist in database')
                self.lineEdit_2.clear()
                return
            try:
                serial = int(self.lineEdit_3.text())
            except Exception:
                serial = sap
            labeloption = sqlquery(f"SELECT labeloption FROM simdb.standardprojectglabels WHERE pn='{sap}'")
            description1 = sqlquery(f"SELECT description1 FROM simdb.standardprojectglabels WHERE pn='{sap}'")
            description2 = sqlquery(f"SELECT description2 FROM simdb.standardprojectglabels WHERE pn='{sap}'")
            description3 = sqlquery(f"SELECT description3 FROM simdb.standardprojectglabels WHERE pn='{sap}'")
            description4 = sqlquery(f"SELECT description4 FROM simdb.standardprojectglabels WHERE pn='{sap}'")
            description5 = sqlquery(f"SELECT description5 FROM simdb.standardprojectglabels WHERE pn='{sap}'")
            revision = sqlquery(f"SELECT revision FROM simdb.standardprojectglabels WHERE pn='{sap}'")
            customer_pn = sqlquery(f"SELECT customer_pn FROM simdb.standardprojectglabels WHERE pn='{sap}'")
            todays_date = datetime.today().strftime('%Y-%m-%d')
            mmyyyy = datetime.today().strftime('%m-%Y')
            commands = []
            cmd = "glabels-batch-qt  "\
                    f"/mnt/fs/Icomera/Line/Supply Chain/Production/Glabels/Templates/{labeloption}.glabels  "\
                    f"-D  description1={description1}  "\
                    f"-D  description2={description2}  "\
                    f"-D  description3={description3}  "\
                    f"-D  description4={description4}  "\
                    f"-D  description5={description5}  "\
                    f"-D  serial={serial}  "\
                    f"-D  pn={sap}  "\
                    f"-D  todays_date={todays_date}  "\
                    f"-D  mmyyyy={mmyyyy}  "\
                    f"-D  customer_pn={customer_pn}  "\
                    f"-D  revision={revision}  "\
                    f"-o  /home/{user}/labelfiles/{serial}.pdf".split("  ")
            commands.append(f"-c /home/{user}/labelfiles/{serial}.pdf")
            try:
                create_pdf = subprocess.run(cmd, capture_output=True)
            except Exception as e:
                warning_dialog(str(e))
                return
            if b'Printing 1 item on 1 page' not in create_pdf.stderr:
                warning_dialog('Unable to find label template')
                return
            files_strings = " ".join(commands)
            cmd = f"lp -n {copies} {files_strings} -d {printer}".split()
            subprocess.call(cmd)

        elif self.lineEdit_7.text() == 'Register Router Rack':
            sapcheck = sqlquery(f"SELECT articlenumber FROM simdb.custspecificracks WHERE articlenumber='{sap}'")
            if sapcheck == False:
                warning_dialog('SAP number does not exist in database')
                self.lineEdit_2.clear()
                return
            serial = int(self.lineEdit_3.text())
            serialcheck = sqlquery(f"SELECT rackid FROM simdb.racks WHERE routerserial='{serial}'")
            if serialcheck:
                if self.reprint_label_dialog() == True:
                    unitname = sqlquery(f"SELECT custarticlename FROM simdb.custspecificracks WHERE articlenumber='{sap}'")
                    sapdb = sqlquery(f"SELECT custarticlenumber FROM simdb.custspecificracks WHERE articlenumber='{sap}'")
                    rackserial = sqlquery(f"SELECT rackserial FROM simdb.racks WHERE routerserial LIKE {serial}")
                    customerserialprefix = sqlquery(f"SELECT customerserialprefix FROM simdb.racks WHERE routerserial LIKE {serial}")
                    customerserial = str(sqlquery(f"SELECT customerserial FROM simdb.racks WHERE routerserial LIKE {serial}"))
                    concatenateserial = customerserialprefix+customerserial
                    rackid = sqlquery(f"SELECT rackid FROM simdb.racks WHERE rackserial LIKE '{rackserial}'")
                    logisticsQR = str(serial)+" - "+str(rackserial)
                    cmd = "glabels-batch-qt  "\
                        f"/mnt/fs/Icomera/Line/Supply Chain/Production/Glabels/Templates/router_rack.glabels  "\
                        f"-D  serial={serial}  "\
                        f"-D  sap={sap}  "\
                        f"-D  sapdb={sapdb}  "\
                        f"-D  name={unitname}  "\
                        f"-D  custs={concatenateserial}  "\
                        f"-D  rackserial={rackserial}  "\
                        f"-o  /home/{user}/labelfiles/{serial}.pdf".split("  ")
                    try:
                        create_pdf = subprocess.run(cmd, capture_output=True)
                    except Exception as e:
                        warning_dialog(str(e))
                        return
                    if b'Printing 1 item on 1 page' not in create_pdf.stderr:
                        warning_dialog('Unable to find label template')
                        return
                    logisticsQR = str(serial)+" - "+str(rackserial)
                    cmd = "glabels-batch-qt  "\
                        f"/mnt/fs/Icomera/Line/Supply Chain/Production/Glabels/Templates/logisticslabel.glabels  "\
                        f"-D  serial={logisticsQR}  "\
                        f"-o  /home/{user}/labelfiles/{serial}l.pdf".split("  ")
                    create_pdf = subprocess.run(cmd, capture_output=True)
                    if b'Printing 1 item on 1 page' not in create_pdf.stderr:
                        warning_dialog('Unable to find label template')
                        return
                    cmd = f"lp -n 1 -c /home/{user}/labelfiles/{serial}.pdf -c /home/{user}/labelfiles/{serial}.pdf -c /home/{user}/labelfiles/{serial}l.pdf -d {printer} -o media={labelsize}".split()
                    subprocess.run(cmd)
                    return
                else:
                    print('Not printing label')
                    return
            racks = sqlquery("SELECT MAX(rackserial)+1 FROM simdb.racks")
            racks=int(racks)
            rackserial=str(racks).zfill(6)
            customerspecific = sqlquery(f"SELECT articlenumber FROM simdb.custspecificracks WHERE articlenumber='{sap}'")
            if customerspecific == False:
                unitname = "Router Rack"
                customerserial = None
            else:
                unitname = sqlquery(f"SELECT custarticlename FROM simdb.custspecificracks WHERE articlenumber='{sap}'")
                sapdb = sqlquery(f"SELECT custarticlenumber FROM simdb.custspecificracks WHERE articlenumber='{sap}'")
                customerserialprefix = sqlquery(f"SELECT serialprefix FROM simdb.custspecificracks WHERE articlenumber='{sap}'")
                customerserial = str(sqlquery(f"SELECT MAX(customerserial)+1 FROM simdb.racks WHERE customerserial IS NOT NULL AND customerserialprefix LIKE '{customerserialprefix}'")).split('.')[0]
                customerserial = customerserial.zfill(4)
            if customerserial:
                dbupload("INSERT INTO simdb.racks (customerid, projectid, articlenumber, rackserial, routerserial, customerserialprefix, customerserial) VALUES (%s, %s, %s, %s, %s, %s, %s)", (f"{customerid}", f"{projectid}", f"{sap}", f"{rackserial}", f"{serial}", f"{customerserialprefix}", f"{customerserial}"))
            else:
                dbupload("INSERT INTO simdb.racks (customerid, projectid, articlenumber, rackserial, routerserial) VALUES (%s, %s, %s, %s, %s)", (f"{customerid}", f"{projectid}", f"{sap}", f"{rackserial}", f"{serial}"))
                #sqlquery(f"INSERT INTO simdb.racks (customerid, projectid, articlenumber, rackserial, routerserial) VALUES ({customerid}, {projectid}, {sap}, {rackserial}, {serial})")
            rackid = sqlquery(f"SELECT rackid FROM simdb.racks WHERE rackserial LIKE '{rackserial}'")
            if rackid:
                if customerserial:
                    if customerserialprefix:
                        customerserialprefix=str(customerserialprefix)
                        customerserial=str(customerserial)
                        concatenateserial = customerserialprefix+customerserial
                    else:
                        concatenateserial = customerserial
                cmd = "glabels-batch-qt  "\
                        f"/mnt/fs/Icomera/Line/Supply Chain/Production/Glabels/Templates/router_rack.glabels  "\
                        f"-D  serial={serial}  "\
                        f"-D  sap={sap}  "\
                        f"-D  sapdb={sapdb}  "\
                        f"-D  name={unitname}  "\
                        f"-D  custs={concatenateserial}  "\
                        f"-D  rackserial={rackserial}  "\
                        f"-o  /home/{user}/labelfiles/{serial}.pdf".split("  ")
                try:
                    create_pdf = subprocess.run(cmd, capture_output=True)
                except Exception as e:
                    warning_dialog(str(e))
                    return
                if b'Printing 1 item on 1 page' not in create_pdf.stderr:
                    warning_dialog('Unable to find label template')
                    return
                logisticsQR = str(serial)+" - "+str(rackserial)
                cmd = "glabels-batch-qt  "\
                    f"/mnt/fs/Icomera/Line/Supply Chain/Production/Glabels/Templates/logisticslabel.glabels  "\
                    f"-D  serial={logisticsQR}  "\
                    f"-o  /home/{user}/labelfiles/{serial}l.pdf".split("  ")
                create_pdf = subprocess.run(cmd, capture_output=True)
                if b'Printing 1 item on 1 page' not in create_pdf.stderr:
                    warning_dialog('Unable to find label template')
                    return
                cmd = f"lp -n 1 -c /home/{user}/labelfiles/{serial}.pdf -c /home/{user}/labelfiles/{serial}.pdf -c /home/{user}/labelfiles/{serial}l.pdf -d {printer} -o media={labelsize}".split()
                subprocess.run(cmd)
            else:
                warning_dialog('Upload to database failed')

        elif self.lineEdit_7.text() == 'Register Filter Rack':
            sapcheck = sqlquery(f"SELECT articlenumber FROM simdb.custspecificracks WHERE articlenumber='{sap}'")
            if sapcheck == False:
                warning_dialog('SAP number does not exist in database')
                self.lineEdit_2.clear()
                return
            filter1 = str(self.lineEdit_3.text())
            filter2 = str(self.lineEdit_4.text())
            filter3 = str(self.lineEdit_5.text())
            filter4 = str(self.lineEdit_6.text())
            filter1check = sqlquery(f"SELECT rackid FROM simdb.racks WHERE filter1 LIKE '{filter1}' OR filter2 LIKE '{filter1}' OR filter3 LIKE '{filter1}' OR filter4 LIKE '{filter1}'")
            filter2check = sqlquery(f"SELECT rackid FROM simdb.racks WHERE filter1 LIKE '{filter2}' OR filter2 LIKE '{filter2}' OR filter3 LIKE '{filter2}' OR filter4 LIKE '{filter2}'")
            filter3check = sqlquery(f"SELECT rackid FROM simdb.racks WHERE filter1 LIKE '{filter3}' OR filter2 LIKE '{filter3}' OR filter3 LIKE '{filter3}' OR filter4 LIKE '{filter3}'")
            filter4check = sqlquery(f"SELECT rackid FROM simdb.racks WHERE filter1 LIKE '{filter4}' OR filter2 LIKE '{filter4}' OR filter3 LIKE '{filter4}' OR filter4 LIKE '{filter4}'")
            if filter1check or filter2check or filter3check or filter4check:
                if self.reprint_label_dialog() == True:
                    rackserial = sqlquery(f"SELECT rackserial FROM simdb.racks WHERE filter1 LIKE '{filter1}' OR filter2 LIKE '{filter1}' OR filter3 LIKE '{filter1}' OR filter4 LIKE '{filter1}'")
                    customerid = sqlquery(f"SELECT customerid FROM simdb.custspecificracks WHERE articlenumber='{sap}'")
                    projectid = sqlquery(f"SELECT projectid FROM simdb.custspecificracks WHERE articlenumber='{sap}'")
                    unitname = sqlquery(f"SELECT custarticlename FROM simdb.custspecificracks WHERE articlenumber='{sap}'")
                    sapdb = sqlquery(f"SELECT custarticlenumber FROM simdb.custspecificracks WHERE articlenumber='{sap}'")
                    customerserialprefix = sqlquery(f"SELECT customerserialprefix FROM simdb.racks WHERE rackserial LIKE {rackserial}")
                    customerserial = str(sqlquery(f"SELECT customerserial FROM simdb.racks WHERE rackserial LIKE {rackserial}"))
                    concatenateserial = customerserialprefix+customerserial
                    rackid = sqlquery(f"SELECT rackid FROM simdb.racks WHERE rackserial LIKE '{rackserial}'")
                    cmd = "glabels-batch-qt  "\
                        f"/mnt/fs/Icomera/Line/Supply Chain/Production/Glabels/Templates/filterrack.glabels  "\
                        f"-D  sap={sap}  "\
                        f"-D  sapdb={sapdb}  "\
                        f"-D  name={unitname}  "\
                        f"-D  custs={concatenateserial}  "\
                        f"-D  rackserial={rackserial}  "\
                        f"-o  /home/{user}/labelfiles/{rackserial}.pdf".split("  ")
                    try:
                        create_pdf = subprocess.run(cmd, capture_output=True)
                    except Exception as e:
                        warning_dialog(str(e))
                        return
                    if b'Printing 1 item on 1 page' not in create_pdf.stderr:
                        warning_dialog('Unable to find label template')
                        return
                    cmd = "glabels-batch-qt  "\
                        f"/mnt/fs/Icomera/Line/Supply Chain/Production/Glabels/Templates/logisticslabel.glabels  "\
                        f"-D  serial={rackserial}  "\
                        f"-o  /home/{user}/labelfiles/{rackserial}l.pdf".split("  ")
                    create_pdf = subprocess.run(cmd, capture_output=True)
                    if b'Printing 1 item on 1 page' not in create_pdf.stderr:
                        warning_dialog('Unable to find label template')
                        return
                    cmd = f"lp -n 1 -c /home/{user}/labelfiles/{rackserial}.pdf -c /home/{user}/labelfiles/{rackserial}.pdf -c /home/{user}/labelfiles/{rackserial}l.pdf -d {printer} -o media={labelsize}".split()
                    subprocess.run(cmd)
                    return
                else:
                    print('Not printing label')
                    return
            customerid = sqlquery(f"SELECT customerid FROM simdb.custspecificracks WHERE articlenumber='{sap}'")
            projectid = sqlquery(f"SELECT projectid FROM simdb.custspecificracks WHERE articlenumber='{sap}'")
            racks = sqlquery("SELECT MAX(rackserial)+1 FROM simdb.racks")
            racks=int(racks)
            rackserial=str(racks).zfill(6)
            print(customerid, projectid, rackserial)
            customerspecific = sqlquery(f"SELECT articlenumber FROM simdb.custspecificracks WHERE articlenumber='{sap}'")
            if customerspecific == False:
                unitname = "Filter Rack"
                customerserial = None
            else:
                unitname = sqlquery(f"SELECT custarticlename FROM simdb.custspecificracks WHERE articlenumber='{sap}'")
                print(unitname)
                sapdb = sqlquery(f"SELECT custarticlenumber FROM simdb.custspecificracks WHERE articlenumber='{sap}'")
                print(sapdb)
                customerserialprefix = sqlquery(f"SELECT serialprefix FROM simdb.custspecificracks WHERE articlenumber='{sap}'")
                #customerserialprefix = customerserialprefix.split('.')[0]
                customerserial = str(sqlquery(f"SELECT MAX(customerserial)+1 FROM simdb.racks WHERE customerserial IS NOT NULL AND customerserialprefix LIKE '{customerserialprefix}'")).split('.')[0]
                customerserial = customerserial.zfill(4)
                print(customerserialprefix,customerserial)
                print(type(customerserial))
            if customerserial:
                dbupload("INSERT INTO simdb.racks (customerid, projectid, articlenumber, rackserial, filter1, filter2, filter3, filter4, customerserialprefix, customerserial) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (f"{customerid}", f"{projectid}", f"{sap}", f"{rackserial}", f"{filter1}", f"{filter2}", f"{filter3}", f"{filter4}", f"{customerserialprefix}", f"{customerserial}"))
            else:
                dbupload("INSERT INTO simdb.racks (customerid, projectid, articlenumber, rackserial, filter1, filter2, filter3, filter4) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (f"{customerid}", f"{projectid}", f"{sap}", f"{rackserial}", f"{filter1}", f"{filter2}", f"{filter3}", f"{filter4}"))
            rackid = sqlquery(f"SELECT rackid FROM simdb.racks WHERE rackserial LIKE '{rackserial}'")
            if rackid:
                if customerserial:
                    if customerserialprefix:
                        customerserialprefix=str(customerserialprefix)
                        customerserial=str(customerserial)
                        concatenateserial = customerserialprefix+customerserial
                    else:
                        concatenateserial = customerserial
                    cmd = "glabels-batch-qt  "\
                            f"/mnt/fs/Icomera/Line/Supply Chain/Production/Glabels/Templates/filterrack.glabels  "\
                            f"-D  sap={sap}  "\
                            f"-D  sapdb={sapdb}  "\
                            f"-D  name={unitname}  "\
                            f"-D  custs={concatenateserial}  "\
                            f"-D  rackserial={rackserial}  "\
                            f"-o  /home/{user}/labelfiles/{rackserial}.pdf".split("  ")
                    try:
                        create_pdf = subprocess.run(cmd, capture_output=True)
                    except Exception as e:
                        warning_dialog(str(e))
                        return
                    if b'Printing 1 item on 1 page' not in create_pdf.stderr:
                        warning_dialog('Unable to find label template')
                        return
                    cmd = "glabels-batch-qt  "\
                            f"/mnt/fs/Icomera/Line/Supply Chain/Production/Glabels/Templates/logisticslabel.glabels  "\
                            f"-D  serial={rackserial}  "\
                            f"-o  /home/{user}/labelfiles/{rackserial}l.pdf".split("  ")
                    create_pdf = subprocess.run(cmd, capture_output=True)
                    if b'Printing 1 item on 1 page' not in create_pdf.stderr:
                        warning_dialog('Unable to find label template')
                        return
                    cmd = f"lp -n 1 -c /home/{user}/labelfiles/{rackserial}.pdf -c /home/{user}/labelfiles/{rackserial}.pdf -c /home/{user}/labelfiles/{rackserial}l.pdf -d {printer} -o media={labelsize}".split()
                    subprocess.run(cmd)
            else:
                warning_dialog('Upload to database failed')

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
