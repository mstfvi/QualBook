# QualBook
QualBook is a dataset of quality featurs extracted from Kaggle's jupyter notebooks. This code, present the methodology of cretaion of this dataset.

As you see in this figure, the architectue use 6 dataset where uploaded in : 10.5281/zenodo.7567333.
The initial dataset is introduced in this paper: https://doi.org/10.5281/zenodo.7567333.

After downloading all notebooks:
1- create_dataframes.py: to convert notebooks to two group of dataframes (50 code cells dataframes and 50 markdown cells dataframes). 
  These splittation is done for ease of use. 
2- concate_codes.ipynb concatenate all dataframes in each group to one dataframe: KG_Codes.csv and KG_Markdown.csv
* if we didn't use batch_size in create_dataframes.py, there would be no need for concate_codes.ipynb
3- cell_metrics.ipynb: This is the main file of the project, which calculate cell metrics of above dataframes and create two new data frame: cell_metrics.csv and markdown_metrics.csv
4- notebook_metrics.ipynb calculating all notebook features by aggreagating two above dataframes or calculating some new features.

    

...


![image](https://user-images.githubusercontent.com/20360501/214763364-54baf4e0-33fd-4d7e-8201-5f9c9ba8c3eb.png)
