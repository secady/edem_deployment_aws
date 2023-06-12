class EventRecommendation:
    def __init__(self):
        self.event_recommendation_df = None

    def get_sorted_events_dict(self):

        # Make a GET request to the webpage
        url = 'https://edem-students-backend.vercel.app/users/dataGetAll' 
        headers = {'Authorization':'desafio2023'}
        payload = ""
        response = requests.get(url,headers=headers, data=payload)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            
            # Convert the data to a DataFrame
            students_df = pd.DataFrame(data)
        else:
            print('Error: Failed to fetch data from the webpage')

        # Make a GET request to the webpage
        url = 'https://edem-students-backend.vercel.app/events/dataGetAll'
        headers = {'Authorization':'desafio2023'}
        payload = ""
        response = requests.get(url,headers=headers, data=payload)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            
            # Convert the data to a DataFrame
            events_df = pd.DataFrame(data)
        else:
            print('Error: Failed to fetch data from the webpage')



        # Initialize empty lists for category details
        category_id_list = []
        category_name_list = []

        # Iterate over each event row
        for event in students_df["categoryIds"]:
            category_ids = []
            category_names = []

            # Iterate over each category in the event
            for category in event:
                category_ids.append(category["_id"])
                category_names.append(category["name"])

            # Append the category details to the lists
            category_id_list.append(category_ids)
            category_name_list.append(category_names)

        # Assign the category details to the DataFrame
        students_df["category_id"] = category_id_list
        students_df["category_name"] = category_name_list

        # Interests ids
        specific_interests= ['64805c99a7607c035063190c', '64805c99a7607c035063190d', '64805c99a7607c035063190e', '64805c99a7607c035063190f', '64805c99a7607c0350631910', '64805c99a7607c0350631911', '64805c99a7607c0350631912', '64805c99a7607c0350631913', '64805c99a7607c0350631914', '64805c99a7607c0350631915', '64805c99a7607c0350631916', '64805c99a7607c0350631917', '64805c99a7607c0350631918', '64805c99a7607c0350631919', '64805c99a7607c035063191a', '64805c99a7607c035063191b']
        
        # Creation of categorical columns for each interest ids for students_df
        for interest in specific_interests:
            students_df[interest] = students_df['category_id'].apply(lambda x: 1 if interest in x else 0)
            
        students_df = students_df.rename(columns={'_id': 'student_id'})

        # Creation of categorical columns for each interest ids for events_df
        for interest in specific_interests:
            events_df[interest] = events_df['categoryIds'].apply(lambda x: 1 if interest in x else 0)
        events_df.drop('categoryIds', axis=1, inplace=True)
        events_df = events_df.rename(columns={'_id': 'event_id'})

        students_df = students_df.drop([ 'name', 'surname', 'email', 'age', 'gender', 'role', 'roleMde','program', 'year', 'connections', 'eventIds','confirmed', 'createdAt', 'updatedAt', '__v', 'image', 'bio', 'chatIds', 'category_name','categoryIds','category_id'], axis=1).copy()
        events_df = events_df.drop([ 'title', 'description', 'date', 'url', '__v','createdAt', 'updatedAt', 'image', 'userIds'], axis=1).copy()

        event_recommendation_df = pd.DataFrame(columns=['student_id'] + list(events_df['event_id']))
        for student in students_df.itertuples():
            student_id = student.student_id
            punctuation = []

            for event in events_df.itertuples():
                event_id = event.event_id
                common_interests = sum([student[index] and event[index] for index in range(3, len(student))])
                punctuation.append(common_interests * 0.333)

            event_recommendation_df.loc[len(event_recommendation_df)] = [student_id] + punctuation

        sorted_events_list = []
        for student in event_recommendation_df.itertuples():
            student_id = student.student_id
            events_sorted_indices = np.argsort(student[2:])
            events_sorted = [event_recommendation_df.columns[index+1] for index in events_sorted_indices]
            sorted_events_list.append((student_id, events_sorted[::-1]))

        # Create a dictonary that contains the student id and all the events ids in order of preference
        student_dict = {}
        for student_events in sorted_events_list:
            student_id, events_sorted_list = student_events
            student_dict[student_id] = events_sorted_list

        return student_dict