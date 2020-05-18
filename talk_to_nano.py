import serial
import time
import sqlite3

# Sensor Keys
# 1 = AM2320 humid; 2 = AM2320 temp; 3 = MQ4; 4 = MQ7; 5 = BMP180 pressure;
# 6 = BMP180 temp; 7 = soil temp; 8 = soil moisture

class Getnanoreadings:

     def __init__(self):
          self.ser = self.connect_to_nano()

     @staticmethod
     def connect_to_nano():
          try:
               ser = serial.Serial('/dev/ttyUSB0', 9600)
          except Exception as e:
               print('not on USB0, trying USB1')
               ser = serial.Serial('/dev/ttyUSB1', 9600)
          time.sleep(2)
          return ser

     def read_sensor(self, sensor_key):
          self.ser.write(str(sensor_key).encode())
          time.sleep(1)
          output = self.ser.readline()
          return output.decode().rstrip()

     def data_clean(self, curr_data_point, past_data_point):
          if not 0 <= curr_data_point <= 100:
               x = past_data_point
          else:
               x = curr_data_point
          low = past_data_point - past_data_point * 0.1
          high = past_data_point + past_data_point * 0.1
          if not low <= curr_data_point <= high:
               x = past_data_point
          else:
               x = curr_data_point
          return x

     def sql_insert(self):
          data = []
          data.append(time.ctime())
          print('reading data')
          conn = sqlite3.connect('/home/pi/Documents/Garden-Monitor/data.db')
          # c = conn.cursor()
          # c.execute('SELECT * FROM from_nano ORDER BY ROWID DESC LIMIT 1')
          # last_data = c.fetchone()
          for i in range(8):
               curr_data = self.read_sensor(i+1)
               # data_point = self.data_clean(curr_data, last_data)
               data.append(curr_data)
          print('inserting data')
          c = conn.cursor()
          c.execute("INSERT INTO from_nano(datatime, humidity, air_temp1, methane_levels, CO_levels, pressure, air_temp2, soil_temp, soil_moisture) VALUES(?,?,?,?,?,?,?,?,?)", data)
          conn.commit()
          print('finished')
          conn.close()
