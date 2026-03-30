#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 09:16:26 2024

@author: suhrit
"""
import pickle, numpy as np, pandas as pd, scipy.stats, nibabel as nib, os
from sklearn.decomposition import PCA


input_folder=[FOLDER WITH INPUT FILES]
DWI=sorted(os.listdir(folder))

list_images=[x.replace('_DWI.nii.gz','') for x in DWI]
scores=pd.read_excel([EXCEL SHEET WITH PATIENT SCORES])
data_all=[]
for i in DWI:
    img_data=nib.load(folder+i).get_fdata()
    data_all.append(np.ndarray.flatten(img_data))
data_all=np.array(data_all)
pca= PCA(n_components=100,svd_solver='full')
transformed_pca = pca.fit_transform(data_all)
with open('PCA','wb') as fp:
    pickle.dump(pca,fp)
with open('transformed_pca','wb') as fp:
    pickle.dump(transformed_pca,fp)

#Taking significant components
significant_components={}

for column in range(1,3): #This will select the 2nd and 3rd columns in your spreadsheet
    print(scores.columns[column])    
    test=scores[['NUM_PAT',scores.columns[column]]].dropna()
    sub_test=test.loc[test['NUM_PAT'].isin(list_images)]
    if len(sub_test)==0:
        print("NOT PRESENT")
        continue
    indice_to_remove=[]
    for i in list_images:
        if(i in sub_test['NUM_PAT'].values)==False:
            indice_to_remove.append(list_images.index(i))
    data=np.delete(transformed_pca,indice_to_remove,axis=0)
    sig=[]
    for i in range(len(pca.components_)):
        if abs(scipy.stats.spearmanr(sub_test[scores.columns[column]].values,data[:,i]).correlation)>0.2:
            sig.append(i)
    if sig==[]:
        print("NO CORRELATIONS")
    significant_components[scores.columns[column]]=sig
   

#SAVE THE FILE WITH SIGNIFICANT BRAIN COMPONENTS
with open('significant_components','wb') as fp:
    pickle.dump(significant_components,fp)
    
    
                                
