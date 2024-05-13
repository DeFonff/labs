import pandas as pd



import matplotlib.pyplot as plt
df = pd.read_csv("C:/Users/dddddd/Desktop/aaad/labs/lab4/data2.csv")
df['Classes'] = df["Classes"].str.strip()
df['year'] = pd.to_datetime(df[["year", "month", "day"]])
df.drop(columns=["month", "day"], inplace=True)
df.rename(columns={"year":"date"}, inplace=True)
df = df.dropna()

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

xs = list(df['Rain'])
ys = list(df['FWI'])
zs = list(df['Ws'])
data_points = [(x, y, z) for x, y, z in zip(xs, ys, zs)]

colors = ['red' if wt == 'fire' else 'green' for wt in list(df['Classes'])]

for data, color in zip(data_points, colors):
    x, y, z = data
    ax.scatter(x, y, z, alpha=0.4, c=color, edgecolors='none', s=30)

ax.set_xlabel('Rain')
ax.set_ylabel('WFI')
ax.set_zlabel('Ws')
ax.view_init(elev=20, azim=30)
plt.show()
