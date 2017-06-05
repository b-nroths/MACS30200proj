import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style="ticks")


data = [
['ward_precincts',						2.8,    0.3301423799751666, 0.32949294980543908, 0, -20, 0.063290053601984045],
# ['tax_increment_financing_districts',	15.9,   1.5299510688405411, 1.5347338971969831, -20, 20],
['police_beats',						23.8,   1.2089522890050575, 1.205197590038726, -20, 20, 0.47869148152709262],
['neighborhoods',						66.2,   3.9701894877298312, 3.9494130121945079, 20, 0, 1.1369498923371204],
['zip_codes',							106.4,  6.4456964559798875, 6.387855025732323, -20, 20, 2.4232999591479203],
['wards',								129.7,  7.4963940355726315, 7.3429847893587565, 0, 20, 2.2448936923681044],
['police_districts',					244.4,  16.700164174192199, 16.286555599414363, -20, 20, 6.2207036231340798],
['state_senate_districts',				324.1,  22.156232776684512, 21.304403194781113, -20, 20, 10.841970951911778],
['congressional_districts',				810.4,  70.562919752199392, 74.7936872894104, -20, 20, 58.772685175888427],
]

names = []
ys = []
xs = []
for group in data:
	name, area, ols_mse, sols_mse, x_offset, y_offset, sd = group
	names.append(name)
	xs.append(area)
	ys.append(ols_mse)

x = [1, 2, 3, 4, 5]
# y = ols_xs

fig = plt.figure()
ax = fig.add_subplot(111)
plt.title("MSE of Crime Prediction (14 days out)")
# plt.legend()
plt.scatter(xs, ys)
# ax.set_xticklabels(names)
ax.set_xlabel("Area of prediction shape")
ax.set_ylabel("Mean Squared Error")
# plt.xlim(0, 6)
# plt.ylim(0, max_mse*1.1)


for group in data:
	name, area, ols_mse, sols_mse, x_offset, y_offset, sd = group
	x = area
	y = ols_mse
	plt.annotate(
		' '.join(name.split('_')).title(),
		xy=(x, y), xytext=(x_offset, y_offset),
		textcoords='offset points', ha='left', va='bottom',
		bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
		arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'), fontsize=5)

plt.savefig("graphs/final.png")
plt.cla()


names = []
ys = []
xs = []
for group in data:
	name, area, ols_mse, sols_mse, x_offset, y_offset, sd = group
	names.append(name)
	xs.append(area)
	ys.append(ols_mse/area)

fig = plt.figure()
ax = fig.add_subplot(111)
plt.title("Normalized MSE (Avg MSE/area)")
# plt.legend()
plt.scatter(xs, ys)
# ax.set_xticklabels(names)
ax.set_xlabel("Area of prediction shape")
ax.set_ylabel("MSE/area")
# plt.xlim(0, 6)
# plt.ylim(0, max_mse*1.1)


for group in data:
	name, area, ols_mse, sols_mse, x_offset, y_offset, sd = group
	x = area
	y = ols_mse/area
	if name == 'neighborhoods':
		x_offset = -60
	if name == 'state_senate_districts':
		x_offset = 30
	plt.annotate(
		' '.join(name.split('_')).title(),
		xy=(x, y), xytext=(x_offset, y_offset),
		textcoords='offset points', ha='left', va='bottom',
		bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
		arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'), fontsize=5)

plt.savefig("graphs/final_accuracy.png")
plt.cla()
