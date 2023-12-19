from ncclient import manager
import xml.dom.minidom

# Cisco router NETCONF parameters
HOST = "192.168.220.128"
PORT = 830
USERNAME = "cisco"
PASSWORD = "cisco123!"

def get_running_config(connection, output_file="running_config.xml"):
    # Specify the target datastore (running config)
    datastore = "running"

    # NETCONF filter for the entire configuration
    netconf_filter = """
        <filter>
            <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native"/>
        </filter>
    """

    # Retrieve the running configuration
    running_config = connection.get_config(source=datastore, filter=netconf_filter).xml

    # Prettify and write the XML content to a file
    with open(output_file, "w") as file:
        file.write(xml.dom.minidom.parseString(running_config).toprettyxml())

    print(f"Running Configuration saved to {output_file}")

if __name__ == "__main__":
    with manager.connect(
        host=HOST,
        port=PORT,
        username=USERNAME,
        password=PASSWORD,
        hostkey_verify=False,
    ) as m:
        # Get and save the running configuration as an XML file
        get_running_config(m)
