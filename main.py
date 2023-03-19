from tkinter import messagebox as mBox
from tkinter import Spinbox
from tkinter import Menu
from tkinter import scrolledtext
from tkinter import ttk
from tkinter import filedialog
from tkinter import PhotoImage
import tkinter as tk
import json
import requests
import os
import subprocess
import platform
import shutil
import zipfile

import vpn_file_concatenator

default_conf_path = "default_conf.py"
default_vpn_path = "./"

domain = "https://my.cyberghostvpn.com/"
api = "api/devices/"
url_countries = domain + api + "get-server-countries"
url_server_groups = domain + api + "get-server-groups"
url_vpn = domain + api + "add-other"
url_download = domain + "devices/download-config/"

protocols = {"openvpn": "Open VPN", "openvpn_tcp": "Open VPN TCP",
             "openvpn_legacy": "Open VPN <= 2.3", "openvpn_tcp_legacy": "Open VPN TCP <= 2.3", "ipsec": "IPsec (useless here)"}
# may be more locales
locales = {"en_US": "English", "de_DE": "Deutsch", "fr_FR": "Français", "es_ES": "Español",
           "it_IT": "Italiano", "pt_PT": "Português", "ru_RU": "Русский", "pl_PL": "Polski", "nl_NL": "Nederlands"}

(server_groups, country_code) = ("", "")
(configsId, groupsId, configname) = ("", "", "")
(source_server, dest_server) = ("", "")
(source_protocol, dest_protocol) = ("", "")
countries = "[]"
try:
    import default_conf
    # cookie have to contain the SESSIONUSER
    cookie = default_conf.cookie
    protocol = default_conf.protocol
    locale = default_conf.locale
except:
    print("default_conf.py not found")
    cookie = ""
    protocol = "openvpn"
    locale = "en_US"
    countries = "[]"


def get_countries(protocol, locale, cookie):
    form = {"protocol": protocol, "locale": locale}
    headers = {
        "Cookie": cookie,
        "referer": "https://my.cyberghostvpn.com/fr_FR/download-hub/other/add-other?",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest"
    }
    response = requests.post(url_countries, headers=headers, data=form)

    # code
    print(response.status_code)
    # print(response.text)
    # convert characters like \u00c9 to É
    response_unicode = response.text.encode('latin1').decode('unicode_escape')
    return json.dumps(json.loads(response_unicode), sort_keys=True, ensure_ascii=False)

"""
takes : 
protocol: openvpn
countryCode: CA
locale: fr_FR
"""

def get_server_groups(protocol, countryCode, locale, cookie):
    form = {"protocol": protocol, "countryCode": countryCode, "locale": locale}
    headers = {
        "Cookie": cookie,
        "referer": "https://my.cyberghostvpn.com/fr_FR/download-hub/other/add-other?",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest"
    }
    response = requests.post(url_server_groups, headers=headers, data=form)

    # code
    print(response.status_code)
    response_unicode = response.text.encode('latin1').decode('unicode_escape')
    return json.dumps(json.loads(response_unicode), sort_keys=True, ensure_ascii=False)

"""
# add-other :
protocol: openvpn
country: AD
server_group: 87-1
device_name: test
locale: fr_FR
"""

def get_vpn(protocol, countryCode, server_group, device_name, locale, cookie):
    form = {"protocol": protocol, "country": countryCode, "server_group": server_group, "device_name": device_name, "locale": locale}
    headers = {
        "Cookie": cookie,
        "referer": "https://my.cyberghostvpn.com/fr_FR/download-hub/other/add-other?",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest"
    }
    response = requests.post(url_vpn, headers=headers, data=form)
    print(response.status_code)
    response_unicode = response.text.encode('latin1').decode('unicode_escape')
    return json.dumps(json.loads(response_unicode), sort_keys=True, ensure_ascii=False)

"""  get request :
https://my.cyberghostvpn.com/devices/download-config/232044442
returns a zip file
"""

def download_zip(name, id):
    headers = {
        "Cookie": cookie,
        "referer": "https://my.cyberghostvpn.com/fr_FR/download-hub/other/add-other?",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest"
    }
    response = requests.get(url_download + str(id), headers=headers)
    print(response.status_code)
    # print(response.text)
    # convert characters like \u00c9 to É
    # download zip
    zip_path = default_vpn_path + name
    with open(zip_path+ ".zip", 'wb') as f:
        f.write(response.content)
    return zip_path

# create instance
win = tk.Tk()
# add logo cyberopenvpn64.png
icon = PhotoImage(file="cyberopenvpn64.png")
win.iconphoto(False, icon)

try:
    import sv_ttk
    import darkdetect
    # get system theme

    if (darkdetect.isDark()):
        sv_ttk.set_theme("dark")
        try:
            #windows title bar
            if platform.system() == "Windows":
                import ctypes as ct
                def dark_title_bar(window):
                    """
                    MORE INFO:
                    https://docs.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmapi-dwmwindowattribute
                    """
                    #window.update()
                    hwnd = ct.windll.user32.GetParent(window.winfo_id())
                    rendering_policy = 20 #DWMWA_USE_IMMERSIVE_DARK_MODE
                    value = ct.c_int(2)
                    ct.windll.dwmapi.DwmSetWindowAttribute(hwnd, rendering_policy, ct.byref(value), ct.sizeof(value))
            dark_title_bar(win)
        except:
            pass
    else:
        sv_ttk.set_theme("light")
    # set default internal margin to 5, up, down, left, right
    ttk.Style().configure(".", padding=(5, 10, 5, 10))
    
    


except:
    print("no theme installed, using default")
    pass
win.title("VPN selector")
# let the user select the language and protocol
# create a container to hold labels
Frame1 = ttk.LabelFrame(win, text='Cookie and Locale')
Frame1.grid(column=0, row=0, padx=10, pady=10, sticky='WNSE')

# create an entry box to enter the cookie
ttk.Label(Frame1, text="Cookie:").grid(column=0, row=0, sticky='W')
cookie_text = tk.StringVar()
cookieEntered = ttk.Entry(Frame1, width=40, textvariable=cookie_text)
cookieEntered.grid(column=1, row=0, sticky='W', columnspan=2)
# default_conf.cookie as current value
cookieEntered.insert(0, cookie)


# create a combobox to choose the locale
ttk.Label(Frame1, text="Locale:").grid(column=0, row=2, sticky='W')
locale_text = tk.StringVar()
localeChosen = ttk.Combobox(Frame1, width=18,
                            textvariable=locale_text, state='readonly')
localeChosen['values'] = list(locales.values())
localeChosen.grid(column=1, row=2)
localeChosen.set(locales[locale])

def try_entries():
    try_status.set("Updating...")
    win.update()
    # get countries
    try:
        global countries
        countries = get_countries(
            list(protocols.keys())[protocolChosen.current()], list(locales.keys())[localeChosen.current()], cookieEntered.get())
        """[
            {"countrycode": "AD", "name": "Andorre"},
            {"countrycode": "AE", "name": "Émirats arabes unis"},
            {"countrycode": "AL", "name": "Albanie"},"""
        countryChosen['values'] = [country["name"]
                           for country in json.loads(countries)]
    except Exception as e:
        save_button.state(['disabled'])
        try_status.set("Error ❌")
        print(e)
        mBox.showerror(
            'Error', 'Check cookie, locale or protocol : \n' + str(e))
        return
    save_button.state(['!disabled'])
    countryChosen.state(['!disabled'])
    try_status.set("Success ✔️")

# add a button
try_button = ttk.Button(Frame1, text="Update", command=try_entries)
try_button.grid(column=0, row=3)

try_status = tk.StringVar()
try_status.set("Not tried")
ttk.Label(Frame1, textvariable=try_status).grid(
    column=1, row=3, sticky='E')

# add a save button
def save_entries():
    save_status.set("Saving...")
    win.update()
    # override the default_conf.py file with the new values
    # create a backup of the file
    if os.path.isfile(default_conf_path+".old"):
        shutil.copyfile(default_conf_path, default_conf_path+".old")
    # override the file
    with open(default_conf_path, 'w') as file:
        file.write("# Path: default_conf.py\n")
        file.write("# This file is generated by the GUI\n")
        file.write("cookie = \"" + cookieEntered.get() + "\"\n")
        file.write("protocol = \"" + list(protocols.keys())
                   [list(protocols.values()).index(protocolChosen.get())] + "\"\n")
        file.write("locale = \"" + list(locales.keys())
                   [list(locales.values()).index(localeChosen.get())] + "\"\n")
    save_status.set("Saved ✔️")
    # disable the button
    save_button.state(['disabled'])

save_button = ttk.Button(Frame1, text="Save", command=save_entries)
save_button.grid(column=0, row=4)
save_button.state(['disabled'])

save_status = tk.StringVar()
save_status.set("Unknown ...")
ttk.Label(Frame1, textvariable=save_status).grid(
    column=1, row=4, sticky='E')

# new frame for the countries, and more
FrameServer = ttk.LabelFrame(win, text='Server')
FrameServer.grid(column=1, row=0, padx=10, pady=10, sticky='WNSE')

# create a combobox to choose the protocol
ttk.Label(FrameServer, text="Protocol:").grid(column=0, row=0, sticky='W')
protocol_text = tk.StringVar()
protocolChosen = ttk.Combobox(
    FrameServer, width=18, textvariable=protocol_text, state='readonly')
protocolChosen['values'] = list(protocols.values())
protocolChosen.grid(column=1, row=0)
# default_conf.protocol as current value
protocolChosen.set(protocols[protocol])
protocolChosen.bind("<<ComboboxSelected>>", lambda e: protocolChosen_changed())

def protocolChosen_changed():
    countryChosen.state(['disabled'])
    server_groupChosen.state(['disabled'])
    try_status.set("")
    try_entries()
    check_config()
    
# create a combobox to choose the country
ttk.Label(FrameServer, text="Country:").grid(column=0, row=1, sticky='W')
country_text = tk.StringVar()
countryChosen = ttk.Combobox(
    FrameServer, width=18, textvariable=country_text, state='readonly')
# countries is a json as :
# [{"countrycode": "AD", "name": "Andorre"}, {"countrycode": "AE", "name": "Émirats arabes unis"}, {"countrycode": "AL", "name": "Albanie"}, {"countrycode": "AM", "name": "Arménie"},

countryChosen['values'] = [country["name"]
                           for country in json.loads(countries)]
countryChosen.grid(column=1, row=1)
# countryChosen.current(0)

def on_country_change():
    # get the country code
    global country_code, server_groups
    country_code = [country["countrycode"] for country in json.loads(
        countries) if country["name"] == countryChosen.get()][0]
    # get the servers
    try:
        server_groups = get_server_groups(list(protocols.keys())[list(protocols.values()).index(protocolChosen.get())], country_code,
                                          list(locales.keys())[list(locales.values()).index(localeChosen.get())], cookieEntered.get())
        print(server_groups)
        #[{"NAME": "Premium Servers - OpenVPN via TCP", "configsId": "97", "groupsId": "1"}]
    except Exception as e:
        # error
        print(e)
        mBox.showerror(
            'Error', 'Please run connection test.\n Maybe wrong country code? \n' + str(e))
        return
    # add the server groups to the combobox
    server_groupChosen['values'] = [server_group["NAME"]
                                    for server_group in json.loads(server_groups)]
    server_groupChosen.state(['!disabled'])
    if len(server_groupChosen['values']) == 1:
        server_groupChosen.current(0)
        set_config_domain(0)
    else:
        # clear the group combobox
        server_groupChosen.set("")
    check_config()
    
def set_config_domain(i):
    global configsId, groupsId, configname
    configsId = json.loads(server_groups)[i]["configsId"],
    groupsId = json.loads(server_groups)[i]["groupsId"],
    configname = configsId[0]+"-"+groupsId[0]+"-"+country_code.lower()
    config_domain_text.set(configname +".cg-dialup.net")    
    Button_download.state(['!disabled'])  
    check_config()
    
countryChosen.bind("<<ComboboxSelected>>", lambda e: on_country_change())

# create a combobox to choose the server group
ttk.Label(FrameServer, text="Server group:").grid(column=0, row=2, sticky='W')
server_group_text = tk.StringVar()
server_groupChosen = ttk.Combobox(
    FrameServer, width=52, textvariable=server_group_text, state='readonly')
server_groupChosen.grid(column=1, row=2)
server_groupChosen.state(['disabled'])
server_groupChosen.bind("<<ComboboxSelected>>", lambda e: set_config_domain(server_groupChosen.current()))

# config domain
# THIS IS A SUPPOSITION, NOTHING IS WRITTEN ABOUT IT, but i seems to work
# configsId-groupsId-countrycode.cg-dialup.net
# ex : 97-1-ad.cg-dialup.net

ttk.Label(FrameServer, text="Config domain:").grid(column=0, row=3, sticky='W')
config_domain_text = tk.StringVar()
config_domain_text.set("**-*-*.cg-dialup.net")
# this text is selectable, but not editable
config_domain = ttk.Entry(FrameServer, width=20, textvariable=config_domain_text,
                            state='readonly')
config_domain.grid(column=1, row=3)

# Frame for OpenVPN File
FrameFile = ttk.LabelFrame(win, text='OpenVPN File editor:')
FrameFile.grid(column=0, row=1, padx=10, pady=10, sticky='WNSE')

# create a text box to ask for the file name
# default : VPN_Selector
ttk.Label(FrameFile, text="Device name:").grid(column=0, row=0, sticky='W')
file_name_text = tk.StringVar()
file_name_text.set("VPN_Selector")
file_name = ttk.Entry(FrameFile, width=21, textvariable=file_name_text)
file_name.grid(column=1, row=0)

def download_file():
    # check if the file name is valid
    if file_name_text.get() == "":
        mBox.showerror('Error', 'Please enter a file name.')
        return
    
    #request the file
    try:
        device_name = file_name_text.get()
        vpn_data = get_vpn(list(protocols.keys())[
                            # protocol, country_code
                            list(protocols.values()).index(protocolChosen.get())], country_code,
                            # server_group
                            configsId[0]+"-"+groupsId[0],
                            # device name
                            device_name,
                            # locale
                            list(locales.keys())[list(locales.values()).index(localeChosen.get())],
                            # cookie
                            cookieEntered.get())
        """
        {   "configuration": {"country": "AE", "protocol": "openvpn_tcp", "serverGroup": "97-1"},
            "createdAt": "2023-03-16 22:21:22",
            "id": 232044806,
            "name": "VPN_Selector",
            "oauthConsumers": 
            {
                "accesslevel": 1,
                "active": 1,
                "appName": "Linux, Router etc.",
                "deviceType": "other",
                "domains": null,
                "id": 10, 
                "isInternal": 0,
                "partners_id": 1
                },
            "token": "e7tPcDwkEe",
            "tokenSecret": "Y5ARvmSgWz"}
        """
        vpn_data = json.loads(vpn_data)
        user = vpn_data["token"]
        password = vpn_data["tokenSecret"]
        id = vpn_data["id"]
        print("user: "+user, "password: "+password, "id: "+str(id))
    except Exception as e:
        # error
        print(e)
        mBox.showerror(
            'Error', 'Please run connection test.\n Maybe name already used, or too many devices ? \n' + str(e))
        return
    zip_path = download_zip(device_name, id)

    # extract zip

    with zipfile.ZipFile(zip_path + ".zip", 'r') as zip_ref:
        zip_ref.extractall(zip_path)

    try:
        #oncatenate(inpath, ovpn_file = "openvpn.ovpn", user = None, password = None, output = None, outpath = None):
        vpn_file_concatenator.concatenate(
            zip_path,
            user = user,
            password = password, 
            output =configname + "_base.ovpn", 
            outpath = default_vpn_path + "VPN_concatenated")
        
        #delete the zip file and extracted folder
        os.remove(zip_path + ".zip")
        shutil.rmtree(zip_path)

        # fill the text box with the file path
        filepath_text.set(default_vpn_path + "VPN_concatenated/" + configname + "_base.ovpn")
        
    #print error and its traceback
    except Exception as e:
        print(e)
        mBox.showerror(
            'Error', 'Concatenation failed. \n' + str(e))
        #print error and its  traceback
        return
    check_config()
        

    

#add a button to download the file
Button_download = ttk.Button(FrameFile, text="Download", command=download_file)
Button_download.grid(column=2, row=0, sticky='W')
# disable the button
Button_download.state(['disabled'])

def check_config():
    global source_server, source_protocol, dest_server, dest_protocol
    # update texts of server_text and protocol_text
    if os.path.isfile(filepath_text.get()):
        #source_server and source_protocol
        with open(filepath_text.get(), 'r') as f:
            for line in f:
                if line.startswith('remote '):
                    source_server = line.split(' ')[1].split('.')[0]
                if line.startswith('proto '):
                    source_protocol = line.split(' ')[1][:-1]
    if protocolChosen.current() != -1:
        #if tcp is contained in the protocol, then the protocol is tcp, else it is udp
        if 'tcp' in protocolChosen.get().lower():
            dest_protocol = 'tcp'
        elif 'ipsec' in protocolChosen.get().lower():
            dest_protocol = ''
        else:
            dest_protocol = 'udp'
        #get the server name
    if server_groupChosen.current() != -1:
        dest_server = configname
    #update the text
    source_server_text.set(source_server)
    source_protocol_text.set(source_protocol)
    dest_server_text.set(dest_server)
    dest_protocol_text.set(dest_protocol)

    # check if the file exists
    if not os.path.isfile(filepath_text.get()):
        Button_create.state(['disabled'])
        pass
    #check if the server group is selected
    elif server_groupChosen.current() == -1:
        Button_create.state(['disabled'])
        pass
    else:
        Button_create.state(['!disabled'])
    
def open_file():
    # open file dialog
    filename = filedialog.askopenfilename(
        initialdir=default_vpn_path,
        title="Select a File",
        filetypes=(("OpenVPN files", "*.ovpn"), ("all files", "*.*")))
    # update the text box
    filepath_text.set(filename)
    #enable the button if the file exists
    check_config()

# button to open VPN file
ttk.Label(FrameFile, text="OpenVPN file:").grid(column=0, row=1, sticky='W')
filepath_text = tk.StringVar()
filepath_text.set("")
filepath = ttk.Entry(FrameFile, width=21, textvariable=filepath_text,)
filepath.grid(column=1, row=1)
# add event to check if the file exists
filepath.bind("<KeyRelease>", lambda e: check_config())

ttk.Button(FrameFile, text="Open", command=open_file).grid(column=2, row=1, sticky='W')

# frame for modifications
FrameModif = ttk.LabelFrame(text="File modifications")
FrameModif.grid(column=1, row=1,  padx=10, pady=10, sticky='WNSE')

# button to create a new file, by editing the current one (if it exists)
def create_file():
    # check if the file exists
    if not os.path.isfile(filepath_text.get()):
        mBox.showerror(
            'Error', 'Please open a file.')
        return
    # check if the server group is selected
    if server_groupChosen.current() == -1:
        mBox.showerror(
            'Error', 'Please select a server group.')
        return
    # read the current file
    with open(filepath_text.get(), 'r') as f:
        dest_path = filepath_text.get()[:-len(filepath_text.get().split('/')[-1])] + dest_server_text.get() + "_new.ovpn"
        with open(dest_path, 'w') as new_f:
            for line in f:
                # change the server name
                if line.startswith('remote '):
                    new_f.write('remote ' + config_domain_text.get() + ' ' + line.split(' ')[-1])
                # change the protocol
                elif line.startswith('proto '):
                    new_f.write('proto ' + dest_protocol + '\n')
                else:
                    new_f.write(line)
    if CheckbuttonOpenFile.state() == ('selected',):
        #open the new file with a system app
        if platform.system() == 'Darwin':       # macOS
            subprocess.call(('open', dest_path))
        elif platform.system() == 'Windows':    # Windows
            os.startfile(dest_path)
        else:                                   # linux variants
            subprocess.call(('xdg-open', dest_path))

# button to create a new file, by editing the current one (if it exists)
Button_create = ttk.Button(FrameModif, text="Create new file with current configuration", command=create_file)
Button_create.grid(column=0, row=4, columnspan=4)
# disable the button
Button_create.state(['disabled'])

# text to display the differences between the current file and the new one
ttk.Label(FrameModif, text="server:").grid(column=0, row=2, sticky='W')
source_server_text = tk.StringVar()
source_server_text.set("")
dest_server_text = tk.StringVar()
dest_server_text.set("")
Label_source_server = ttk.Label(FrameModif, width=20, textvariable=source_server_text)
Label_dest_server = ttk.Label(FrameModif, width=20, textvariable=dest_server_text)
Label_source_server.grid(column=1, row=2, columnspan=2, sticky='W')
Label_dest_server.grid(column=3, row=2, columnspan=2, sticky='W')
ttk.Label(FrameModif, text="→", width=2).grid(column=2, row=2)

ttk.Label(FrameModif, text="protocol:").grid(column=0, row=3, sticky='W')
source_protocol_text = tk.StringVar()
source_protocol_text.set("")
dest_protocol_text = tk.StringVar()
dest_protocol_text.set("")
Label_source_protocol = ttk.Label(FrameModif, width=4, textvariable=source_protocol_text)
Label_dest_protocol = ttk.Label(FrameModif, width=4, textvariable=dest_protocol_text)
Label_source_protocol.grid(column=1, row=3, columnspan=2, sticky='W')
Label_dest_protocol.grid(column=3, row=3, columnspan=2, sticky='W')
ttk.Label(FrameModif, text="→", width=2).grid(column=2, row=3)

#checkbox for automatic opening of the new file
open_file_var = tk.IntVar()
open_file_var.set(1)
CheckbuttonOpenFile = ttk.Checkbutton(FrameModif, text="Open the new file automatically", variable=open_file_var)
CheckbuttonOpenFile.grid(column=0, row=5, columnspan=4)

win.update()

try:
    countries = get_countries(default_conf.protocol,
                              default_conf.locale, default_conf.cookie)
    # print(countries)
    save_status.set("Already saved✔️")
    try_status.set("Updated ✔️")
except Exception as e:
    save_status.set("Not saved❌")
    print(e)

# display the window
win.mainloop()