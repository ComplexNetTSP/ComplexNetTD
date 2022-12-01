# NET 4103/7431: Labs materials

## Contents of the git Repository
#### Documentation  
* [Intoduction à la programmation avec le language Python](doc/IntroPython.pdf)
* [Python for data Analysis](doc/Python-for-Data-Analysis.pdf)

#### Lab exercices 
* [Lab 1](release/Lab%201/Lab%201.ipynb)
    * [Lab 1 Solution](source//Lab%201/Lab%201.ipynb)
* [Lab 2](release/Lab%202/Lab%202.ipynb)
* [Lab 3](release/Lab%203/Lab%203.ipynb)
* [Lab 4](release/Lab%204/Lab%204.ipynb)

## install virtual environement required for all the labs

#### With virtualenv
```bash
$ python -m venv net
$ source net/bin/activate
$ pip install --upgrade pip
$ python -m pip install -r requirements.txt  
```

#### with conda 
```bash
$ conda create -n net python=3.8
$ conda activate net
$ pip3 install --upgrade pip
$ pip install -r requirements.txt  
```

## Create the jupyter kernel for the labs
```bash
$ python -m ipykernel install --user --name=net 
```

#### Data
* Comtrade: The [UN Comtrade](https://comtrade.un.org/) Database houses detailed global trade data.
* Game Of Thrones: [Kaggle Game of Thrones: Network Analysis](https://www.kaggle.com/mmmarchetti/game-of-thrones-network-analysis/notebook)
* Wikipedia: Small subset of wikipedia articles in form : Page Id, Page Title, Keywords 
* Facebook: this dataset consists of 'circles' (or 'friends lists') from Facebook. Facebook data was collected by [1] from survey participants using this Facebook app. The dataset includes node features (profiles), circles, and ego networks.

_[1]_ the J. McAuley and J. Leskovec. [Learning to Discover Social Circles in Ego Networks](http://i.stanford.edu/~julian/pdfs/nips2012.pdf). NIPS, 2012.

#### Other Python resources online 
* [Jake VanderPlas, Python Data Science Handbook,  O′Reilly  (2016)](https://jakevdp.github.io/PythonDataScienceHandbook/)
* [Wes McKinney, Python for Data Analysis: Data Wrangling with Pandas, NumPy, and IPython, O′Reilly (2017)](https://bedford-computing.co.uk/learning/wp-content/uploads/2015/10/Python-for-Data-Analysis.pdf)
* [Scipy Lecture Notes](http://www.scipy-lectures.org/)
* [Une introduction à Python 3](http://hebergement.u-psud.fr/iut-orsay/Pedagogie/MPHY/Python/courspython3.pdf).

## Recomended Python distribution 
* [Download Anaconda pour OSX/Windows/Linux](https://www.anaconda.com/products/individual)
* [Google Colab](https://colab.research.google.com/)