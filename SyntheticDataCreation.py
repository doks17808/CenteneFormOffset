import cv2
import os
import numpy as np
import pandas as pd
from random import randint
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--img_path", "-img", help = 'path to folder containing images of initial forms')
parser.add_argument("--out_path", "-out", help = 'path to folder where generated images will be saved')
parser.add_argument("--replication", "-r", type=int, help = 'how many times you want the image to be replicated')
parser.add_argument("--offsets", type=int, help = 'upper limit of how many places you want the form to be offset')
parser.add_argument("--lower_range" ,"-lr", type=int, help = 'lower range of how many pixels you want the offset to be')
parser.add_argument("--upper_range" , "-ur", type=int, help = 'upper range of how many pixels you want the offset to be')
parser.add_argument("--white", "-w", help = 'set to yes if you want the insertion to be a white box')
args = parser.parse_args()


def dataGen(img_path, out_path, replication = 20, offsets = 3, lower_range = 2, upper_range = 12, white = "no"):
    
    '''
    This function takes in a folder of images and outputs the same image with a specified offset. 
    The function must have the path to the images folder (img_path) and a path to save the synthetic data (out_path)
    All other arguments are optional and if left blank have default values. 
    "--img_path", "-img":     'path to folder containing images of initial forms'
    "--out_path", "-out":     'path to folder where generated images will be saved'
    "--replication", "-r":    'how many times you want the image to be replicated'                 default = 20
    "--offsets", :            'upper limit of how many places you want the form to be offset'      default = 3
    "--lower_range" ,"-lr":   'lower range of how many pixels you want the offset to be'           default = 2
    "--upper_range" , "-ur":  'upper range of how many pixels you want the offset to be'           default = 12
    "--white", "-w":          'set to yes if you want the insertion to be a white box'             default = no
    '''
    
    
    x = 0
    #Iterates through images in the file
    for image in os.listdir(img_path):
        #Determine the number of times the image is replicated
        for replicate in range(replication):
            #reads in the image and turn it grayscale
            img = cv2.imread(f'{img_path}/{image}')
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            glist = gray.tolist()
            #Randomly decide how many times and where the form will be offset
            for place in range(randint(1, offsets)):
                ind = randint(0,int(len(glist) - 1))
                #Randomly decide how large the offset will be
                for counter in range(randint(lower_range, upper_range)):
                    #Determine if the pixel will be stretched across the range or a white box will be inserted
                    if white == 'yes':
                        glist.insert(ind, glist[0])
                    else:
                        glist.insert(ind, glist[ind+1])                                    
            stretch = np.asarray(glist)
            x += 1
            #Output the image
            cv2.imwrite(f'{out_path}/{x}.jpg', stretch)



dataGen(args.img_path, args.out_path, args.replication, args.offsets, args.lower_range, args.upper_range, args.white)