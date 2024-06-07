import subprocess

keys_file = open("recovery_keys_dump.txt", "r")
keys = keys_file.readlines()

for key in keys:
    key = key.replace("\n", "")
    output = subprocess.run(['sudo', 'dislocker', '-V', '/dev/loop1', '-p'+key, '/media/encrypted_usb'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    if output.find("Abort") == -1:
        print("Found Key: " + key)