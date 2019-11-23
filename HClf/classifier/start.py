
from .training import *
import joblib

def start_training(data_path, model_name, ):

    data = preprocess(data_path)
    graph_dict = generate_graph(data)
    rootModel = HirarchicalModel(model_name, graph_dict)
    data_source, data_target = get_dataset(data)
    rootModel.initialize("ROOT")
    rootModel.fit(data_source, data_target)
    learned_model = graph_path(graph_dict, data, rootModel, start_node="ROOT")
    learned_model.save()

def predict(title, description, model_name):
    level_arr = ['category', 'subcategory', 'subsubcategory']
    model_path = 'media/models/'+model_name
    data = prediction_preprocess(title, description)
    model = joblib.load(model_path)
    graph_dict = model['graph']
    root_model = model['ROOT']
    predicted = root_model.predict(data)[0]
    prediction_list = [predicted]
    predicted_values = predict_graph_path(graph_dict, data, model, predicted, prediction_list, level_arr)
    return predicted_values

def train_existing(data_path, model_name, trained_model):

    data = preprocess(data_path)

    model_path = 'media/models/'+trained_model
    model = joblib.load(model_path)
    graph_dict = model['graph']
    graph_dict = generate_graph(data, graph_dict)

    rootModel = HirarchicalModel(model_name, graph_dict, new_model=False, trained_model=model)

    data_source, data_target = get_dataset(data)
    rootModel.initialize("ROOT")
    rootModel.fit(data_source, data_target)
    learned_model = graph_path(graph_dict, data, rootModel, start_node="ROOT")

    learned_model.save()
