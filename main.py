import collections
import itertools
import os
from PIL import Image

from pillow_heif import register_heif_opener

register_heif_opener()
base_dir = r'F:\theod media\images\Bilder'

subdirs = [x for x in os.walk(base_dir)]


'''
I want a python script that given a folder, look at every image in that folder : 
- convert the heic image to jpg
- if there is a associated mov (same name), show the image and propose to type g to keep the mov or p to remove the associated mov
- check if the year the picture was taken match the year being in the folder name (e.g. 2018.08.31 ...)
'''



def get_date_taken(path):
        exif = Image.open(path).getexif()
        if not exif:
            raise Exception('Image {0} does not have EXIF data.'.format(path))
        return exif[306].rsplit(' ', 1)[0]

def hash_file_name(file_name, file_path):
    type = file_name.rsplit('.', 1)[1]
    file_path = file_path.replace("\\", "/") + "/" + file_name
    try:
        date_taken = get_date_taken(file_path)
        return type + " " + date_taken
    except Exception as e:
        with open('error.txt', 'w') as error_file:
            print(e, file=error_file)
        return type

with open('output.txt', 'w') as f:
    for subdir in subdirs:
        file_name_reduced = list(map(hash_file_name, subdir[2], itertools.repeat(subdir[0], len(subdir[2]))))
        counter = collections.Counter(file_name_reduced)
        print("{0:120} {1}".format(subdir[0], counter), file=f)

