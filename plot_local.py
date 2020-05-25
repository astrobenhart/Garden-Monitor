import sqlite3
import pandas as pd

conn = sqlite3.connect("data.db")
df = pd.read_sql_query("select * from from_nano;", conn)
df = df.set_index('datatime')