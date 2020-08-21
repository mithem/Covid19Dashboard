import requests
from fileloghelper import Logger
import tabulate

population_sizes = {
    "us": 328_239_000,
    "es": 47_331_000,
    "gb": 63_786_000,
    "br": 210_430_000,
    "it": 60_317_000,
    "fr": 67_081_000,
    "de": 83_149_000,
    "au": 8_902_000,
    "ch": 8_466_000
}

code_to_country = {}

country_to_code = {}

def setup(logger: Logger, debug: bool):
    r = requests.get("https://api.covid19api.com/countries")
    for country in r.json():
        code_lower = country["ISO2"].lower()
        country_name_lower = country["Country"].lower()
        
        code_to_country[code_lower] = country_name_lower
        country_to_code[country_name_lower] = code_lower
    logger.debug("Updated list of supported countries", True)
    if debug:
        print(tabulate.tabulate([[code, name, population_sizes.get(code, "N/A")] for code, name in code_to_country.items()], ("Code", "Name", "Population")))

str_total_cases = "Fälle insgesamt"
str_total_recovered = "Genesene"
str_total_deaths = "Todesfälle"
str_population_percent = "% der Bevölkerung (Gesamtfälle)"