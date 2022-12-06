cp fml.png /usr/share/icons/fml.png
cp fml.desktop ~/.local/share/applications/fml.desktop
echo "//internal.icomera.com/dfs /mnt/fs cifs credentials=/home/$USER/.smbcredentials,user	0	0" | sudo tee -a /etc/fstab
echo "username:svc-supply-chain" > /home/$USER/.smbcredentials
read -sp "Enter password for svc-supply-chain: " pwd
echo "password:$pwd" >> /home/$USER/.smbcredentials
chmod 600 /home/$USER/.smbcredentials
mkdir /mnt/fs
chmod 777 /mnt/fs
chmod $USER:$USER /mnt/fs
