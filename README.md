# PCA Post-Stroke Mood Predictive Model

## **Before you use**

* Familiarity with Python is required, at least to the extent of completely understanding these packages:   
  **pickle, numpy, pandas, scipy, nibabel, scikit-learn.**   
  Regardless of your proficiency, I strongly recommend using a Python interface instead of running the scripts through Command Prompt to better understand how you need to modify the code for your work. I use [Spyder](https://www.spyder-ide.org/), it will take a few things to download but is great to work with.  
* It is fairly easy to modify the scripts to set all the file and folder names. In case you are using a Python interface where you can’t drag the file to get its complete destination, here’s a pro-tip: press Ctrl \+ C on the item and paste it inside the text of the code, it’ll give the destination name.  
* If your only objective is to view the brain components associated with the mood evaluations in your cohort, you just need to run *preprocessing.py*, *identify\_components.py*, and *component\_plot.py*.  
* To design a predictive model based on your cohort, I believe that ADC images would be best. If not, FLAIR would be plan B or mean DWI images as plan C \- and either case would require *shift\_intensities.py*.  
* The only intense code is to compute the principal component analysis over the complete voxels of MRI images. A computer with good processing power and RAM is required: a set of 250 patients needed at least 12 GB RAM and an 8-core CPU.  
  Important factors:  
  (i) Around 74% of the voxels in an MRI image are outside the brain, so the current code discards them before the PCA. This saves a lot of computational time, but I’ve found in several cases that it is not the same as conducting the PCA on the whole image \- the calculations over a sparse dataset isn’t the same as a denser one. Although it should be possible to tweak this to get the best results, I used the complete images myself.  
  (ii) The PCA function uses full SVD, which is supposed to give the same compressed data every time. It is quicker to use other forms of compression such as sparse PCA, incrementalPCA and TruncatedSVD that you can examine [here](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html). However, all of these techniques will give different results, and I’ve always found the best results from full SVD.

I will do my best to improve the codes for efficiency and performance. However, of course, it’s all completely open for you to modify and explore.

## **preprocessing.py**

* You don't have to use this code if you have preprocessed images \- the only thing that matters is **ALL** the images you use have undergone the exact same treatment, especially if you have a validation cohort.  
* This code conducts skull-stripping and spatial normalization to produce images with the MNI 1 mm resolution 182 x 218 x 182\. This will be done on Python using the deep-learning tool HD-BET and the DWI\_MNI\_1 mm file in the repository. The instructions for installing the tool are [here](https://github.com/MIC-DKFZ/HD-BET).  
* Two optional edits mentioned in inverted commas:  
  1. ANTs creates a lot of temporary files, about 150 MB space per subject. This program clears the images in the Linux temporary folder /tmp/ after each loop, which would have to be changed to the Windows one.  
  2. DWI images from older MRI machines may have unusually high intensity levels \- over 1750 or so \- which would need to be smoothened. The smoothened function is at the end.

## **identify\_components.py**

\-\> This script assumes that you are using DWI images and you have a spreadsheet with your clinical scores where the first column is called **NUM\_PAT** with the list of patients. The image and patient names in the spreadsheet have to be same: if the patient names in **NUM\_PAT** are *Patient1*,*Patient2*, etc., the imaging files need to be *Patient1\_DWI.nii.gz*, *Patient2\_DWI.nii.gz*, and so on. The code is supposed to discard patients with missing images or scores, so all patients will be removed if the naming isn’t correct. As long as you have a uniform format for the patient names in the spreadsheet, this is not difficult to adjust.

\-\> At the end of the script, the files required for other tasks are saved. Assuming that you are using a Python application, all the variables will be kept until you close it. But if you will not run anything else for the moment, *data\_all* is required to run *components\_plot.py* and *PCA* for the predictive model. The two files are very large \- around 5 GB each for me \- so they are kept as comments. Make a note of the significant components as well.

## **component\_plot.py**

\-\> Along with the template MNI image, the outputs from the previous code are required \- the MRI data after removing null voxels (*data\_all*), the transformed PCA matrix (*transformed\_pca*), and the significant components (*significant\_components*).

\-\>The component plot is based on Spearman correlations between *data\_all* and *transformed\_pca.* This could take between 5-10 minutes for each component to generate. If you want to only look at a few components, change the line 13 to create a list instead such as: *comps=\[21,69\]* 

\-\> The output(s) will be NIFTI image(s) to show the brain patterns of the overall dataset used. The Spearman correlation values have been shifted to make the image have all values above 0\. I use [ITK-SNAP](https://www.itksnap.org/) to view the images:

<img width="2048" height="1139" alt="image" src="https://github.com/user-attachments/assets/c64bad28-20dd-4a33-abbe-71aff5ac2945" />


This is the 4th component from the DWI images of a cohort that was negatively correlated with depression scores and the color map changed to **Jet** instead of **Grayscale**. red regions have values closer to 1 and blue regions are closer to \-1. For DWI images, this would mean that lesions in blue regions such as the frontal lobe cause higher depression scores and vice-versa (quick reminder: most tools will have inverted left-right orientation). If this was done using ADC images, where lesion voxels are darker than the rest of the brain, the colors would have the opposite meaning.

\-\> Importantly, not all component plots will be informative: PCA will isolate the large patterns within the first 10 or 15 components. Here’s the 60th component from a sample that was significantly negatively correlated with CESD scores:

<img width="769" height="701" alt="image" src="https://github.com/user-attachments/assets/802e486e-0958-4924-9492-d9543f76d092" />


Components like this can be significant but not really useful visually, although you can see that the same red region near the posterior right hemisphere as well as a large blue cluster near the cingulate, a region known to be associated with depression.

In conclusion, keep in mind that these are purely visual representations of the data being used \- nothing more, nothing less. ITK and other tools can also make 3D plots, which could be interesting to explore.

## **testing\_phase.py**

The testing sample images must be preprocessed and if using FLAIR or DWI, *shifted\_intensities.py* must be run. The other inputs are the files generated from previous steps: the PCA file from *identify\_components.py* and *new\_significant\_components*, the regression parameters, and standardized scores from *training\_model.py*.
