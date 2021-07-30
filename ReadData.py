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
    lastWeek = pd.DataFrame(columns=['state', 'state_name', 'cartodb_id', 'state_code', 'date', 'confirmed', '7-days-ago_confirmed', 'today_confirmed', 'deceased', '7-days-ago_deceased', 'today_deceased', 'recovered', '7-days-ago_recovered', 'today_recovered', 'tested', '7-days-ago_tested', 'today_tested', 'vaccinated1', '7-days-ago_vaccinated1', 'today_vaccinated1', 'vaccinated2', '7-days-ago_vaccinated2', 'today_vaccinated2'])

    # Get info about states
    df_statesToIDs = pd.read_csv('India States with Codes.csv')
    statesToIDs = dict()
    statePopulations = dict()

    # Take info about states and store in well-designed dictionaries
    for index, row in df_statesToIDs.iterrows():
        statesToIDs[row['Input Data Listing']] = list()
        statesToIDs[row['Input Data Listing']].append(row['cartodb_id'])
        statesToIDs[row['Input Data Listing']].append(row['state_code'])
        statePopulations[row['cartodb_id']] = row['population']

    # Parse out weekly data for all states
    for s in all_states:
        dates = list(data_json[s]['dates'].keys())
        lastElementIndex = len(dates) - 1
        seventhToLastElementIndex = lastElementIndex - 7
        lastSevenDaysKeys = dates[seventhToLastElementIndex:lastElementIndex]
        sevenDaysAgoKey = lastSevenDaysKeys[0]
        todayKey = lastSevenDaysKeys[6]
        #for fd in lastSevenDaysKeys:
        sevenDaysAgoRecord = (((data_json[s])['dates'])[sevenDaysAgoKey])['total']
        #print("Seven days ago...", sevenDaysAgoRecord)
        todayRecord = (((data_json[s])['dates'])[todayKey])['total']
        #print("Today...", todayRecord)
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
        date = sevenDaysAgoKey
        confirmed = int()
        todayConfirmed = int()
        sevenDaysAgoConfirmed = int()
        try:
            todayConfirmed = todayRecord['confirmed']
            sevenDaysAgoConfirmed = sevenDaysAgoRecord['confirmed']
            confirmed = todayConfirmed - sevenDaysAgoConfirmed
        except:
            confirmed = -1
            todayConfirmed = -1
            sevenDaysAgoConfirmed = -1
        deceased = int()
        todayDeceased = int()
        sevenDaysAgoDeceased = int()
        try:
            todayDeceased = todayRecord['deceased']
            sevenDaysAgoDeceased = sevenDaysAgoRecord['deceased']
            deceased = todayDeceased - sevenDaysAgoDeceased
        except:
            deceased = -1
            todayDeceased = -1
            sevenDaysAgoDeceased = -1
        recovered = int()
        todayRecovered = int()
        sevenDaysAgoRecovered = int()
        try:
            todayRecovered = todayRecord['recovered']
            sevenDaysAgoRecovered = sevenDaysAgoRecord['recovered']
            recovered = todayRecovered - sevenDaysAgoRecovered
        except:
            recovered = -1
            todayRecovered = -1
            sevenDaysAgoRecovered = -1
        tested = int()
        todayTested = int()
        sevenDaysAgoTested = int()
        try:
            todayTested = todayRecord['tested']
            sevenDaysAgoTested = sevenDaysAgoRecord['tested']
            tested = todayTested - sevenDaysAgoTested
        except:
            tested = -1
            todayTested = -1
            sevenDaysAgoTested = -1
        vaccinated1 = int()
        todayVaccinated1 = int()
        sevenDaysAgoVaccinated1 = int()
        try:
            todayVaccinated1 = todayRecord['vaccinated1']
            sevenDaysAgoVaccinated1 = sevenDaysAgoRecord['vaccinated1']
            vaccinated1 = todayVaccinated1 - sevenDaysAgoVaccinated1
        except:
            vaccinated1 = -1
            todayVaccinated1 = -1
            sevenDaysAgoVaccinated1 = -1
        vaccinated2 = int()
        todayVaccinated2 = int()
        sevenDaysAgoVaccinated2 = int()
        try:
            todayVaccinated2 = todayRecord['vaccinated2']
            sevenDaysAgoVaccinated2 = sevenDaysAgoRecord['vaccinated2']
            vaccinated2 = todayVaccinated2 - sevenDaysAgoVaccinated2
        except:
            vaccinated2 = -1
            todayVaccinated2 = -1
            sevenDaysAgoVaccinated2 = -1
        #print(type(confirmed))
        #print(type(cartodb_id))
        if state_name != "" and state_name != "Ladakh" and not isinstance(confirmed, str) and not isinstance(confirmed, str): # Ladakh is not a state in the GeoJSON
            lastWeek.loc[len(lastWeek.index)] = [str(state), str(state_name), int(cartodb_id), int(state_code), str(date), int(confirmed), int(sevenDaysAgoConfirmed), int(todayConfirmed), int(deceased), int(sevenDaysAgoDeceased), int(todayDeceased), int(recovered), int(sevenDaysAgoRecovered), int(todayRecovered), int(tested), int(sevenDaysAgoTested), int(todayTested), int(vaccinated1), int(sevenDaysAgoVaccinated1), int(todayVaccinated1), int(vaccinated2), int(sevenDaysAgoVaccinated2), int(todayVaccinated2)]
    for index, row in lastWeek.iterrows():
        for category in ['confirmed', '7-days-ago_confirmed', 'today_confirmed', 'deceased', '7-days-ago_deceased', 'today_deceased', 'recovered', '7-days-ago_recovered', 'today_recovered', 'tested', '7-days-ago_tested', 'today_tested', 'vaccinated1', '7-days-ago_vaccinated1', 'today_vaccinated1', 'vaccinated2', '7-days-ago_vaccinated2', 'today_vaccinated2']:
            try:
                # Express in cases per million
                row[category] = row[category] / statePopulations[row['cartodb_id']] * 1000000
            except:
                print("Error in population adjustment for", row['state_name'])
    print(lastWeek)
    # Save data set as CSV
    lastWeek.to_csv("weekly-india-covid-numbers.csv")
    return lastWeek

def visualizeData(data):
    # GeoJSON file that creates heat map background for Indian states
    india_geojson = json.load(open("C:/Users/Tad/PycharmProjects/covid-heat-maps/states_india.geojson", 'r'))

    # Make sure all necessary fields are numeric... otherwise color continuous scale will be discrete, not continuous
    for category in ['cartodb_id', 'state_code', 'confirmed', '7-days-ago_confirmed', 'today_confirmed', 'deceased', '7-days-ago_deceased', 'today_deceased', 'recovered', '7-days-ago_recovered', 'today_recovered', 'tested', '7-days-ago_tested', 'today_tested', 'vaccinated1', '7-days-ago_vaccinated1', 'today_vaccinated1', 'vaccinated2', '7-days-ago_vaccinated2', 'today_vaccinated2']:
        data[[category]] = data[[category]].apply(pd.to_numeric)

    # Create choropleth heat map
    fig = px.choropleth(data, geojson=india_geojson, locations='cartodb_id', featureidkey='properties.cartodb_id', title='New, Weekly COVID-19 Confirmed Cases per Million by State' ,color='confirmed', color_continuous_scale=["white", "red"], scope='asia', hover_name='state_name', hover_data=['confirmed', 'deceased', 'recovered', 'tested', 'vaccinated1', 'vaccinated2'])
    data['vaccine_shots_administered'] = data['vaccinated1'] + data['vaccinated2']
    figVaccinations = px.choropleth(data, geojson=india_geojson, locations='cartodb_id', featureidkey='properties.cartodb_id', title='New, Weekly COVID-19 Vaccination Shots Administered per Million by State' ,color='vaccine_shots_administered', color_continuous_scale=["white", "green"], scope='asia', hover_name='state_name', hover_data=['confirmed', 'deceased', 'recovered', 'tested', 'vaccinated1', 'vaccinated2'])
    figDeaths = px.choropleth(data, geojson=india_geojson, locations='cartodb_id', featureidkey='properties.cartodb_id', title='New, Weekly COVID-19 Deaths per Million by State', color='deceased', color_continuous_scale=["white", "orange"], scope='asia', hover_name='state_name', hover_data=['confirmed', 'deceased', 'recovered', 'tested', 'vaccinated1', 'vaccinated2'])
    figTests = px.choropleth(data, geojson=india_geojson, locations='cartodb_id', featureidkey='properties.cartodb_id', title='New, Weekly COVID-19 Tests Conducted per Million by State', color='tested', color_continuous_scale=["white", "blue"], scope='asia', hover_name='state_name', hover_data=['confirmed', 'deceased', 'recovered', 'tested', 'vaccinated1', 'vaccinated2'])
    # Zoom in on India
    fig.update_geos(fitbounds="locations")
    figVaccinations.update_geos(fitbounds="locations")
    figDeaths.update_geos(fitbounds="locations")
    figTests.update_geos(fitbounds="locations")
    print("figures built")

    # Show figure
    fig.show()
    figVaccinations.show()
    figDeaths.show()
    figTests.show()
    print("figures showing")

def main():
    visualizeData(read_data())

if __name__ == "__main__":
    main()

