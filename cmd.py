from DataManager import DataManager
import tabulate
from matplotlib import pyplot as plt
from fileloghelper import Logger
import argparse

p = argparse.ArgumentParser()
p.add_argument("--debug", "-d", action="store_true")
args = p.parse_args()

logger = Logger("cmd.log", autosave=True)

manager = DataManager(logger, ["germany"], args.debug)
manager.load_from_api()

rows = []
for measurement in manager.latest_measurements:
    rows.append(list(measurement))

print("Got rows matrix")
print(tabulate.tabulate(rows, headers=("Country", "T-Confirmed", "N-Confirmed", "T-Deaths", "N-Deaths", "T-Recovered", "N-Recovered", "Active", "Population %")))

print(manager.country_history["de"][100].allData())

plt.plot([i.active for i in manager.country_history["de"]])

plt.show()