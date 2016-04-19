import plotly.plotly as py
import plotly.graph_objs as go
from plotly.graph_objs import *
import pandas as pd
import plotly
 
candidates=['Clinton, Hillary Rodham', 'Sanders, Bernard', 'Rubio, Marco',\
            'Cruz, Rafael Edward \'Ted\'','Trump, Donald J.', 'Kasich, John R.'] 
  
def getData(candidate):    
    data = pd.read_csv('data/P00000001-ALL.csv', dtype={'contbr_city': str, 'cmte_id': str, 'contbr_st': str, 'receipt_desc': str}, index_col=False)    
    data = data[data['cand_nm']==candidate]
    
    df=data.groupby('contbr_occupation').sum()
    
    if 'INFORMATION REQUESTED' in list(df.index):
        df=df.drop('INFORMATION REQUESTED')

    if 'INFORMATION REQUESTED PER BEST EFFORTS' in list(df.index):
        df=df.drop('INFORMATION REQUESTED PER BEST EFFORTS')

    if 'NONE' in list(df.index):
        df=df.drop('NONE')        
    
    totalContributionPerOccupation = data.groupby('contbr_occupation').size()    
    df['occupation_sum']=totalContributionPerOccupation
    df['occupation']=df.index
    df['occupation']=[x.lstrip() for x in df.occupation.values]
    df['occupation']=[x.lower().capitalize() for x in df.occupation.values]
#    df = df.sort_values(by='contb_receipt_amt',ascending=False)[:10]    
#    top10 = list(df.sort_values(by='contb_receipt_amt',ascending=False)[:10].index.values)    

    return df

def getTop10():
    selectedOccupations=[]
    #candidates=['Clinton, Hillary Rodham', 'Sanders, Bernard', 'Rubio, Marco',\
    #            'Cruz, Rafael Edward \'Ted\'','Trump, Donald J.', 'Kasich, John R.']
    for candidate in candidates:
        df=getData(candidate)
        top10 = list(df.sort_values(by='contb_receipt_amt',ascending=False)[:10].index.values)    
        for occupation in top10:
            if occupation not in selectedOccupations:
                selectedOccupations.append(occupation)
    return selectedOccupations
    
def make_trace(candidate, selectedOccupations, sbplt, perCent=False):
    
    df=getData(candidate)    
    #select occupations
    #selectedOccupations=getTop10()

    df['selected']=[True if x in selectedOccupations else False for x in df.occupation.values]
    df=df[df['selected']==True]    
    
    totalAmount = df.contb_receipt_amt.sum()

    return Bar(
        x=df['occupation'].values,  # x-coords are the months' names
        y=100*df['contb_receipt_amt'].values/totalAmount if perCent else df['contb_receipt_amt'].values,            # take in the y-coords     
        name=candidate,      # label for hover
        #        marker=Marker(color=color),  # set bar color
        xaxis='x{}'.format(sbplt),                    # (!) both subplots on same x-axis
        yaxis='y{}'.format(sbplt)      # (!) plot on y-axis of 'sbplt'
        )
    
# Define a function for updating up the axes (return a dictionary)
def update_axis(title, tickangle, ticksize, titlesize=12):
     return dict(
        title=title,              # axis title
        tickangle=tickangle,      # set tick label angles
        tickfont=dict(size=ticksize),
        titlefont=dict(size=titlesize),   # font size, default is 12
        gridcolor='#FFFFFF',      # white grid lines
        showline=True,
        zeroline=False           # remove thick zero line
    )
    
def makePlot(perCent=False):
    #candidates=['Clinton, Hillary Rodham', 'Sanders, Bernard', 'Rubio, Marco',\
    #            'Cruz, Rafael Edward \'Ted\'','Trump, Donald J.', 'Kasich, John R.']
    
    selectedOccupations=getTop10()

    fig = plotly.tools.make_subplots(rows=2, cols=1, shared_xaxes=False)
    
    
    traces_D=[]
    traces_R=[]    
    for candidate in candidates[:2]:
        traces_D.append(make_trace(candidate, selectedOccupations, 1, perCent))
    for candidate in candidates[2:]:
        traces_R.append(make_trace(candidate, selectedOccupations, 2, perCent))

    fig['data'] = Data(traces_D + traces_R)
    
    fig['layout'].update(
    title='2016 US Presidential Candidates<br>Highest contributions per occupation',
    titlefont=dict(size=16),
    barmode='group',     # (!) bars are in groups on this plot
    bargroupgap=0.1,       # norm. spacing between group members
    bargap=0.25          # norm. spacing between groups
    )

    # (2.2) Add frame options to the 'layout' key 
    fig['layout'].update(
    showlegend=True, # remove legend
    autosize=False,   # (!) turn off autosize 
    height=580,       # plot's height and
    width=1150,        #   width in pixels, as recommended by Sunlight Found.
    margin=Margin( # set frame to plotting area margins
        t=50,     #   top,
        b=75,     #   bottom,
        r=20,      #   right,
        l=70       #   left
        ),
    #    plot_bgcolor='#EFECEA',  # set plot and 
    #    paper_bgcolor='#EFECEA', #   frame background color
    )
    
    # (2.4a) Update top axis options in the 'layout' key in Figure object
    fig['layout']['xaxis1'].update(
        update_axis('', -45, 9, 9)
    )

    fig['layout']['xaxis2'].update(
        update_axis('', -45, 9, 9)
    )

    if not perCent:
        fig['layout']['yaxis2'].update(
            update_axis('Total amount of contributions (USD)', 0, 10, 10)
        )
        fig['layout']['yaxis1'].update(
            update_axis('Total amount of contributions (USD)', 0, 10, 10)
        )
    else:
        fig['layout']['yaxis2'].update(
            update_axis('Fraction of Total Contributions (%)', 0, 10, 12)
        )
        fig['layout']['yaxis1'].update(
            update_axis('Fraction of Total Contributions (%)', 0, 10, 12)
        )        
        
    annotations = Annotations([
    make_anno1('Source: <a href="http://www.fec.gov/disclosurep/PDownload.do">Federal Election Commission</a>',\
                10, -0.05, 1.1)
    ])

    # (2.5b) Append annotation list with the two legend items
    annotations += [
        make_anno2('<b>Democratic candidates</b>', '#0000FF', 0.25, 1.0),
        make_anno2('<b>Republican candidates</b>', '#BD2D28', 0.25, 0.35)
    ]


    fig['layout'].update(
        annotations=annotations
    )

    plotly.offline.plot(fig, filename='contributions_per_occupation_'+str(int(perCent))+'.html')


def make_anno1(text, fontsize, x, y):
    return Annotation(
        text=text,   # annotation text
        xref='paper',  # use paper coordinates
        yref='paper',  #   for both x and y coords
        x=x,           # x and y position 
        y=y,           #   in norm. coord. 
        font=Font(size=fontsize),  # text font size
        showarrow=False,       # no arrow (default is True)
        #bgcolor='#F5F3F2',     # light grey background color
        #bordercolor='#F5F3F2', # white borders
        borderwidth=1,         # border width
        borderpad=fontsize     # set border/text space to 1 fontsize
    )


# Define a 2nd annotation-generating function (for the legend)
def make_anno2(text, fontcolor, x, y):
    return Annotation(
        text=text,  # annotation text
        xref='paper',     # use paper coordinates
        yref='paper',     #   for both x and y coords
        x=x,              # x and y position
        y=y,            #   in norm. coord.
        xanchor='right',  # 'x' at right border of annotation
        font=Font(
            size=13,           # set text font size 
            color=fontcolor    #   and color
        ),
        showarrow=False,   # no arrow (default is True)
        #bgcolor='#F5F3F2', # light grey background color
        #bordercolor='#F5F3F2', # white borders
        borderpad=10       # set border/text space (in pixels)
    )

