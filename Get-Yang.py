from ncclient import manager

def get_schema(module_name, output_file):
    with manager.connect(
        host="192.168.220.128",
        port=830,
        username="cisco",
        password="cisco123!",
        hostkey_verify=False,
        device_params={'name': 'iosxe'},
        allow_agent=False,
        look_for_keys=False,
    ) as m:

        # Issue a <get-schema> operation to retrieve the YANG module
        result = m.get_schema(module_name)

        # Save the YANG model to a file
        with open(output_file, "w") as yang_file:
            yang_file.write(result.data)

if __name__ == "__main__":
    # Specify the module name for the native container
    module_name = "Cisco-IOS-XE-native"

    # Specify the output file name
    output_file = "yang_model_output.yang"

    get_schema(module_name, output_file)
