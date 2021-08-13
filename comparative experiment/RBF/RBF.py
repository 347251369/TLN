import argparse
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split 
from sklearn.svm import SVR
from read_dataset import *
import os

parser = argparse.ArgumentParser(description='PyTorch Example')
parser.add_argument('--model', type=str, default='RBF', metavar='N', help='model')
#
parser.add_argument('--dim', type=int, default=0, help='prediction dimension')
#
parser.add_argument('--dataset', type=str, default='lorenz', metavar='N', help='dataset')
#
parser.add_argument('--feature', type=int, default=0, help='Is feature selected')
#
parser.add_argument('--dy', type=int, default=20, metavar='N', help='dimension of y')
#
parser.add_argument('--noise', type=float, default=0.0, help='noise of data')
#
parser.add_argument('--c', type=float, default=1.0, help='C')
#
args = parser.parse_args()
np.random.seed(0)
#******************************************************************************
# load data 
#******************************************************************************
X = data_from_name(args.dataset,args.dim,args.feature,args.noise)
t = X.shape[0]
Xtrain = X[0:t-2*args.dy+2]
Xtest = X[t-2*args.dy+2:t-args.dy+1]

Y = X[:,0]
Ytrain = Y[args.dy-1:t-args.dy+1]
Ytest = Y[t-args.dy+1:]
#==============================================================================
# Model
#==============================================================================
model = SVR(kernel='rbf', C=args.c)
#==============================================================================
# Training
#==============================================================================
model.fit(Xtrain, Ytrain)
#==============================================================================
# Prediction
#==============================================================================
Ypred = model.predict(Xtest)
#==============================================================================
# result
#==============================================================================
Pearson = np.corrcoef(Ypred, Ytest)[0,1]
RMSE = np.sqrt(sum((Ypred-Ytest)**2)/len(Ypred))
StdY = Y[t-2*args.dy+2:t]
RMSE = RMSE / np.sqrt(sum((StdY-sum(StdY)/len(StdY))**2)/len(StdY))
#******************************************************************************
# Save data
#******************************************************************************
address = '../../results/' + args.dataset + str(args.dim) + '_feature' + str(args.feature) + (('_noise' + str(args.noise)) if args.dataset == "lorenz" else '')
if not os.path.exists(address):
	os.makedirs(address)

np.save(address +'/'+args.model+'_Ypred.npy', Ypred)
#******************************************************************************
# draw pic
#******************************************************************************
#legend
plt.title("Pearson :"+ str(round(Pearson,4)) +"  RMSE :" + str(round(RMSE,4)))
plt.xlabel('Time')
plt.ylabel('Value')
plt.xlim(xmin=0,xmax=t)
plt.ylim(ymin=min(Y.min(),Ypred.min())-0.3, ymax=max(Y.max(),Ypred.max())+0.3)
# draw line
plt.plot(np.arange(1,t-args.dy+2,1), Y[0:t-args.dy+1], color='blue', linestyle='-',marker = "o", MarkerSize=3)
plt.plot(np.arange(t-args.dy+1,t+1,1),Y[t-args.dy:t], label='True',color='green', linestyle='-',marker = "o", MarkerSize=3)
plt.plot(np.arange(t-args.dy+1,t+1,1), np.concatenate([Y[t-args.dy:t-args.dy+1],Ypred]),label='Prediction',color='red', linestyle='-',marker = "o", MarkerSize=3)
name = address +'/'+args.model+'.png'
plt.savefig(name, dpi=100)
plt.show()