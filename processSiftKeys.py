from __future__ import division
from scipy.cluster.vq import *
import os, sys
import numpy as np

descriptor_count = 0
result = []
codebook = []
k = 50

def processSiftKey(sift_key):
    global descriptor_count
    key = open(sift_key)
    new_line = ""

    lines = key.readlines()
    lines = lines[1:]
    for i in range(len(lines)):

        if (i % 8) == 0:
            if new_line != "":
                result.append(new_line.strip())
                descriptor_count += 1
            new_line = ""
        else:
            new_line += (lines[i].strip() + ' ')


def getAllDescriptors(image_list):

    imlist = open(image_list)
    for im in imlist:
        file_name = im.strip().split('.')[0]
        key_file = file_name + ".key"
        os.system("./../sift <" + im.strip() + " >" + key_file)
        processSiftKey(key_file)

    print "shashank"
    out_file = open("100images_all_descriptors", 'w')
    for item in result:
        print>>out_file, item


def generateCodebook(descriptor_file):
    global codebook

    all_descriptors = open(descriptor_file)
    npArray = []
    for descriptor in all_descriptors:
        tokens = descriptor.split()
        tokens = map(int, tokens)
        npArray.append(tokens)

    x = np.array(npArray)
    print len(x)

    whitened = whiten(x)
    print "whitened " + str(len(whitened))

    print "Initiating k-means.."
    codebook, distortion = kmeans(whitened, k)

    print "Distortion: " + str(distortion)
    print "----------CODEBOOK---------"
    for code in codebook:
        print code


def getBOVW(sift_key):
    global codebook
    new_line = ""
    sift_key_points = []

    lines = sift_key.readlines()
    lines = lines[1:]
    for i in range(len(lines)):
        if (i % 8) == 0:
            if new_line != "":
                new_line = new_line.strip()
                tokens = new_line.split()
                tokens = map(int, tokens)
                sift_key_points.append(tokens)
            new_line = ""
        else:
            new_line += (lines[i].strip() + ' ')

    sift_key_points = np.array(sift_key_points)
    codebook = np.array(codebook)
    idx, _ = vq(sift_key_points, codebook)

    BOVW = []
    for i in range(k):
        BOVW.append(list(idx).count(i+1)/ len(sift_key_points))

    return BOVW


def main():

    # cnt = 1
    # dataset = open("people_dataset", 'w')
    # generateCodebook("small_dataset_descriptors")

    # imlist = open('nonpeople_imlist')
    # for i in range(k):
    #     cnt = i
    #     cnt += 1
    #     os.system("./../sift <" + "nonpeople_" + str(cnt) + ".pgm >" + "nonpeople_" + str(cnt) + ".key")
    #     sift_key = open("nonpeople_" + str(cnt) + ".key")
    #     BOVW = getBOVW(sift_key)
    #     print "instance " + str(cnt) + " added"
    #     print>>dataset, BOVW
    #     os.system("rm nonpeople_" + str(cnt) + ".key")

    # dataset.close()
    getAllDescriptors("imlist")

main()
