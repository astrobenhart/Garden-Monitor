import sqlite3
import pandas as pd

db_file = 'data.db'


def get_env_data():
	"""
        Query Air Temperature data rows between two ranges
        :params start: start row id
        :params end: end row id
        :returns: pandas dataframe object
        """

	con = sqlite3.connect(str(db_file))
	statement = f'SELECT * FROM from_nano;'
	df = pd.read_sql_query(statement, con)
	return df


def get_data_by_id(row_id):
	"""
    Query a row from the Wind Table
    :params row_id: a row id
    :returns: pandas dataframe object
    """

	con = sqlite3.connect(str(db_file))
	statement = f'SELECT * FROM from_nano WHERE rowid = "{row_id}";'
	df = pd.read_sql_query(statement, con)
	return df
