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

grouped = grouped[grouped.product_code == 'AIRF06']

raw_data = []


ç
