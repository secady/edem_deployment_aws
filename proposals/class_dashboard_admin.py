import requests
import pandas as pd
import matplotlib.pyplot as plt
import itertools
from collections import Counter

class AdminDashboard:
    def __init__(self, url_users, url_programs, headers):
        self.url_users = url_users
        self.url_programs = url_programs
        self.headers = headers
        self.users_df_stat = None
        self.programs_df = None
        
    def fetch_data(self):
        response_programs = requests.get(self.url_programs, headers=self.headers)
        response_users = requests.get(self.url_users, headers=self.headers)
        
        if response_programs.status_code == 200 and response_users.status_code == 200:
            data_programs = response_programs.json()
            programs_df = pd.DataFrame(data_programs)
            
            data_users = response_users.json()
            users_df = pd.DataFrame(data_users)
            
            category_id_list = []
            category_name_list = []
            
            for user in users_df["categoryIds"]:
                category_ids = []
                category_names = []
                
                for category in user:
                    category_ids.append(category["_id"])
                    category_names.append(category["name"])
                
                category_id_list.append(category_ids)
                category_name_list.append(category_names)
            
            users_df["category_id"] = category_id_list
            users_df["category_name"] = category_name_list
            
            program_dict = dict(zip(programs_df["_id"], programs_df["name"]))
            users_df["program_name"] = users_df["program"].map(program_dict)
            
            users_df = users_df[['_id', 'name', 'surname', 'email', 'age', 'gender', 'role', 'roleMde',
                                'program', 'program_name', 'year', 'connections', 'categoryIds', 'category_id',
                                'category_name', 'eventIds', 'confirmed', 'createdAt', 'updatedAt', '__v',
                                'image', 'bio', 'chatIds']]
            
            users_df_stat = users_df.copy()
            users_df_stat = users_df_stat[['_id', 'name', 'surname', 'email', 'age', 'gender', 'program_name',
                                           'year', 'category_name', 'eventIds']]
            users_df_stat = users_df_stat[users_df_stat["gender"] != "N/A"]
            
            self.users_df_stat = users_df_stat
            self.programs_df = programs_df
        else:
            print('Error: Failed to fetch data from the webpage')
    
    def fetch_additional_data(self):
        url_categories = "https://edem-students-backend.vercel.app/categories/dataGetAll"
        url_events = "https://edem-students-backend.vercel.app/events/dataGetAll"
        headers = {"Authorization": "desafio2023"}
        payload = ""
        
        response_categories = requests.get(url_categories, headers=headers, data=payload)
        response_events = requests.get(url_events, headers=headers, data=payload)
        
        if response_categories.status_code == 200 and response_events.status_code == 200:
            data_categories = response_categories.json()
            categories_df = pd.DataFrame(data_categories)
            
            data_events = response_events.json()
            events_df = pd.DataFrame(data_events)
            
            events_df['category_id'] = events_df['categoryIds'].apply(lambda x: [id for id in x])
            events_df['category_name'] = events_df['categoryIds'].apply(lambda x: [categories_df.loc[categories_df['_id'] == id, 'name'].values[0] if categories_df['_id'].isin([id]).any() else None for id in x])
            
            self.categories_df = categories_df
            self.events_df = events_df
        else:
            print('Error: Failed to fetch data from the webpage')


    def visualize_users_per_program(self):
        if self.users_df_stat is None:
            print('Error: Data has not been fetched yet.')
            return
        
        user_per_program = self.users_df_stat.groupby("program_name")["_id"].count().sort_values(ascending=False)
        
        plt.bar(user_per_program.index, user_per_program.values, color='#004368')
        plt.ylabel('Cantidad de usuarios', fontweight='bold', color='#004368')
        plt.title('Usuarios registrados por programa formativo', fontweight='bold', color='#004368')
        plt.xticks(rotation=90, fontweight='bold', color='#004368')
        
        plt.show()
    
    
    def visualize_users_per_gender(self):
        if self.users_df_stat is None:
            print('Error: Data has not been fetched yet.')
            return
        
        users_per_gender = self.users_df_stat.groupby("gender")["_id"].count().sort_values(ascending=False)
        
        colors = ['#CB7862', '#004368', '#847C7B']
        plt.pie(users_per_gender, labels=users_per_gender.index, autopct='%1.1f%%', colors=colors,
                startangle=90, wedgeprops={'edgecolor': 'white'})
        
        center_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(center_circle)
        
        plt.axis('equal')
        plt.title('Usuarios registrados por género', fontweight='bold', color='#004368')
        
        plt.show()
    
    def visualize_users_per_year(self):
        if self.users_df_stat is None:
            print('Error: Data has not been fetched yet.')
            return
        
        users_per_year = self.users_df_stat.groupby("year")["_id"].count()
        
        plt.bar(users_per_year.index, users_per_year.values, color='#004368')
        plt.ylabel('Cantidad de usuarios', fontweight='bold', color='#004368')
        plt.title('Usuarios registrados por año de estudio', fontweight='bold', color='#004368')
        plt.xticks(rotation=45, fontweight='bold', color='#004368')
        
        plt.show()

    
    def visualize_users_per_interest(self):
        if self.users_df_stat is None:
            print('Error: Data has not been fetched yet.')
            return

        categories = list(itertools.chain.from_iterable(self.users_df_stat['category_name']))

        # Count occurrences of each category
        category_counts = Counter(categories)

        # Sort categories by count in descending order
        sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
        category_names = [category[0] for category in sorted_categories]
        category_values = [category[1] for category in sorted_categories]

        # Plot the bar chart
        plt.figure(figsize=(12, 6))
        plt.bar(category_names, category_values, color='#004368')
        plt.xlabel('Categorías de Interés', fontweight='bold', color='#004368')
        plt.ylabel('Cantidad de Usuarios', fontweight='bold', color='#004368')
        plt.title('Cantidad de Usuarios por Interés', fontweight='bold', color='#004368')
        plt.xticks(rotation=45, ha='right', fontweight='bold', color='#004368')
        plt.tight_layout()
        plt.show()   


    def visualize_events_per_month(self):
        if self.events_df is None:
            print('Error: Data has not been fetched yet.')
            return
        
        events_df_stat = self.events_df.copy()
        events_df_stat = events_df_stat[['_id', 'title', 'description', 'date', 'userIds', 'category_id', 'category_name']]
        events_df_stat['date'] = pd.to_datetime(events_df_stat['date'])

        events_per_month = events_df_stat.groupby(events_df_stat['date'].dt.to_period('M')).size()

        plt.bar(events_per_month.index.strftime('%Y-%m'), events_per_month.values, color='#004368')

        plt.xlabel('Mes', fontweight='bold', color='#004368')
        plt.ylabel('Cantidad de Eventos', fontweight='bold', color='#004368')
        plt.title('Eventos por Mes', fontweight='bold', color='#004368')

        plt.xticks(rotation=45, fontweight='bold', color='#004368')

        plt.show()

    def visualize_users_per_event_category(self):
        if self.events_df is None:
            print('Error: Data has not been fetched yet.')
            return

        categories = list(itertools.chain.from_iterable(self.events_df['category_name']))

        category_counts = Counter(categories)

        sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
        category_names = [category[0] for category in sorted_categories]
        category_values = [category[1] for category in sorted_categories]

        plt.figure(figsize=(12, 6))
        plt.bar(category_names, category_values, color='#004368')
        plt.xlabel('Categorías de Evento', fontweight='bold', color='#004368')
        plt.ylabel('Cantidad de Usuarios', fontweight='bold', color='#004368')
        plt.title('Cantidad de Usuarios Registrados por Evento', fontweight='bold', color='#004368')
        plt.xticks(rotation=45, ha='right', fontweight='bold', color='#004368')
        plt.tight_layout()
        plt.show()