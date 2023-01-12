import pandas as pd
import pip

birddata = pd.read_csv("C:\\Users\\user\\Desktop\\bird_tracking.csv")
birddata.head()
import matplotlib.pyplot as plt
import numpy as np
bird_names = pd.unique(birddata.bird_name)
plt.figure(figsize=(7, 7))
for bird_name in bird_names:
    ix = birddata.bird_name == "Eric"
    x, y = birddata.longitude[ix], birddata.latitude[ix]
    plt.plot(x,y,".")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.legend(loc="lower right")
plt.savefig("3traj.pdf")

import datetime
ix = birddata.bird_name == "Eric"
speed = birddata.speed_2d[ix]
plt.hist(speed)
date_str = birddata.date_time[0]
daily_mean_speed = []
data = birddata[birddata.bird_name == "Eric"]
times = data.to_timestamp
elapsed_time = [time - times[0] for time in times]
elapsed_days = np.array(elapsed_time) / datetime.timedelta(days=1)
next_day = 1
inds = []
for (i,t) in enumerate(elapsed_days):
    if t < next_day:
        inds.append(i)
    else:
        # compute mean speed
        daily_mean_speed.append(np.mean(data.speed_2d[inds]))
        next_day += 1
        inds = []

plt.figure(figsize=(8,6))
plt.plot(daily_mean_speed)
plt.xlabel("Day")
plt.ylabel("Mean speed (m/s)")
plt.savefig("dms.pdf")

import pandas as pd
import numpy as np
birddata = pd.read_csv("https://courses.edx.org/asset-v1:HarvardX+PH526x+2T2019+type@asset+block@bird_tracking.csv", index_col=0)
birddata.head()
birddata.groupby()

birddata.mean() # speed_2d
birddata.mean() # altitude
import datetime
ix = birddata.bird_name == "Sanne"
speed = birddata.speed_2d[ix]