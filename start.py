#!/usr/bin/python3
import os
import call_to_dxcc
from time import sleep
from cabrillo import qso
from cabrillo import QSO
from cabrillo.parser import parse_log_file
from datetime import datetime
class myClass:
    call_list = ""
    mult_list = ""
    points = 0
    final_points = 0
    final_score = 0
    multiplicator = 0
    mult_exist = ""
    mode = ""

#### Log files has to be UPPERCASE , to be fixed 


    def log_compute(self):
        print("computing "+ logname + " log file")
        cab = parse_log_file("logs/"+str(logname))
        for line in cab.qso:
            self.dx_callsign  = str(line).split()[8]
            self.date = str(line).split()[3] + " " + str(line).split()[4][:2]+":"+str(line).split()[4][2:]
            #self.time = str(line).split()[4] #.replace('-', ',')   +','+str(line).split()[4][:2]+":"+str(line).split()[4][2:]
            self.mode = str(line).split()[2]
            self.band = str(line).split()[1]
            self.exch_sent = str(line).split()[7]
            self.exch_rcvd = str(line).split()[10]
            self.de_callsign = str(line).split()[5]
            qso1 = QSO(self.band , self.mode, datetime.strptime(self.date, '%Y-%m-%d %H:%M'), self.de_callsign, self.dx_callsign, ['599', self.exch_sent], ['599', self.exch_rcvd], t=None)

            try:
                dx_cab = parse_log_file("logs/"+self.dx_callsign+".cbr")
                for dx_line in dx_cab.qso:
                    self.dx_callsign2  = ( str(dx_line).split()[8] )
                    self.date2 = str(dx_line).split()[3] + " " + str(dx_line).split()[4][:2] + ":" + str(dx_line).split()[4][2:]
                    #self.time2 = str(dx_line).split()[4]  # .replace('-', ',')   +','+str(line).split()[4][:2]+","+str(line).split()[4][2:]
                    self.mode2 = str(dx_line).split()[2]
                    self.band2 = str(dx_line).split()[1]
                    self.exch_sent2 = str(dx_line).split()[7]
                    self.exch_rcvd2 = str(dx_line).split()[10]
                    self.de_callsign2 = str(dx_line).split()[5]
                    qso2 = QSO(self.band2 , self.mode2, datetime.strptime(self.date2, '%Y-%m-%d %H:%M'), self.de_callsign2, self.dx_callsign2, ['599', self.exch_sent2], ['599', self.exch_rcvd2], t=None)
                    compare_qso = qso1.match_against(qso2)
                    print (qso1)
                    print (qso2)				
                    if compare_qso == True : 
                        print ("CONDITIE TRUE")
                        print(compare_qso)
                        print (qso1)
                        print (qso2)

                        country, continent, dxcc_number = call_to_dxcc.data_for_call(self.dx_callsign)
                        self.call_exist = self.call_list.rfind(str(self.dx_callsign)+",")
                        self.call_list = str(self.call_list) + self.dx_callsign + ","
                        self.mult_exist = self.mult_list.rfind(str(country) + ",")
       	                if (continent != "EU"):
                            self.points = 8
                        else:
                            self.points = 4
                        if  country == "YO":
                            self.points = 0
                        if self.call_exist != -1 :
                            self.points =0
                            self.qso_status = "Duplicate QSO"
                        else:
                            self.qso_status =  "Valid QSO"
                        if self.mult_exist == -1 :
                            self.multiplicator = self.multiplicator + 1
                            self.mult_list = self.mult_list + country + ","
                        self.final_points = self.final_points + self.points
                        #print (str(self.date) + "," + str(self.dx_callsign) + "," + str(self.points) +"," + self.qso_status + "," + self.mode + "," + self.band + "," + self.exch_sent + "," + self.exch_rcvd)
                        print ("##### " + logname +" SUMARY #####")
                        print("points = " + str(self.final_points))
                        print( "multipliers = " + str(self.multiplicator) )
                        print ("final score = " + str(self.multiplicator*self.final_points) + " points")
                        print ("##### END SUMMARY #####")
                        #print (qso1)
                        #print (qso2)
                        break
                    else:
                        print("No match")     
            except:
                print("Missing log " + self.dx_callsign + ".cbr file")


for logname in sorted(os.listdir("logs/")):
    try:
        cab = parse_log_file("logs/"+str(logname))
        myClass().log_compute()

    except:
        print("file " + str(logname)+ " is not valid cabrillo")
    
