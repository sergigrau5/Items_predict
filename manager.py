import pandas as pd
from tqdm import tqdm

cols = ['product_code', 'date_added', 'qty', 'order_id', 'pick_id', 'weight',
        'width', 'height', 'length', 'cbm', 'boxer_per_unit', 'min_order_qty',
        'multiple_order_qty', 'pick_single_qty', 'pick_xtra_qty', 'pick_inner_qty',
        'pick_carton_qty']
df = pd.read_csv('products_selled.csv', sep=';')
# df.columns = cols
# df['date_added'] = pd.to_datetime(df['date_added'], unit='s').dt.strftime("%Y-%m")
# df = df.sort_values(['product_code', 'date_added'])
# df.to_csv('products_selled.csv', sep=';', index=False)
grouped = df.groupby(['product_code', 'date_added'])['qty'].sum().reset_index()

raw_data = []


with tqdm(total=grouped.size) as pbar:
    for index, row in grouped.iterrows():
        element = df[(df.product_code == row['product_code']) & (df.date_added == row['date_added'])]
        element = element.drop(columns=['product_code', 'qty'])
        del element['date_added']
        if len(raw_data) == 0:
            raw_data.append(list(row) + list(element.values[0]))
        else:
            raw_data.append(list(row) + list(element.values[0]))
        pbar.update(1)

df_final = pd.DataFrame(raw_data, columns=cols)
df_final.to_csv('products_selled_final.csv', sep=';', index=False)
