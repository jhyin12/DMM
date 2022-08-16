### DMM

#### File Structure

* ```/data/ ``` The dataset is stored in this folder, the format of the dataset is ```{"text":"","cluster":num}```.
* /result/  The result is stored in this folder.  Each line in clustering result is as ```id clusterId```, where ```id``` represents the document ```id```. ```id``` starts with 1.
* ```/src/``` The DMM code is stored in this folder.

#### Usage

* put the dataset which you want to cluster in ```/data/``` folder.
* modify the hyper-parameter ```dataset``` in ```/src/main.py``` with the right dataset.
* run with ```python main.py```

#### Related Paper

```latex
@inproceedings{10.1145/2623330.2623715,
author = {Yin, Jianhua and Wang, Jianyong},
title = {A Dirichlet Multinomial Mixture Model-Based Approach for Short Text Clustering},
year = {2014},
isbn = {9781450329569},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/2623330.2623715},
doi = {10.1145/2623330.2623715},
abstract = {Short text clustering has become an increasingly important task with the popularity of social media like Twitter, Google+, and Facebook. It is a challenging problem due to its sparse, high-dimensional, and large-volume characteristics. In this paper, we proposed a collapsed Gibbs Sampling algorithm for the Dirichlet Multinomial Mixture model for short text clustering (abbr. to GSDMM). We found that GSDMM can infer the number of clusters automatically with a good balance between the completeness and homogeneity of the clustering results, and is fast to converge. GSDMM can also cope with the sparse and high-dimensional problem of short texts, and can obtain the representative words of each cluster. Our extensive experimental study shows that GSDMM can achieve significantly better performance than three other clustering models.},
booktitle = {Proceedings of the 20th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining},
pages = {233–242},
numpages = {10},
keywords = {gibbs sampling, dirichlet multinomial mixture, short text clustering},
location = {New York, New York, USA},
series = {KDD '14}
}
```



