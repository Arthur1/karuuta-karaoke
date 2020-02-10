import pandas as pd
import urllib.request
import re
import csv
import os
import MeCab

def main():
    tagger = MeCab.Tagger('-Ochasen')
    tagger.parse('')
    df_ranking = pd.read_csv('csv/ranking.csv')
    df_ranking = df_ranking.head(1000)
    df_karuuta = pd.read_csv('karuuta_terms.csv')
     
    keys = []
    vals = []
    keys.append('title')
    vals.append('')
    keys.append('artist')
    vals.append('')
    for card_id in zip(df_karuuta['card_id']):
        keys.append(card_id)
        vals.append(0)
    series_tmp = pd.Series(vals, index=keys)

    df_result = pd.DataFrame(index=[], columns=keys)

    for title, artist in zip(df_ranking['曲名'], df_ranking['歌手名']):
        print(title + ' / ' + artist)
        lyric_path = 'lyrics/' + title.replace('/', '') + '_' + artist.replace('/', '') + '.txt'
        series = series_tmp.copy()
        series['title'] = title
        series['artist'] = artist
        try:
            with open(lyric_path, mode='r') as f_lyric:
                for line in f_lyric:
                    node = tagger.parseToNode(line)
                    while node:
                        wclass = node.feature.split(',')
                        for card_id, word, ruby in zip(df_karuuta['card_id'], df_karuuta['word'], df_karuuta['ruby']):
                            if word == wclass[6] and ruby == wclass[7]:
                                if series[card_id] == 0:
                                    series[card_id] = 1           
                        node = node.next
            #print(series)
            df_result = df_result.append(series, ignore_index=True)
        except:
            continue
        df_result.to_csv('csv/result.csv')

if __name__ == '__main__':
    main()
