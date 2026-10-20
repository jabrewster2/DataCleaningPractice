import numpy as np
import pandas as pd
import re
from word2number import w2n

# Import the csv File to clean
df = pd.read_csv("dcc_client_orders_messy.csv")

# Print the head of the file
def print_head():  
  print(df.head())

# Print the tail of the file
def print_tail():
  print(f"\n\n")
  print(df.tail())

# Print the description of the file
def print_desc():
  print(f"\n\n")
  print(df.describe())

# Print the Shape of the file NxM
def print_shape():  
  print(f"\n\n")
  print(df.shape) # 60 rows and 10 columns

# Print the elements that are NA and the total elements that are NA
def print_na_info():
  print(f"\n\n")
  print(df.isna().head()) # Capping it to the head just for the space
  print(f"\n\n")
  print(df.isna().sum())

# Standardize the Order Id column
# Standard is Uppercase, trimmed, format: ORD-####
# Each ID has to be unique
def std_order_id_col():
  col_i = 0
  rows_i = 0

  for value in df["order_id"]:
    value = value.strip()
    number = value[4:]
    df.iloc[rows_i, col_i] = "ORD-" + number

    rows_i += 1

# Standardize the Customer Name column
# Standard is trimmed, title case, from approved list 
# Blank or N/A becomed null and gets flagged
def std_customer_name_col():
  col_i = 1
  rows_i = 0

  approved_list = ["Carl", "Princess Donut", "Mordecai"] 

  for value in df["customer_name"]:
    if type(value) is str:
      cleaned_value = value.strip().title()
      if cleaned_value in approved_list:
        df.iloc[rows_i, col_i] = cleaned_value
      else:
        if cleaned_value == "Donut":
          df.iloc[rows_i, col_i] = "Princess Donut"
        elif cleaned_value == "" or cleaned_value == "N/A":
          df.iloc[rows_i, col_i] = None
        else:
          print("THERE IS ANOTHER NAME IN THE LIST")
    rows_i += 1

# Standardize the Order Date column
# Standard is YYYY-MM-DD
def std_order_date_col():
  col_i = 2
  rows_i = 0

  dates = pd.to_datetime(df["order_date"], format="mixed", errors="coerce")

  valid = dates.between("2026-01-01", "2026-10-20")
  dates = dates.where(valid)

  df["order_date"] = dates.dt.date

# Standardize the City column
# Standard is trimmed and title case
def std_city_col():
  col_i = 3
  rows_i = 0

  for value in df["city"]:
    if type(value) is str:
      cleaned_value = value.strip().title()
      df.iloc[rows_i, col_i] = cleaned_value
    rows_i += 1

# Standardize the item column
# Standard is trimmed and title case
# Each item must map to an item from the catalog
item_catalog = {
  "Healing Potion": 45.00,
  "Iron Dagger": 320.50,
  "Leather Boots": 180,
  "Cat Treats (Bulk)": 24.99,
  "Sparkly Tiara": 1250.00,
  "Ration Crate": 75.25,
  "Torch Bundle": 12.50,
  "Climbing Rope": 58.00,
  "Grooming Kit": 96.75,
  "Padded Armor Set": 1480.00,
  "Lockpick Set": 210.00,
  "Map Scroll": 33.00
}

# Standardize the item column
# Standard is trimmed and title case
# All items have to part of the catalog above
def std_item_col():
  col_i = 4
  rows_i = 0

  for value in df["item"]:
    cleaned_value = value.strip().title()
    if cleaned_value in item_catalog:
      df.iloc[rows_i, col_i] = cleaned_value
    else:
      df.iloc[rows_i, col_i] = "unknown item " + cleaned_value
    rows_i += 1

# Standardize the quantity column
# Standard is whole number 1-100
def std_quantity_col():
  cols_i = 5
  rows_i = 0

  for value in df["quantity"]:
    cleaned_value = re.sub(r'-', '', value)
    cleaned_value = cleaned_value.strip().lower()
    cleaned_value = str(w2n.word_to_num(cleaned_value))

    if int(cleaned_value) < 0 or int(cleaned_value) > 100:
      df.iloc[rows_i, cols_i] = None
    else:
      df.iloc[rows_i, cols_i] = cleaned_value

    rows_i += 1

# Standardize the Unit Price column
# Standard is numeric, 2 decimal places, no symbols ($)
def std_unit_price_col():
  cols_i = 6
  rows_i = 0

  for value in df["unit_price"]:
    df.iloc[rows_i, cols_i] = f"{item_catalog[df.iloc[rows_i, 4]]:.2f}"
    rows_i += 1

# Standardize the Order Amount Column
# Standard is numeric, 2 decimals, equal to quantity x unit price
def std_order_amount_col():
  cols_i = 7
  rows_i = 0

  for value in df["order_amount"]:
    df.iloc[rows_i, cols_i] = f"${(float(df.iloc[rows_i, 5]) * float(df.iloc[rows_i, 6])):.2f}"
    rows_i += 1

def std_statis_col():
  cols_i = 8
  rows_i = 0

  valid_status = {"P": "Pending", 
                  "S": "Shipped", 
                  "D": "Delivered", 
                  "C": "Cancelled"}
  
  for value in df["status"]:
    if type(value) is str:
      if value[0].upper() in valid_status:
        df.iloc[rows_i, cols_i] = valid_status[value[0].upper()]
      else: 
        df.iloc[rows_i, cols_i] = "Unknown"
    else: 
      df.iloc[rows_i, cols_i] = "Unknown"

    rows_i += 1

def std_notes_col():
  cols_i = 9
  rows_i = 0

  for value in df["notes"]:
    if type(value) is str:
      df.iloc[rows_i, cols_i] = value.strip()
    rows_i += 1





# Standardize all the columns that should be strings
# by removing all leading and trailing whitespace and 
# making it lowercase
std_order_id_col()
std_customer_name_col()
std_order_date_col()
std_city_col()
std_item_col()
std_quantity_col()
std_unit_price_col()
std_order_amount_col()
std_statis_col()
std_notes_col()

df_cleaned = df.drop_duplicates()
other_cols = df.columns.difference(['notes'])

df_cleaned = df_cleaned.dropna(subset=df.columns.difference(['notes']))
invalid_rows = df[df[other_cols].isna().any(axis=1)]

cleaned_dataset = df_cleaned.to_csv("cleaned_dcc_client_orders.csv", index=False)
invalid_rows = invalid_rows.to_csv("messy_rows_dcc_client_orders.csv", index=False)