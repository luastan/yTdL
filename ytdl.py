#!/usr/bin/env python3
import requests
import sys
import re
import os.path

def downloader(link, filename = 'whatever'):

    #Scrapping the song link
    print(' [*] Scrapping ... ')
    base_link = 'http://www.youtubeinmp3.com/es/download/?video=' + link

    #print(' [!] youtubeinmp3 link -> ' + base_link)
    print(' [*] Exctracting direct link')
    download_page = requests.get(base_link).text
    downloads = re.findall(r'/download/get/.{40}', download_page)
    direct_mp3_link = 'http://www.youtubeinmp3.com' + downloads[0]

    #Scrapping the song name ->  (.*?) and "generating filename with extension"
    if filename == 'whatever':
        print(' [*] Getting song name')
        names = re.findall(r'videoTitle">(.*?)</span', download_page)

    #Ensuring filename ends with.mp3
        filename = names[0] + '.mp3'
    else:
        if filename[-4:] != '.mp3':
            filename = filename + '.mp3'

    #Checks if file exists
    if not os.path.isfile(filename):
        #Downloading file
        print(' [*] Downloading file: ' + filename[:20] + '...')
        mp3_file = requests.get(direct_mp3_link)
        with open(filename, "wb") as rythm:
            rythm.write(mp3_file.content)
        print(' [!] Download completed !\n')
    else:
        print(' [!] File already exists. Skipping download\n')

def title():
    print(
    """     _______  _ _
    |__   __|| | |
  _   _| | __| | |
 | | | | |/ _` | |
 | |_| | | (_| | |____
  \__, |_|\__,_|______|
   __/ |
  |___/   by Luastan
    """
    )

def main(args = None):

    if args is None:
        args = sys.argv

    title()
    if len(args) > 1 :
        link = args[1]
        if len(args) > 2:
            downloader(link, args[2])
        else:
            downloader(link)
    else:
        print('Command line usage -> yTdL [link] [filename](optional)')


if __name__ == "__main__":
    main()
