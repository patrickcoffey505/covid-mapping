
import pandas as pd
from urllib.request import urlopen
import json

state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}


def get_state_pop():
    state_pop = pd.DataFrame(pd.read_json('https://api.census.gov/data/2019/pep/population?get=NAME,POP&for=state:*'))
    
    header = list(state_pop.iloc[0])
    state_pop = state_pop[1:]
    state_pop.columns = header
    state_pop = state_pop.set_index('NAME')
    state_pop = state_pop.sort_index()
    
    state_pop = state_pop.drop('District of Columbia', axis=0)
    state_pop = state_pop.drop('Puerto Rico', axis=0)
    
    state_pop = state_pop.astype({'POP': 'int'})

    state_pop['state'] = state_abbrev.values()
    state_pop = state_pop.set_index('state')
    state_pop = state_pop.sort_index()
    
    return state_pop['POP']

def get_us_covid_data():
    url = urlopen('https://api.covidtracking.com/v1/us/current.json')
    usdata = json.loads(url.read())
    usdata = dict(usdata[0])
    
    return usdata
    
def get_state_data():
    # only includes num of cases
    
    statesdata = pd.DataFrame(pd.read_json('https://api.covidtracking.com/v1/states/current.json'), columns = ['state', 'positive', 'negative', 'totalTestResults', 'positiveIncrease', 'negativeIncrease'])
    statesdata = statesdata.set_index('state')
    statesdata = statesdata.sort_index()
    
    statesdata['population'] = get_state_pop()
    
    statesdata = statesdata[statesdata.population.isnull() == False]

    return statesdata
    


curr_statesdata = get_state_data()
curr_usdata = get_us_covid_data()

curr_usdata['population'] = curr_statesdata['population'].sum()

curr_statesdata['rel_positive'] = curr_statesdata['positive'] / curr_usdata['positive']
curr_statesdata['rel_population'] = curr_statesdata['population'] / curr_usdata['population']
curr_statesdata['value'] = 100.00 * (curr_statesdata['positive'] / curr_statesdata['population'])
