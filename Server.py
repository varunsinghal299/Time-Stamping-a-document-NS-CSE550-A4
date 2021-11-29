import socket
import datetime
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

public_key_server =  (114319815123858897694909, 317110937638372124355851)
private_key_server =  (273887013010879996742389, 317110937638372124355851)
public_key_client =  (74594497642439042403421, 79292053079056066600697)

IP = socket.gethostbyname(socket.gethostname())
PORT = 4455
ADDR = (IP, PORT)
SIZE = 65536
FORMAT = "utf-8"

def main():
    print("[STARTING] Server is starting.")
    """ Staring a TCP socket. """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    """ Bind the IP and PORT to the server. """
    s.bind(ADDR)

    """ Server is listening, i.e., server is now waiting for the client to connected. """
    s.listen()
    print("[LISTENING] Server is listening.")

    while True:
        """ Server has accepted the connection from the client. """
        conn, addr = s.accept()
        print(f"[NEW CONNECTION] {addr} connected.")


        """ Receiving the file data from the client. """
        data = conn.recv(SIZE).decode(FORMAT)
        print(f"[RECV] Receiving the file data.")
        #file.write(data)

        gmt_time = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%Z")
        # gmt_time = str(gmt_time)
        gmt_time = encrypt(gmt_time, public_key_client)

        data = data + " " +str(gmt_time[0])
        for i in range(1, len(gmt_time)):
            data += " " + str(gmt_time[i])


        list_data = data.split(" ")

        # hashvalue = str(hashlib.sha1(data).hexdigest())
        hash_object = hashlib.sha256(str(data).encode('utf-8'))
        hashvalue = hash_object.hexdigest()

        hashvalue_encrpyt = encrypt(hashvalue, private_key_server)

        hash_added = str(hashvalue_encrpyt[0])
        for i in range(1, len(hashvalue_encrpyt)):
            hash_added += " " + str(hashvalue_encrpyt[i])

        actual_data = data + "$" + hash_added

        print(actual_data)
        conn.send(actual_data.encode(FORMAT))
        print("actual data length -> ",len(actual_data))

        conn.close()
        print(f"[DISCONNECTED] {addr} disconnected.")

if __name__ == "__main__":
    main()