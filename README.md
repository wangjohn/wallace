Wallace
=======

Wallace is a framework for distributed evolutionary algorithms. It trains machine learning models on datasets. One only needs to specify settings and the dependent variable to train on, and Wallace will do the rest.

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
