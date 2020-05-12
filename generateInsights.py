import pandas as pd

editions=pd.read_csv("datasets/SOM_EDITIONS.tsv",delimiter="\t")
editions=editions[["Edition","Grand Total","City","Country"]]
editions.to_csv("ex1a_eval.csv")


ioc_codes=pd.read_csv("datasets/iOC_COUNTRY_CODES.csv")
ioc_codes=ioc_codes[["Country","NOC"]]
print(ioc_codes)

medals_dict={}
medals=pd.DataFrame()
for year in editions['Edition']:
    file_path='datasets/summer_{:d}.csv'.format(year)
    medals_dict[year]= pd.read_csv(file_path)
    medals_dict[year]= medals_dict[year][['Athlete', 'NOC','Medal']]
    medals_dict[year]["Edition"]=year
medals = pd.concat(medals_dict, ignore_index=True)

print(medals.head().append(medals.tail()))

medal_counts=pd.pivot_table(medals,index='Edition',columns='NOC',values='Athlete',aggfunc='count')
medal_counts.to_csv("ex1d_eval.csv")


#####
totals=editions.set_index("Edition")
totals=totals['Grand Total']
fractions=medal_counts.divide(totals,axis='rows')

mean_fractions = fractions.expanding().mean()
fractions_change = mean_fractions.pct_change() * 100
fractions_change = fractions_change.reset_index()
fractions_change.to_csv("ex1f_eval.csv")

hosts = pd.merge(editions, ioc_codes, how='left')
hosts = hosts[['Edition','NOC']].set_index('Edition')
hosts.loc[1972, 'NOC'] = 'FRG'
hosts.loc[1980, 'NOC'] = 'URS'
hosts.loc[1988, 'NOC'] = 'KOR'
hosts = hosts.reset_index()
hosts.to_csv("ex1g_eval.csv")

reshaped = pd.melt(fractions_change, id_vars='Edition', value_name='Change')
print(reshaped.shape, fractions_change.shape)
chn = reshaped.loc[reshaped.NOC == 'CHN']
print(chn.tail())

merged = pd.merge(reshaped, hosts, how='inner')
print(merged.head())
influence = merged.set_index('Edition').sort_index()
influence.to_csv("ex1i_eval.csv")

import matplotlib.pyplot as plt
change = influence['Change']
ax = change.plot(kind='bar')
ax.set_ylabel("% Change of Host Country Medal Count")
ax.set_title("Is there a Host Country Advantage?")
ax.set_xticklabels(editions['City'])
plt.savefig('host_plot.png')