# PCA post-stroke mood predictive model
## Before you use
* Everything is relatively easy to modify. This was designed on Linux; the appropriate file and folder names will have to be set - you can press Ctrl + C on a file/folder in Windows and paste it inside the code to get the destination name.
* If your only objective is to view the brain components associated with the mood evaluations in your cohort, you just need to run _preprocessing.py_, _identify_components.py_, and _component_plot.py_. 
* To design a predictive model based on your cohort, a computer with good processing power is required: for 300 patients, a 16-core CPU would be recommended. If not available, I would recommend starting off with 150-200 images and see if _identify_components.py_ can run.
* The required Python libraries are pickle, numpy, pandas, scipy, nibabel, sklearn

## preprocessing.py
* The images must be skull-stripped and spatially normalized to match the MNI 1 mm resolution 182 x 218 x 182. This file uses the deep-learning tool HD-BET, which is run on Bash or Command Prompt, and the DWI_MNI_1 mm file in the repository. The instructions for installing it are [here](https://github.com/MIC-DKFZ/HD-BET).
* You don't have to preprocess it using this - the only thing that matters is all the images you use, including from your validation cohort, should have undergone the exact same treatment.
* Two optional edits mentioned in inverted commas:
  1. ANTs creates a lot of temporary files, about 150 MB space per subject. This program clears the images in the Linux temporary folder /tmp/ after each loop, which would have to be changed to the Windows one.
  2. DWI images from older MRI machines may have unusually high intensity levels - over 1750 or so would need to be smoothened. The smoothened function is at the end.

## identify_components.py
This script assumes that you are using DWI images and you have a spreadsheet with your clinical scores where the first column is called **NUM_PAT** with the list of patients. The image and patient names in the spreadsheet have to be same: if the patient names in **NUM_PAT** are _Patient1_,_Patient2_, etc., the imaging files need to be _Patient1_DWI.nii.gz_, _Patient2_DWI.nii.gz_, and so on. As long as you have a uniform format for the patient names in the spreadsheet, this is not difficult to adjust. 

## testing_phase.py
The testing sample images must be preprocessed, including shifted_intensities.py if they are DWI. The other inputs are the files generated from previous steps: the PCA file from identify_components.py along with new_significant_components, the regression parameters, and standardized scores from training_model.py.
