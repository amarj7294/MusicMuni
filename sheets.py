import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd 
import json


def getSheet():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(r'<path>\Desktop\Project\Riyaz\client_secret.json',scope)
    client = gspread.authorize(creds)
    
    
    
    sh = client.open_by_key('1A3Ph6mfzKO-Aollw8zCx86-PwCoI-wMJVf5hTtEb3bs')
    
    
    Course = sh.worksheet("Course").get_all_values()[1:]
    Module = sh.worksheet("Module").get_all_values()[1:]
    Lesson = sh.worksheet("Lesson").get_all_values()[1:]
    Media = sh.worksheet("Media").get_all_values()[1:]
    
    
    
    dfCourse = pd.DataFrame(data = Course[1:] , columns = Course[0]) 
    dfCourse.drop([''],axis=1,inplace=True)
    dfCourse.replace('\n','', regex=True , inplace=True)
    dfModule = pd.DataFrame(data = Module[1:] , columns = Module[0]) 
    dfModule.replace('\n','', regex=True , inplace=True)
    dfLesson = pd.DataFrame(data = Lesson[1:] , columns = Lesson[0]) 
    dfLesson.replace('\n','', regex=True , inplace=True)
    dfMedia = pd.DataFrame(data = Media[1:] , columns = Media[0])
    dfMedia.replace('\n','', regex=True , inplace=True)
    
    return dfCourse,dfModule,dfLesson,dfMedia





def validator():
    validator=True
    modules_Course = dfCourse['modules'].str.split(',')
    modules_Module = list(dfModule['UID'])
    
    lesson_Module = dfModule['lessons'].str.split(',')
    lesson_Lesson = list(dfLesson['UID'])
    
    media_Lesson = dfLesson['medias'].str.split(',')
    media_Media = list(dfMedia['UID'])
    
    if modules_Course[0] == modules_Module:
        print("SUCCESS : MODULE parent/child check pass") 
    else:
        validator=False
        print("FAILED : MODULE parent/child check failed")
        
    if set([item for lesson in lesson_Module for item in lesson]) == set(lesson_Lesson):
        print("SUCCESS : LESSON parent/child check pass") 
    else:
        validator=False
        print("FAILED : LESSON parent/child check failed")
    
    
    if set([item for media in media_Lesson for item in media]) == set(media_Media):
        print("SUCCESS : MEDIA parent/child check pass") 
    else:
        validator=False
        print("FAILED : MEDIAS parent/child check failed")
    
    return validator


def mediaAppender(media):
    for m in dfMe:
        if (media == m['UID']):
            return m

def lessonAppender(lesson):
    for l in dfL:
        if (lesson == l['UID']):
            arrMedia=l['medias'].split(',')
            l['medias']=list(map(mediaAppender,arrMedia))
            return l






dfCourse,dfModule,dfLesson,dfMedia = getSheet()

dfC=json.loads(dfCourse.to_json(orient="records"))
dfM=json.loads(dfModule.to_json(orient="records"))
dfL=json.loads(dfLesson.to_json(orient="records"))
dfMe=json.loads(dfMedia.to_json(orient="records"))

validate = validator()

if validator:
    finalObj=dfC
    finalObj[0]["modules"]=dfM
    for module in finalObj[0]["modules"]:
        arrLessons=module['lessons'].split(',')
        module["lessons"]=list(map(lessonAppender,arrLessons))
    print(finalObj)
        
else:
    print("vadidation failed, hence existing without creating JSON object")

    


        
        
        
    
        
    

    
    
    




