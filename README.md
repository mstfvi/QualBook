# QualBook
QualBook is a dataset of quality featurs extracted from Kaggle's jupyter notebooks. This code, present the methodology of cretaion of this dataset.

As you see in this figure, the architectue use 6 dataset where uploaded in : https://doi.org/10.5281/zenodo.7567333. 
The initial dataset is introduced in this paper: https://arxiv.org/abs/2103.10558.

After downloading all notebooks:
* create_dataframes.py: to convert notebooks to two group of dataframes (50 code cells dataframes and 50 markdown cells dataframes). 
  These splittation is done for ease of use.
* concate_codes.ipynb concatenate all dataframes in each group to one dataframe: KG_Codes.csv and KG_Markdown.csv.
  + if we didn't use batch_size in create_dataframes.py, there would be no need for concate_codes.ipynb.
* cell_metrics.ipynb: This is the main file of the project, which calculate cell metrics of above dataframes and create two new data frame: cell_metrics.csv and markdown_metrics.csv.
* notebook_metrics.ipynb calculates all notebook features by aggreagating two above dataframes or calculating some new features.vTherefore, the final notebook is made with the name QualBook (notebook_metrics.csv).


![image](https://user-images.githubusercontent.com/20360501/214763364-54baf4e0-33fd-4d7e-8201-5f9c9ba8c3eb.png)
