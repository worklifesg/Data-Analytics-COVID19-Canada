import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import matplotlib.animation as animation

Writer = animation.writers['ffmpeg']
writer = Writer(fps=10, metadata=dict(artist='Shraman'), bitrate=7500)

## Loading Data ##
covid_df=pd.read_excel('D:\Python\GitHub\COVID Data analytics\Cases_Canada.xlsx', index_col ="Province")

covid_qc=covid_df.loc['QUEBEC']
covid_qc = covid_qc.groupby(['SummaryDate']).agg({'TotalCases':np.sum,'TotalDeaths':np.sum,
                                                            'TotalRecovered':np.sum,'TotalActive':np.sum})

covid_qc.rename(columns={'TotalCases': 'Total Cases', 'TotalDeaths': 'Total Deaths',
                   'TotalRecovered': 'Total Recovered', 'TotalActive': 'Total Active'}, inplace=True)
covid_qc.index = pd.to_datetime(covid_qc.index)
color = ['red', 'green', 'blue', 'orange']
fig = plt.figure()
plt.xticks(rotation=45, ha="right", rotation_mode="anchor") 
plt.subplots_adjust(bottom = 0.2, top = 0.9)
plt.ylabel('Quebec COVID-19 Situation',fontname="Times New Roman", fontsize=12)

ax=plt.gca()
##ax.set_yscale('log')

dates=np.sort(np.unique(covid_qc.index.get_level_values(level=0)))
n=len(dates)

def anim(i=int):
    L=plt.legend(covid_qc.columns)
    plt.setp(L.texts, family='Times New Roman')
    p = plt.plot(covid_qc[:i].index, covid_qc[:i].values,label="test1")
    for i in range(0,4):
        p[i].set_color(color[i])
    for tick in ax.get_xticklabels():
        tick.set_fontname("Times New Roman")
    for tick in ax.get_yticklabels():
        tick.set_fontname("Times New Roman")
        tick.set_fontsize(10)

##animator = ani.FuncAnimation(fig, anim, interval = 100)
##plt.show()

a = animation.FuncAnimation(fig, anim, interval=100, frames=n,repeat=False)
a.save('covid_line.mp4',writer=writer,dpi=500)
