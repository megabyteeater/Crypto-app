import cv2
import numpy as np


def Binary_convertor(msg):
    if type(msg) == str:
        return ''.join([format(ord(i), "08b") for i in msg])
    elif type(msg) == bytes or type(message) == np.ndarray:
        return [format(i, "08b") for i in msg]
    elif type(msg) == int or type(msg) == np.uint8:
        return format(msg, "08b")
    else:
        raise TypeError("Input type not supported")


def hide_data(img, sec_msg):
    # Max Byte
    n_bytes = img.shape[0] * img.shape[1] * 3 // 8
    print("Maximum bytes to encode:", n_bytes)

    # Check if the number of bytes to encode is less than the maximum bytes in the image
    if len(sec_msg) > n_bytes:
        raise ValueError("Error encountered insufficient bytes, need bigger image or less data !!")

    sec_msg += "$t3g0"  #delimeter

    index = 0
    # convert input data to binary format
    bin_sec_msg = Binary_convertor(sec_msg)

    data_len = len(bin_sec_msg)  # Find the length of data that needs to be hidden
    for values in img:
        for pixel in values:
            # convert RGB values to binary format
            r, g, b = Binary_convertor(pixel)
            # modify the least significant bit only if there is still data to store
            if index < data_len:
                # hide the data into least significant bit of red pixel
                pixel[0] = int(r[:-1] + bin_sec_msg[index], 2)
                index += 1
            if data_index < data_len:
                # hide the data into least significant bit of green pixel
                pixel[1] = int(g[:-1] + bin_sec_msg[index], 2)
                index += 1
            if index < data_len:
                # hide the data into least significant bit of  blue pixel
                pixel[2] = int(b[:-1] + bin_sec_msg[index], 2)
                index += 1
            # if data is encoded, just break out of the loop
            if index >= data_len:
                break

    return img


def present_data(img):
    binary_data = ""
    for values in img:
        for pixel in values:
            r, g, b = Binary_convertor(pixel)  # convert the red,green and blue values into binary format
            binary_data += r[-1]  # extracting data from the least significant bit of red pixel
            binary_data += g[-1]  # extracting data from the least significant bit of red pixel
            binary_data += b[-1]  # extracting data from the least significant bit of red pixel
    # split by 8-bits
    all_bytes = [binary_data[i: i + 8] for i in range(0, len(binary_data), 8)]
    # convert from bits to characters
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-5:] == "$t3g0":  # check if we have reached the delimeter which is "#####"
            break
    # print(decoded_data)
    return decoded_data[:-5]  # remove the delimeter to show the original hidden message


def encode_text():
    image_name = input("Enter image name(with extension): ")
    image = cv2.imread(image_name)  # Read the input image using OpenCV-Python.

    # details of the image
    print("The shape of the image is: ", image.shape)  # check the shape of image to calculate the number of bytes in it
    resized_image = cv2.resize(image, (500, 500))  # resize the image as per your requirement


    data = input("Enter data to be encoded : ")
    if (len(data) == 0):
        raise ValueError('Data is empty')

    filename = input("Enter the path and name of new encoded image(with extension): ")
    encoded_image = hide_data(image,data)  # call the hideData function to hide the secret message into the selected image
    cv2.imwrite(filename, encoded_image)


def decode_text():
    # read the image that contains the hidden image
    image_name = input("Enter the path of the image to be decode (with extension) :")
    image = cv2.imread(image_name)  # read the image using cv2.imread()

    resized_image = cv2.resize(image, (500, 500))  # resize the original image as per your requirement


    text = present_data(image)
    return text


def Steganography():
    a = input("Image Steganography \n 1. Encode the data \n 2. Decode the data \n Choose Option: ")
    userinput = int(a)
    if (userinput == 1):
        print("\nEncoding....")
        encode_text()

    elif (userinput == 2):
        print("\nDecoding....")
        print("Decoded message is " + decode_text())
    else:
        raise Exception("Enter correct input")


Steganography()