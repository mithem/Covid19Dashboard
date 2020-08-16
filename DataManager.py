import datetime
import json
import time

import requests
from fileloghelper import Logger

from models import *


class DataManager:
    
    latest_measurements: LatestMeasurements
    countries_to_observe: [str]
    country_history: dict
    logger: Logger
    debug: bool
    
    def load_from_api(self):
        self.logger.debug("Loading data from API...", self.debug)
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
        
        for country in self.countries_to_observe:
            capCountry = country[0].upper() + country[1:]
            self.logger.debug(f"Getting data for {capCountry}", self.debug)
            t3 = time.perf_counter()
            r = requests.get(f"https://api.covid19api.com/country/{country}")
            l = r.json()
            c = Country(l[0]["Country"], l[0]["CountryCode"])
            lower_code = c.code.lower()
            self.country_history[lower_code] = []
            for data in l:
                measurement = Measurement(c, datetime.datetime.fromisoformat(data["Date"][:-1]), data["Confirmed"], 0, data["Deaths"], 0, data["Recovered"], 0, data["Active"])
                self.country_history[lower_code].append(measurement)
            t4 = time.perf_counter()
            self.logger.debug(f"Got and processed data for {capCountry} in {t4 - t3}s", self.debug)
        
        t2 = time.perf_counter()
        self.logger.debug(f"Got and processed data from API: {t2 - t1}s", self.debug)
    
    def __init__(self, logger: Logger, countries_to_observe: list, debug: bool):
        self.latest_measurements = LatestMeasurements()
        self.countries_to_observe = countries_to_observe
        self.country_history = {}
        self.logger = logger
        self.debug = debug
        self.logger.debug(f"Countries to observe: {self.countries_to_observe}", self.debug)
        self.logger.success("Initialized DataManager", False)
