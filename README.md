# Bento-Kitchen
BentoML is an open platform that simplifies ML model deployment and enables you to serve your models at production scale in minutes. This repo is a playground to try integrating BentoML with other services and put it through its paces.

## Python virtual environment
All of the following commands should be run in a terminal on a machine with python installed, a python download can be found [here](https://www.python.org/downloads/).
1) Create the virtual environment:
```
$py -m venv venv
```
2) Activate the virtual enviornment:
```
.\.venv\Scripts\activate
```
3) Done. It is as easy as that!
Bonus step is to install of all the required python packages from the requirements.txt
- Install the requirements:
```
pip install -r requirements.txt
```

## Train and Save Models
To train an iris model and save it to BentoML run the script `train_model.py` using the following command:
```
python src/train_model.py
```
This will create a scaler and train 5 machine learning models to classify iris plants.
You can see a list of all the versions of the models in BentoML by running the following command:
```
bentoml models list
```
The output should look something like this:
```
Tag                                    Module           Size       Creation Time       
 random_forest:yjus3n67mk5wtldu         bentoml.sklearn  84.17 KiB  2023-04-20 11:04:37
 decision_tree:yiup63g7mkdy7ldu         bentoml.sklearn  3.03 KiB   2023-04-20 11:04:37
 gaussian_naive_bayes:yibvyzw7mky5hldu  bentoml.sklearn  1.31 KiB   2023-04-20 11:04:37
 knn:yhgsjzg7mkezxldu                   bentoml.sklearn  9.80 KiB   2023-04-20 11:04:36
 logistic_regression:ygtuocw7mk2g7ldu   bentoml.sklearn  1.25 KiB   2023-04-20 11:04:36
 scaler:yfssyqo7mke2xldu                bentoml.sklearn  1.39 KiB   2023-04-20 11:04:36
```

## Run a Bento Service Api to Query a Model
To run the bento service locally simply use the following command:
```
bentoml serve .\src\bento_app.py:service --reload
```
Once this is up an running it will provide you with an endpoint that can be queried to get predictions from the model.
You can do this by making a HTTP request, an example of a cURL command to query the model is found below:
```
curl --location --request POST 'http://localhost:3000/predict' \
--header 'Content-Type: application/json' \
--data-raw '{
  "Sepal_Length": 5.1,
  "Sepal_Width": 3.5,
  "Petal_Length": 1.4,
  "Petal_Width": 0.2
}'
```
This will return the following prediction:
```
{
    "Results": 0,
    "Model": "Random Forest"
}
```