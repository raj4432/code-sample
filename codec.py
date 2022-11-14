"""
assignmnet: PA3
author: Raj Singh
date: 11/07/2022
file: codec.py is a module for the cryptography program that contains the Codec class and its methods and attributes that are used to encode and decode messages in images using different codec methods.
input: the file contains the Codec class and its methods and attributes that are used to encode and decode messages in images using different codec methods.
output: the output is a message that is encoded or decoded using different codec methods.
"""

import numpy as np # import numpy

class Codec():
    # constructor method for the Codec class that initializes the delimiter attribute of the Codec class to the value of the delimiter parameter passed to the constructor method.
    def __init__(self, delimiter = '#'):
        self.name = 'binary'
        self.delimiter = delimiter

    # convert text or numbers into binary form    
    def encode(self, text):
        if type(text) == str:
            return ''.join([format(ord(i), "08b") for i in text]) # text to binary
        else:
            print('Format error')

    # convert binary data into text
    def decode(self, data):
        binary = [] # list of binary numbers
        for i in range(0,len(data),8):
            byte = data[i: i+8] # 8 bits
            if byte == self.encode(self.delimiter): # delimiter
                break
            binary.append(byte)
        text = '' # text
        for byte in binary: # convert binary to text
            text += chr(int(byte,2))       
        return text # return text

class CaesarCypher(Codec):

    def __init__(self, shift=3, delimiter = '#'):
        self.name = 'caesar' # name of the codec
        self.delimiter = delimiter # delimiter is used to separate the message from the rest of the data
        self.shift = shift # shift value
        self.chars = 256      # total number of characters

    def encode(self, text):
        # encode the text using the Caesar Cypher
        if type(text) == str:
            text = ''.join([format(((ord(i) + self.shift) % self.chars), "08b") for i in text]) # convert text to binary
        else:
            print('Format error') # print error if text is not a string

        return text # Huffman Codes
    
    def decode (self, data):
        # decode the text using the Caesar Cypher
        binary = [] # list of binary values
        for i in range(0,len(data),8):
            byte = data[i: i+8]
            if byte == self.encode(self.delimiter):
                break
            binary.append(byte)
        text = ''
        for byte in binary: # convert binary to text
            text += chr(int(byte,2) - self.shift)       
        return text # return the decoded text

# a helper class used for class HuffmanCodes that implements a Huffman tree
class Node:
    def __init__(self, freq, symbol, left=None, right=None):
        self.left = left
        self.right = right
        self.freq = freq
        self.symbol = symbol
        self.code = ''
        
class HuffmanCodes(Codec):
    # initialize the class
    """ make a Huffman tree and traverse it """
    def __init__(self, delimiter = '#'):
        self.nodes = None
        self.data = {}
        self.name = 'huffman'
        self.delimiter = delimiter

    # make a Huffman Tree    
    def make_tree(self, data):
        # make a list of nodes
        nodes = []
        for char, freq in data.items():
            nodes.append(Node(freq, char))
            
        # assemble the nodes into a tree
        while len(nodes) > 1:
            # sort the current nodes by frequency
            nodes = sorted(nodes, key=lambda x: x.freq)

            # pick two nodes with the lowest frequencies
            left = nodes[0]
            right = nodes[1]

            # assign codes
            left.code = '0'
            right.code = '1'

            # combine the nodes into a tree
            root = Node(left.freq+right.freq, left.symbol+right.symbol,
                        left, right)

            # remove the two nodes and add their parent to the list of nodes
            nodes.remove(left)
            nodes.remove(right)
            nodes.append(root)

        return nodes

    # traverse a Huffman tree
    def traverse_tree(self, node, val):
        # traverse the tree and store the codes in a dictionary
        next_val = val + node.code
        if(node.left):
            self.traverse_tree(node.left, next_val) # traverse left
        if(node.right):
            self.traverse_tree(node.right, next_val) # traverse right
        if(not node.left and not node.right):
            #print(f"{node.symbol}->{next_val}")
            self.data[node.symbol] = next_val

    # convert text into binary form
    def encode(self, text):
        # encode the text using the Huffman Cypher
        data = ''
        freq_dict = {}
        for i in text: # count the frequency of each character
            if i in freq_dict:
                freq_dict[i] += 1
            else:
                freq_dict[i] = 1
        self.nodes = self.make_tree(freq_dict) # make the tree
        self.traverse_tree(self.nodes[0], '') # traverse the tree
        for i in text: # encode the text
            data += self.data[i]
        return data

    # convert binary data into text
    def decode(self, data):
        # decodes the text using the Huffman Cypher
        text = ''
        tree_head = self.nodes[0]
        for i in data: # traverse the tree
            if i == '0':
                tree_head = tree_head.left # go left
            else:
                tree_head = tree_head.right # go right
            if tree_head.left == None and tree_head.right == None: # if we are at a leaf node then we have decoded a character
                text += tree_head.symbol
                tree_head = self.nodes[0]
        return text[:text.index(self.delimiter)] # return the decoded text

# driver program for codec classes
if __name__ == '__main__':
    text = 'hello'
    text = 'Casino Royale 10:30 Order martini'
    print('Original:', text)

    c = Codec()
    binary = c.encode(text + c.delimiter)
    print('Binary:',binary)
    data = c.decode(binary)
    print('Text:',data)

    cc = CaesarCypher()
    binary = cc.encode(text + cc.delimiter)
    print('Binary:',binary)
    data = cc.decode(binary)
    print('Text:',data)

    h = HuffmanCodes()
    binary = h.encode(text + h.delimiter)
    print('Binary:',binary)
    data = h.decode(binary)
    print('Text:',data)  

