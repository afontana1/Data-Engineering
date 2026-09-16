# Zillow Scraper


This repo allows the user to scrape Zillow for properties in Chicago meeting certain criteria\*.
It's divided into two parts: a scraper and a processing pipeline.

The **scraper** pulls all properties added to Zillow within the last week that meet the criteria and stores them as a JSON file in `raw_data/`, named by date.
For example, data pulled on Jan 13, 2021 would be stored in `raw_data/20210113.json`.
The scraper is invoked as follows:
```bash
python -m zillow-scraper.scrape [max-pages]
```
The `max-pages` argument is optional, and indicates how many search pages to search through before stopping.
If omitted, the scraper will exhaust all pages.
(Providing `max-pages` is mainly useful for testing.)

The **pipeline** just does some basic cleaning on the scraped data.
It is invoked with
```bash
python -m zillow_scraper.process <date>
```
where `<date>` is replaced with the date of the file to be processed (e.g 20210402).


\* The city and criteria could be modified but are not parameterized.


## Installing

I did this using a virtual environment, but that was a pain -- geopandas has complicated dependencies.
I would recommend creating a conda environment using:
```bash
conda create -n zillow-scraper python=3.9 pandas matplotlib geopy geopandas beautifulsoup requests
```
I haven't done this, but I think it should handle the hard parts of the dependencies.

If you wish to use a virtual environment, before installing from the requirements file (`pip install -r requirements.txt`) I think you'll need to install [GDAL](https://gdal.org) first, which I was able to do on a Mac with `brew install GDAL`.
