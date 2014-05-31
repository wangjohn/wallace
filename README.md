Wallace
=======

Wallace is a framework for distributed evolutionary algorithms. It trains machine learning models on datasets. One only needs to specify settings and the dependent variable to train on, and Wallace will do the rest.

Wallace provides a simple way to predict or categorize variables. It employs many modern machine learning techniques and attempts to build the best possible model for predicting a particular variable.

## Simple Example

Let's suppose you're looking to buy a home and want to predict the price of a house you're interested in (let's say it isn't for sale yet). You have the following dataset and you want to create a machine learning model that will be a good predictor of Boston housing prices:

```
Price, CrimeRate, NitricOxideConcentration, HouseAge, Rooms
13000, 1.5, 0.2, 11, 3
16000, 1.3, 0.4, 23, 5
...
```

You have a lot of rows of data and you'd like to predict `Price`, but maybe you don't have very much statistics or machine learning expertise. Wallace will solve that for you!

Wallace uses various [evolutionary algorithms](http://en.wikipedia.org/wiki/Evolutionary_algorithm) to create a good machine learning model and predict prices. The following code is all you need to create a model for predicting housing prices:

```python
from wallace.initialization import WallaceInitialization

settings = {
    "optimization_algorithm_tracking.final_results_filename": "final_results.log"
    }
dependent_variable = "Price"
filename = "boston_housing_data.csv"

WallaceInitialization.initialize(settings, dependent_variable, filename)
```

The above will initialize a new instance of Wallace which will search for a machine learning model with the best parameters and independent variables for predicting the dependent variable `Price`.

# How it Works

Wallace works by using a flavor of an evolutionary algorithm for constantly improving upon prediction models that have already been created. The best models continue to live and get mutations in a process that continually improves the predictive power of the best model.

## Dataset Cleaner

When Wallace obtains a dataset, it automatically performs a number of cleaning operations on the dataset. It will detect whether or not the dataset contains headers, what those headers are, and the data types of each column of data.

Wallace will also handle missing values. By default, Wallace will remove rows that have missing values. However, this behavior can be turned off. In addition, Wallace will not remove rows wih missing values if those missing values occur in columns with a high percentage of missing values (over 10%).

## Evolutionary Algorithms

## Optimizing Machine Learning Algorithms

Wallace uses a set of machine learning algorithms and optimizes the parameters and indepenendent variables used in these algorithms. The ML algorithms currently supported by wallace are the following:

* Bayesian Ridge Regression
* Decision Tree Regression
* Extra Trees Regression
* Gradient Boosting Regression
* Lars Lasso Regression
* Lars Regression
* Lasso Regression
* OLS Linear Regression
* Random Forest Regression
* Ridge Regression
* SVM Regression

The parameters in each machine learning algorithm are optimized using an evolutionary algorithm. The independent variables used in each model also have probabilities of being included in a particular model that are optimized.

To create a new machine learning algorithm, one simply needs to subclass the `PredictiveModel` class.

## Checking Fitness

The fitness of each potential model is checked using [k-fold cross validation](http://en.wikipedia.org/wiki/Cross-validation_(statistics)#K-fold_cross-validation) on a subset of the data (note that the `k` used by Wallace can be changed via the settings).The data is split into `k` randomly selected sections, and `k-1` of them are used to train the model on and 1 section is used for testing. The predicted data is compared to the actual data from the section, and an error measured is used for fitness. The default error measure is the Mean Squared Error measure and the currently supported error measures are the following:

* Mean Squared Error
* R Squared Score
* Mean Absolute Error
* F1 Score


# Tests

To run tests, you must download nose:

```
pip install nose
```

Then run `nosetests` from the main directory. If you haven't already installed scikit-learn, then you will have to do so:

```
sudo apt-get install build-essential python-dev python-numpy python-setuptools python-scipy libatlas-dev libatlas3-base
sudo pip install numpy
sudo pip install scipy
sudo pip install scikit-learn
```
