import plotly.plotly as py
import pandas as pd
import plotly
import colorlover as cl
import plotly.graph_objs as go

USstates = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

def prepareData(candidate):    
    data = pd.read_csv('data/P00000001-ALL.csv', dtype={'contbr_city': str, 'cmte_id': str, 'contbr_st': str, 'receipt_desc': str}, index_col=False)    
    data = data[data['cand_nm']==candidate]
    df=data.groupby('contbr_st').sum()
    
    totalContributionPerState = data.groupby('contbr_st').size()    
    df['State']=df.index
    df['cont_sum']=totalContributionPerState
    
    if 'ON' in list(df.State):
        df=df.drop('ON') # wrong state code ??
    if 'AA' in list(df.State):
        df=df.drop('AA') # wrong state code ??
    if 'AE' in list(df.State):
        df=df.drop('AE') # wrong state code ??
    if 'AP' in list(df.State):
        df=df.drop('AP') # wrong state code ??
    if 'BC' in list(df.State):
        df=df.drop('BC') # wrong state code ??
    if 'GU' in list(df.State):
        df=df.drop('GU') # wrong state code ??
    if 'QC' in list(df.State):
        df=df.drop('QC') # wrong state code ??
    if 'SO' in list(df.State):
        df=df.drop('SO') # wrong state code ??
    if 'AS' in list(df.State):
        df=df.drop('AS') # wrong state code ??
    if 'MP' in list(df.State):
        df=df.drop('MP') # wrong state code ??
    if 'VI' in list(df.State):
        df=df.drop('VI') # wrong state code ??
    if 'PR' in list(df.State):
        df=df.drop('PR') # wrong state code ??
    if 'ZZ' in list(df.State):
        df=df.drop('ZZ') # wrong state code ??
    if 'YT' in list(df.State):
        df=df.drop('YT') # wrong state code ??
    if 'TO' in list(df.State):
        df=df.drop('TO') # wrong state code ??
    if 'NS' in list(df.State):
        df=df.drop('NS') # wrong state code ??
    if 'NL' in list(df.State):
        df=df.drop('NL') # wrong state code ??
    if 'MB' in list(df.State):
        df=df.drop('MB') # wrong state code ??
    if 'LO' in list(df.State):
        df=df.drop('LO') # wrong state code ??
    if 'HO' in list(df.State):
        df=df.drop('HO') # wrong state code ??
    if 'SI' in list(df.State):
        df=df.drop('SI') # wrong state code ??

    states=df['State'].unique()

    latlon=pd.read_csv('data/state_latlon.csv')
    pop=pd.read_csv('data/SCPRC-EST2015-18+POP-RES.csv')

    lons=[]
    lats=[]
    population=[]
    for state_code in states:
        if state_code in list(latlon.state):        
            lons.append(latlon[latlon.state==state_code].longitude.values[0])
            lats.append(latlon[latlon.state==state_code].latitude.values[0])
        else:
            lons.append(0)
            lats.append(0)
    df['lon']=lons
    df['lat']=lats    
    
    # small shift to make the NY label better visible
    df.ix['NY','lat']=43
    df.ix['NY','lon']=-76.
    df['name']=df['State']
    df=df.replace({'name': USstates})
    
    for name in list(df['name']):
        if name in list(pop.NAME):        
            population.append(pop[pop.NAME==name].POPEST18PLUS2015.values[0])
        else:
            population.append(1)

    df['population']=population

    df['text'] = df['name'] + '<br>Amount: ' + (df['contb_receipt_amt']).astype(str)+' USD'
    
    return df    
                                    
def createMap(candidate):
    df=prepareData(candidate)    

    data = []
    totalContributions=df.cont_sum.sum()

    colorscl=[]
    bupu = cl.scales['5']['seq']['Blues']
    thresholds=[0.0, 0.2, 0.4, 0.7, 1.0]

    for i in range(len(thresholds)):
        colorscl.append((thresholds[i],bupu[i]))

    geo_key='geo'
    contributions_data = dict(
        type = 'choropleth',
        colorscale=colorscl,
        geo=geo_key,
        autocolorscale=False,
#        z=df['contb_receipt_amt'].astype(float),
#        z=df['cont_sum']/df['population']/df['cont_sum'],
#        z=df['cont_sum']/totalContributions/df['population'],
        z=df['cont_sum']/totalContributions,
        locationmode = 'USA-states',
        locations=df['State'],
        text = df['text'],
        hoverinfo='text',
        marker = dict( 
            line = dict(width = 2,color = 'rgb(255,255,255)'
            )
        ),
        #showscale=False,
        colorbar=dict(
            title='%',
            xpad=0,
            ypad=0,
            len=1,
            x=1.0,
            y=0.5,
            thickness=25.
            )
        )
    
    data.append(contributions_data)
        
    layout = dict(
        title = '2016 US Presidential Elections<br>Contributions Receipt Amounts<br>Candidate: <b>'+candidate+'</b><br>Source: <a href="http://www.fec.gov/disclosurep/PDownload.do">Federal Election Commission</a>',
        showlegend = True,
        geo = dict(
            scope='usa',
            projection=dict( type='albers usa' ),
            showland = True,
            landcolor = 'rgb(217, 217, 217)',       
            subunitwidth=1,
            countrywidth=1,
            subunitcolor="rgb(255, 255, 255)",
            countrycolor="rgb(255, 255, 255)",
            domain = dict( x = [], y = [] ),           
        ),  
    )
        
    labels=dict(
        type = 'scattergeo',
        mode = 'text',
        showlegend=False,        
        lat = df['lat'],
        lon = df['lon'],
        text = df['State'],
        textfont = dict(size=8),
        )
    data.append(labels)

    fig = dict( data=data, layout=layout )            
    return fig, contributions_data
    
def plotMap(candidate):    
    fig, data = createMap(candidate)
    plotly.offline.plot(fig)
    
def plotAll():
    candidates=['Clinton, Hillary Rodham', 'Sanders, Bernard', 'Rubio, Marco',\
                'Cruz, Rafael Edward \'Ted\'','Trump, Donald J.', 'Kasich, John R.']
    data=[]

    layout = dict(
        title = '2016 US Presidential Elections<br>Contributions Receipt Amounts<br>Source: <a href="http://www.fec.gov/disclosurep/PDownload.do">Federal Election Commission</a>',
        showlegend = True,
    )

    bar_offset_x=[0.31, 0.65, 0.98, 0.31, 0.65, 0.98]
    bar_offset_y=[0.8, 0.8, 0.8, 0.3, 0.3, 0.3]
    for index in range(len(candidates)):
        geo_key='geo'+str(index+1) if index!=0 else 'geo'
        layout[geo_key]=dict(
        scope='usa',
        projection=dict( type='albers usa' ),
        showland = True,
        landcolor = 'rgb(217, 217, 217)',       
        subunitwidth=1,
        countrywidth=1,
        subunitcolor="rgb(255, 255, 255)",
        countrycolor="rgb(255, 255, 255)", 
        domain = dict( x = [], y = [] )           
        )
                        

    index=0        
    for candidate in candidates:
        geo_key='geo'+str(index+1) if index!=0 else 'geo'
        data.append(dict(
            type = 'scattergeo',
            showlegend = False,
            lon = [-95],
            lat = [51],
            geo = geo_key,
            text = '<b>'+candidate+'</b>',
            mode = 'text',
            )
        )        
        fig, dat = createMap(candidate)        
        dat['geo']=geo_key
        dat['colorbar']['len']=0.4
        dat['colorbar']['thickness']=7.
        dat['colorbar']['x']=bar_offset_x[index]
        dat['colorbar']['y']=bar_offset_y[index]
        data.append(dat)
        index=index+1
 
    z = 0
    COLS = 3
    ROWS = 2
    for y in reversed(range(ROWS)):
        for x in range(COLS):
            geo_key = 'geo'+str(z+1) if z != 0 else 'geo'
            layout[geo_key]['domain']['x'] = [float(x)/float(COLS), float(x+1)/float(COLS)]
            layout[geo_key]['domain']['y'] = [float(y)/float(ROWS), float(y+1)/float(ROWS)]
            z=z+1
#            print geo_key, ' ', layout[geo_key]['domain']['x'], ' ', layout[geo_key]['domain']['y']

    fig = {'data': data, 'layout': layout}
    plotly.offline.plot(fig)