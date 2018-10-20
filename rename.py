"""
Written by: Matthew Chang

mass renames files given a directory and a pattern to search
written specifically from renaming Foodie image files
"""

import os, glob, re


def rename(dir, pattern):
    for pathAndFilename in glob.iglob(os.path.join(dir, pattern)):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))
        if bool(re.match(r'([0-9]{2,4}-){5}[0-9]{2}', title)):
            dateTime = title.split('-')
            new_filename = 'P_{0}{1}{2}_{3}{4}{5}'.format(*dateTime)

            print(new_filename)
            os.rename(pathAndFilename, os.path.join(dir, new_filename + ext))


if __name__ == "__main__":
    rename(r'C:\Users\Matthew\Desktop\Temp', r'*.jpg')
