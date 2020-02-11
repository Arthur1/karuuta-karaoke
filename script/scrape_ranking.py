import pandas as pd

def scrape_ranking():
    url = 'https://www.karatetsu.com/ranking/total/2019'
    dfs = pd.read_html(url, displayed_only=False, index_col=0)
    df = pd.concat(dfs)
    df['曲名'] = df['曲名'].str.normalize('NFKC')
    df['曲名'] = df['曲名'].str.replace('’', '\'')
    df['歌手名'] = df['歌手名'].str.normalize('NFKC')
    df['歌手名'] = df['歌手名'].str.replace('’', '\'')
    df.to_csv('csv/ranking.csv')
    return df

if __name__ == '__main__':
    scrape_ranking()
