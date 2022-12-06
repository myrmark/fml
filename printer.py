import getpass
import keyring
import lzma
import os
import subprocess
import sys
import tarfile

user = os.getlogin()

print('Checking for labelfiles folder')
try:
    os.listdir(f"/home/{user}/labelfiles")
except Exception:
    print("labelfiles folder was not found. Creating folder")
    os.mkdir(f"/home/{user}/labelfiles")

print('Checking for printers')
try:
    ps = subprocess.Popen('sudo lpinfo -m', stdout=subprocess.PIPE, shell=True)
    drivers_check = subprocess.check_output(('grep', 'TTP-644MT'), stdin=ps.stdout)
    ps.wait()
    drivers_check = drivers_check.decode().strip()
except Exception:
    print(f"Printer drivers not installed. Installing..")
    with lzma.open('drivers.tar.xz') as fd:
        with tarfile.open(fileobj=fd) as tar:
            content = tar.extractall('drivers')
    os.chdir('drivers')
    cmd = 'sudo ./install-driver'.split()
    subprocess.run(cmd)


try:
    ps = subprocess.Popen('lpstat -p -d', stdout=subprocess.PIPE, shell=True)
    printer_check = subprocess.check_output(('grep', 'TTP-644MT'), stdin=ps.stdout)
    ps.wait()
    printer_check = printer_check.decode().strip()
except Exception:
    print(f"Printer TTP-644MT not installed. Installing..")
    cmd = 'sudo lpadmin -p TTP-644MT -E -m tscbarcode/TTP-644MT.ppd -v lpd://172.28.88.43/queue -o PageSize=Custom.60x30mm'.split()
    subprocess.run(cmd)


try:
    ps = subprocess.Popen('lpstat -p -d', stdout=subprocess.PIPE, shell=True)
    printer_check = subprocess.check_output(('grep', 'ME340_lager'), stdin=ps.stdout)
    ps.wait()
    printer_check = printer_check.decode().strip()
except Exception:
    print(f"Printer ME340_lager not installed. Installing..")
    cmd = 'sudo lpadmin -p ME340_lager -E -m tscbarcode/ME340.ppd -v lpd://172.28.88.46/queue -o PageSize=Custom.60x30mm'.split()
    subprocess.run(cmd)


try:
    ps = subprocess.Popen('lpstat -p -d', stdout=subprocess.PIPE, shell=True)
    printer_check = subprocess.check_output(('grep', 'ME340_production'), stdin=ps.stdout)
    ps.wait()
    printer_check = printer_check.decode().strip()
except Exception:
    print(f"Printer ME340_production not installed. Installing..")
    cmd = 'sudo lpadmin -p ME340_production -E -m tscbarcode/ME340.ppd -v lpd://172.28.88.60/queue -o PageSize=Custom.60x30mm'.split()
    subprocess.run(cmd)


try:
    ps = subprocess.Popen('lpstat -p -d', stdout=subprocess.PIPE, shell=True)
    printer_check = subprocess.check_output(('grep', 'Zebra_ZT230_production'), stdin=ps.stdout)
    ps.wait()
    printer_check = printer_check.decode().strip()
except Exception:
    print(f"Printer Zebra_ZT230_production not installed. Installing..")
    cmd = 'sudo lpadmin -p Zebra_ZT230_production -E -m drv:///sample.drv/zebra.ppd -v socket://172.28.88.44:9100 -o PageSize=Custom.101x152mm'.split()
    subprocess.run(cmd)


try:
    ps = subprocess.Popen('lpstat -p -d', stdout=subprocess.PIPE, shell=True)
    printer_check = subprocess.check_output(('grep', 'Zebra_ZT230_lager'), stdin=ps.stdout)
    ps.wait()
    printer_check = printer_check.decode().strip()
except Exception:
    print(f"Printer Zebra_ZT230_lager not installed. Installing..")
    cmd = 'sudo lpadmin -p Zebra_ZT230_lager -E -m drv:///sample.drv/zebra.ppd -v socket://172.28.88.45:9100 -o PageSize=Custom.101x152mm'.split()
    subprocess.run(cmd)
