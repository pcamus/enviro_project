# Enviro+ test
# https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-enviro-plus
# display of T, H, P, Lum, Ox, rdduc NH3 in a Qt window.
# log on a Google sheet
# average measurements for logging on Google sheet
# philippe.camus@hepl.be
# 21/4/2020

import sys, random, time
from enviro_v3 import *   #Qt window Python description
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from bme280 import BME280 # T, H, P lib
try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus  #I2C
    
from ltr559 import LTR559  # luminosity lib
from enviroplus import gas # read gas sensor value with ADC

from pms5003 import PMS5003, ReadTimeoutError

# Set up BME280 weather sensor
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

# Set up light sensor
ltr559 = LTR559()

# Set up particles sensor
pms5003 = PMS5003()
time.sleep(1.0)

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('ThermostatPCA01.json', scope)
# https://towardsdatascience.com/accessing-google-spreadsheet-data-using-python-90a5bc214fd2

class mywindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # add timers to window.
        
        # timer 3 min      
        self.timer_log = QTimer()
        self.timer_log.timeout.connect(self.handleTimer_log)
        self.timer_log.start(3*60*1000) # each 3 minutes
       
        # timer 10s 
        self.timer_10s = QTimer()
        self.timer_10s.timeout.connect(self.handleTimer_10s)
        self.timer_10s.start(10000) # 10000 ms = 10 s
       
        # timer 1s 
        self.timer_1s = QTimer()
        self.timer_1s.timeout.connect(self.handleTimer_1s)
        self.timer_1s.start(1000) # 1000 ms
        
        self.ui.btn_rec.clicked.connect(self.rec_goo)  # record button action
        
        self.ui.actionQuitter.triggered.connect(lambda:app.quit()) # File -> Quit menu
        
        t=time.localtime()
        now_date= "{:0>2d}".format(t.tm_mday)+"/"+"{:0>2d}".format(t.tm_mon)+"/"+str(t.tm_year)
        now_time= "{:0>2d}".format(t.tm_hour)+":"+"{:0>2d}".format(t.tm_min)+":"+"{:0>2d}".format(t.tm_sec)
        self.statusBar().showMessage(now_date+"  "+now_time)
        
        # some instance variables
        self.state = "Not recording" # state variable
        
        # initialize sums and count
        self.sum_temp = 0
        self.sum_hum = 0
        self.sum_pres = 0
        self.sum_lum = 0
        self.sum_redg = 0
        self.sum_oxg = 0
        self.sum_nh3g = 0
        self.sum_pm1_0 = 0
        self.sum_pm2_5 = 0
        self.sum_pm10 = 0
        self.num_s = 0 # number of samples for average
        
        
    def handleTimer_log(self):
        # each log time
        # Compute average and round it 
        self.sum_temp = round(self.sum_temp / self.num_s, 1)
        self.sum_hum = round(self.sum_hum / self.num_s, 0)
        self.sum_pres = round(self.sum_pres / self.num_s, 0)
        self.sum_lum = round(self.sum_lum / self.num_s, 0)
        self.sum_redg = round(self.sum_redg / self.num_s, 0)
        self.sum_oxg = round(self.sum_oxg / self.num_s, 0)
        self.sum_nh3g = round(self.sum_nh3g / self.num_s, 0)
        self.sum_pm1_0 = round(self.sum_pm1_0 / self.num_s, 0)
        self.sum_pm2_5 = round(self.sum_pm2_5 / self.num_s, 0)
        self.sum_pm10 = round(self.sum_pm10 / self.num_s, 0)
    
       
        if self.state == "Recording":
            try:
                client = gspread.authorize(creds)
                sheet = client.open("Thermostatdata").sheet1
            except:   # sometimes the authentification fails, so retry it (a N approach retry will be useful)
                client = gspread.authorize(creds)
                sheet = client.open("Thermostatdata").sheet1
               
            t=time.localtime()
            now_date= "{:0>2d}".format(t.tm_mday)+"/"+"{:0>2d}".format(t.tm_mon)+"/"+str(t.tm_year)
            now_time= "{:0>2d}".format(t.tm_hour)+":"+"{:0>2d}".format(t.tm_min)+":"+"{:0>2d}".format(t.tm_sec)
            
            now_row=[now_date, now_time, self.sum_temp, self.sum_hum, self.sum_pres,self.sum_lum]
            now_row= now_row + [self.sum_redg, self.sum_oxg, self.sum_nh3g, self.sum_pm1_0, self.sum_pm2_5, self.sum_pm10]
            sheet.append_row(now_row) #raw data are sent to the Google sheet
        
        # initialize sums and count
        self.sum_temp = 0
        self.sum_hum = 0
        self.sum_pres = 0
        self.sum_lum = 0
        self.sum_redg = 0
        self.sum_oxg = 0
        self.sum_nh3g = 0
        self.sum_pm1_0 = 0
        self.sum_pm2_5 = 0
        self.sum_pm10 = 0
        self.num_s = 0 # number of samples for avergae
    
    def handleTimer_10s(self):
        # each 10s take measurement display it and sum it for averaging
        
        # measurements must be calibrated  
        temperature = bme280.get_temperature()
        self.sum_temp += temperature
        self.ui.lcd_temp.display(round(temperature,1))
         
        humidity = bme280.get_humidity()
        self.sum_hum += humidity
        self.ui.lcd_hum.display(round(humidity,0))
 
        pressure = bme280.get_pressure()
        self.sum_pres += pressure
        self.ui.lcd_pres.display(round(pressure,0))
 
        luminosity=ltr559.get_lux()
        self.sum_lum += luminosity
        self.ui.lcd_lum.display(round(luminosity,0))
        
        reduc_gaz=gas.read_reducing()# 100 kohms-> 1500 kohms 0-> 1000ppm
        reduc_gaz=(reduc_gaz-100000)/1500
        if reduc_gaz < 0 :
            reduc_gaz = 0 # negative values are not physical (sensor error)
        self.sum_redg += reduc_gaz
        self.ui.prog_reduc.setValue(reduc_gaz)
                
        ox_gaz=gas.read_oxidising() # 800 ohms-> 20 kohms 0-> 10ppm
        ox_gaz=(ox_gaz-800)/2000
        if ox_gaz < 0 :
            ox_gaz = 0 # negative values are not physical (sensor error)
        self.sum_oxg += ox_gaz
        self.ui.prog_ox.setValue(ox_gaz)
                
        nh3_gaz=gas.read_nh3() # 10 kohms-> 1500 kohms 0-> 300ppm
        nh3_gaz=(nh3_gaz-10000)/5000
        if nh3_gaz < 0 :
            nh3_gaz = 0 # negative values are not physical (sensor error)
        self.sum_nh3g += nh3_gaz
        self.ui.prog_nh3.setValue(nh3_gaz)
        
        readings = pms5003.read()      
        
        pm1_0=readings.pm_ug_per_m3(1.0) # PM 1.0 µg / m3
        self.sum_pm1_0 += pm1_0
        self.ui.lcd_pm1_0.display(pm1_0)
        pm2_5=readings.pm_ug_per_m3(2.5) # PM 2.5 µg / m3
        self.sum_pm2_5 += pm2_5
        self.ui.lcd_pm2_5.display(pm2_5)
        pm10=readings.pm_ug_per_m3(10) # PM 10 µg / m3
        self.sum_pm10 += pm10
        self.ui.lcd_pm10.display(pm10)
        
        self.num_s= self.num_s +1
        
    
    def handleTimer_1s(self):
        # each 1s display time
        t=time.localtime()
        now_date= "{:0>2d}".format(t.tm_mday)+"/"+"{:0>2d}".format(t.tm_mon)+"/"+str(t.tm_year)
        now_time= "{:0>2d}".format(t.tm_hour)+":"+"{:0>2d}".format(t.tm_min)+":"+"{:0>2d}".format(t.tm_sec)
        self.statusBar().showMessage(now_date+"  "+now_time)
        

    def rec_goo(self):  # Toogle state when pushing btn_rec button
        if self.state == "Recording":
            self.state = "Not recording"
            self.ui.btn_rec.setText("Start Recording")
        else:
            self.state = "Recording"
            self.ui.btn_rec.setText("Stop Recording")
        
app = QtWidgets.QApplication([])

application = mywindow()

application.show()

sys.exit(app.exec())  