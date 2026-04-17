import pickle, numpy as np, pandas as pd, scipy.stats, nibabel as nib, os
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error

input_folder=''
DWI=sorted(os.listdir(input_folder))

list_images=[x.replace('_DWI.nii.gz','') for x in DWI] 
scores=pd.read_excel('')

with open('transformed_pca','rb') as fp:
    transformed_pca=pickle.load(fp)
with open('significant_components','rb') as wp:
    significant_components=pickle.load(wp)

for column in significant_components:
    print(column)  
    if len(significant_components[column])==0:
        print("Not enough correlations")
        continue
    
    ##Removing all missing images or scores before regression
    test=scores[['NUM_PAT',column]].dropna()
    sub_test=test.loc[test['NUM_PAT'].isin(list_images)]
    indice_to_remove=[]
    for i in list_images:
        if(i in sub_test['NUM_PAT'].values)==False:
            indice_to_remove.append(list_images.index(i))
    data=np.delete(transformed_pca,indice_to_remove,axis=0)  
    col=data[:,significant_components[column]]                      #Keeping only the required transformed PCA columns 
 
    #Too many columns spoil the broth
    if len(significant_components[column])>4:
        non_sig_col=[]   
        for i in range(col.shape[1]):      
            if abs(scipy.stats.pearsonr(col[:,i],sub_test[column])[1])>0.01:
                non_sig_col.append(i)
        col=np.delete(col,non_sig_col,1)
        significant_components[column]=[significant_components[column][i] for i in range(len(significant_components[column])) if i not in non_sig_col]
        if col.shape[1]==0:
            print("All components were removed")
            continue

    k = 5                                                   #The parameter to change the neighbors used for regression, ideally between 5-30
    knn_reg = KNeighborsRegressor(n_neighbors=k)
    score=np.array(sub_test[column])
    knn_reg.fit(col, score)
    y_train = knn_reg.predict(col)
    with open('/home/suhrit/Downloads/Stuff/reg_'+column,'wb') as fp:                 #Saving the regression parameter for future testing
        pickle.dump(knn_reg,fp)
    ##To improve the generalizability, the mood scores are standardized, but it is useless if you only have one dataset
    total=np.array(scores[column].dropna())
    total_std=(total - total.mean())/(total.std())
    with open('/home/suhrit/Downloads/Stuff/tup_'+column,'wb') as fp:
        pickle.dump((total,total_std),fp)
        
        
    print("Mean Squared Error:",mean_squared_error(y_train,score))
    print("Variance explained:",scipy.stats.pearsonr(y_train,score)[0])
    print("Predicted values standard deviation:",str(np.std(y_train)))          ##There shouldn't be a tiny standard dev

with open('/home/suhrit/Downloads/Stuff/new_significant_components','wb') as fp:     ##Saving the significant components again
    pickle.dump(significant_components,fp)
    
    
