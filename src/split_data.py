from get_data import read_params
import argparse
import pandas as pd
from sklearn.linear_model import Lasso
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import train_test_split


def split_data(config_path):
    config = read_params(config_path)
    raw_data_path = config["preprocessed_data"]["preprocessed_data_csv"]
    df = pd.read_csv(raw_data_path)
    
    X = df.drop(['Item_Outlet_Sales'],axis=1)
    y = df['Item_Outlet_Sales']
    feature_sel_model = SelectFromModel(Lasso(alpha=0.005, random_state=0)) # remember to set the seed, the random state in this function
    feature_sel_model.fit(X, y)
    selected_feat = X.columns[(feature_sel_model.get_support())]
    X = X[selected_feat]
    X.rename(columns = {'Outlet_Type_Supermarket Type1':'Outlet_Type_Supermarket_Type1', 'Outlet_Type_Supermarket Type2':'Outlet_Type_Supermarket_Type2',
                        'Outlet_Type_Supermarket Type3':'Outlet_Type_Supermarket_Type3'} , inplace = True)
    X['Item_Outlet_Sales'] = y

    test_data_path = config["split_data"]["test_path"] 
    train_data_path = config["split_data"]["train_path"]
    split_ratio = config["split_data"]["test_size"]
    random_state = config["base"]["random_state"]
    train, test = train_test_split(X, test_size=split_ratio, random_state=random_state)
    train.to_csv(train_data_path, sep=",", index=False, encoding="utf-8")
    test.to_csv(test_data_path, sep=",", index=False, encoding="utf-8")
    



if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    split_data(config_path=parsed_args.config)