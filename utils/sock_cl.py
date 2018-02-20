import cv2
import socket
import numpy as np
from .rec import pred

def main():
    s = socket.socket()
    host = '192.168.1.222'
    port = 8000
    print(host)
    s.connect((host, port))
    print(s.recv(1024).decode('ascii'))
    print(s.recv(1024).decode('ascii'))
    # data = s.recv(16589)
    data = b''
    # print(data)
    with open('temp.npy', 'wb') as np_file:
        while True:
            rec = s.recv(4096)
            if not rec:
                break
            print('receiving data')
            data += rec
        print('write file')
        np_file.write(data)

    # load = np.load('temp.npy')
    # for i in load[()].keys():
    #     cv2.imshow('crop', load[()][i])
    #     cv2.waitKey(0)

    # 11print(s.recv(1024).decode('ascii'))
    s.close()

    placement = pred('temp.npy')
    # print(placement)
    return placement

if __name__ == "__main__":
    main()