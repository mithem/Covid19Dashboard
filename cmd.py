from DataManager import DataManager
import tabulate
from matplotlib import pyplot as plt
from fileloghelper import Logger
import argparse
import constants

def capitalized(somestring: str):
    r = []
    l = somestring.split(" ")
    for i in l:
        r.append(i[0].upper() + i[1:])
    return " ".join(r)

def print_summary():
    rows = []
    for measurement in manager.latest_measurements:
        rows.append(list(measurement))
    print(tabulate.tabulate(rows, headers=("Country", "T-Confirmed", "N-Confirmed", "T-Deaths", "N-Deaths", "T-Recovered", "N-Recovered", "Active", "Population %")))

def present_history(countries: [str]):
    constants.setup(logger, args.debug)
    manager.countries_to_observe = countries
    logger.debug(f"Countries to observe: {manager.countries_to_observe}", True)
    manager.load_history()
    
    def showProperty(label: str):
        plt.figure()
        plt.title(label)
        for country in manager.countries_to_observe:
            l = []
            for i in manager.country_history[constants.country_to_code[country]]:
                if label == constants.str_total_cases:
                    l.append(i.active)
                elif label == constants.str_total_recovered:
                    l.append(i.total_recovered)
                elif label == constants.str_total_deaths:
                    l.append(i.total_deaths)
                elif label == constants.str_population_percent:
                    l.append(i.population_percent)
                else:
                    raise ValueError(f"Invalid label: {label}")
            plt.plot(l, label=capitalized(country))
        
        plt.legend()
    
    if args.active:
        showProperty(constants.str_total_cases)
    if args.recovered:
        showProperty(constants.str_total_recovered)
    if args.deaths:
        showProperty(constants.str_total_deaths)
    if args.population_percent:
        showProperty(constants.str_population_percent)
    plt.show()

p = argparse.ArgumentParser()
p.add_argument("countries", type=str, nargs="+", help="Countries to observe")
p.add_argument("--summary", "-s", action="store_true", help="Show summary (all countries), latest data")
p.add_argument("--summary-only", "-so", action="store_true", help="Show summary (see above) and exit")
p.add_argument("--cases", "-c", action="store_true", help="Plot active cases")
p.add_argument("--recovered", "-r", action="store_true", help="Plot recovered people")
p.add_argument("--deaths", "-d", action="store_true", help="Plot dead people")
p.add_argument("--all", "-a", action="store_true", help="Plot active, recovered and dead")
p.add_argument("--debug", action="store_true", help="Debug mode")
p.add_argument("--population-percent", "--population-%", "--pop-percent", "--pop-%", "-p-%", "-p%", "-pp", action="store_true", help="Plot % of active cases of population")
args = p.parse_args()

if args.all:
    args.active = True
    args.recovered = True
    args.deaths = True
    args.population_percent = True

logger = Logger("log", autosave=True)


if not args.summary and not args.summary_only and not (args.active or args.recovered or args.deaths or args.population_percent):
    logger.warning("No output specified (active/recovered etc.). Use the -h option to get more information.")
    exit(0)

manager = DataManager(logger, args.countries, True)

if args.summary_only:
    manager.load_summary()
    print_summary()
    exit(0)
elif args.summary:
    manager.load_summary()
    print_summary()

present_history(args.countries)