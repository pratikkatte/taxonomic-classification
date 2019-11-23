import pandas as pd
import numpy as np
import json
import os
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


import collections


from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn import metrics

from sklearn.model_selection import train_test_split

def preprocess(data_path):
    """
    1. Combine title and description into a single column.\
    2.  drop title and description columns.
    Remove NaN values of categories and fill na values with "None".
    """
    data_path = 'media/data/'+data_path
    data = pd.read_csv(data_path)

    data['title_description'] = data['title'].map(str) + ". "+ data['description']

    data.drop(['title', "description"],axis=1, inplace=True)

    data.dropna(subset=['category'], inplace=True)

    data.fillna(value='None', inplace=True)

    train_data, test_data = train_test_split(data, train_size=0.8, shuffle=True )

    return data

def prediction_preprocess(title, description):
    data = [title+" ."+description]
    return data



def generate_graph(data, graph=None):

    if graph:
        for i in graph:
            graph[i] = set(graph[i])
        graph_dict = graph
    else:
        graph_dict = collections.defaultdict(set)

    for i, row in data.iterrows():
        graph_dict['ROOT'].add("category_"+str(row.category))
        graph_dict["category_"+str(row.category)].add("subcategory_"+str(row.sub_cat))
        graph_dict["subcategory_"+str(row.sub_cat)].add("subsubcategory_"+str(row.sub_sub_cat))

    for i in graph_dict:
      if len(graph_dict[i])==1:
        graph_dict[i] = []
      else:
        graph_dict[i] = list(graph_dict[i])
    return graph_dict



def graph_path(graph_dict, data, model, start_node="ROOT"):

    for i in graph_dict[start_node]:

        print(i)
        if not graph_dict[i]:
            print("{} is empty".format(i))
            continue
        else:
            if any(i == x for x in ["category_None", "subcategory_None", "subsubcategory_None"]):
              print("skipping ")
              continue

            level, value = i.split("_")
            if level == 'subcategory': level = 'sub_cat'
            if level == 'subsubcategory': level = 'sub_sub_cat'

            data_source, data_target = get_dataset(data, level, value=value)

            model.initialize(i)

            model.fit(data_source, data_target)

            graph_path(graph_dict, data, model, start_node=i)
    return model

def predict_graph_path(graph_dict, data, model,predict_node, prediction_list, level_arr):
    print(predict_node)
    level = level_arr[len(prediction_list)-1]
    predict_node = level+"_"+predict_node
    if predict_node in model:
        node_model = model[predict_node]
        predict = node_model.predict(data)[0]
        prediction_list.append(predict)
        predict_graph_path(graph_dict, data, model, predict, prediction_list, level_arr)
    return prediction_list

def get_dataset(data, level="category", value=None):
    level_dict = {'category':'sub_cat', 'sub_cat':'sub_sub_cat'}
    if value is None:
        data_target = data[level]
        data_source = data['title_description']
    else:
        data_extract = data[data[level] == value]
        data_source = data_extract['title_description']
        data_target = data_extract[level_dict[level]]

    return data_source, data_target


class HirarchicalModel:

    def __init__(self, name, graph_dict, new_model=True,trained_model=None):

        self.root_name = name
        if new_model:
            self.model = {}
        else:
            self.model = trained_model

        self.model['graph'] = graph_dict

    def initialize(self, name ):
        self.local_classifier_name = name

        if self.local_classifier_name in self.model:
            self.text_clf = self.model[self.local_classifier_name]
        else:
            self.text_clf =  Pipeline([('vect', CountVectorizer()),
                         ('tfidf', TfidfTransformer()),
                         ('clf', LinearSVC()),
                         ])


        print("initialized {} Model".format(self.local_classifier_name))

    def fit(self, input_data, target_data):
        self.text_clf.fit(input_data, target_data)
        self.model[self.local_classifier_name] = self.text_clf


    def save(self):

        print("saving model with name {}".format(self.root_name)+".model")
        joblib.dump(self.model,os.path.join('media/models', self.root_name+".model"))
