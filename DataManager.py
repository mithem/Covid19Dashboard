import datetime
import json
import time

import requests
from fileloghelper import Logger

import constants
from models import *


class DataManager:
    
    latest_measurements: LatestMeasurements
    _countries_to_observe: [str]
    country_history: dict
    logger: Logger
    debug: bool
    
    @property
    def countries_to_observe(self):
        return self._countries_to_observe
    
    @countries_to_observe.setter
    def countries_to_observe(self, c_to_observe: [str]):
        self._countries_to_observe = []
        supported_countries = constants.country_to_code.keys()
        for i in c_to_observe:
            i_lower = i.lower()
            if i_lower in supported_countries:
                self._countries_to_observe.append(i)
            maybe_country_name = constants.code_to_country.get(i_lower, None)
            if maybe_country_name != None:
                self._countries_to_observe.append(maybe_country_name)
            else:
                try:
                    self.logger.warning(f"Unable to identify country {i}.", self.debug)
                except:
                    pass
    
    def load_summary(self):
        self.logger.debug("Loading summary...", self.debug)
        t1 = time.perf_counter()
        
        r = requests.get("https://api.covid19api.com/summary")
        data = r.json()
        
        global_data = data["Global"]
        global_country = Country("Global", "Global")
        global_measurement = Measurement(global_country, datetime.datetime.now(), global_data["TotalConfirmed"], global_data["NewConfirmed"], global_data["TotalDeaths"], global_data["NewDeaths"], global_data["TotalRecovered"], global_data["NewRecovered"])
        
        for country in data["Countries"]:
            c = Country(country["Country"], country["CountryCode"])
            measurement = Measurement(c, datetime.datetime.fromisoformat(country["Date"][:-1]), country["TotalConfirmed"], country["NewConfirmed"], country["TotalDeaths"], country["NewDeaths"], country["TotalRecovered"], country["NewRecovered"])
            self.latest_measurements.append(measurement)
        
        self.latest_measurements.sort()
        self.latest_measurements.insert(0, global_measurement)
        t2 = time.perf_counter()
        self.logger.debug(f"Got summary for {len(data['Countries'])} countries in {t2 - t1}s", self.debug)
        
    def load_history(self):
        print(f"CTOObserve before loading: {self.countries_to_observe}")
        for country in self.countries_to_observe:
            capCountry = country[0].upper() + country[1:]
            self.logger.debug(f"Getting data for {capCountry}", self.debug)
            t1 = time.perf_counter()
            r = requests.get(f"https://api.covid19api.com/total/country/{country}")
            l = r.json()
            code = l[0].get("CountryCode", "")
            if code == "":
                name = l[0].get("Country", "")
                if name == "":
                    try:
                        c = Country(country, constants.country_to_code[country])
                    except:
                        try:
                            c = Country(constants.code_to_country[country])
                        except:
                            self.logger.warning(f"Needed to skip country {country} as it is unidentifiable though known to covid19api.com")
                else:
                    c = Country(name, constants.country_to_code[name.lower()])
            else:
                c = Country(constants.code_to_country[code.lower()], code)
            lower_code = c.code.lower()
            self.country_history[lower_code] = []
            for data in l:
                measurement = Measurement(c, datetime.datetime.fromisoformat(data["Date"][:-1]), data["Confirmed"], 0, data["Deaths"], 0, data["Recovered"], 0, data["Active"])
                self.country_history[lower_code].append(measurement)
            t2 = time.perf_counter()
            self.logger.debug(f"Got and processed data for {capCountry} in {t2 - t1}s", self.debug)
    
    def __init__(self, logger: Logger, countries_to_observe: list, debug: bool):
        self.latest_measurements = LatestMeasurements()
        self.countries_to_observe = countries_to_observe
        self.country_history = {}
        self.logger = logger
        self.debug = debug
        try:
            self.logger.success("Initialized DataManager", False)
        except:
            pass
