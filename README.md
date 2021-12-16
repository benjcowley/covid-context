# Covid with Context
Linear Regression based analysis of COVID-19 statistics. 

Any Feedback and additional requests of are more than welcome, if you want to run the program for yourself for any reason, just install the library and add your API keys, uses in anyway possible, apart from for use spreading misinformation.

All credit to Our world in data, dataset used is found [here.](https://github.com/owid/covid-19-data/tree/master/public/data)

All original work, use as required via license.
## Calculations & Rational
Idea behind the project was to add some more context to the covid statistics. 
The correlation of cases and tests are plotted, then linear regression is used to plot the best fit line. The assumptions are low testing numbers and higher covid cases results in the worst performing outcomes for countries. The residuals are calculated and the high postive points (below the line) result as the worst performing. 

## Installation Requirements 
Python 3.7.7 or higher is required.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the following requirements.
```bash
pip install pandas
pip install tweepy
pip install plotly
```

## File Scrutcture 
main.py - Data processing, calculations, plotting and twitter API posting.
keys.py - Dictionary containing developer API keys.
readme.md - Read me file.
## License
[ MIT ](https://choosealicense.com/licenses/mit/)