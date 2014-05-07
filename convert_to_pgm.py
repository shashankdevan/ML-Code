import os

def main():
    ffile = "nonpeople_list"
    imlist = open(ffile)
    for im in imlist:
        file_name = im.strip().split('.')[0]
        print "convert " + im.strip() + " " + file_name + ".pgm"
        os.system("convert " + im.strip() + " " + file_name + ".pgm")

main()
