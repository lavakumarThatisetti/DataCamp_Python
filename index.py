import pandas as pd


editions=pd.read_csv("datasets/SOM_EDITIONS.tsv",delimiter="\t")
editions=editions[["Edition","Grand Total","City","Country"]]
editions.to_csv("results/exc1a_eval.csv")
#print(editions.head())

ioc_codes=pd.read_csv("datasets/IOC_COUNTRY_CODES.csv")
ioc_codes=ioc_codes[["Country","NOC"]]
#print(ioc_codes)

medals_dict={}
for year in editions['Edition']:
    file_path='datasets/summer_{:d}.csv'.format(year)
    medals_dict[year]=pd.read_csv(file_path)
    medals_dict[year]=medals_dict[year][["Athlete","NOC","Medal"]]
    medals_dict[year]["Edition"]=year
medals=pd.concat(medals_dict,ignore_index=True)
#print(medals.head(5).append(medals.tail(5)))


medals_count=pd.pivot_table(medals,index="Edition",columns="NOC",values="Athlete",aggfunc='count')
medals_count.to_csv("results/ex1d.csv")

totals=editions.set_index("Edition")
totals=totals['Grand Total']
fractions=medals_count.divide(totals,axis='rows')

mean_fractions=fractions.expanding().mean()
fractions_change=mean_fractions.pct_change()*100
fractions_change=fractions_change.reset_index()
fractions_change.to_csv("results/fractions.csv")

hosts=pd.merge(editions,ioc_codes,how="left")
hosts=hosts[["Edition","NOC"]].set_index("Edition")
hosts.loc[1972,'NOC']="FRG"
hosts.loc[1980,'NOC']="USR"
hosts.loc[1988,'NOC']="USA"

hosts=hosts.reset_index()
hosts.to_csv("results/hosts.csv")

reshaphed=pd.melt(fractions_change,id_vars='Edition',value_name='Change')
print(reshaphed.shape,fractions_change.shape)
chn=reshaphed.loc[reshaphed.NOC=="CHN"]
print(chn.tail())


merged=pd.merge(reshaphed,hosts,how="inner")
influence=merged.set_index("Edition").sort_index()
influence.to_csv("results/influence.csv")


import matplotlib.pyplot as plt

change=influence['Change']
ax=change.plot(kind="bar")
ax.set_ylabel("% Change of Host Country Medal Count")
ax.set_xlabel("% City Influence")
ax.set_title("Is there a Host Country Advantage?")
ax.set_xticklabels(editions['City'])
plt.savefig("results/plot.png")
