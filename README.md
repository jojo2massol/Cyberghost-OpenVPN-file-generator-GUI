# Cyberghost OpenVPN file generator GUI
This python3 script is a Tkinter Graphical User Interface that sends requests to my.cyberghostvpn.com to get the VPN configs, and download and edit these configs.

## Features
- **Download VPN File**
- aggregate certificates in the `.ovpn` file
  - add user and password in auth.txt  
- **Edit and create multiple `.ovpn` files** for other countries, or other protocols, using the same user and password
- **autoload the new file in your VPN app  
  (tested with OpenVPN Connect on Windows,**
  doesn't work with linux gnome network manager, it opens the file in a text editor)

# How to use
- **Download the script**  
  `git clone https://github.com/jojo2massol/Cyberghost-OpenVPN-file-generator-GUI.git`
- **Install the requirements** : 
  - interpreter: `python3`  
  - ```pip install tkinter json requests os subprocess platform shutil zipfile```
- **Run the script**  
  ```sh
  cd Cyberghost-OpenVPN-file-generator-GUI
  python main.py
  ```  
  The window should open, and you can start using it.
  
- get your cookie from your browser, and paste it in the entry field
  - connect to your Cyberghost account : https://my.cyberghostvpn.com/en_US/login
  - Press `F12` to open the developer tools
  - open the `Network` tab
  - refresh the page
  - click on the first entry, and search in the request headers for `cookie`. 
  - Copy the `SESSIONUSER` value in the cookie, and paste it in the entry field in the GUI
![How to get session user](https://user-images.githubusercontent.com/54369031/225950343-3e274c03-1fd4-4dd3-b4a6-8c56f03999eb.png)
