from talk_to_nano import Getnanoreadings
from plots import Genplots
import time
import os

reading = Getnanoreadings()
plots = Genplots()

while True:
	reading.sql_insert()
	print('done {}'.format(time.ctime()))
	plots.gen_plots()
	os.system('git add *')
	os.system('git commit -m "update {}"'.format(time.ctime()))
	os.system('git push')
	time.sleep(300)