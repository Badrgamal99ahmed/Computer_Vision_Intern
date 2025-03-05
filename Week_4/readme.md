Water Segmentation using DeepLabV3+

# Project Overview

This project focuses on segmenting water bodies using multispectral and optical satellite data from Sentinel-2/Landsat. We leverage DeepLabV3+ with different backbones (ResNet-50, ResNet-101, MobileNetV3) to improve segmentation accuracy. The model is fine-tuned using a dataset containing 12 spectral bands with a binary water mask.

🚀 Features

* Multispectral Image Processing: Uses Sentinel-2/Landsat data for better water segmentation.

* Deep Learning Architecture: Implements DeepLabV3+ for high-quality semantic segmentation.

* Fine-Tuning on Large Dataset: Trained on a diverse dataset to improve generalization.

* Evaluation Metrics: Includes IoU, Precision, Recall, and F1-score for performance assessment.

* Support for Multiple Backbones: Experiments with ResNet-50, ResNet-101, and MobileNetV3.

# 📂 Dataset

Input: Sentinel-2/Landsat harmonized images (12 bands, 128×128 resolution per patch).

Labels: Binary water masks (water = 1, non-water = 0).

Additional Features:

Coastal aerosol, Blue, Green, Red, NIR, SWIR1, SWIR2 bands.

MERIT DEM, Copernicus DEM, ESA World Cover Map, and Water Occurrence Probability.
