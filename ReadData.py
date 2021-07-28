from urllib.request import urlopen
import pandas as pd
import numpy as np
import plotly.express as px
import json
def read_data():
    # List of states by abbreviation
    all_states = ['AN', 'AP', 'AR', 'AS', 'BR', 'CH', 'CT', 'DL', 'DN', 'GA', 'GJ', 'HP',
                  'HR', 'JH', 'JK', 'KA', 'KL', 'LA', 'LD', 'MH', 'ML', 'MN', 'MP', 'MZ',
                  'NL', 'OR', 'PB', 'PY', 'RJ', 'SK', 'TG', 'TN', 'TR', 'TT', 'UN', 'UP',
                  'UT', 'WB']
    # Create dictionary relating state abbreviations to state names
    states_info = pd.read_csv("india_states.csv")
    states_keys = dict()
    for index, row in states_info.iterrows():
        states_keys[row['abbreviation']] = row['state']

    # Get data from covid19india.org API
    from urllib.request import urlopen
    import json
    url = "https://api.covid19india.org/v4/min/timeseries.min.json"
    response = urlopen(url)
    data_json = json.loads(response.read())
    lastWeek = pd.DataFrame(columns=['state', 'state_name', 'cartodb_id', 'state_code', 'date', 'confirmed', 'deceased', 'recovered', 'tested', 'vaccinated1', 'vaccinated2'])
    df_statesToIDs = pd.read_csv('India States with Codes.csv')
    statesToIDs = dict()
    for index, row in df_statesToIDs.iterrows():
        statesToIDs[row['Input Data Listing']] = list()
        statesToIDs[row['Input Data Listing']].append(row['cartodb_id'])
        statesToIDs[row['Input Data Listing']].append(row['state_code'])
    for s in all_states:
        dates = list(data_json[s]['dates'].keys())
        lastElementIndex = len(dates) - 1
        seventhToLastElementIndex = lastElementIndex - 7
        lastSevenDaysKeys = dates[seventhToLastElementIndex:lastElementIndex]
        for fd in lastSevenDaysKeys:
            record = (((data_json[s])['dates'])[fd])['total']
            print(record)
            state = s
            state_name = str()
            cartodb_id = int()
            state_code = int()
            if state in states_keys.keys():
                state_name = states_keys[state]
                try:
                    cartodb_id = (statesToIDs[state_name])[0]
                    state_code = ((statesToIDs[state_name])[1])
                except:
                    print("Error with cartodb_id and/or state_code conversion for ", state_name)
            else:
                state_name = ""
                cartodb_id = -1
                state_code = -1
            date = fd
            confirmed = int()
            try:
                confirmed = record['confirmed']
            except:
                confirmed = np.nan
            deceased = int()
            try:
                deceased = record['deceased']
            except:
                deceased = np.nan
            recovered = int()
            try:
                recovered = record['recovered']
            except:
                recovered = np.nan
            tested = int()
            try:
                tested = record['tested']
            except:
                tested = np.nan
            vaccinated1 = int()
            try:
                vaccinated1 = record['vaccinated1']
            except:
                vaccinated1 = np.nan
            vaccinated2 = int()
            try:
                vaccinated2 = record['vaccinated2']
            except:
                vaccinated2 = np.nan
            if state_name != "" and state_name != "Ladakh": # Ladakh is not a state in the GeoJSON
                lastWeek.loc[len(lastWeek.index)] = [state, state_name, cartodb_id, state_code, date, confirmed, deceased, recovered, tested, vaccinated1, vaccinated2]
    print(lastWeek)
    lastWeek.to_csv("weekly-india-covid-numbers.csv")
    aggregatedWeek = pd.DataFrame(columns=['state', 'state_name', 'cartodb_id', 'state_code', 'confirmed', 'deceased', 'recovered', 'tested', 'vaccinated1', 'vaccinated2'])
    aggregatedWeek = lastWeek.groupby(['state', 'state_name', 'cartodb_id', 'state_code'], as_index=False).sum([['confirmed', 'deceased', 'recovered', 'tested', 'vaccinated1', 'vaccinated2']])
    # aggregatedWeek.rename(columns=['state', 'state_name', 'cartodb_id', 'state_code', 'confirmed', 'deceased', 'recovered', 'tested', 'vaccinated1', 'vaccinated2'])
    print(list(aggregatedWeek.columns.values))
    aggregatedWeek.to_csv("aggregated-weekly-india-covid-numbers.csv")
    return aggregatedWeek

def visualizeData(data):
    india_geojson = json.load(open("C:/Users/Tad/PycharmProjects/covid-heat-maps/states_india.geojson", 'r'))
    # india_geojson = json.load(open("C:/Users/Tad/PycharmProjects/covid-heat-maps/states_india.geojson", "r"))
    fig = px.choropleth(data, geojson=india_geojson, locations='cartodb_id', featureidkey='properties.cartodb_id', color='confirmed', color_continuous_scale=["white", "red"], scope='asia', hover_name='state_name', hover_data=['confirmed', 'deceased', 'recovered', 'tested', 'vaccinated1', 'vaccinated2'])
    fig.update_geos(fitbounds="locations")
    print("figure built")
    fig.show()
    fig.write_html("india-state-wise-heat-maps")
    print("figure showing")

def main():
    visualizeData(read_data())

if __name__ == "__main__":
    main()

