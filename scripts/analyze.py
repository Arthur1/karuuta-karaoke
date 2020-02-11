import pandas as pd

df_karuuta = pd.read_csv('karuuta_terms.csv', index_col=0)
df_result = pd.read_csv('csv/result.csv', index_col=0)

def main():
    convert_table_to_bool()
    analyze_for_daifugou()

def convert_table_to_bool():
    df_bool = df_result.copy()
    f = lambda x: int(bool(x))
    for card_id in df_karuuta.index:
        df_bool[str(card_id)] = df_bool[str(card_id)].map(f)
    df_bool.to_csv('csv/result_bool.csv')

def analyze_for_daifugou():
    df_daifugou = df_result.copy()
    df_daifugou['daifugou'] = 0
    for index, row in df_daifugou.iterrows():
        order = 1
        min_point = 0
        while True:
            card_id = find_index(row, order)
            if card_id is None:
                break
            point = df_karuuta.at[df_karuuta.index[int(card_id) - 1], 'point']
            if min_point > point:
                break
            min_point = point
            order += 1
        daifugou = order - 1
        df_daifugou.at[index, 'daifugou'] = daifugou
        f = lambda x: 1 if x > 0 and x <= daifugou else 0
        for card_id in df_karuuta.index:
            df_daifugou.at[index, str(card_id)] = f(df_daifugou.at[index, str(card_id)])
    df_daifugou.to_csv('csv/result_daifugou.csv')


def find_index(record, item):
    return record.where(record == item).first_valid_index()

if __name__ == '__main__':
    main()
