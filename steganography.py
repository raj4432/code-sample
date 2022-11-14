"""
assignment: PA3
author: Raj Singh
date: 11/07/2022
file: steganography.py is a module for the cryptography program that contains the Steganography class and its methods and attributes that are used to encode and decode messages in images using different codec methods.
input: the user is prompted to choose an image file, an output image file, a message, and a codec method.
output: the user is prompted to choose an image file, an output image file, a message, and a codec method.
"""
# steganography
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from math import ceil
from codec import Codec, CaesarCypher, HuffmanCodes

class Steganography():
    
    def __init__(self):
        self.text = ''
        self.binary = ''
        self.delimiter = '#'
        self.codec = None

    def encode(self, filein, fileout, message, codec):
        image = cv2.imread(filein) # read the image
        #print(image) # for debugging
        
        # calculate available bytes
        max_bytes = image.shape[0] * image.shape[1] * 3 // 8 # number of bytes available
        print("Maximum bytes available:", max_bytes)

        # convert into binary
        if codec == 'binary':
            self.codec = Codec(delimiter = self.delimiter)
        elif codec == 'caesar':
            self.codec = CaesarCypher(delimiter = self.delimiter)
        elif codec == 'huffman':
            self.codec = HuffmanCodes(delimiter = self.delimiter)

        binary = self.codec.encode(message + self.delimiter) # add delimiter
        
        # check if possible to encode the message
        num_bytes = ceil(len(binary)//8) + 1 # number of bytes required
        if  num_bytes > max_bytes:
            print("Error: Insufficient bytes!")
        else:
            print("Bytes to encode:", num_bytes) 
            self.text = message
            self.binary = binary

            binary_split = [binary[i:i+3] for i in range(0, len(binary), 3)] # split into 3-bit chunks

            height, width, _ = image.shape # get the image dimensions

            for i in range(height): # loop through the image
                for j in range(width): 
                    try:
                        num = binary_split.pop(0) # get the next 3-bit chunk
                    except IndexError: # if there are no more chunks, break
                        break
                    
                    first_pixel = int(image[i][j][0]) # get the first pixel
                    second_pixel = int(image[i][j][1]) # get the second pixel
                    third_pixel = int(image[i][j][2]) # get the third pixel

                    if len(num) == 3: 
                        first_encoder = int(num[0])
                        second_encoder = int(num[1])
                        third_encoder = int(num[2])
                        flag = 3 # flag to indicate that all 3 pixels were encoded
                    elif len(num) == 2:
                        first_encoder = int(num[0])
                        second_encoder = int(num[1])
                        flag = 2 # flag to indicate that only the first 2 pixels were encoded
                    elif len(num) == 1:
                        first_encoder = int(num[0])
                        flag = 1 # flag to indicate that only the first pixel was encoded

                    if flag == 3: # if there are 3 bits to encode

                        if (first_pixel % 2 == 0) and (first_encoder % 2 == 0):
                            pass
                        if (first_pixel % 2 == 1) and (first_encoder % 2 == 1):
                            pass
                        if (first_pixel % 2 == 0) and (first_encoder % 2 == 1):
                            first_pixel += 1
                        if (first_pixel % 2 == 1) and (first_encoder % 2 == 0):
                            first_pixel += 1
                        
                        if (second_pixel % 2 == 0) and (second_encoder % 2 == 0):
                            pass
                        if (second_pixel % 2 == 1) and (second_encoder % 2 == 1):
                            pass
                        if (second_pixel % 2 == 0) and (second_encoder % 2 == 1):
                            second_pixel += 1
                        if (second_pixel % 2 == 1) and (second_encoder % 2 == 0):
                            second_pixel += 1

                        if (third_pixel % 2 == 0) and (third_encoder % 2 == 0):
                            pass
                        if (third_pixel % 2 == 1) and (third_encoder % 2 == 1):
                            pass
                        if (third_pixel % 2 == 0) and (third_encoder % 2 == 1):
                            third_pixel += 1
                        if (third_pixel % 2 == 1) and (third_encoder % 2 == 0):
                            third_pixel += 1


                    if flag == 2: # if there are 2 bits to encode

                        if (first_pixel % 2 == 0) and (first_encoder % 2 == 0):
                            pass
                        if (first_pixel % 2 == 1) and (first_encoder % 2 == 1):
                            pass
                        if (first_pixel % 2 == 0) and (first_encoder % 2 == 1):
                            first_pixel += 1
                        if (first_pixel % 2 == 1) and (first_encoder % 2 == 0):
                            first_pixel += 1
                        
                        if (second_pixel % 2 == 0) and (second_encoder % 2 == 0):
                            pass
                        if (second_pixel % 2 == 1) and (second_encoder % 2 == 1):
                            pass
                        if (second_pixel % 2 == 0) and (second_encoder % 2 == 1):
                            second_pixel += 1
                        if (second_pixel % 2 == 1) and (second_encoder % 2 == 0):
                            second_pixel += 1
                        
                    if flag == 1: # if there is 1 bit to encode

                        if (first_pixel % 2 == 0) and (first_encoder % 2 == 0):
                            pass
                        if (first_pixel % 2 == 1) and (first_encoder % 2 == 1):
                            pass
                        if (first_pixel % 2 == 0) and (first_encoder % 2 == 1):
                            first_pixel += 1
                        if (first_pixel % 2 == 1) and (first_encoder % 2 == 0):
                            first_pixel += 1
                    
                    image[i][j] = (first_pixel, second_pixel, third_pixel) # update the pixel

            cv2.imwrite(fileout, image) # write the image
                   
    def decode(self, filein, codec):
        # read the image
        flag = True # set flag to True
        image = cv2.imread(filein)
        
        # convert into text
        if codec == 'binary':
            self.codec = Codec(delimiter = self.delimiter) 
        elif codec == 'caesar':
            self.codec = CaesarCypher(delimiter = self.delimiter)
        elif codec == 'huffman':
            if self.codec == None or self.codec.name != 'huffman':
                print("A Huffman tree is not set!")
                flag = False
        if flag:
            # get the image dimensions
            height, width, _ = image.shape
            all_list = []
            # loop through the image
            for i in range(height):
                for j in range(width):
                    pixel = image[i][j]
                    for k in pixel:
                        all_list.append(k)
            
            binary_data = ''
            for i in all_list:
                if i % 2 == 0:
                    binary_data += '0' # if the pixel is even, add a 0
                if i % 2 == 1:
                    binary_data += '1' # if the pixel is odd, add a 1

            # update the data attributes:
            self.text = self.codec.decode(binary_data)
            
            binary_e = []        
            for i in range(0,len(binary_data),8): # split into 8-bit chunks
                byte = binary_data[i: i+8]
                if byte == self.delimiter:
                    break
                binary_e.append(byte) # add the chunk to the list
            
            self.binary = ''.join(binary_e) # join the list into a string
        
    def print(self):
        if self.text == '':
            print("The message is not set.") # if the message is not set, print this
        else:
            print("Text message:", self.text) # print the message
            print("Binary message:", self.binary) # print the message and the binary message       

    def show(self, filename): # show the image
        plt.imshow(mpimg.imread(filename))
        plt.show()

