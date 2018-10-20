"""
Written by: Matthew Chang

generates direct download links for Google Drive shareable links

reads a .txt file with shareable links and outputs a .txt file with
the corresponding direct download links
"""

import re


def genLink(url):
    temp = re.match(r'^https://drive.google.com/file/d/([^/]+)/view\?usp=sharing$', url)
    if bool(temp):
        id = temp.group(1)
        return 'https://drive.google.com/uc?export=download&id='+id


if __name__ == '__main__':
    filename = input('Enter filename: ')
    with open(filename) as f:
        with open('output.txt', 'w') as out:
            for line in f:
                out.write(genLink(line)+'\n')
