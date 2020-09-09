import pandas as pd
import pygal

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

file = 'тестовое_мл_аналитик.xlsx'
xl = pd.ExcelFile(file)
data1 = xl.parse('Лист1')
data2 = xl.parse('Лист2')

client = 'client_retail_id'
invoice = 'invoice_id'
product = 'product_article'
amount = 'invoice_product_all_amount'
price = 'invoice_product_price'
shop = 'shop_id'
invoice_sum = 'invoice_sum'


# Histogram making function
def make_hist(title, x_name, x_ax, y1_name, y1, y2_name=None, y2=None, y3_name=None, y3=None):
    hist = pygal.Bar()
    hist.title = title
    hist.x_labels = x_ax
    hist.x_title = x_name
    hist.add(y1_name, y1)
    hist.add(y2_name, y2)
    hist.add(y3_name, y3)
    hist.render_to_file('{}.svg'.format(title))


# Product info
title_popular = 'Top_10_products'

# Popular product
top_10_popular_products = data1.groupby(product)[amount].agg(['sum']).\
                        sort_values(by='sum', ascending=False).head(10)
popular_products = list(top_10_popular_products.index)
popular_values = list(top_10_popular_products['sum'])
# Product sales frequency
freq_products = data1.groupby(product)[client].agg(['count'])
# Product income
product_income = data1.groupby([product, price])[amount].sum()
product_freq_values = []
product_income_list = []
for i in popular_products:
    product_freq_values += list(freq_products[freq_products.index == i]['count'])
    ind = 0
    total = 0
    while ind < len(product_income[i]):
        price_i = list(product_income[i].index)[ind]
        amount_i = list(product_income[i])[ind]
        total += price_i * amount_i / 100
        ind += 1
    product_income_list += [total]
make_hist(title_popular, product, popular_products,
          'Sales', popular_values, 'Sales frequency', product_freq_values,
          'Income *100 $', product_income_list)


# Shop info
title_popular_shop = 'Top_10_shops'

# shops by sold products
top_10_shops = data1.groupby(shop)[amount].agg(['sum']).\
                sort_values(by='sum', ascending=False).head(10)
popular_shops = list(top_10_shops.index)
popular_val_shops = list(top_10_shops['sum'])
# clients of shops
shops_clients = data1.groupby([shop])[client].unique()
# shops income
shop_income = data1.groupby([shop, price])[amount].sum()
# render to lists
shop_clients_list = []
shop_income_list = []
for i in popular_shops:
    shop_clients_list += [len(shops_clients[i])]
    ind = 0
    total = 0
    while ind < len(shop_income[i]):
        price_i = list(shop_income[i].index)[ind]
        amount_i = list(shop_income[i])[ind]
        total += price_i * amount_i / 1000
        ind += 1
    shop_income_list += [total]
make_hist(title_popular_shop, shop, popular_shops,
          'Sold products', popular_val_shops, 'Clients', shop_clients_list,
          'Income *1000 $', shop_income_list)

# In addition
# only 2 is max converse
shops_conversion = data1.groupby([shop, client])[invoice].unique()

# Inconsistency of data
clients_1 = len(data1[client].unique())
clients_2 = len(data2[client].unique())
print(clients_1, clients_2)

invoice_1 = len(data1[invoice].unique())
invoice_2 = len(data2[invoice].unique())
print(invoice_1, invoice_2)

amount_1 = list(data1[amount])
price_1 = list(data1[price])
sum_1 = 0
for i, j in zip(amount_1, price_1):
    try:
        sum_1 += int(i) * int(j)
    except ValueError:
        None
sum_2 = data2[invoice_sum].sum()
print(sum_1, sum_2)


