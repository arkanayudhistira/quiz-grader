import os
import pandas as pd
import streamlit as st
from quiz_grader import QuizGrader
import time


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
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
                sheet_name = st.text_input("Input Score Academy Sheet Name", value=f"Academy: Batch {ord(course_name.split()[0][0])-64}")

        filepath = st.file_uploader("Upload Algoritma Online CSV", type="csv")

    if filepath != None:
        _, _, col3, col4, _ = st.columns(5)

        with col3:
            button = st.button('Grade Quiz')
        with col4:
            if button:
                with st.spinner('Grading...'):
                    grade_table, warnings = QuizGrader(filepath=filepath,
                                                    link='https://docs.google.com/spreadsheets/d/1cGJ0pn9k9gKCBnceWVwaL9D7BBDMNjLh8uPYlaBlJi8/edit#gid=455932940',
                                                    specialization=specialization,
                                                    sheet_name=sheet_name, 
                                                    course_name=course_name, 
                                                    quiz_name=quiz_name, 
                                                    credentials=creds)
        if button:
            success = st.success('Grading Successful!')
            my_bar = st.progress(0, text="Loading result. Please wait...")

            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1, text="Loading result. Please wait...")
            time.sleep(1)
            
            my_bar.empty()
            success.empty()

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

