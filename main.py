from tkinter import messagebox as mBox
from tkinter import Spinbox
from tkinter import Menu
from tkinter import scrolledtext
from tkinter import ttk
import tkinter as tk
import json
import requests
default_conf_path = "default_conf.py"

domain = "https://my.cyberghostvpn.com/"
api = "api/devices/"
url_countries = domain + api + "get-server-countries"
url_server_groups = domain + api + "get-server-groups"
# let the user choose the country in a GUI


protocols = {"openvpn": "Open VPN", "openvpn_tcp": "Open VPN TCP",
             "openvpn_legacy": "Open VPN <= 2.3", "openvpn_tcp_legacy": "Open VPN TCP <= 2.3", "ipsec": "IPsec"}
# may be more locales
locales = {"en_US": "English", "de_DE": "Deutsch", "fr_FR": "Français", "es_ES": "Español",
           "it_IT": "Italiano", "pt_PT": "Português", "ru_RU": "Русский", "pl_PL": "Polski", "nl_NL": "Nederlands"}

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


# create instance
win = tk.Tk()
win.title("VPN slector")
# let the user select the language and protocol
# create a container to hold labels
labelsFrame = ttk.LabelFrame(win, text='Cookie, locale, protocol')
labelsFrame.grid(column=0, row=0, padx=40, pady=40)

# create an entry box to enter the cookie
ttk.Label(labelsFrame, text="Cookie:").grid(column=0, row=0, sticky='W')
cookie_text = tk.StringVar()
cookieEntered = ttk.Entry(labelsFrame, width=18, textvariable=cookie_text)
cookieEntered.grid(column=1, row=0)
# default_conf.cookie as current value
cookieEntered.insert(0, cookie)

# create a combobox to choose the protocol
ttk.Label(labelsFrame, text="Protocol:").grid(column=0, row=1, sticky='W')
protocol_text = tk.StringVar()
protocolChosen = ttk.Combobox(
    labelsFrame, width=18, textvariable=protocol_text, state='readonly')
protocolChosen['values'] = list(protocols.values())
protocolChosen.grid(column=1, row=1)
# default_conf.protocol as current value
protocolChosen.set(protocols[protocol])
protocolChosen.bind("<<ComboboxSelected>>", lambda e: diable_coutry_choice())

def diable_coutry_choice():
    countryChosen.state(['disabled'])
    server_groupChosen.state(['disabled'])
    try_status.set("")

# create a combobox to choose the locale
ttk.Label(labelsFrame, text="Locale:").grid(column=0, row=2, sticky='W')
locale_text = tk.StringVar()
localeChosen = ttk.Combobox(labelsFrame, width=18,
                            textvariable=locale_text, state='readonly')
localeChosen['values'] = list(locales.values())
localeChosen.grid(column=1, row=2)
localeChosen.set(locales[locale])

# add "try" button


def try_entries():
    try_status.set("Updating...")
    # get countries
    try:
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
        mBox.showerror(
            'Error', 'Check cookie, locale or protocol : \n' + str(e))
        return
    save_button.state(['!disabled'])
    countryChosen.state(['!disabled'])
    try_status.set("Success ✔️")


# add a button
try_button = ttk.Button(labelsFrame, text="Update", command=try_entries)
try_button.grid(column=0, row=3)

try_status = tk.StringVar()
try_status.set("Not tried")
ttk.Label(labelsFrame, textvariable=try_status).grid(
    column=1, row=3, sticky='E')


# add a save button
def save_entries():
    save_status.set("Saving...")
    # override the default_conf.py file with the new values
    import os
    import shutil
    # delay
    import time
    # create a backup of the file
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


save_button = ttk.Button(labelsFrame, text="Save", command=save_entries)
save_button.grid(column=0, row=4)
save_button.state(['disabled'])

save_status = tk.StringVar()
try:
    countries = get_countries(default_conf.protocol,
                              default_conf.locale, default_conf.cookie)
    # print(countries)
    save_status.set("Already saved✔️")
except Exception as e:
    save_status.set("Not saved❌")
ttk.Label(labelsFrame, textvariable=save_status).grid(
    column=1, row=4, sticky='E')


# new frame for the countries, and more
labelsFrame2 = ttk.LabelFrame(win, text='Countries')
labelsFrame2.grid(column=1, row=0, padx=40, pady=40)

# create a combobox to choose the country
ttk.Label(labelsFrame2, text="Country:").grid(column=0, row=0, sticky='W')
country_text = tk.StringVar()
countryChosen = ttk.Combobox(
    labelsFrame2, width=18, textvariable=country_text, state='readonly')
# countries is a json as :
# [{"countrycode": "AD", "name": "Andorre"}, {"countrycode": "AE", "name": "Émirats arabes unis"}, {"countrycode": "AL", "name": "Albanie"}, {"countrycode": "AM", "name": "Arménie"},

countryChosen['values'] = [country["name"]
                           for country in json.loads(countries)]
countryChosen.grid(column=1, row=0)
# countryChosen.current(0)


def on_country_change():
    # get the country code
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
        mBox.showerror(
            'Error', 'Please run connection test.\n Maybe wrong country code? \n' + str(e))
        return
    # add the server groups to the combobox
    server_groupChosen['values'] = [server_group["NAME"]
                                    for server_group in json.loads(server_groups)]
    server_groupChosen.state(['!disabled'])
    if len(server_groupChosen['values']) == 1:
        server_groupChosen.current(0)
        configsId = json.loads(server_groups)[0]["configsId"],
        groupsId = json.loads(server_groups)[0]["groupsId"],
        config_domain_text.set(
            # configsId-groupsId-countrycode.cg-dialup.net
            configsId[0]+"-"+groupsId[0]+"-"+country_code.lower()+".cg-dialup.net")
        
countryChosen.bind("<<ComboboxSelected>>", lambda e: on_country_change())

# create a combobox to choose the server group
ttk.Label(labelsFrame2, text="Server group:").grid(column=0, row=1, sticky='W')
server_group_text = tk.StringVar()
server_groupChosen = ttk.Combobox(
    labelsFrame2, width=52, textvariable=server_group_text, state='readonly')
server_groupChosen.grid(column=1, row=1)

# config domain
# THIS IS A SUPPOSITION, NOTHING IS WRITTEN ABOUT IT, but i seems to work
# configsId-groupsId-countrycode.cg-dialup.net
# ex : 97-1-ad.cg-dialup.net

ttk.Label(labelsFrame2, text="Config domain:").grid(column=0, row=2, sticky='W')
config_domain_text = tk.StringVar()
config_domain_text.set("**-*-*.cg-dialup.net")
# this text is selectable, but not editable
config_domain = ttk.Entry(labelsFrame2, width=20, textvariable=config_domain_text,
                            state='readonly')
config_domain.grid(column=1, row=2)






# display the window
win.mainloop()
