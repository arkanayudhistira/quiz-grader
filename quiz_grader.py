# Import required dependencies to use Google's API
import pandas as pd

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Convert class code abbreviation into the full quiz name in Classroom for easier input

def classcode(code):
        code = code.lower()
        if code == 'p4ds':
                return '1. Q: Programming for Data Science (P4DS) & Practical Statistic (PS)'
        elif code == 'dv':
                return '2. Q: Data Visualization (DV)'
        elif code == 'ip':
                return '3. Q: Interactive Plotting (IP)'
        elif code == 'rm':
                return '1. Q: Regression Model (RM)'
        elif code == 'c1':
                return '2. Q: Classification in Machine Learning I (C1)'
        elif code == 'c2':
                return '3. Q: Classification in Machine Learning II (C2)'
        elif code == 'ul':
                return '4. Q: Unsupervised Learning (UL)'
        elif code == 'ts':
                return '5. Q: Time Series & Forecasting (TSF)'
        elif code == 'nn':
                return '6. Q : Neural Network and Deep Learning (NN)'
        elif code == 'p4da':
                return '1. Q: Python for Data Analysts (P4DA)'
        elif code == 'eda':
                return '2. Q: Exploratory Data Analysis (EDA)'
        elif code == 'dwv':
                return '3. Q: Data Wrangling and Visualization (DWV)'
        elif code == 'sql':
                return '4. Q: Structured Query Language (SQL)'
        elif code == 'iml1':
                return '5. Q: Introduction to Machine Learning I'
        elif code == 'iml2':
                return '6. Q: Introduction to Machine Learning II'
        else:
                raise Exception(f'{code} quiz not found')

# Convert class code abbreviation into the full column name in Google Sheets for easier input
     
def quizcode(code):
        code = code.lower()
        if code == 'p4ds':
                return 'P4DS-PS Quiz'
        elif code == 'dv':
                return 'DV Quiz'
        elif code == 'ip':
                return 'IP Quiz'
        elif code == 'rm':
                return 'RM Quiz'
        elif code == 'c1':
                return 'C1 Quiz'
        elif code == 'c2':
                return 'C2 Quiz'
        elif code == 'ul':
                return 'UL Quiz'
        elif code == 'ts':
                return 'TS Quiz'
        elif code == 'nn':
                return 'NN Quiz'
        elif code == 'p4da':
                return 'P4DA'
        elif code == 'eda':
                return 'EDA'
        elif code == 'dwv':
                return 'DWV'
        elif code == 'sql':
                return 'SQL'
        elif code == 'iml1':
                return 'IML 1'
        elif code == 'iml2':
                return 'IML 2'
        else:
                raise Exception(f'{code} quiz not found')

# Convert class code abbreviation into the cell range value in Google Sheets for easier input

def quiz_range(code):
        code = code.lower()
        if code == 'p4ds':
                return 'F2:F200'
        elif code == 'dv':
                return 'G2:G200'
        elif code == 'ip':
                return 'H2:H200'
        elif code == 'rm':
                return 'M2:M200'
        elif code == 'c1':
                return 'N2:N200'
        elif code == 'c2':
                return 'O2:O200'
        elif code == 'ul':
                return 'P2:P200'
        elif code == 'ts':
                return 'Q2:Q200'
        elif code == 'nn':
                return 'R2:R200'
        elif code == 'p4da':
                return 'F2:F200'
        elif code == 'eda':
                return 'G2:G200'
        elif code == 'dwv':
                return 'H2:H200'
        elif code == 'sql':
                return 'I2:I200'
        elif code == 'iml1':
                return 'J2:J200'
        elif code == 'iml2':
                return 'K2:K200'
        else:
                raise Exception(f'{code} quiz not found')
        
# Convert class code abbreviation into the maximum score for each quizzes
        
def max_score(code):
        code = code.lower()
        if code == 'p4ds':
                return 4
        elif code == 'dv':
                return 2
        elif code == 'ip':
                return 1
        elif code == 'rm':
                return 4
        elif code == 'c1':
                return 4
        elif code == 'c2':
                return 4
        elif code == 'ul':
                return 4
        elif code == 'ts':
                return 4
        elif code == 'nn':
                return 4
        elif code == 'p4da':
                return 6
        elif code == 'eda':
                return 6
        elif code == 'dwv':
                return 6
        elif code == 'sql':
                return 6
        elif code == 'iml1':
                return 5
        elif code == 'iml2':
                return 5
        else:
                raise Exception(f'{code} quiz not found')
        

def QuizGrader(filepath, link, sheet_name, specialization, course_name, quiz_name, credentials):  

    QUIZ_DF = pd.read_csv(filepath) # Quiz CSV Path
    SCORE_ACADEMY_LINK = link # Score Academy Link
    NAMA_SHEET = sheet_name # Sheet Name (Wizard) 

    creds = credentials

    # In the section, the user is going to access the scores that have been entered on the spreadsheet `Score Academy`  
    # Input the link to the Score Academy spreadsheet and retrieve the Spreadsheet ID

    SCORE_ACADEMY_ID = SCORE_ACADEMY_LINK.split(sep='/')[-2]

    # Specify the sheet and the cell ranges that is going to be accessed
    if specialization == "Data Analytics":
        GRADE_RANGE = [f'{NAMA_SHEET}!D:E', f'{NAMA_SHEET}!F:I', f'{NAMA_SHEET}!J:K']
    else:
        GRADE_RANGE = [f'{NAMA_SHEET}!D:E', f'{NAMA_SHEET}!F:H', f'{NAMA_SHEET}!M:R']

    # Call the Google Spreadsheet API and retrieve the values of the ranges that have been specified

    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets().values().batchGet(spreadsheetId=SCORE_ACADEMY_ID,
                                                         ranges=GRADE_RANGE).execute()
        values = sheet.get('valueRanges', [])
            
    except HttpError as error:
        print(error)

    # Concat the retrieved values as a dataframe

    email = pd.DataFrame(values[0].get('values'))
    grade_dv = pd.DataFrame(values[1].get('values'))
    grade_ml = pd.DataFrame(values[2].get('values'))

    df = pd.concat([email, grade_dv, grade_ml], axis=1)
    df.columns = df.iloc[0]
    df.drop(index=0, inplace=True)
    df['Email Algoritma Online'] = df['Email Algoritma Online'].str.strip().str.lower()
    df['Email Classroom'] = df['Email Classroom'].str.strip().str.lower()

    # In this section, the user is going to choose which Google Classroom Course that is going to be accessed
    # Call the Google Classroom API to access various methods with user's access from the credential that has been authenticated

    service = build('classroom', 'v1', credentials=creds)

    # Use the `courses().list()` method to show a list of the user's courses

    results = service.courses().list(pageSize=20).execute()
    courses = results.get('courses', [])

    if not courses:
        print('No courses found.')

    course_input = course_name
    course_lowercase = course_input.lower()
    course_id = None

    for course in courses:
        if course_lowercase == course['name'].lower():
            course_id = course['id']
            break

    if course_id == None:
        raise Exception(f"{course_input} course not found")

    else:
        print(f'{course_input} found with ID {course_id}')

    service = build('classroom', 'v1', credentials=creds)
    response = service.courses().courseWork().list(courseId=course_id).execute()
    classworks = response.get('courseWork')

    while response.get('nextPageToken'):
        response = service.courses().students().list(courseId=course_id, pageToken = response['nextPageToken']).execute()
        classworks.extend(response.get('courseWork'))

    quiz_input = quiz_name
    quiz_id = None

    for classwork in classworks:
        if classwork['title'] == classcode(quiz_input):
            quiz_id = classwork['id']
            break

    if quiz_id == None:
        raise Exception(f"Quiz not found")
    else:
        print(f"{classwork['title']} Quiz was found")

    # In this section, the received grade is going to be written in Score Academy

    QUIZ_DF['USER EMAIL'] = QUIZ_DF['USER EMAIL'].str.strip().str.lower()
    QUIZ_DF['PASSED STATUS'] = QUIZ_DF['PASSED STATUS'].str.strip().str.lower()
    QUIZ_DF = QUIZ_DF[QUIZ_DF['PASSED STATUS'] == "yes"]
    QUIZ_DF = QUIZ_DF.drop_duplicates("USER EMAIL")
    passed_email = QUIZ_DF["USER EMAIL"]

    df.loc[df["Email Algoritma Online"].isin(passed_email.values), quizcode(quiz_input)] = max_score(quiz_input)
    df.loc[~df["Email Algoritma Online"].isin(passed_email.values), quizcode(quiz_input)] = 0

    try:
        service = build('sheets', 'v4', credentials=creds)
        
        values = [[x] for x in df[quizcode(quiz_input)].values.tolist()]

        body = {
            'values': values
        }
        result = service.spreadsheets().values().update(
            spreadsheetId=SCORE_ACADEMY_ID, range=f'{NAMA_SHEET}!{quiz_range(quiz_input)}',
            valueInputOption="USER_ENTERED", body=body).execute()
        print(f"{result.get('updatedCells')} cells updated.")

    except HttpError as error:
        print(f"An error occurred: {error}")

    return df

    # Use the `courses().courseWork().studentSubmissions().list()` method to store a list of the quiz's submissions

def ReturnClassroom(df, course_name, quiz_name, credentials): 
    
    # In this section, the user is going to choose which Google Classroom Course that is going to be accessed
    # Call the Google Classroom API to access various methods with user's access from the credential that has been authenticated
    creds = credentials
    service = build('classroom', 'v1', credentials=creds)

    # Use the `courses().list()` method to show a list of the user's courses

    results = service.courses().list(pageSize=20).execute()
    courses = results.get('courses', [])

    if not courses:
        print('No courses found.')

    course_input = course_name
    course_lowercase = course_input.lower()
    course_id = None

    for course in courses:
        if course_lowercase == course['name'].lower():
            course_id = course['id']
            break

    if course_id == None:
        raise Exception(f"{course_input} course not found")

    else:
        print(f'{course_input} found with ID {course_id}')

    service = build('classroom', 'v1', credentials=creds)
    response = service.courses().courseWork().list(courseId=course_id).execute()
    classworks = response.get('courseWork')

    while response.get('nextPageToken'):
        response = service.courses().students().list(courseId=course_id, pageToken = response['nextPageToken']).execute()
        classworks.extend(response.get('courseWork'))

    quiz_input = quiz_name
    quiz_id = None

    for classwork in classworks:
        if classwork['title'] == classcode(quiz_input):
            quiz_id = classwork['id']
            break

    if quiz_id == None:
        raise Exception(f"Quiz not found")
    else:
        print(f"{classwork['title']} Quiz was found")
    submissions = []

    service = build('classroom', 'v1', credentials=creds)
    response = service.courses().courseWork().studentSubmissions().list(
        courseId=course_id,
        courseWorkId=quiz_id).execute()
    submissions.extend(response.get('studentSubmissions', []))

    while response.get('nextPageToken'):
        response = service.courses().courseWork().studentSubmissions().list(
            courseId=course_id,
            courseWorkId=quiz_id,
            pageToken = response['nextPageToken']).execute()
        submissions.extend(response.get('studentSubmissions'))

    
    # All the stored submission are graded as draft in accordance with the student's e-mail in the Google Classroom using `courses().courseWork().studentSubmissions().patch()` method

    grade = []
    warn = []
    quiz_code = quizcode(quiz_input)

    for submission in submissions:
        try:
            # Retrieve student's email
            submission_profile = service.courses().students().get(courseId=course_id, userId=submission['userId']).execute()
            student_df = df.loc[df['Email Classroom'] == submission_profile['profile']['emailAddress'].lower()]
            
            # Retrieve student's grade
            if not student_df.empty:
                if isinstance(student_df[quiz_code].values[0], int) or student_df[quiz_code].values[0].isnumeric():
                    submission_grade = student_df[quiz_code].values[0]
                else:
                    warn.append(f"{submission_profile['profile']['name']['fullName']} ({submission_profile['profile']['emailAddress']}) has no grade")
                    grade.append([submission_profile['profile']['name']['fullName'], submission_profile['profile']['emailAddress'], None, "NO GRADE"])
                    continue      
            else:
                warn.append(f"{submission_profile['profile']['name']['fullName']} ({submission_profile['profile']['emailAddress']}) was not found")
                grade.append([submission_profile['profile']['name']['fullName'], submission_profile['profile']['emailAddress'], None, "NOT FOUND"])
                continue

            # Grade the submission as draftGrade
            studentSubmission = {
                'draftGrade': str(submission_grade),
                'assignedGrade': str(submission_grade)
            }
            
        
            response = service.courses().courseWork().studentSubmissions().patch(
                courseId=course_id,
                courseWorkId=classwork['id'],
                id=submission['id'],
                updateMask='assignedGrade,draftGrade',
                body = studentSubmission).execute()
        
            if submission['state'] == 'TURNED_IN':
                response = service.courses().courseWork().studentSubmissions().return_(
                    courseId=course_id,
                    courseWorkId=classwork['id'],
                    id=submission['id']).execute()
        except:
            continue
        
        grade.append([submission_profile['profile']['name']['fullName'], submission_profile['profile']['emailAddress'], submission_grade, "GRADED"])

    grade_df = pd.DataFrame(grade, columns=['Name', 'Email Classroom', 'Grade', 'Status'])
    grade_df.sort_values('Status')
    
    return grade_df, warn


