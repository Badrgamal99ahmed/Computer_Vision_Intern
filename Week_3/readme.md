# Water Segmentation using Multispectral and Optical Data

**Overview**

This project focuses on segmenting water bodies using multispectral and optical data from harmonized Sentinel-2/Landsat images. 
The dataset includes 12 spectral bands along with a binary water mask for supervised deep learning segmentation.

**Project Structure**

*1-Preprocessing*

* Load and normalize multispectral images

* Standardize the data for stable model training

*2-Visualization*

* Display spectral bands

* Show binary water masks alongside original images

*3-Model Architecture & Training*

* Implement U-Net for segmentation

* Train with Adam optimizer & Binary Cross-Entropy loss

* Evaluate using accuracy, IoU, and loss metrics
