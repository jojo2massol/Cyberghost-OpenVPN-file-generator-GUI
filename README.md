# Cyberghost OpenVPN file generator GUI
This python3 script is a Tkinter Graphical User Interface that sends requests to my.cyberghostvpn.com to get the VPN configs, and download and edit these configs.

## Features
- **Download VPN File**
- Aggregate certificates in the `.ovpn` file
  - Add user and password in auth.txt  
- **Edit and create multiple `.ovpn` files** for other countries, or other protocols, using the same user and password
- **Autoload the new file in your VPN app  
  (tested with OpenVPN Connect on Windows,**
  doesn't work with linux gnome network manager, it opens the file in a text editor)
- auto system theme
![image](https://user-images.githubusercontent.com/54369031/225980723-f69fc7c4-e5ab-458a-8f68-13dc7f2336ba.png)
![image](https://user-images.githubusercontent.com/54369031/225975732-75e35abd-3715-4242-aade-19952ab3a2da.png)


## Compatibility
- Windows: Tested: Win11✔️
- Linux:   Tested: Arch with Gnome ✔️
- Macos: Untested


## How to use
- **Download the script**  
  `git clone https://github.com/jojo2massol/Cyberghost-OpenVPN-file-generator-GUI.git`
- **Install the requirements** : 
  - Interpreter: `python3`  
  - ```pip install tk jsonlib requests os-sys shutils sv_ttk darkdetect```
- **Run the script**  
  ```sh
  cd Cyberghost-OpenVPN-file-generator-GUI
  python main.py
  ```  
  The window should open, and you can start using it.
  
- Get your cookie from your browser, and paste it in the entry field
  - Connect to your Cyberghost account : https://my.cyberghostvpn.com/en_US/login
  - Press `F12` to open the developer tools
  - Open the `Network` tab
  - Refresh the page
  - Click on the first entry, and search in the request headers for `cookie`. 
  - Copy the `SESSIONUSER` value in the cookie, and paste it in the entry field in the GUI
![How to get session user](https://user-images.githubusercontent.com/54369031/225950343-3e274c03-1fd4-4dd3-b4a6-8c56f03999eb.png)
