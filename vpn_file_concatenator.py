import os

def concatenate(inpath, ovpn_file = "openvpn.ovpn", user = None, password = None, output = None, outpath = None):
    """Concatenate the VPN files into one file.
    Args:
        path (str): The path to the directory containing the VPN files.
        vpn_file (str): The name of the VPN file.
        user (str): The username to authenticate with.
        password (str): The password to authenticate with.
    Returns:
        str: The path to the concatenated VPN file.
    """

    if outpath is None:
        outpath = inpath

    if output is None:
        if inpath == outpath:
            output = "openvpn_full.ovpn"
        else :
            output = "openvpn.ovpn"
    
    # create outpath if it doesn't exist
    if not os.path.exists(outpath):
        os.makedirs(outpath)

    if user is not None and password is not None:
        print("Using username and password authentication.")

    vpn_file_path = os.path.join(inpath, ovpn_file)
    with open(vpn_file_path, "r") as ovpn_file:
        with open(os.path.join(outpath, output), "w") as output_file:
            for line in ovpn_file:
                if line.startswith("auth-user-pass") and user is not None and password is not None:
                    output_file.write("auth-user-pass " + "auth.txt" + "\n")
                    with open(os.path.join(outpath, "auth.txt"), "w") as auth_file:
                        auth_file.write(user + "\n")
                        auth_file.write(password)
                elif line.startswith("ca "):
                    with open(os.path.join(inpath, "ca.crt"), "r") as ca_file:
                        ca_file_contents = ca_file.read()
                        output_file.write("<ca>\n" + ca_file_contents + "</ca>\n")

                elif line.startswith("cert "):
                    with open(os.path.join(inpath, "client.crt"), "r") as cert_file:
                        cert_file_contents = cert_file.read()
                        output_file.write("<cert>\n" + cert_file_contents + "</cert>\n")
                elif line.startswith("key "):
                    with open(os.path.join(inpath, "client.key"), "r") as key_file:
                        key_file_contents = key_file.read()
                        output_file.write("<key>\n" + key_file_contents + "</key>\n")
                else:
                    output_file.write(line)
    return os.path.join(inpath, output)
    
# default main function running if executed, and not imported
if __name__ == "__main__":
    print("Concatenating VPN files...")
    concatenate("VPN_Selector", user = "user_test", password = "password_test", outpath = "VPN_Test", output = "openvpn_test.ovpn")