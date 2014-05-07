import os

def rename():
    cnt = 1
    f = open("rename_list")
    for im in f:
        cnt += 1
        new = "nonpeople_" + str(cnt) + ".pgm"
        os.system("mv " + im.strip() + " " + new)

rename()
