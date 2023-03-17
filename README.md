# Cyberghost OpenVPN file generator GUI
This python3 script is a Tkinter Graphical User Interface that sends requests to my.cyberghostvpn.com to get the VPN configs, and download and edit these configs.

## Features
- Download VPN File
- aggregate certificates in the `.ovpn` file
  - add user and password in auth.txt
- Edit and create multiple `.ovpn` file for other countries, or other protocols, using the same user and password
- autoload the new file in your VPN app
