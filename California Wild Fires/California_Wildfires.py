import numpy as np
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt

def column_grabber(df,columns):
    temp_dict = {}
    for col in columns:
        temp_dict[col] = df[col]
    return pd.DataFrame(temp_dict)    

def create_bar_plot(df):
    year = df.index[0][0]
    labels = [ label[1] for label in df.index ]
    pos = np.arange(len(labels))
    width = 0.75
    
    acres = np.array(df['AcresBurned'])

    fig, ax = plt.subplots()
    ax.bar(pos, acres, width, label='Acres Burned')
    ax.set_ylabel('Acres Burned')
    ax.set_title('Acres burned in {} by County'.format(year))
    ax.set_xticks(pos)
    ax.set_xticklabels(labels)

    fig.tight_layout()
    fig.set_size_inches(12,6)
    
    plt.xticks(rotation=45, ha="right")
    plt.savefig('Acres in {} by County.png'.format(year), bbox_inches='tight', dpi = 100)            

df = pd.read_csv('California_Fire_Incidents.csv')
features = ['ArchiveYear', 'Counties','AcresBurned'] #, 'Fatalities']
df1 = column_grabber(df, features)

index = pd.MultiIndex.from_arrays([df1['ArchiveYear'],df1['Counties']], names=('Year','County'))
df2 = pd.DataFrame({'AcresBurned': np.array(df1['AcresBurned'])},index=index)

df_new = df2.groupby(['Year','County']).aggregate({'AcresBurned': 'sum'})

years = pd.unique(df['ArchiveYear'])

for year in years:
    df_Year = df_new.loc[df_new.index.get_level_values(0) == year]
    create_bar_plot(df_Year)
    plt.close('all')

