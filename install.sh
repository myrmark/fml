username=$(logname)
cp fml.png /usr/share/icons/fml.png
cp fml.desktop /home/$username/.local/share/applications/fml.desktop
echo "username=svc-supply-chain" > /home/$username/.smbcredentials
read -sp "Enter password for svc-supply-chain: " pwd
echo "password=$pwd" >> /home/$username/.smbcredentials
chmod 600 /home/$username/.smbcredentials
mkdir /mnt/fs
chmod 777 /mnt/fs
echo "//internal.icomera.com/dfs /mnt/fs cifs credentials=/home/$username/.smbcredentials,user	0	0" | sudo tee -a /etc/fstab
