from talk_to_nano import Getnanoreadings
import time

reading = Getnanoreadings()

while True:
	reading.sql_insert()
	print('done {}'.format(time.ctime()))
	time.sleep(300)