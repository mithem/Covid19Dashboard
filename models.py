import datetime
from constants import population_sizes

class Country:
    name: str
    code: str
    
    def __init__(self, name: str, code: str):
        self.name = name
        self.code = code
    
    def __gt__(self, other):
        return self.code > other.code

class Measurement:
    country: Country
    date: datetime.datetime
    total_confirmed: int
    new_confirmed: int
    total_deaths: int
    new_deaths: int
    total_recovered: int
    new_recovered: int
    population_percent: float
    active: int
    
    iter_idx: int
    
    def __init__(self, country: Country, date: datetime.datetime, total_confirmed: int, new_confirmed: int, total_deaths: int, new_deaths: int, total_recovered: int, new_recovered: int, active: int = "N/A"):
        self.country = country
        self.date = date
        self.total_confirmed = total_confirmed
        self.new_confirmed = new_confirmed
        self.total_deaths = total_deaths
        self.new_deaths = new_deaths
        self.total_recovered = total_recovered
        self.new_recovered = new_recovered
        self.active = active
        
        pop = population_sizes.get(country.code.lower(), None)
        if pop != None:
            self.population_percent = (float(total_confirmed) / float(pop)) * 100.0
        else:
            self.population_percent = None
        
        self.iter_idx = -1
    
    def __str__(self):
        return f"{self.country.code.upper()}:{self.total_confirmed}"
    
    def __gt__(self, other):
        return self.country > other.country
    
    def __iter__(self):
        self.iter_idx = -1
        return self
    
    def __next__(self):
        self.iter_idx += 1
        if self.iter_idx == 0:
            return self.country.code
        elif self.iter_idx == 1:
            return self.total_confirmed
        elif self.iter_idx == 2:
            return self.new_confirmed
        elif self.iter_idx == 3:
            return self.total_deaths
        elif self.iter_idx == 4:
            return self.new_deaths
        elif self.iter_idx == 5:
            return self.total_recovered
        elif self.iter_idx == 6:
            return self.new_recovered
        elif self.iter_idx == 7:
            return self.active
        elif self.iter_idx == 8:
            if self.population_percent == None:
                return "N/A"
            else:
                return f"{self.population_percent}%"
        else:
            raise StopIteration
    
    def humanReadable(self):
        return f"""Country: {self.country.code.upper()}
T-Confirmed: {self.total_confirmed}
N-Confirmed: {self.new_confirmed}
T-Deaths: {self.total_deaths}
N-Deaths: {self.new_deaths}
T-Recovered: {self.total_recovered}
N-Recovered: {self.new_recovered}
Active: {self.active}
    """

class LatestMeasurements(list):
    def __getitem__(self, key):
        key = str(key).lower()
        for measurement in self:
            if measurement.country.code == key or measurement.country.name.lower() == key:
                return measurement
        return None
    
    def __str__(self):
        for m in self:
            print(str(m))