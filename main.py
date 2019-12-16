import glob
import os
import mutagen
from mutagen.easyid3 import EasyID3
import ntpath

def extract_filename(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def strip_to_title(path):
    return os.path.splitext(extract_filename(path).lstrip('0123456789.- '))[0]

if __name__ == "__main__":
    pathlist = glob.glob('test_resources/*.mp3')

    for path in pathlist:
        path_in_str = str(path)
        print(path_in_str)
        try:
            tag = EasyID3(path)
        except:
            tag = mutagen.File(path, easy=True)
            tag.add_tags()

        tag['title'] = strip_to_title(path)
        tag.save(path)
