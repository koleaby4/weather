# Overview

This is a small project built around jupyter notebook,
which looks at some weather data sourced from https://www.whiteswandata.com/s/weatherjson.gz

# Installation instructions

### Get sources

1. open command line
1. clone the project `git clone https://github.com/koleaby4/weather.git`
1. open project folder `cd weather`

### Install dependencies
1. OPTIONAL: create and activate your virtual environment
1. install dependencies `pip install -r requirements.txt`

### Configure google API key

One of charts is using google maps.

For it to work:
1. follow [these instructions]( https://developers.google.com/maps/documentation/javascript/get-api-key) to get google API key
1. either put it into `secret.txt` file or store it in `GOOGLE_API_KEY` environment variable

### Open jupyter notebook
1. in command line execute `jupyter notebook`
1. click on `data_explorer.ipynb` to open notebook
1. In menu bar select `Cell > Run All`
