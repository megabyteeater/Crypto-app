import cv2
import sys
import numpy as np
from PIL import Image
n=1
def binary(data):
    #convert data to binary format as string
    if isinstance(data,str):
        return ''.join([format(ord(i), "08b" ) for i in data])

    elif isinstance(data, bytes) or isinstance(data, np.ndarray):
        return [format(i, "08b") for i in data]
    elif isinstance(data,int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Type not supported. ")


def encode_img(img_name, secret_msg):
    #read image
    # img = Image.open(img_name, 'r')
    imag=cv2.imread(img_name)
    # img = cv2.imread(sys.argv[1])
    #max byte to encode
    # array = np.array(list(img.getdata()))
    # global n
    # if img.mode == 'RGB':
    #     n = 3
    # elif img.mode == 'RGBA':
    #     n = 4
    #
    # n_byte = array.size//n

    n_byte = imag.shape[0] * imag.shape[1] * 3 // 8

    print("[*] Maximum bytes to encode: ",n_byte)
    if len(secret_msg)>n_byte:
        raise ValueError("!!!Insufficient bytes. Need BIG image or SMALL data")
    print("[*] Encoding data...")
    #stopping criteria
    secret_msg+="===="
    data_ind=0;
    #convert data to binary
    bin_sec_msg= binary(secret_msg)
    #size of data to hide
    data_len=len(bin_sec_msg)

    for row in imag:
        for pixel in row:
            #convert rgb to binary
            r,g,b = binary(pixel)
            if data_ind<data_len:
                pixel[0]=int(r[:1] + bin_sec_msg[data_ind], 2)
                data_ind+=1
            if data_ind < data_len:
                pixel[1] = int(g[:-1] + bin_sec_msg[data_ind], 2)
                data_ind += 1
            if data_ind<data_len:
                pixel[2]=int(b[:1] + bin_sec_msg[data_ind], 2)
                data_ind+=1

            if data_ind >=data_len:
                break
    return imag


def decode_img(img_name):
    print("Decoding....")
    #read image
    img=cv2.imread(img_name)
    bin_data = ""
    for row in img:
        for pixel in row:
            r,g,b=binary(pixel)
            bin_data += r[-1]
            bin_data += g[-1]
            bin_data += b[-1]
    #split by 8-bits
    all_bytes= [bin_data[i:i+8] for i in range (0,len(bin_data), 8)]
    # conver bits to characters
    decoded_msg=""
    for byte in all_bytes:
        decoded_msg+= chr(int(byte,2))
        if decoded_msg[-5:]=="====":
            break
    return decoded_msg[:-5]

# def stego():
#     print("---> Welcome to stego <---")
#     print("1: Encode")
#     print("2: Decode")
#
#     func=input()
#
#     if func=='1':
#         print("Enter Source Image Path")
#         src =input()
#         print("Enter Message to Hide")
#         msg=input()
#         print("Enter Destination Image Path")
#         dest=input()
#         print("Encoding...")
#         encoded_img = encode_img(src,msg)
#         cv2.imwrite(dest, encoded_img())
#
#     elif func=='2':
#         print("Enter Source Image Path")
#         src = input()
#         print("Decoding..")
#         decoded_img = decode_img(src)
#         print("Decoded image :   ", decoded_img)
#     else:
#         print("Error : Invalid Option Chosen")
#
# stego()


if __name__ == "__main__":
    input_image = r'C:\Users\ASUS\PycharmProjects\test\6.jpg'
    output_image = 'encoded_image.jpg'
    secret_data = "hlo"
    # encode the data into the image
    encoded_image = encode_img(img_name=input_image, secret_msg=secret_data)
    # save the output image (encoded image)
    cv2.imwrite(output_image, encoded_image)
    # decode the secret data from the image
    decoded_data = decode_img(output_image)
    print("[+] Decoded data:", decoded_data)
