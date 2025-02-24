import os
import pandas as pd
import streamlit as st
from quiz_grader import QuizGrader, ReturnClassroom
import time

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import streamlit_authenticator as stauth

import yaml
from yaml.loader import SafeLoader

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

name, authentication_status, username = authenticator.login()

if authentication_status:
    @st.cache_data
    def Get_Courses():
        # Define the accesses to be granted
        SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly', # View your Google Classroom classes.
                'https://www.googleapis.com/auth/classroom.rosters', # Manage your Google Classroom class rosters.
                'https://www.googleapis.com/auth/classroom.profile.emails', # View the email addresses of people in your classes.
                'https://www.googleapis.com/auth/classroom.topics', #See, create, and edit topics in Google Classroom.
                'https://www.googleapis.com/auth/classroom.coursework.students', # Manage coursework and grades for students
                'https://www.googleapis.com/auth/classroom.courseworkmaterials', # See, edit, and create classwork materials in Google Classroom.
                'https://www.googleapis.com/auth/spreadsheets'] # See all your Google Sheets spreadsheets.

        creds = Credentials.from_authorized_user_info({"token": st.secrets['token'], 
                                                    "refresh_token": st.secrets['refresh_token'], 
                                                    "token_uri": "https://oauth2.googleapis.com/token", 
                                                    "client_id": st.secrets['client_id'], 
                                                    "client_secret": st.secrets['client_secret'], 
                                                    "scopes": ["https://www.googleapis.com/auth/classroom.courses.readonly", "https://www.googleapis.com/auth/classroom.rosters", "https://www.googleapis.com/auth/classroom.profile.emails", "https://www.googleapis.com/auth/classroom.topics", "https://www.googleapis.com/auth/classroom.coursework.students", "https://www.googleapis.com/auth/classroom.courseworkmaterials", "https://www.googleapis.com/auth/spreadsheets"], 
                                                    "expiry": "2024-02-05T10:21:31.547832Z"}, SCOPES)

        service = build('classroom', 'v1', credentials=creds)

        # Use the `courses().list()` method to show a list of the user's courses
        results = service.courses().list(pageSize=20).execute()
        courses = results.get('courses', [])

        return creds, courses

    st.title("Algoritma Online Quiz Grader")
    st.write("#")

    course_name = None
    specialization = None
    filepath = None
    grade_table = pd.DataFrame()
    warning_text = ""

    st.markdown(
        """
        <style>
            section[data-testid="stSidebar"] {
                width: 500px !important; # Set the width to your desired value
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.header('💡 How to Use:')
    st.sidebar.markdown(
'''
1. Please select the Google Classroom Course, Specialization, and Class Name of the Quiz.
2. Make sure that the sheet name from [Algoritma Score Academy](https://docs.google.com/spreadsheets/d/1cGJ0pn9k9gKCBnceWVwaL9D7BBDMNjLh8uPYlaBlJi8) is correct.
3. Download the quiz grades file from [Algortima WP Admin](https://algoritmaonline.com/wp-admin/edit.php?post_type=sfwd-quiz) and upload the CSV file.
4. Press the **Grade Quiz to Score Academy** button and check [Algoritma Score Academy](https://docs.google.com/spreadsheets/d/1cGJ0pn9k9gKCBnceWVwaL9D7BBDMNjLh8uPYlaBlJi8) to see if the grades are correct.
5. If you encountered a mistake, you can manually change the grades.
6. Press the **Return Grade to Google Classroom** button to return the grades to the students in the Google Classroom.
'''
    )

    creds, courses = Get_Courses()
    course_name = st.selectbox("Select Course", [course['name'] for course in courses], index=None)

    if course_name != None:
        if ' '.join(course_name.split()[-2:]) == 'Data Analytics': 
            spec = 0
        elif ' '.join(course_name.split()[-2:]) == 'Data Visualization': 
            spec = 1
        elif ' '.join(course_name.split()[-2:]) == 'Machine Learning': 
            spec = 2
        else: 
            spec = None
        
        # Select box for class session
        specialization = st.selectbox("Select Specialization", ['Data Analytics', 'Data Visualization', 'Machine Learning'], index=spec)

    if specialization != None:
        col1, col2 = st.columns(2)
        with col1:
            if specialization == 'Data Visualization':
                quiz_name = st.selectbox("Select Class", ['P4DS', 'DV', 'IP'])
            elif specialization == 'Machine Learning':
                quiz_name = st.selectbox("Select Class", ['RM', 'C1', 'C2', 'UL', 'TS', 'NN'])
            elif specialization == 'Data Analytics':
                quiz_name = st.selectbox("Select Class", ['P4DA', 'EDA', 'DWV', 'SQL', 'IML1', 'IML2'])

        with col2:
            if specialization == 'Data Analytics':
                sheet_name = st.text_input("Input Score Academy Sheet Name", value=f"{course_name.split()[0]} DA")
            else:
                sheet_name = st.text_input("Input Score Academy Sheet Name", value=f"Academy: Batch {ord(course_name.split()[0][0])-38}")

        filepath = st.file_uploader("Upload Algoritma Online CSV", type="csv")

    if 'graded' not in st.session_state:
        st.session_state['graded'] = False

    if filepath != None:
        _, col2, col3, col4, _ = st.columns([1,3,1,3,1])

        with col2:
            grade = st.button('Grade Quiz to \n\n Score Academy', use_container_width=True)

        with col4:
            return_classroom = st.button('Return Grade to \n\n Google Classroom', use_container_width=True)

        if grade:
            with st.spinner('Grading Quiz to Score Academy...'):
                df = QuizGrader(filepath=filepath,
                                link='https://docs.google.com/spreadsheets/d/1cGJ0pn9k9gKCBnceWVwaL9D7BBDMNjLh8uPYlaBlJi8/edit#gid=455932940',
                                specialization=specialization,
                                sheet_name=sheet_name, 
                                quiz_name=quiz_name, 
                                credentials=creds)
            success = st.success('Grading Successful!')

            st.session_state['graded'] = True

            time.sleep(3)
            success.empty()
                
        if return_classroom and st.session_state['graded'] == False:
            st.error('Please Grade the Quiz first using the **Grade Quiz to Score Academy** button')
        
        elif return_classroom and st.session_state['graded'] == True:
            with st.spinner('Returning Grade to Google Classroom...'):
                grade_table, warnings = ReturnClassroom(link='https://docs.google.com/spreadsheets/d/1cGJ0pn9k9gKCBnceWVwaL9D7BBDMNjLh8uPYlaBlJi8/edit#gid=455932940',
                                                        specialization=specialization,
                                                        sheet_name=sheet_name, 
                                                        course_name=course_name, 
                                                        quiz_name=quiz_name, 
                                                        credentials=creds)
                
            success = st.success('Return Successful!')
            my_bar = st.progress(0, text="Loading result. Please wait...")

            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1, text="Loading result. Please wait...")
            time.sleep(1)
            
            my_bar.empty()

            percent_complete = True
            
            if percent_complete:
                for warning in warnings:
                    warning_text += f'  {warning}  \n'

                st.info(warning_text, icon='⚠️')
                st.dataframe(grade_table, use_container_width=True)

elif authentication_status == False:
    st.error('Username/password is incorrect')

elif authentication_status == None:
    st.warning('Please enter your username and password')

