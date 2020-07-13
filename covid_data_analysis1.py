import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import rc

Writer = animation.writers['ffmpeg']
writer = Writer(fps=10, metadata=dict(artist='Shraman'), bitrate=7500)

## Loading Data ##
covid_df=pd.read_excel('D:\Python\GitHub\COVID Data analytics\Cases_Canada.xlsx')


covid_df = covid_df.groupby(['SummaryDate','Province']).agg({'TotalCases':np.sum})

covid_df = covid_df.groupby('SummaryDate')['TotalCases'].nlargest(15).reset_index(level=1,drop=True)

##Model Visualization ##

provinces=np.array([province[1] for province in covid_df.index])
provinces=np.unique(provinces)

cmap=plt.get_cmap('tab20')
colors=cmap(np.linspace(0,1,len(provinces)))
color_dict=dict(zip(provinces,colors))


##Plotting for single date graph ## (Uncomment it when needed to plot single bar graph

##plt.figure()
##date=pd.to_datetime('4/22/20',format='%m/%d/%y')
##x_values=covid_df.loc[date].index
##x_data=covid_df.loc[date].values
##
##condition = np.mod(x_data, 1)==0
##x_new=(np.extract(condition, x_data))
##
##bars=plt.barh(x_values,x_new,color=[color_dict[province] for province in x_values])
##
##plt.suptitle('Total COVID-19 cases in Canada')
##plt.title(date.strftime('%d %b %Y'))
##ax=plt.gca()
##ax.invert_yaxis()
##
##
### Removing borders
##for spine in ax.spines.values():
##    spine.set_visible(False)
### Removing Tickmarks and values in X-axis
##plt.tick_params(left=False, bottom=False, labelbottom=False)
### Labelling The bars directly
##for bar in bars:
##    ax.text(bar.get_width(), bar.get_y() + bar.get_height()/2, '  ' + str(bar.get_width()), va='center')
##
##plt.show()

## Animation setup and modeling ##

dates=np.sort(np.unique(covid_df.index.get_level_values(level=0)))
n=len(dates)
def nice_axes(ax):
    ax.set_facecolor('1')
    ax.tick_params(labelsize=8, length=0)
    ax.grid(True, axis='x', color='black')
    ax.set_axisbelow(True)
    [spine.set_visible(False) for spine in ax.spines.values()]
    
def update(curr):
    if curr == n:
        a.event_source.stop()
    plt.cla()
    date=dates[curr]
    x_values=covid_df.loc[date].index
    x_data=covid_df.loc[date].values

    condition = np.mod(x_data, 1)==0
    x_new=(np.extract(condition, x_data))

    bars=plt.barh(x_values,x_new,color=[color_dict[province] for province in x_values])
    plt.suptitle('Cumulative Total COVID-19 Cases in Canada',fontname="Times New Roman", fontsize=12)
    plt.title(pd.to_datetime(date).strftime('%d %b %Y'),fontname="Times New Roman", fontsize=12)
    ax=plt.gca()
    ax.invert_yaxis()

    for spine in ax.spines.values():
        spine.set_visible(False)
    plt.tick_params(left=False, bottom=False, labelbottom=False)
    for bar in bars:
        ax.text(bar.get_width(), bar.get_y() + bar.get_height()/2, '' + str(bar.get_width()),va='center',
                fontname="Times New Roman", fontsize=10)
    for tick in ax.get_xticklabels():
        tick.set_fontname("Times New Roman")
    for tick in ax.get_yticklabels():
        tick.set_fontname("Times New Roman")
        tick.set_fontsize(10)
##    nice_axes(ax)
fig = plt.figure(figsize=[12,6]) #Adjusting margins
plt.subplots_adjust(left=0.2)
a = animation.FuncAnimation(fig, update, interval=100, frames=n,repeat=False)
a.save('covid_case.mp4',writer=writer,dpi=500)
