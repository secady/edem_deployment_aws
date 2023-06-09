import pandas as pd
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.metrics import accuracy_score
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans

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
        return X


columns = ['student_id', 'student_name', 'gender', 'age', 'year_of_study', 'school_email', 'personal_email', 'address', 'zip_code', 'prog_maj_id', 
           'prog_maj_title', 'interests']