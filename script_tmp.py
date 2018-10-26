# encoding:utf-8
# __author__:DeyLies,WangYu
import pickle as pkl
with open('resource/order.pkl','wb') as ff:
    pkl.dump([1 for i in range(30)],ff)