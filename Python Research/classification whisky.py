import numpy as np
import pandas as pd
x = pd.Series([6,3,8,6], index=["q","w","e","r"])
x["w"]
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

data = {'name ' : ['Tim','Jim','Pam','Sam'],
        'age' : [29, 31, 27, 35], 'Zip' : ['02115','02130','67700','00100'] }
whisky = pd.read_csv("C:\\Users\\user\\Downloads\\whiskies.txt")
whisky.iloc[5:10,0:5]
whisky.columns
flavors = whisky.iloc[:,]
whisky["Region"] = pd.read_csv("regions.txt")
corr_flavors = pd.DataFrame.corr(flavors)
corr_whisky = pd.DataFrame(flavors.transpose())
print(corr_flavors)
import matplotlib.pyplot as plt
plt.figure(figsize=(10,10))
plt.pcolor(corr_flavors)
plt.pcolor(corr_whisky)
plt.colorbar()
plt.savefig("corr_flavors.pdf")
from sklearn.cluster._bicluster import SpectralCoclustering
model = SpectralCoclustering(n_clusters=6, random_state=0)
model.fit(corr_flavors)
whisky['Group'] = pd.Series(model.row_labels_, index=whisky.index)
whisky = whisky.ix(np.argsort(model.row_labels_))
whisky = whisky.reset_index(drop=True)
correlations = pd.DataFrame.corr(whisky.iloc[:,2:14].transpose())
correlations = np.array(correlations)
import pandas as pd
data = pd.Series([1,2,3,4])
data = data.ix[[3,0,1,2]]