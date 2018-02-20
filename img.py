#
#   copy images for cigarettes compare GUI
#   image name from csv file
#   

import os
import csv
from shutil import copyfile


ls = {}
with open("class_cigarettes.csv", "r") as f:
    reader = csv.reader(f)

    for row in reader:
        data = row[0].split(',')
        name = data[0]
        id = data[1]
        ls[id] = name
# print(ls)
PATH = '..\coord_ciga\conv_images'
image_dirs = os.listdir(PATH)
print(image_dirs)
for dr in image_dirs:
    # print(dr)
    p = os.path.join(PATH, dr)
    # print(p)
    dir_list = os.listdir(p)[0]
    print(dir_list)
    copyfile(os.path.join(p, dir_list), './images/%s.jpg' % ls[dr])