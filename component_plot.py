import pickle, numpy as np, nibabel as nib, scipy.stats

"""
#IF YOU USED ADC IMAGES OR WANT TO TAKE A QUICK LOOK AT THE COMPONENTS, USE THIS SECTION

#pca=pickle.load((open('pca','rb')))                     #Use this line if the pca from identify_components.py isn't open
comps=[i[0] for i in significant_components.values()]    #To select which components to plot. You can also enter them as a list, such as [4,13,69]
map=nib.load('DWI_MNI_1mm.nii.gz')
for z in comps:
    print("Component",z)
    map_data=map.get_fdata()
    map_data[map_data!=0]=pca.components_[z]- np.min(pca.components_[z])                                  #Shifting negative values 
    nib.save(nib.Nifti1Image(map_data,affine=map.affine),'ADC_comp_'+str(z)+'.nii.gz')

"""

"""

THE PROCEDURE FOR DWI & FLAIR IMAGES (Could take 5-15 minutes)

# FILES TO LOAD IF PREVIOUS VARIABLES AREN'T STORED

data_all=pickle.load((open('data_all','rb'))) 
transformed_pca=pickle.load((open('transformed_pca','rb'))) 
significant_components=pickle.load((open('significant_components','rb'))) 
"""


comps=[i[0] for i in significant_components.values()]    #To select which components to plot. You can also enter them as a list, e.g. [4,13,69]
map=nib.load('DWI_MNI_1mm.nii.gz')
map_data=map.get_fdata()
cor=np.zeros_like(data_all[1]) #Empty matrix with the same size as an image without zero values 
progress=np.linspace(0,len(cor),100,dtype="int")-1    #A counter to tell you the percentage completed
for z in comps:
    print("Component",z)
    for i in range(len(cor)):
        if i in progress:                              #Kowalski, status report
            print(str(np.where(i==progress)[0][0])+"% completed")
        cor[i]=scipy.stats.spearmanr(data_all[:,i],transformed_pca[:,z])[0]
    print("100% Complete")
    map_data[map_data!=0]=cor+1
    
    nib.save(nib.Nifti1Image(map_data,affine=map.affine),'cor_'+str(z)+'.nii.gz')
