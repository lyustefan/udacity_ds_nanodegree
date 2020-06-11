import pandas as pd
import plotly.graph_objects as go
import math

# TODO: Scroll down to line 157 and set up a fifth visualization for the data dashboard

def cleandata(dataset, keepcolumns = ['Country Name', '1990', '2015'], value_variables = ['1990', '2015']):
    """Clean world bank data for a visualizaiton dashboard

    Keeps data range of dates in keep_columns variable and data for the top 10 economies
    Reorients the columns into a year, country and value
    Saves the results to a csv file

    Args:
        dataset (str): name of the csv data file

    Returns:
        None

    """    
    df = pd.read_csv(dataset, skiprows=4)

    # Keep only the columns of interest (years and country name)
    df = df[keepcolumns]

    top10country = ['United States', 'China', 'Japan', 'Germany', 'United Kingdom', 'India', 'France', 'Brazil', 'Italy', 'Canada']
    df = df[df['Country Name'].isin(top10country)]

    # melt year columns  and convert year to date time
    df_melt = df.melt(id_vars='Country Name', value_vars = value_variables)
    df_melt.columns = ['country','year', 'variable']
    df_melt['year'] = df_melt['year'].astype('datetime64[ns]').dt.year

    # output clean csv file
    return df_melt

def clean_data(dataset_url, cols_to_drop = ['Lat', 'Long'], n_country = 10):
    
    '''
    Convert covid19 dataset from wide to long format
    Drop unused columns
    
    Args:
        dataset_url (str): url of the dataset
        cols_to_keep (list): columsn to exclude from dataset
        
    Returns:
        DataFrame
    '''
    
    df = (pd.read_csv(dataset_url)
          .drop(cols_to_drop, axis = 1) # drop Lat and Long
         )
    
    # Get top 10 countries based on latest aggregated confirmed cases
    df = (df.groupby('Country/Region')
          .sum().reset_index()
          .sort_values(by = df.columns[-1], ascending = False)[:n_country])
    
    # Melt date columns and convert to date time object
    df_melt = df.melt(id_vars = 'Country/Region')
    df_melt.columns = ['country', 'date', 'number_of_cases']
    df_melt['date'] = df_melt['date'].astype('datetime64[ns]')
    
    return df_melt.sort_values(['country','date'])

def clean_us(dataset_url, cols_to_drop = ['Lat', 'Long'], n_country = 10):
    
    '''
    Convert covid19 dataset from wide to long format
    Drop unused columns
    
    Args:
        dataset_url (str): url of the dataset
        cols_to_keep (list): columsn to exclude from dataset
        
    Returns:
        DataFrame
    '''
    
    df = (pd.read_csv(dataset_url)
          .drop(cols_to_drop, axis = 1) # drop Lat and Long
         )
    
    # Get top 10 countries based on latest aggregated confirmed cases
    df = (df.groupby('Country_Region')
          .sum().reset_index()
          .sort_values(by = df.columns[-1],ascending = False)[:n_country])
    
    # Melt date columns and convert to date time object
    df_melt = df.melt(id_vars = 'Country_Region')
    df_melt.columns = ['country', 'date', 'number_of_cases']
    df_melt['date'] = df_melt['date'].astype('datetime64[ns]')
    
    return df_melt.sort_values(['country','date'])

def get_daily(df):
    df = df.groupby('date').sum()
    df['daily_new_case'] = df.diff().fillna(0)
    df = df.reset_index()
    df['daily_new_case'] = df['daily_new_case'].astype(int)
    return df

def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """

  # US confirmed case chart
    graph_one = []
    graph_two = []
    us_confirmed = clean_us('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv',
             cols_to_drop = ['Lat', 'Long_', 'iso2', 'iso3', 'code3', 'UID', 'FIPS', 'Admin2'])

    us_confirmed = get_daily(us_confirmed)

    graph_one.append(
        go.Scatter(
        x = us_confirmed['date'].tolist(),
        y = us_confirmed['number_of_cases'].tolist(),
        name = 'Total confirmed cases',
        yaxis = 'y1'
        )
    )

    graph_one.append(
        go.Scatter(
        x = us_confirmed['date'],
        y = us_confirmed['daily_new_case'],
        # base = us_confirmed['daily_new_case'] * -1,
        name = 'Daily new cases',
        yaxis = 'y2'
        )
    )

    layout_one = dict(title = 'US Confirmed Cases',
                xaxis = dict(title = 'Date', showgrid = False, autotick = True),
                yaxis = dict(title = '', showgrid = False),
                yaxis2 = dict(title = '', 
                  showgrid = False, overlaying = 'y', side = 'right'),
                legend=dict(x=0.1, y=1))

    # US death case chart
    
    us_death = clean_us('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv',
             cols_to_drop = ['Lat', 'Long_', 'iso2', 'iso3', 'code3', 'UID', 'FIPS', 'Admin2', 'Population'])

    us_death = get_daily(us_death)

    graph_two.append(
        go.Bar(
        x = us_death['date'],
        y = us_death['number_of_cases'],
        name = 'Total death',
        yaxis = 'y1'
        )
    )

    graph_two.append(
        go.Bar(
        x = us_death['date'].tolist(),
        y = us_death['daily_new_case'].tolist(),
        base = us_death['daily_new_case'] * -1,
        name = 'Daily new death',
        yaxis = 'y1'
        )
    )

    layout_two = dict(title = 'US Death Cases',
                xaxis = dict(title = 'Date', showgrid = False, autotick = True),
                yaxis = dict(title = '', showgrid = False),
                yaxis2 = dict(title = '', 
                  showgrid = False, overlaying = 'y', side = 'right'),
                legend=dict(x=0.1, y=1))

# Aggregated/Newly confirmed cases
    graph_five = []
    df_confirmed_global = clean_data('https://raw.githubusercontent.com/CSSEGISandData/COVID-19'
                 + '/master/csse_covid_19_data/' 
                 + 'csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',
                 n_country = 500)

    df_confirmed_global = get_daily(df_confirmed_global)

    graph_five.append(
        go.Scatter(
        x = df_confirmed_global['date'].tolist(),
        y = df_confirmed_global['number_of_cases'].tolist(),
        name = 'Total confirmed cases',
        yaxis = 'y1'
        )
    )

    graph_five.append(
        go.Scatter(
        x = df_confirmed_global['date'].tolist(),
        y = df_confirmed_global['daily_new_case'].tolist(),
        name = 'Daily new cases',
        yaxis = 'y2'
        )
    )

    layout_five = dict(title = 'Global Confirmed Cases',
                xaxis = dict(title = 'Date', showgrid = False, autotick = True),
                yaxis = dict(title = 'Total confirmed cases', showgrid = False),
                yaxis2 = dict(title = 'Daily new cases', 
                  showgrid = False, overlaying = 'y', side = 'right'),
                legend=dict(x=0.1, y=1))


# Aggregated/Newly death/recovered cases
    graph_six = []
    df_deaths_global = clean_data('https://raw.githubusercontent.com/'
      + 'CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv',
                 n_country = 500)

    df_recovered_global = clean_data('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv',
                 n_country = 500)

    df_deaths_global = get_daily(df_deaths_global)
    df_recovered_global = get_daily(df_recovered_global)

    # df_recovered_global['number_of_cases'] = df_recovered_global['number_of_cases'] * -1
    # df_recovered_global['daily_new_case'] = df_recovered_global['daily_new_case'] * -1

    graph_six.append(
        go.Bar(
        x = df_deaths_global['date'].tolist(),
        y = df_deaths_global['number_of_cases'].tolist(),
        base = df_deaths_global['number_of_cases'] * -1,
        name = 'Total death',
        yaxis = 'y2'
        )
    )

    graph_six.append(
        go.Bar(
        x = df_deaths_global['date'].tolist(),
        y = df_deaths_global['daily_new_case'].tolist(),
        base = df_deaths_global['daily_new_case'] * -1,
        name = 'Daily new death',
        yaxis = 'y2'
        )
    )

    graph_six.append(
        go.Bar(
        x = df_recovered_global['date'].tolist(),
        y = df_recovered_global['daily_new_case'].tolist(),
        name = 'Daily new recovered',
        yaxis = 'y2'
        )
    )

    graph_six.append(
        go.Bar(
        x = df_recovered_global['date'].tolist(),
        y = df_recovered_global['number_of_cases'].tolist(),
        name = 'Total recovered',
        yaxis = 'y2'
        )
    )

    layout_six = dict(title = 'Global Death/Recover Cases',
                xaxis = dict(title = 'Date', showgrid = False, autotick = True),
                yaxis = dict(title = '', showgrid = False),
                yaxis2 = dict(title = '', 
                showgrid = False, overlaying = 'y', side = 'right'),
                legend=dict(x=0.1, y=1)
                )

    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    #figures.append(dict(data=graph_three, layout=layout_three))
    #figures.append(dict(data=graph_four, layout=layout_four))
    figures.append(dict(data=graph_five, layout=layout_five))
    figures.append(dict(data=graph_six, layout=layout_six))


    return figures