from ncclient import manager
from xml.etree import ElementTree as ET
import requests
import xml.dom.minidom

# Cisco router NETCONF parameters
HOST = "192.168.220.128"
PORT = 830
USERNAME = "cisco"
PASSWORD = "cisco123!"

def change_hostname(connection, new_hostname):
    netconf_device_name = f"""
        <config>
          <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
             <hostname>{new_hostname}</hostname>
          </native>
        </config>
    """
    print("XML for changing hostname:\n", xml.dom.minidom.parseString(netconf_device_name).toprettyxml())
    connection.edit_config(target="running", config=netconf_device_name)
    print(f"Hostname changed to: {new_hostname}")

def secure_privileged_exec(connection, enable_secret_password):
    netconf_priv_exec = f"""
        <config>
          <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
             <enable>
                <password>
                   <secret>{enable_secret_password}</secret>
                </password>
             </enable>
          </native>
        </config>
    """
    print("XML for securing privileged EXEC mode:\n", xml.dom.minidom.parseString(netconf_priv_exec).toprettyxml())
    connection.edit_config(target="running", config=netconf_priv_exec)
    print("Privileged EXEC mode secured.")

def set_motd_banner(connection, motd):
    netconf_motd = f"""
        <config>
          <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
             <banner>
                <motd>
                   <banner>{motd}</banner>
                </motd>
             </banner>
          </native>
        </config>
    """
    print("XML for setting MOTD banner:\n", xml.dom.minidom.parseString(netconf_motd).toprettyxml())
    connection.edit_config(target="running", config=netconf_motd)
    print("MOTD banner set.")


def send_webex_teams_notification(token, room_id, message):
    headers = {'Authorization': f'Bearer {token}'}
    data = {'roomId': room_id, 'text': message}
    response = requests.post('https://api.ciscospark.com/v1/messages', headers=headers, data=data)
    if response.status_code == 200:
        print("WebEx Teams notification sent successfully.")
    else:
        print(f"Failed to send WebEx Teams notification. Status code: {response.status_code}")

if __name__ == "__main__":
    with manager.connect(
        host=HOST,
        port=PORT,
        username=USERNAME,
        password=PASSWORD,
        hostkey_verify=False,
    ) as m:
        # Change the hostname
        new_hostname = "TeamNebula"
        change_hostname(m, new_hostname)

        # Secure privileged EXEC mode
        secretpass = "password123"
        secure_privileged_exec(m, secretpass)

        # Set MOTD banner
        motd_banner = "Unauthorized Access is Prohibited!"
        set_motd_banner(m, motd_banner)

        # Send WebEx Teams notification
        webex_teams_token = 'YWIwYzA4ZjItYzdmOC00ZTY1LWI0ZWQtMDQyZDRlYjE5M2ZmMTI0YWI5NTgtMTM2_P0A1_18f592ad-9e27-4e21-bdda-c79873a7f7cd'
        room_id = 'Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vY2ZmMGFlMTAtOWU2MC0xMWVlLWJlMmMtNGQ1ZWNkNTFiMGVj'
        message = (
            f"Configuration update:\n"
            f"Hostname: {new_hostname}\n"
            f"Privileged EXEC password: {secretpass}\n"
            f"MOTD Banner: {motd_banner}"
        )
        send_webex_teams_notification(webex_teams_token, room_id, message)
