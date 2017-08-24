"""
Small script to download every youtube video
parsed in mp3
"""

import sys
import re
import tempfile
import hashlib
import os
import subprocess

import youtube_dl
import requests

def prompt_user():
    """
    Asks the user for for youtube links
    Will detect all the links in the given string using regular expresions
    """
    raw_string = input('[?] Whitch videos would you like to convert ? -> ')
    
    yt_ids = []
    patterns = [r'\/watch\?v=(.{11})',
                r'youtu\.be\/(.{11})']

    for pattern in patterns:
        yt_link_regex = re.compile(pattern)
        yt_ids += yt_link_regex.findall(raw_string)

    base_yt_link = 'https://youtu.be/'

    valid_links = [base_yt_link + video_id for video_id in yt_ids]

    return valid_links


def downloader(link):
    """
    Function used to download and convert to mp3 from a given link
    """

    """
    Will use tmp folder to download the files.
    """

    hashed_link = hashlib.md5(link.encode()).hexdigest()
    base_tmp_path = tempfile.gettempdir()
    tmp_webm = base_tmp_path + '\\' + hashed_link + '.webm'
    tmp_pic = base_tmp_path + '\\' + hashed_link + '.jpg'

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': tmp_webm
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])
        info_dict = ydl.extract_info(link, download=False)

    title = info_dict['title']
    thumbnail_url = info_dict['thumbnails'][0]['url']

    print('Downloading album cover')
    cover = requests.get(thumbnail_url, stream=True)

    with open(tmp_pic, 'wb') as pict:
        for chunk in cover:
            pict.write(chunk)

    full_path = title + '.mp3'

    ffmpeg_args = ['ffmpeg.exe', '-i', tmp_webm, '-i', tmp_pic, '-id3v2_version', '3',
                   '-write_id3v1', '1', '-c', 'copy', '-map', '0', '-map', '1', '-metadata:s:v',
                   'title=Front Cover', '-metadata:s:v', 'comment=Cover (Front)', '-codec:a',
                   'libmp3lame', full_path]

    if not os.path.isfile(full_path):  # Checks if the song has already been converted
        print('Converting to MP3')
        subprocess.call(ffmpeg_args)

    for tmp_file in [tmp_webm, tmp_pic]:  # Removes temporary files
        if os.path.isfile(tmp_file):
            os.remove(tmp_file)


def main(link_list):
    """Main routine"""
    print(" - Luastan's YT 2 MP3 -")

    for link in link_list:
        downloader(link)


if __name__ == '__main__':
    """
    Uses the links parsed by arguments if any.
    Otherwise it prompts the user for youtube links
    """
    YT_LINKS = sys.argv[1:] if len(sys.argv) > 1 else prompt_user()

    main(YT_LINKS)
