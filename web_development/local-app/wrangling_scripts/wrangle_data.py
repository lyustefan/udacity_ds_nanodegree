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

def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """

  # first chart plots arable land from 1990 to 2015 in top 10 economies 
  # as a line chart
    
    graph_one = []
    df = clean_data('https://raw.githubusercontent.com/CSSEGISandData/COVID-19'
                 + '/master/csse_covid_19_data/' 
                 + 'csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
    
    countrylist = df.country.unique().tolist()
    
    for country in countrylist:
      x_val = df[df['country'] == country].date.tolist()
      y_val =  df[df['country'] == country].number_of_cases.tolist()
      graph_one.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name = country
          )
      )

    layout_one = dict(title = 'Aggregated Daily Number of Confirmed Cases',
                xaxis = dict(title = 'date',
                  autotick=True, showgrid=False),
                yaxis = dict(title = 'Number of Cases',
                  showgrid=False),
                )


# second chart plots ararble land for 2015 as a bar chart    
    graph_two = []
    df = cleandata('data/API_AG.LND.ARBL.HA.PC_DS2_en_csv_v2.csv')
    df.columns = ['country','year','hectaresarablelandperperson']
    df.sort_values('hectaresarablelandperperson', ascending=False, inplace=True)
    df = df[df['year'] == 2015] 

    graph_two.append(
      go.Bar(
      x = df.country.tolist(),
      y = df.hectaresarablelandperperson.tolist(),
      )
    )

    layout_two = dict(title = 'Hectares Arable Land per Person in 2015',
                xaxis = dict(title = 'Country',),
                yaxis = dict(title = 'Hectares per person'),
                )


# third chart plots percent of population that is rural from 1990 to 2015
    graph_three = []
    df = cleandata('data/API_SP.RUR.TOTL.ZS_DS2_en_csv_v2_9948275.csv')
    df.columns = ['country', 'year', 'percentrural']
    df.sort_values('percentrural', ascending=False, inplace=True)
    for country in countrylist:
      x_val = df[df['country'] == country].year.tolist()
      y_val =  df[df['country'] == country].percentrural.tolist()
      graph_three.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name = country
          )
      )

    layout_three = dict(title = 'Change in Rural Population <br> (Percent of Total Population)',
                xaxis = dict(title = 'Year',
                  autotick=False, tick0=1990, dtick=25),
                yaxis = dict(title = 'Percent'),
                )
    
# fourth chart shows rural population vs arable land
    graph_four = []
    
    valuevariables = [str(x) for x in range(1995, 2016)]
    keepcolumns = [str(x) for x in range(1995, 2016)]
    keepcolumns.insert(0, 'Country Name')

    df_one = cleandata('data/API_SP.RUR.TOTL_DS2_en_csv_v2_9914824.csv', keepcolumns, valuevariables)
    df_two = cleandata('data/API_AG.LND.FRST.K2_DS2_en_csv_v2_9910393.csv', keepcolumns, valuevariables)
    
    df_one.columns = ['country', 'year', 'variable']
    df_two.columns = ['country', 'year', 'variable']
    
    df = df_one.merge(df_two, on=['country', 'year'])

    for country in countrylist:
      x_val = df[df['country'] == country].variable_x.tolist()
      y_val = df[df['country'] == country].variable_y.tolist()
      year = df[df['country'] == country].year.tolist()
      country_label = df[df['country'] == country].country.tolist()

      text = []
      for country, year in zip(country_label, year):
          text.append(str(country) + ' ' + str(year))

      graph_four.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'markers',
          text = text,
          name = country,
          textposition = 'top center'
          )
      )

    layout_four = dict(title = 'Rural Population versus <br> Forested Area (Square Km) 1990-2015',
                xaxis = dict(title = 'Rural Population'),
                yaxis = dict(title = 'Forest Area (square km)'),
                )

# Aggregated/Newly confirmed cases
    graph_five = []
    df_confirmed_global = clean_data('https://raw.githubusercontent.com/CSSEGISandData/COVID-19'
                 + '/master/csse_covid_19_data/' 
                 + 'csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',
                 n_country = 500)

    def clean_func(df_confirmed_global):
      df_confirmed_global = df_confirmed_global.groupby('date').sum()
      df_confirmed_global['daily_new_case'] = df_confirmed_global.diff().fillna(0)
      df_confirmed_global = df_confirmed_global.reset_index()
      df_confirmed_global['daily_new_case'] = df_confirmed_global['daily_new_case'].astype(int)
      return df_confirmed_global

    df_confirmed_global = clean_func(df_confirmed_global)

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

    layout_five = dict(title = 'Aggregated/Newly confirmed cases',
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

    df_deaths_global = clean_func(df_deaths_global)
    df_recovered_global = clean_func(df_recovered_global)

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

    layout_six = dict(title = 'Aggregated/Newly death cases',
                xaxis = dict(title = 'Date', showgrid = False, autotick = True),
                yaxis = dict(title = '', showgrid = False),
                yaxis2 = dict(title = '', 
                showgrid = False, overlaying = 'y', side = 'right'),
                legend=dict(x=0.1, y=1)
                )
# bubble chart
    graph_seven = []
    
    df_confirmed = clean_data('https://raw.githubusercontent.com/CSSEGISandData/COVID-19'
                 + '/master/csse_covid_19_data/' 
                 + 'csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',
                         n_country = 500)

    df_death = clean_data('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv',
                 n_country = 500)

    df_recovered = clean_data('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv',
                     n_country = 500)
    df_bubble = df_confirmed.merge(df_death, on = ['country','date']).merge(df_recovered, on = ['country','date'])

    df_bubble.columns = ['country', 'date', 'confirmed', 'death', 'recovered']
    
    mapp = pd.read_excel('data/mapper.xlsx')

    def bubble_func(df_bubble):
        
        exclude = ['Diamond Princess', 'Holy See', 'Kosovo', 'MS Zaandam', 'Taiwan*', 'Western Sahara']
        
        df_bubble = df_bubble[~df_bubble.country.isin(exclude)]
        
        df_bubble = df_bubble.merge(mapp, how = 'left', left_on = 'country', right_on = 'Country Name')
      
        df_bubble.drop(columns = 'Country Name', inplace = True)
        
        df_bubble['death_rate'] = (df_bubble['death'] / df_bubble['confirmed']).fillna(0)
      
        df_bubble['recover_rate'] = (df_bubble['recovered'] / df_bubble['confirmed']).fillna(0)
        
        df_bubble = df_bubble[df_bubble['date'] == df_bubble.date.unique()[-1]]
        
        df_bubble.rename(columns = {'region':'continent'}, inplace = True)

      # only showing country with more than 10,000 cases
        df_bubble = df_bubble[df_bubble.confirmed > 50000]
        
        include = ['country', 'confirmed','date', 'continent', 'death_rate', 'recover_rate']
        
        return df_bubble[include]

    df_bubble = bubble_func(df_bubble)

    hover_text = []
    bubble_size = []

    for index, row in df_bubble.iterrows():
        hover_text.append(('Country: {country}<br>'+
                          'Confirmed Cases: {confirmed}<br>'+
                          'Death Rate: {death_rate:.2f}%<br>'+
                          'Recover Rate: {recover_rate:.2f}%<br>'+
                          'Date: {date}').format(country=row['country'],
                                                confirmed=row['confirmed'],
                                                death_rate=row['death_rate'] * 100,
                                                recover_rate=row['recover_rate'] * 100,
                                                date=row['date']))
        bubble_size.append(math.sqrt(row['confirmed']))

    df_bubble['text'] = hover_text
    df_bubble['size'] = bubble_size
    sizeref = 2.*max(df_bubble['size'])/(100**2)

    # Dictionary with dataframes for each continent
    continent_names = ['Africa', 'Americas', 'Asia', 'Europe', 'Oceania']
    continent_data = {continent:df_bubble.query("continent == '%s'" %continent)
                                  for continent in continent_names}

    for continent_name, continent in continent_data.items():

      graph_seven.append(
        go.Scatter(
          x=continent['recover_rate'], y=continent['death_rate'],
          name=continent_name, text=continent['text'],
          marker_size=continent['size'],
          mode='markers', 
          marker=dict(sizemode='area', sizeref=sizeref, line_width=2)
          )
          )

    layout_seven = dict(
      title='Death Rate vs Recover Rate',
      xaxis=dict(title='Recover Rate',
        # gridcolor='white',
        # type='log',
        gridwidth=2,
        showgrid = False),
      yaxis=dict(
        title='Death Rate',
        # gridcolor='white',
        gridwidth=2,
        showgrid=False),
      )

    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))
    figures.append(dict(data=graph_five, layout=layout_five))
    figures.append(dict(data=graph_six, layout=layout_six))
    figures.append(dict(data=graph_seven, layout=layout_seven))

    return figures