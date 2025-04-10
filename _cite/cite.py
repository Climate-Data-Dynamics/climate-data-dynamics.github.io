"""
cite process to convert sources and metasources into full citations
"""

from importlib import import_module
from pathlib import Path
from dotenv import load_dotenv
from util import *


# load environment variables
load_dotenv()


# error flag
error = False

# output citations file
output_file = "_data/citations.yaml"


log()

log("Compiling sources")

# master list of sources
sources = []

# in-order list of plugins to run
plugins = ["google-scholar", "orcid", "sources"]

# loop through plugins
for plugin in plugins:
    # convert into path object
    plugin = Path(f"plugins/{plugin}.py")

    log(f"Running {plugin.stem} plugin")

    # get all data files to process with current plugin
    files = Path.cwd().glob(f"_data/{plugin.stem}*.*")
    files = list(filter(lambda p: p.suffix in [".yaml", ".yml", ".json"], files))

    log(f"Found {len(files)} {plugin.stem}* data file(s)", 1)

    # loop through data files
    for file in files:
        log(f"Processing data file {file.name}", 1)

        # load data from file
        try:
            data = load_data(file)
            # check if file in correct format
            if not list_of_dicts(data):
                raise Exception("File not a list of dicts")
        except Exception as e:
            log(e, 2, "ERROR")
            error = True
            continue

        # loop through data entries
        for index, entry in enumerate(data):
            log(f"Processing entry {index + 1} of {len(data)}, {label(entry)}", 2)

            # run plugin on data entry to expand into multiple sources
            try:
                entry = import_module(f"plugins.{plugin.stem}").main(entry)
                # check that plugin returned correct format
                if not list_of_dicts(entry):
                    raise Exception("Plugin didn't return list of dicts")
            except Exception as e:
                log(e, 3, "ERROR")
                error = True
                continue

            # loop through sources
            for source in entry:
                if plugin.stem != "sources":
                    log(label(source), 3)

                # include meta info about source
                source["plugin"] = plugin.name
                source["file"] = file.name
                # add source to master list
                sources.append(source)

            if plugin.stem != "sources":
                log(f"{len(entry)} source(s)", 3)


# merge sources with matching (non-blank) ids
for a in range(0, len(sources)):
    _id = sources[a].get("id", "")
    if not _id:
        continue
    for b in range(a + 1, len(sources)):
        if sources[b].get("id", "").lower() == _id.lower():
            sources[a].update(sources[b])
            sources[b] = {}
sources = [entry for entry in sources if entry]


log(f"{len(sources)} total source(s) to cite")


log()

log("Generating citations")

# List of Journals to include as publishers on the website
journals = [
            "Annual Review of Marine Science",
            "Bulletin of the American Meteorological Society", 
            "Climate Dynamics", 
            "Environmental Research Letters",
            "Frontiers in Climate", 
            "Frontiers in Marine Science",
            "Geophysical Research Letters", 
            "Geoscientific Model Development",
            "Journal of Advances in Modeling Earth Systems",
            "Journal of Atmospheric and Oceanic Technology", 
            "Journal of Climate", 
            "Journal of Fluid Mechanics",
            "Journal of Geophysical Research: Oceans",
            "Journal of Physical Oceanography", 
            "Journal of the Atmospheric Sciences", 
            "Nature Climate Change",
            "Nature Communications", 
            "Nature Reviews Earth &amp; Environment",
            "Nature", 
            "Ocean Mixing", 
            "Ocean Modelling", 
            "Ocean Science", 
            "Philosophical Transactions of the Royal Society A: Mathematical, Physical and Engineering Sciences",
            "Reviews of Geophysics",
            "Science", 
            "Scientific Reports"
            ]

# list of new citations
citations = []

# loop through compiled sources
for index, source in enumerate(sources):
    log(f"Processing source {index + 1} of {len(sources)}, {label(source)}")

    # new citation data for source
    citation = {}

    # source id
    _id = source.get("id", "").strip()

    # Manubot doesn't work without an id
    if _id:
        log("Using Manubot to generate citation", 1)

        try:
            # run Manubot and set citation
            citation = cite_with_manubot(_id)

        # if Manubot cannot cite source
        except Exception as e:
            # if regular source (id entered by user), throw error
            if source.get("plugin", "") == "sources.py":
                log(e, 3, "ERROR")
                error = True
            # otherwise, if from metasource (id retrieved from some third-party API), just warn
            else:
                log(e, 3, "WARNING")
                # discard source
                # continue

    # preserve fields from input source, overriding existing fields
    citation.update(source)

    # ensure date in proper format for correct date sorting
    if citation.get("date", ""):
        citation["date"] = format_date(citation.get("date", ""))
        # remove entries that are not from journal publications
        if citation["publisher"] in journals:
            # add new citation to list
            citations.append(citation)

log()

log("Saving updated citations")

# save new citations
try:
    save_data(output_file, citations)
except Exception as e:
    log(e, level="ERROR")
    error = True


# exit at end, so user can see all errors in one run
if error:
    log("Error(s) occurred above", level="ERROR")
    exit(1)
else:
    log("All done!", level="SUCCESS")

log("\n")
