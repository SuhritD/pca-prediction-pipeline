#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 16:44:26 2025

@author: suhrit
"""
import numpy as np, os, nibabel as nib
from scipy.stats import rankdata

def match_histograms(source, template):
    """
    Adjust the distribution of the source array to match the histogram of the template array.
    
    - source: 1D array to be transformed
    - template: 1D array whose histogram the source will match
    
    Returns:
    - matched: 1D array with a histogram similar to the template
    """
    # Flatten the arrays (if they are not already 1D)
    source = np.asarray(source).ravel()
    template = np.asarray(template).ravel()
    mask = np.where(source != 0, 1, 0)
    # Sort the source and template
    #source_sorted = np.sort(source)
    template_sorted = np.sort(template)
    
    # Compute the ranks of the source
    source_ranks = rankdata(source, method='ordinal') - 1  # Ranks start from 0
    
    # Map the ranks to the template's sorted values
    matched = template_sorted[source_ranks]*mask
    
    return matched

template=nib.load()
affine=template.affine
template=template.get_fdata()

folder=''  #Original images
Shift=''   #Where to put the shifted images
for i in sorted(os.listdir(folder)):
    print(i)
    nib.save(nib.Nifti1Image(match_histograms(nib.load(folder+i).get_fdata(),template).reshape((182,218,182)),affine),Shift+i)