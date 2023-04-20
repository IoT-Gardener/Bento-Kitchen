"""
Script to load a dataset, train a series of ML models, and save them to bentoml
"""
import bentoml
import os
import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier
from typing import Tuple


def load_dataset(data_path: str, col_names: list[str]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Function to load a dataset from memory

    :param data_path: File path to the data to be loaded
    :type data_path: str
    :param col_names: A list of the desired colun names
    :type col_names: list[str]
    :return: _description_
    :rtype: Tuple[pd.DataFrame, pd.DataFrame]
    """
    # Load the iris dataset
    temp_df = pd.read_csv(data_path, header=None)
    # Give each column a meaninful name
    temp_df.columns = col_names
    # Create a label encoder
    label_encoder = LabelEncoder()
    # Assign labels to the iris species class
    temp_labels = pd.DataFrame()
    temp_labels["Label"] = label_encoder.fit_transform(temp_df["Class"])
    # Drop the class from the main data
    temp_df = temp_df.drop(columns=["Class"])

    return temp_df, temp_labels


def fit_scaler(df: pd.DataFrame) -> StandardScaler:
    """Function to fit a standard scaler to the Iris dataset

    :param df: DataFrame of iris data, including: Sepal Length, Sepal Width, Petal Length, and Petal Width
    :type df: pd.DataFrame
    :return: Returns a fitted standard scaler
    :rtype: StandardScaler
    """
    scaler = StandardScaler()
    scaler.fit(df)

    return scaler


def scale_data(df: pd.DataFrame, scaler: StandardScaler) -> pd.DataFrame:
    """Function to fit data using a StandardScaler

    :param df: DataFrame of data to be scaled
    :type df: pd.DataFrame
    :param scaler: A fitted scaler object
    :type scaler: StandardScaler
    :return: Returns a dataframe of scaled data
    :rtype: pd.DataFrame
    """
    return pd.DataFrame(scaler.transform(df), columns=df.columns)


def split_dataset(df: pd.DataFrame, labels: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Function to split a dataset 70/30 train/test

    :param df: Dataframe containing data to be split
    :type df: pd.DataFrame
    :param labels: DataFrame containing iris labels
    :type labels: pd.DataFrame
    :return: Returns a tuple of train/test data and labels
    :rtype: Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]
    """    

    features = df.values[:, 0:4].reshape(len(df), 4)
    labels = labels.values[:, 0]

    tr_X, ts_X, tr_y, ts_y = train_test_split(features, labels, test_size=0.3, random_state=42)
    tr_y = tr_y.astype('int')
    ts_y = ts_y.astype('int')

    return tr_X, ts_X, tr_y, ts_y


if __name__ == "__main__":
    print("Hello world")

    # Load the iris dataset
    iris_df, iris_labels = load_dataset(f"{os.getcwd()}/data/iris.data", ["Sepal Length", "Sepal Width",
                                              "Petal Length", "Petal Width", "Class"])

    # Create, fit, and save a standard scaler
    iris_scaler = fit_scaler(iris_df)
    bentoml.sklearn.save_model("scaler", iris_scaler)

    # Scale the dataset
    scaled_df = scale_data(iris_df, iris_scaler)

    # Split the data into train and test
    train_features, test_features, train_labels, test_labels = split_dataset(iris_df, iris_labels)

    # Train and save a range of basic ML models
    lr = LogisticRegression(random_state=0).fit(train_features, train_labels)
    bentoml.sklearn.save_model("logistic_regression", lr)

    knn = KNeighborsClassifier(n_neighbors=3).fit(train_features, train_labels)
    bentoml.sklearn.save_model("knn", knn)

    gnb = GaussianNB().fit(train_features, train_labels)
    bentoml.sklearn.save_model("gaussian_naive_bayes", gnb)

    dt = DecisionTreeClassifier().fit(train_features, train_labels)
    bentoml.sklearn.save_model("decision_tree", dt)

    rf = RandomForestClassifier(max_depth=2, random_state=0).fit(train_features, train_labels)
    bentoml.sklearn.save_model("random_forest", rf)
