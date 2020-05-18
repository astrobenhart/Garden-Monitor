import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

class Genplots():
	def __init__(self):
		self.conn = self.sql_conn()
		self.data = pd.DataFrame(self.select_all(), columns=['datetime', 'humidity', 'air_temp1', 'methane_levels', 'CO_levels', 'pressure', 'air_temp2', 'soil_temp', 'soil_moisture'])
		self.data.datetime = pd.to_datetime(self.data.datetime)
		self.data = self.data.set_index('datetime')

	def sql_conn(self):
		conn = None
		try:
			conn = sqlite3.connect('/home/pi/Documents/Garden-Monitor/data.db')
		except Exception as e:
			print(e)

		return conn

	def select_all(self):
		cur = self.conn.cursor()
		cur.execute("SELECT * FROM from_nano")

		rows = cur.fetchall()

		return rows

	def gen_plots(self, save_fig=True):
		fig, ax = plt.subplots(3,2, figsize=(12,18))
		self.data.humidity.tail(24).plot(ax=ax[0][0])
		ax[0][0].set_title('Humidity')
		ax[0][0].set_xlabel('Datetime')
		ax[0][0].set_ylabel('Humidity (%)')

		self.data.air_temp1.tail(24).plot(ax=ax[0][1], label='AM2320', color='b')
		self.data.air_temp2.tail(24).plot(ax=ax[0][1], label='BMP180', color='orange')
		ax[0][1].set_title('Air Temperature')
		ax[0][1].set_xlabel('Datetime')
		ax[0][1].set_ylabel('Temperature (C)')
		ax[0][1].legend()

		self.data.methane_levels.tail(24).plot(ax=ax[1][0], label='Methane', color='b')
		self.data.CO_levels.tail(24).plot(ax=ax[1][0], label='CO', color='r')
		ax[1][0].set_title('Methane and CO Levels')
		ax[1][0].set_xlabel('Datetime')
		ax[1][0].set_ylabel('Levels (%)')
		ax[1][0].legend()

		self.data.pressure.tail(24).plot(ax=ax[1][1])
		ax[1][1].set_title('Pressure')
		ax[1][1].set_xlabel('Datetime')
		ax[1][1].set_ylabel('Pressure (Pa)')

		self.data.soil_temp.tail(24).plot(ax=ax[2][0])
		ax[2][0].set_title('Soil Temperature')
		ax[2][0].set_xlabel('Datetime')
		ax[2][0].set_ylabel('Temperature (C)')

		self.data.soil_moisture.tail(24).plot(ax=ax[2][1])
		ax[2][1].set_title('Soil Moisture')
		ax[2][1].set_xlabel('Datetime')
		ax[2][1].set_ylabel('Moisture (%)')

		plt.tight_layout()

		if save_fig:
			os.remove('plots/plots.png')
			plt.savefig('plots/plots.png')
			plt.close()
