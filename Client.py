import socket
import hashlib

def decrypt(ctext, private_key):
    try:
        key, n = private_key
        text = [chr(pow(char, key, n)) for char in ctext]
        return "".join(text)
    except TypeError as e:
        print(e)


def encrypt(text, public_key):
    key, n = public_key
    ctext = [pow(ord(char), key, n) for char in text]
    return ctext

public_key_client =  (74594497642439042403421, 79292053079056066600697)
private_key_client =  (37315076390064917859001, 79292053079056066600697)
public_key_server =  (114319815123858897694909, 317110937638372124355851)

IP = socket.gethostbyname(socket.gethostname())
PORT = 4455
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 65536

def main():
    """ Staring a TCP socket. """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    """ Connecting to the server. """
    s.connect(ADDR)

    """ Opening and reading the file data. """
    file = open("yt.txt", "r")
    data = file.read()

    """ encrpyt data of file"""
    encrypt_data = encrypt(data, public_key_client)

    print(encrypt_data)
    """ Sending the file data to the server. """
    data_str = str(encrypt_data[0])
    for i in range(1, len(encrypt_data)):
        data_str += " "+ str(encrypt_data[i])

    s.send(data_str.encode(FORMAT))

    msg = s.recv(65536).decode(FORMAT)
    print(f"[SERVER]: {msg}")
    print("receive data length -> ", len(msg))

    cipher_data = msg.split("$")
    gmt_data = cipher_data[0]
    hash_data = cipher_data[1]

    gmt_data_split = gmt_data.split(" ")
    new_gmt_data = []
    for i in gmt_data_split:
        new_gmt_data.append(int(i))

    hash_data = hash_data.split(" ")
    new_hash_data = []
    for i in hash_data:
        new_hash_data.append(int(i))

    gmt_data_decrpyt = decrypt(new_gmt_data, private_key_client)
    hash_data_decrpyt = decrypt(new_hash_data, public_key_server)

    hash_object = hashlib.sha256(str(gmt_data).encode('utf-8'))
    hashvalue = hash_object.hexdigest()

    if hashvalue == hash_data_decrpyt:
        print("digital signature Verify , Authenticated")
        print(gmt_data_decrpyt)

        text_file = open("Output.txt", "w")
        text_file.write(gmt_data_decrpyt)
        text_file.close()


    else:
        print("Not Authenticated")


    print("Thank you.....")
    """ Closing the file. """
    file.close()

    """ Closing the connection from the server. """
    s.close()


if __name__ == "__main__":
    main()
