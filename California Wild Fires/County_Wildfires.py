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
    county = df.index[0][0]
    labels = [ label[1] for label in df.index ]
    pos = np.arange(len(labels))
    width = 0.75
    
    acres = np.array(df['AcresBurned'])

    fig, ax = plt.subplots()
    ax.bar(pos, acres, width, label='Acres Burned')
    ax.set_ylabel('Acres Burned')
    ax.set_title('Acres burned in {} County by Year'.format(county))
    ax.set_xticks(pos)
    ax.set_xticklabels(labels)

    fig.tight_layout()
    fig.set_size_inches(10,6)
    plt.xticks(rotation=45, ha="right")
    plt.savefig('Acres Per Year in {}.png'.format(county), bbox_inches='tight', dpi=100)            
    

df = pd.read_csv('California_Fire_Incidents.csv')
features = ['ArchiveYear', 'Counties','AcresBurned'] #, 'Fatalities']
df1 = column_grabber(df, features)

index = pd.MultiIndex.from_arrays([df1['Counties'],df1['ArchiveYear']], names=('County', 'Year'))
df2 = pd.DataFrame({'AcresBurned': np.array(df1['AcresBurned'])},index=index)

df_new = df2.groupby(['County','Year']).aggregate({'AcresBurned': 'sum'})

counties = pd.unique(df['Counties'])

for county in counties:
    df_County = df_new.loc[df_new.index.get_level_values(0) == county]
    create_bar_plot(df_County)
    plt.close('all')
