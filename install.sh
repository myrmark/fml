username=$(logname)
apt install python3-pip -y
pip install pymysql PyQt5
cp fml.png /usr/share/icons/fml.png
cp fml.desktop /home/$username/.local/share/applications/fml.desktop
cp fml.pyw /usr/local/bin/fml.pyw
echo "username=svc-supply-chain" > /home/$username/.smbcredentials
read -sp "Enter password for svc-supply-chain: " pwd
echo "password=$pwd" >> /home/$username/.smbcredentials
chmod 600 /home/$username/.smbcredentials
mkdir /mnt/fs
chmod 777 /mnt/fs
echo "//internal.icomera.com/dfs /mnt/fs cifs credentials=/home/$username/.smbcredentials,user	0	0" | sudo tee -a /etc/fstab
python3 printer.py
echo "Enter the following command in a python3 session to store the database password: keyring.set_password("172.28.88.47", "simdbuploader", getpass.getpass())"
