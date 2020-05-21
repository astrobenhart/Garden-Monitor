from talk_to_nano import Getnanoreadings
from plots import Genplots
import time
import os

reading = Getnanoreadings()
#plots = Genplots()

while True:
	reading.sql_insert()
	# plots.gen_plots()
	# os.system('git add plots/plots.png')
	os.system('git add data.db')
	os.system('git commit -m "update db {}"'.format(time.ctime()))
	os.system('git push')
	print('done {}'.format(time.ctime()))
	time.sleep(300)
