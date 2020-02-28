import pandas as pd
import pandas as pd
import category_encoders as ce
from pandas import concat
from tqdm import tqdm
from sklearn.preprocessing import MinMaxScaler
from datetime import timedelta, date, datetime
import calendar
from collections import OrderedDict
import matplotlib.pyplot as plt

def getGraphByProductAndShop(df):
    df.plot(kind='line', x='date_added', y='qty', color='red')
    plt.show()
    exit()

def addEmptyLines(dataframe, item):
    dates = [dataframe['date_added'].min(), dataframe['date_added'].max()]
    start, end = [datetime.strptime(_, "%Y-%m") for _ in dates]

    months = list(OrderedDict(((start + timedelta(_)).strftime(r"%Y-%m"), None) for _ in range((end - start).days)).keys())
    months.append(dataframe['date_added'].max())

    dataframe.index = dataframe.date_added
    df2 = pd.DataFrame({'product_code': item, 'date_added': months, 'qty': 0})
    df2.index = df2.date_added
    df2.qty = dataframe.qty
    df2 = df2.fillna(0)
    del df2['date_added']
    return df2

def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    """

    Arguments:
      data: Sequence of observations as a list or NumPy array.
      n_in: Number of lag observations as input (X).
      n_out: Number of observations as output (y).
      dropnan: Boolean whether or not to drop rows with NaN values.
    Returns:
      Pandas DataFrame of series framed for supervised learning.

    """
    n_vars = 1 if type(data) is list else data.shape[1]

    df = data
    cols, names = list(), list()

    # input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
      cols.append(df.shift(i))
      names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]

    # forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
      cols.append(df.shift(-i))
      if i == 0:
        names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
      else:
        names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]

    # put it all together
    agg = concat(cols, axis=1)
    agg.columns = names

    # drop rows with NaN values
    if dropnan:
      agg.dropna(inplace=True)
    return agg


df = pd.read_csv('products_selled_final.csv', sep=';')
df_series = df.drop(columns=['order_id', 'pick_id', 'weight', 'width', 'height', 'length', 'cbm', 'boxer_per_unit', 'min_order_qty',
                             'multiple_order_qty', 'pick_single_qty', 'pick_xtra_qty', 'pick_inner_qty', 'pick_carton_qty'])

raw_data = []
unique_items = df_series['product_code'].unique()

with tqdm(total=len(unique_items)) as pbar:
    for item in unique_items:
        df = df_series[df_series.product_code == item]
        if len(raw_data) == 0:
            raw_data = addEmptyLines(df, item).values
        else:
            raw_data += addEmptyLines(df, item).values
        pbar.update(1)

df_full = pd.DataFrame(raw_data, columns=['product_code', 'qty'])

print(df_full.head(100))
exit()
# getGraphByProductAndShop(df)

del df['date_added']

for element in range(1, 13):
    df_final = series_to_supervised(df, element)
    df_final.to_csv('dataset_{}_series.csv'.format(element), sep=';', index=False)
