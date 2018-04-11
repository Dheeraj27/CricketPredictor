import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import sklearn
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
import numpy as np
import pandas as pd
from numpy.linalg import inv
from statsmodels.regression.linear_model import OLS
import matplotlib.patches as mpatches
# import seaborn as sns
# sns.set_style("whitegrid")
# sns.set_context("poster")
# special matplotlib argument for improved plots
from matplotlib import rcParams

Y_plt=[]
K1=[]
K2=[]
wkt =[]
path_to_csv='/home/dheeraj/Desktop/odis/cleaned_csv/'
df=pd.read_csv(path_to_csv+"/India/India.csv",usecols=['over','runs','wickets','tot_runs'])
for i in range(1,49):
	df1 = df.loc[df['over'] == i]
	X = df1.drop('tot_runs', axis = 1)
	Y = df1['tot_runs']
	X_train, X_test, Y_train, Y_test = sklearn.cross_validation.train_test_split(X, Y, test_size = 0.1)
	print(X_train.shape)
	print(X_test.shape)
	print(Y_train.shape)
	print(Y_test.shape)
	lm = LinearRegression()
	lm.fit(X_train, Y_train)

	Y_pred = lm.predict(X_test)

	# plt.scatter(Y_test, Y_pred)
	Y_err=(Y_pred-Y_test)
	# print(Y_err.agg('mean'))
	Y_plt.append(Y_err.agg('mean'))
	# Y_act.append()
	K1.append(Y_pred.mean())
	K2.append(Y_test.mean())
	wkt.append(X['wickets'].mean())
	print(wkt)
# print(Y_plt)

Z=[]
for i in range(1,49):
	Z.append(i)

plt.figure(1)
plt.plot(Z,K1,'red')
plt.plot(Z,K2,'blue')
plt.xlabel("Overs")
plt.ylabel("Scores")
plt.title("Predicted vs Actual Scores")
red_patch = mpatches.Patch(color='red', label='Predicted Scores')
blue_patch = mpatches.Patch(color='blue', label='Actual Scores')
plt.legend(handles=[red_patch,blue_patch])


plt.figure(2)
plt.plot(Z, Y_plt, 'green')
plt.plot((0, 50), (0, 0), 'black')
plt.xlabel("Overs")
plt.ylabel("Scores")
plt.title("Predicted vs Actual Scores")
green_patch = mpatches.Patch(color='green', label='Mean Error')
plt.legend(handles=[green_patch])

plt.figure(3)
plt.plot(wkt, K1, 'yellow')
plt.xlabel("Wickets")
plt.ylabel("Predicted Scores")
plt.show()
