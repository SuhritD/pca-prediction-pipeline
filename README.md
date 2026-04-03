# PCA post-stroke mood predictive model

## **Before you use**

* Everything in the Python code is relatively easy to modify. This was designed on Linux; the appropriate file and folder names will have to be set \- you can press Ctrl \+ C on a file/folder in Windows and paste it inside the code to get the destination name.  
* I strongly recommend using a Python interface instead of running the scripts through Command Prompt to better understand what code you need to modify for your work. I use [Spyder](https://www.spyder-ide.org/), it will take a few things to download but is really easy to work with.  
* The required Python libraries are pickle, numpy, pandas, scipy, nibabel, sklearn.  
* If your only objective is to view the brain components associated with the mood evaluations in your cohort, you just need to run *preprocessing.py*, *identify\_components.py*, and *component\_plot.py*.  
* To design a predictive model based on your cohort, I believe that ADC images would be best. If not, FLAIR would be plan B or mean DWI images as plan C \- and either case would require *shift\_intensities.py*.  
* The only intense code is to compute the principal component analysis over the complete voxels of MRI images. A computer with good processing power and RAM is required: a set of 250 patients needed at least 16 GB ram and 12-core CPU.  
  Two potential ways of speeding up:  
  (i) Although 60% of the voxels in an image have zero values, I do not get the same results by shrinking the data array of each subject. This is because a PCA on a sparse dataset isn’t the same as one without it. Theoretically, it could still give good results in some format, but I’ve not found it.  
  (ii) The PCA function uses full SVD, which is supposed to give the same compressed data every time. It is quicker to use other forms of compression such as incrementalPCA and TruncatedSVD, but warning \- all of these techniques will give different results.  

  I will do my best to find the least demanding compression method that gives robust results to update the script here. For now, I would recommend using the full SVD PCA and starting off with 150 images in *identify\_components.py*. It takes roughly 5 minutes to run it and would crash before that if there's insufficient RAM.

## **preprocessing.py**

* The images must be skull-stripped and spatially normalized to match the MNI 1 mm resolution 182 x 218 x 182\. This file uses the deep-learning tool HD-BET, which is run on Bash or Command Prompt, and the DWI\_MNI\_1 mm file in the repository. The instructions for installing it are [here](https://github.com/MIC-DKFZ/HD-BET).  
* You don't have to preprocess it using this \- the only thing that matters is all the images you use, including from your validation cohort, should have undergone the exact same treatment.  
* Two optional edits mentioned in inverted commas:  
  1. ANTs creates a lot of temporary files, about 150 MB space per subject. This program clears the images in the Linux temporary folder /tmp/ after each loop, which would have to be changed to the Windows one.  
  2. DWI images from older MRI machines may have unusually high intensity levels \- over 1750 or so would need to be smoothened. The smoothened function is at the end.

## **identify\_components.py**

This script assumes that you are using DWI images and you have a spreadsheet with your clinical scores where the first column is called **NUM\_PAT** with the list of patients. The image and patient names in the spreadsheet have to be same: if the patient names in **NUM\_PAT** are *Patient1*,*Patient2*, etc., the imaging files need to be *Patient1\_DWI.nii.gz*, *Patient2\_DWI.nii.gz*, and so on. As long as you have a uniform format for the patient names in the spreadsheet, this is not difficult to adjust.

## **testing\_phase.py**

The testing sample images must be preprocessed, including shifted\_intensities.py if they are DWI. The other inputs are the files generated from previous steps: the PCA file from identify\_components.py along with new\_significant\_components, the regression parameters, and standardized scores from training\_model.py.
