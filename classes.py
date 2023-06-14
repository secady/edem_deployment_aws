import pandas as pd
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.metrics import accuracy_score
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
from sqlalchemy import create_engine,text
from joblib import load
import requests

class InterestsTransformer():
    def __init__(self, columns):
        self.columns = columns

    def fit(self, X, y=None):
        return self
    
    def transform(self, df):
        df['Finance and Investment'] = ''
        df['Management Skills'] = ''
        df['Tech'] = ''
        df['Business Management'] = ''
        df['Marketing'] = ''
        df['Sustainability'] = ''
        df['Networking'] = ''
        df['HR'] = ''
        df['Sport'] = ''
        df['Music'] = ''
        df['Artificial Intelligence'] = ''
        df['Crypto'] = ''
        df['Economy'] = ''
        df['Entrepreneurship'] = ''
        df['Design'] = ''
        df['Employment'] = ''

        for index, row in df.iterrows():
            for column in self.columns:
                interests = row[column]
                if isinstance(interests, str):
                    interests = interests.split(', ')
                    for interest in interests:
                        if (interest == 'Finance and Investment') and (interest not in list(df.columns)):
                            df.at[index, 'Finance and Investment'] = interest
                        elif (interest == 'Management Skills') and (interest not in list(df.columns)):
                            df.at[index, 'Management Skills'] = interest
                        elif (interest == 'Tech') and (interest not in list(df.columns)):
                            df.at[index, 'Tech'] = interest
                        elif (interest == 'Business Management') and (interest not in list(df.columns)):
                            df.at[index, 'Business Management'] = interest
                        elif (interest == 'Marketing') and (interest not in list(df.columns)):
                            df.at[index, 'Marketing'] = interest
                        elif (interest == 'Sustainability') and (interest not in list(df.columns)):
                            df.at[index, 'Sustainability'] = interest
                        elif (interest == 'Networking') and (interest not in list(df.columns)):
                            df.at[index, 'Networking'] = interest
                        elif (interest == 'HR') and (interest not in list(df.columns)):
                            df.at[index, 'HR'] = interest
                        elif (interest == 'Sport') and (interest not in list(df.columns)):
                            df.at[index, 'Sport'] = interest
                        elif (interest == 'Music') and (interest not in list(df.columns)):
                            df.at[index, 'Music'] = interest
                        elif (interest == 'Artificial Intelligence') and (interest not in list(df.columns)):
                            df.at[index, 'Artificial Intelligence'] = interest
                        elif (interest == 'Crypto') and (interest not in list(df.columns)):
                            df.at[index, 'Crypto'] = interest
                        elif (interest == 'Economy') and (interest not in list(df.columns)):
                            df.at[index, 'Economy'] = interest
                        elif (interest == 'Entrepreneurship') and (interest not in list(df.columns)):
                            df.at[index, 'Entrepreneurship'] = interest
                        elif (interest == 'Design') and (interest not in list(df.columns)):
                            df.at[index, 'Design'] = interest
                        elif (interest == 'Employment') and (interest not in list(df.columns)):
                            df.at[index, 'Employment'] = interest
                        
        return df

class ColumnDropperTransformer():
    def __init__(self, columns):
        self.columns = columns

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.drop(columns=self.columns)


class ColumnOneHotEncoder():
    def __init__(self, columns):
        self.columns = columns

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        onehot = OneHotEncoder(sparse=False)
        encoded_cols = onehot.fit_transform(X[self.columns])
        feature_names = onehot.get_feature_names_out(input_features=self.columns)
        X_copy = X.copy()
        X_copy[feature_names] = encoded_cols
        X_copy = X_copy.drop(columns=self.columns)
        return X_copy


class ColumnOrdinalEncoder():
    def __init__(self, **category_values):
        self.category_values = category_values
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        ordinal = OrdinalEncoder(categories=[self.category_values[column] for column in self.category_values.keys()])
        encoded_cols = ordinal.fit_transform(X[list(self.category_values.keys())])
        X_copy = X.copy()
        X_copy[list(self.category_values.keys())] = encoded_cols
        return X_copy
    

class ModelScorer(BaseEstimator, TransformerMixin):
    def __init__(self, model):
        self.model = model
        self.labels = None
        self.inertia = None
        self.silhouette = None

    def fit(self, X, y=None):
        self.model.fit(X)
        self.labels = self.model.labels_
        self.inertia = self.model.inertia_
        self.silhouette = silhouette_score(X, self.labels)
        return self

    def transform(self, X):
        return self.model.predict(X)

class RecommendUsers():
    def __init__(self):
        self.model = None
    def users(self):
        model = load('pipeline.pkl') 
        url_users = "https://edem-students-backend.vercel.app/users/dataGetAll"
        headers = {"Authorization": "desafio2023"}
        payload = ""
        response = requests.get(url_users,headers=headers, data=payload)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data_users = response.json()  # Assuming the response contains JSON data
            # Convert the data to a DataFrame
            users_df = pd.DataFrame(data_users)
        else:
            return 'Error: Failed to fetch users data from the webpage'
        
        category_id_list = []
        category_name_list = []

        # Iterate over each event row
        for user in users_df["categoryIds"]:
            category_ids = []
            category_names = []

            # Iterate over each category in the event
            for category in user:
                category_ids.append(category["_id"])
                category_names.append(category["name"])

            # Append the category details to the lists
            category_id_list.append(category_ids)
            category_name_list.append(category_names)

        # Assign the category details to the DataFrame
        users_df["category_id"] = category_id_list
        users_df["category_name"] = category_name_list

        #programs ----------------------------------------------------------
        url_programs = "https://edem-students-backend.vercel.app/programs/dataGetAll"
        headers = {"Authorization": "desafio2023"}
        payload = ""

        response = requests.get(url_programs,headers=headers, data=payload)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data_programs = response.json()  # Assuming the response contains JSON data
            
            # Convert the data to a DataFrame
            programs_df = pd.DataFrame(data_programs)
        else:
            return 'Error: Failed to fetch events data from the webpage'

        # Create a dictionary mapping program IDs to program names
        program_dict = dict(zip(programs_df["_id"], programs_df["name"]))

        # Use the map function to create the new column "program_name"
        users_df["program_name"] = users_df["program"].map(program_dict)
        #---------------------------------------------------------------------
        users_id = users_df['_id']
        users_df.drop(['role','chatIds','roleMde','program','connections','eventIds','confirmed','createdAt','updatedAt','__v','image','bio','category_id'],axis=1,inplace=True)
        users_df.rename(columns={'_id': 'student_id','categoryIds': 'category_id','category_name':'category','program_name':'programme'},inplace=True, errors='raise')

        # Define the mapping of values to labels
        mapping = {'1': '1st year', '2': '2nd year', '3': '3rd year', '4': '4th year'}

        # Replace values in the 'year_of_study' column
        users_df['year'] = users_df['year'].replace(mapping)
        users_df = users_df.dropna()
        users_df = model.transform(users_df)
        df_final = pd.DataFrame(users_df,columns=['cluster'])
        df_final['_id'] = users_id

        return df_final
    
    def group_users(self,requested_student_id):
        df_final = self.users()
        # Step 1: Group DataFrame by "cluster" column
        grouped_clusters = df_final.groupby(["cluster"])
        
        #Step 2: Create dictionary of clusters and user_ids
        clusters_dict = {}
        for cluster, group in grouped_clusters:
            clusters_dict[cluster] = list(group["_id"])
        for list_users in clusters_dict.values():
            if requested_student_id in list_users:
                list_users.remove(requested_student_id)
                return list_users
            else:
                continue
