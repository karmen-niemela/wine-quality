# Red Wine Quality Analysis


This repository analyzes the relationships between wine properties and quality ratings. The goal of the analysis is to answer:
1. Which of the measured properties relate most strongly to the quality rating? Which of the measured properties do not relate to the quality rating?
2. What properties would you recommend to test next to increase the quality rating?

## Dataset 

The dataset consists of physicochemical wine properties and perceived quality of a dataset of 1599 red *vinho verde* wines from Portugal. The quality rating is a subjective rating from 0 (worst) to 10 (best), calculated as the median rating of 3 taste testers. More details are available in the paper:

P. Cortez, A. Cerdeira, F. Almeida, T. Matos and J. Reis. Modeling wine preferences by data mining from physicochemical properties. In Decision Support Systems, Elsevier, 47(4):547-553, 2009.

The dataset is available on [Kaggle](https://www.kaggle.com/datasets/uciml/red-wine-quality-cortez-et-al-2009).

### Input variables (based on physicochemical tests):  
* Fixed acidity  
* Volatile acidity  
* Citric acid  
* Residual sugar  
* Chlorides  
* Free sulfur dioxide  
* Total sulfur dioxide  
* Density  
* pH  
* Sulphates  
* Alcohol  

### Output variable (based on sensory data):  
* Quality (score between 0 and 10)

## Requirements

This repository uses **Python 3.13.5**. Set up a virtual environment with an
appropriate python version and install the libraries from `requirements.txt`.