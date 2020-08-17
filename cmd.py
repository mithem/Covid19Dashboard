from DataManager import DataManager
import tabulate
from matplotlib import pyplot as plt
from fileloghelper import Logger
import argparse
import constants

def print_summary():
    rows = []
    for measurement in manager.latest_measurements:
        rows.append(list(measurement))
    print(tabulate.tabulate(rows, headers=("Country", "T-Confirmed", "N-Confirmed", "T-Deaths", "N-Deaths", "T-Recovered", "N-Recovered", "Active", "Population %")))

def present_history():
    constants.setup(logger)

    supported_countries = constants.country_to_code.keys()
    countries_to_get = []
    for c in args.countries:
        c_lower = c.lower()
        if not c_lower in supported_countries:
            logger.warning(f"Country {c} not supported.")
        else:
            countries_to_get.append(c_lower)
    
    manager.countries_to_observe = countries_to_get
    logger.debug(f"Countries to observe: {countries_to_get}", True)
    manager.load_history()
    
    def showProperty(label: str):
        plt.figure()
        plt.title(label)
        for country in countries_to_get:
            l = []
            for i in manager.country_history[constants.country_to_code[country]]:
                if label == "Aktive Fälle":
                    l.append(i.active)
                elif label == "Genesene":
                    l.append(i.total_recovered)
                elif label == "Todesfälle":
                    l.append(i.total_deaths)
                else:
                    raise ValueError(f"Invalid label: {label}")
            plt.plot(l, label=country)
        
        plt.legend()
    
    if args.active:
        showProperty("Aktive Fälle")
    if args.recovered:
        showProperty("Genesene")
    if args.deaths:
        showProperty("Todesfälle")
    plt.show()

p = argparse.ArgumentParser()
p.add_argument("countries", type=str, nargs="+", help="Countries to observe")
p.add_argument("--summary", "-s", action="store_true", help="Show summary (all countries), latest data")
p.add_argument("--summary-only", "-so", action="store_true", help="Show summary (see above) and exit.")
p.add_argument("--active", "-a", action="store_true", help="Plot active cases")
p.add_argument("--recovered", "-r", action="store_true", help="Plot recovered people")
p.add_argument("--deaths", "-d", action="store_true", help="Plot dead people")
p.add_argument("--all", action="store_true", help="Plot active, recovered and dead.")
p.add_argument("--debug", action="store_true", help="Debug mode")
args = p.parse_args()

if args.all:
    args.active = True
    args.recovered = True
    args.deaths = True

logger = Logger("log", autosave=True)
manager = DataManager(logger, [], True)

if args.summary_only:
    manager.load_summary()
    print_summary()
    exit(0)
elif args.summary:
    manager.load_summary()
    print_summary()

present_history()