import pandas as pd
import urllib.request
import time
import re
import csv
import os
from bs4 import BeautifulSoup

def main():
    df = pd.read_csv('csv/ranking.csv')
    df = df.head(1000)
    for title, artist in zip(df['曲名'], df['歌手名']):
        print(title + ' / ' + artist)
        lyric_path = 'lyrics/' + title.replace('/', '') + '_' + artist.replace('/', '') + '.txt'
        if not os.path.exists(lyric_path):
            get_lyric(title=title, artist=artist)

def get_lyric_url(title, artist):
    payload = {
        'kt': title_filter(title),
        'ct': 2,
        'ka': artist_filter(artist),
        'ca': 2,
        'kl': '',
        'cl': 2
    }
    query = urllib.parse.urlencode(payload)
    search_url = 'http://search.j-lyric.net/index.php?' + query
    response = urllib.request.urlopen(search_url)
    bs = BeautifulSoup(response.read(), 'lxml')
    sleep()
    element = bs.find('div', id='mnb').find('div', class_='bdy').find('p', class_='mid').find('a')
    lyric_url = element.get('href')
    return lyric_url

def get_lyric(title, artist, url=None):
    try:
        if url is None:
            url = get_lyric_url(title=title, artist=artist)
        response = urllib.request.urlopen(url)
        bs = BeautifulSoup(response.read(), 'lxml')
        sleep()
        element = bs.find('div', id='mnb').find('div', class_='lbdy').find('p', id='Lyric')
    except AttributeError:
        with open('csv/get_lyric_errors.csv', 'a') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow([title, artist])
        return
    lyric = str(element).replace('<p id="Lyric">', '').replace('</p>', '').replace('<br/>', '\n')
    with open('lyrics/' + title.replace('/', '') + '_' + artist.replace('/', '') + '.txt', 'w') as f:
        f.write(lyric)

def get_lyrics_manual():
    df = pd.read_csv('csv/get_lyric_errors_fix.csv')
    for title, artist, url in zip(df['曲名'], df['歌手名'], df['URL']):
        print(title + ' / ' + artist)
        lyric_path = 'lyrics/' + title.replace('/', '') + '_' + artist.replace('/', '') + '.txt'
        if not os.path.exists(lyric_path):
            get_lyric(title=title, artist=artist, url=url)   

def title_filter(str):
    str = re.sub(r'[\(\-〜].+?[\)\-〜]', '', str)
    str = str.replace('･', ' ').replace('…', ' ').replace('＆', ' ')
    return str

def artist_filter(str):
    str = re.sub(r'[\(〜].+?[\)〜]', '', str)
    str = re.sub(r'feat\..+', '', str)
    str = str.replace('･', ' ').replace('…', ' ').replace('＆', ' ')
    return str

def sleep():
    time.sleep(1)

if __name__ == '__main__':
    main()
    # get_lyrics_manual()
