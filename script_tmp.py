# encoding:utf-8
# __author__:DeyLies,WangYu
import pickle as pkl
import os
with open('resource/file.pkl','wb') as ff:
    pkl.dump(os.path.join(os.getcwd(),"test.xlsx"),ff)