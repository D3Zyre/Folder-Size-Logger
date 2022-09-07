print("Importing Libraries...")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import csv
import datetime

folder = input("\n\ninsert path here (or E for everything):\n\n")
folder = folder.replace("\\","/")
print("Path:", folder)
print("Processing Data...")
y1 = list()
x = list()
with open("Files/Folder Size Log.csv", "r") as file:
    read = csv.reader(file)
    for i in read:
        if folder != "E":
            if i[1].replace("\\","/") == folder:
                y1.append(str(int(i[2])/1000000000))
                x.append(datetime.datetime.strptime(i[0], "%Y-%m-%d %H:%M:%S.%f"))
        else:
            if i[1].replace("\\","/") == "C:/":
                y1.append(str(int(i[3])/1000000000))
                x.append(datetime.datetime.strptime(i[0], "%Y-%m-%d %H:%M:%S.%f"))

print(len(x), "Points...")
print("Plotting...")
y1 = np.asarray(y1[1:], np.float64)

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d/%m/%Y"))
plt.gca().xaxis.set_major_locator(mdates.DayLocator())

plt.plot(x[1:], y1)
plt.gcf().autofmt_xdate()
plt.yticks(np.arange(0, max(y1)+1, (max(y1) - 0) / 15))
plt.xticks(np.arange(min(x), max(x)+datetime.timedelta(1), (max(x) - min(x)) / 20))
plt.title("{} Folder Size (GB) as a Function of Time (date)".format(folder))
plt.xlabel("Time (date)")
plt.ylabel("Folder Size (GB)")
print("Done")
plt.show()

# add legend
# add stats
