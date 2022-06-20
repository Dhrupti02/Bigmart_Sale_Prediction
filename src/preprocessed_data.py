from get_data import read_params
import argparse
import pandas as pd
import numpy as np
from sklearn import preprocessing
import category_encoders as ce
import json

''' Preprocessing the data before training. Missing values filled, categorical data are encoded, Outlires are detected 
    and handled, transformed the data, and saved to CSV files. '''

def fill_data(df):
    df['Item_Fat_Content'] = df['Item_Fat_Content'].replace(to_replace='low fat', value='Low Fat')
    df['Item_Fat_Content'] = df['Item_Fat_Content'].replace(to_replace='LF', value='Low Fat')
    df['Item_Fat_Content'] = df['Item_Fat_Content'].replace(to_replace='reg', value='Regular')

    df['Item_Visibility'].replace(0, np.nan, inplace = True)
    df['Item_Weight'].fillna(df.groupby(['Item_Identifier']).Item_Weight.transform(np.median), inplace=True)
    df['Item_Visibility'].fillna(df.groupby(['Item_Identifier']).Item_Visibility.transform(np.median), inplace=True)
    df['Outlet_Size'].fillna(df['Outlet_Size'].mode()[0], inplace = True)
    df = df.dropna()
    return df

def encode(config_path):
    config = read_params(config_path)
    raw_data_path = config["load_data"]["raw_dataset_csv"]
    df = pd.read_csv(raw_data_path)
    df = fill_data(df)

    # Label encoding
    label_encoder = preprocessing.LabelEncoder()
    df['Outlet_Size']= label_encoder.fit_transform(df['Outlet_Size'])
    
    # Target encoding 
    item_encode = df.groupby(['Item_Identifier'])['Item_Outlet_Sales'].mean().to_dict()
    df['Item_Identifier'] = df['Item_Identifier'].map(item_encode)
    json.dump(item_encode, open("data/dictd.txt",'w'))

    # one-hot encoding
    obj = df[['Outlet_Identifier', 'Item_Type', 'Item_Fat_Content', 'Outlet_Location_Type', 'Outlet_Type']]
    other = df[['Item_Identifier','Item_Weight',
     'Item_Visibility',
     'Item_MRP',
     'Item_Outlet_Sales', 
     'Outlet_Establishment_Year', 
     'Outlet_Size']]
    encode = pd.get_dummies(obj, drop_first = True)
    df = pd.concat([other, encode], axis = 1)

    # Detect Outliers
    q1 = np.percentile(df['Item_Outlet_Sales'], 12.5)
    q3 = np.percentile(df['Item_Outlet_Sales'], 87.5)
    # print(q1, q3)
    IQR = q3-q1
    lwr_bound = q1-(1.5*IQR)
    upr_bound = q3+(1.5*IQR)

    q11 = np.percentile(df['Item_Visibility'], 11.5)
    q33 = np.percentile(df['Item_Visibility'], 88.5)
    # print(q1, q3)
    IQR1 = q33-q11
    lwr_bound1 = q11-(1.5*IQR1)
    upr_bound1 = q33+(1.5*IQR1)


    # Drop extreme outliers
    df.drop(df[ (df.Item_Outlet_Sales > upr_bound) | (df.Item_Outlet_Sales < lwr_bound) ].index , inplace=True)
    df.drop(df[ (df.Item_Visibility > upr_bound1) | (df.Item_Visibility < lwr_bound1) ].index , inplace=True)

    df.drop(index=[2109, 4873, 8245, 1821, 2293, 332, 4313, 1755], inplace=True)
    
    # Log transformation on skewed data
    df['Item_Outlet_Sales'] = np.log(df['Item_Outlet_Sales'])
    df['Item_Visibility'] = np.log(df['Item_Visibility'])
    df['Item_Identifier'] = np.log(df['Item_Identifier'])
    df['Item_Weight'] = np.log(df['Item_Weight'])
    df['Item_MRP'] = np.log(df['Item_MRP'])

    df.drop(index=[2374, 3862, 4499, 6847, 7464, 7551], inplace = True)

    # Save data to CSV file
    raw_data_path = config["preprocessed_data"]["preprocessed_data_csv"]
    df.to_csv(raw_data_path, sep=",", index=False, encoding="utf-8")

    

if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    encode(config_path=parsed_args.config)