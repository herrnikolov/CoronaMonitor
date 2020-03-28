#!/usr/bin/env python
from lcdproc.server import Server
from bs4 import BeautifulSoup
import requests
import re
import time
import math
import datetime

def main():
    #Variables
    lcd_proc_server = "127.0.0.1"
    measurement_interval = 60
   
    # Instantiate LCDProc
    lcd = Server(debug=False, hostname=lcd_proc_server)
    lcd.start_session()

    # Add screen
    screenCovid = lcd.add_screen("Covid")
    # screenCovid.set_heartbeat("off")
    screenCovid.set_duration(99)

    #Dates
    days_value= ""
    days_widget = screenCovid.add_string_widget("Date", x=1, y=1, text=days_value)
    #Infected
    infected_value= ""
    infected_widget = screenCovid.add_string_widget("Infected", x=1, y=2, text=infected_value)
    # #Deaths
    deaths_value= ""
    deaths_widget = screenCovid.add_string_widget("Deaths", x=1, y=3, text=deaths_value)
    # #Recovered
    recovered_value= ""
    recovered_widget = screenCovid.add_string_widget("Recovered", x=1, y=4, text=recovered_value)
    
    infected_h  = [""] *3
    deaths_h = [""] *3
    recover_h = [""] *3
    
    try:
        while True:
            print "Update   " + str(datetime.datetime.now())
            current_day_0 = datetime.date.today().day
            prevous_day_1 = datetime.date.today().day - 1
            prevous_day_2 = datetime.date.today().day - 2
            days = "  " + str(current_day_0) + "  " + str(prevous_day_1) + "  " + str(prevous_day_2)
            days_value="Date: " + days
            days_widget.set_text(days_value)
            
            # Insert your country URL here
            url_c = "https://corona.help/country/bulgaria"
            page_c = requests.get(url_c)
            soup_c = BeautifulSoup(page_c.text, 'html.parser')
            history = re.findall('^\s+data: \[([0-9,]+)\],$',str(soup_c),re.MULTILINE)
            
            history_cases = history[0].split(',')
            history_deaths = history[1].split(',')
            history_cured = history[2].split(',')
            
            # Print
            current_day_0_infected = infections_c = soup_c.select('h2')[1].text.strip()
            current_day_0_deaths = soup_c.select('h2')[2].text.strip()
            current_day_0_recovered = soup_c.select('h2')[3].text.strip()
            
            #Curent Infected
            current_day_0_infected = current_day_0_infected.encode('ascii', 'ignore')
            infected_h[0] = current_day_0_infected
            print infected_h
            infected_value="Cases:  " + current_day_0_infected            
            infected_widget.set_text(infected_value)
            
            #Curent Deaths
            current_day_0_deaths = current_day_0_deaths.encode('ascii', 'ignore')
            deaths_h[0] = current_day_0_deaths
            print deaths_h
            deaths_value="Deaths: " + current_day_0_deaths
            deaths_widget.set_text(deaths_value)
            
            #Curent Recovered
            current_day_0_recovered = current_day_0_recovered.encode('ascii', 'ignore')
            recover_h [0] = current_day_0_recovered
            print recover_h
            recovered_value="Cured:  " + current_day_0_recovered
            recovered_widget.set_text(recovered_value)
            
            #Yesterday
            infected_h[1] = history_cases[-3]
            deaths_h[1] = history_deaths[-3]
            recover_h[1] = history_cured[-2]
            
            #Yesterday - 1
            infected_h[2] = history_cases[-4]
            deaths_h[2] = history_deaths[-4]
            recover_h[2] = history_cured[-3]

            infected_complete =  "Cases: " + str(infected_h[0]) + " " + str(infected_h[1])+ " " + str(infected_h[2])
            infected_widget.set_text(infected_complete)
            
            deaths_complete = "Deaths:  " + str(deaths_h[0]) + "   " + str(deaths_h[1]) + "   " + str(deaths_h[2])
            deaths_widget.set_text(deaths_complete)
            
            recover_complete = "Cured:   " + str(recover_h[0]) + "   " + str(recover_h[1]) + "   " + str(recover_h[2])
            recovered_widget.set_text(recover_complete)
            
            time.sleep(measurement_interval)
    finally:     # clean up on exit
        lcd.del_screen(screenCovid.ref)
# Run
if __name__ == "__main__":
    main()