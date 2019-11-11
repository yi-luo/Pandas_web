# http://alanwsmith.com/capturing-python-log-output-in-a-variable

import json
import pandas as pd
import boto3 as bt3
import re
import os
import logging
import io

logger = logging.getLogger('basic_logger')
logger.setLevel(logging.DEBUG)

status_check = [0]*10  

def lambda_handler(event, context):
    
    ### Setup the console handler with a StringIO object
    log_capture_string = io.StringIO()
    ch = logging.StreamHandler(log_capture_string)
    ch.setLevel(logging.DEBUG)
    
    ### Optionally add a formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    
    ### Add the console handler to the logger
    logger.addHandler(ch)
    
    def runCode(myDF, myCode):
        namespace = {'original_df': myDF, 'expected_output': ''}
        exec('import pandas as pd', namespace)
        exec(myCode, namespace)
        return namespace['expected_output']
    
    s3 = bt3.client('s3')
    method = event.get('httpMethod',{}) 
    
    with open('index.html', 'r') as f:
        indexPage = f.read()
    
    
    if method == 'GET':
        return {
            "statusCode": 200,
            "headers": {
            'Content-Type': 'text/html',
            },
            "body": indexPage
        }
        
    if method == 'POST':
        bodyContent = event.get('body',{}) 
        parsedBodyContent = json.loads(bodyContent)
        testCases = re.sub('&zwnj;.*&zwnj;','',parsedBodyContent["shown"]["0"], flags=re.DOTALL) 
        userSolution = parsedBodyContent["editable"]["0"] 
        questionName = parsedBodyContent["qname"]["0"]
        
        # Reading the original dataframe from S3 
        original_df = pd.read_csv('https://frame-pandas.s3.amazonaws.com/pandas_data.csv')
        default_df = original_df.copy()
        expected_output = ""
        
        errorStatus = False
        # Evaluating User Inputs
        try:
            expected_output = runCode(original_df, userSolution)
        except:
            errorStatus = True
            logger.exception('Debug Message')
            
        print("Hello World", expected_output)
        
        if not errorStatus:
            if isinstance(expected_output , str):
                userHtmlFeedback = expected_output 
            elif isinstance(expected_output, pd.core.series.Series):
                expected_output = expected_output.to_frame()
                userHtmlFeedback = expected_output.to_html()
            else:
                userHtmlFeedback = expected_output.to_html()
        else:
            userHtmlFeedback = "Error - Please Look at Python Logs"
        
        right_answer_text = "temp"
        isComplete = 0
        
        if questionName == 'Selecting Rows': #Q1
            right_answer = default_df.iloc[[1,4,9]]
            right_answer_text = 'expected_output.iloc[[1,4,9]]'
            if(right_answer.equals(expected_output)):
                status_check[0]=1
                isComplete = 1
        elif questionName == 'Selecting Columns':#Q2
            right_answer = default_df[['ID','NAME','RESIDENCE']]
            right_answer_text = 'expected_output[[\'ID\',\'NAME\',\'RESIDENCE\']]'
            if(right_answer.equals(expected_output)):
                status_check[1]=1
                isComplete = 1
        elif questionName == 'Selecting Specific Cells':#Q3
            right_answer = default_df.iloc[8]['NAME']
            right_answer_text = 'expected_output.iloc[8][\'NAME\']'
            if(right_answer==(expected_output)):
                status_check[2]=1
                isComplete = 1
        elif questionName == 'Replacing String Occurrences':#Q4
            right_answer = default_df.replace(["F","M"],["Female","Male"])
            right_answer_text = 'expected_output.replace("USA","United States")'
            if(right_answer.equals(expected_output)):
                status_check[3]=1
                isComplete = 1
        elif questionName == 'Filtering Data in Columns':#Q5
            right_answer = default_df[default_df['CHILDREN']=='Yes']
            right_answer_text = 'expected_output[original_df[\'CHILDREN\']==\'Yes\']'
            if(right_answer.equals(expected_output)):
                status_check[4]=1
                isComplete = 1
        elif questionName == 'Filtering Data based on Multiple Conditions':#Q6
            right_answer = default_df[(default_df['RESIDENCE']=='China')|(default_df['AGE']>15)]
            right_answer_text = 'expected_output[(original_df[\'RESIDENCE\']==\'China\')|(original_df[\'AGE\']>\'15\')]'
            if(right_answer.equals(expected_output)):
                status_check[5]=1
                isComplete = 1
        elif questionName == 'Adding Rows':#Q7
            right_answer = default_df.append(pd.Series([11,'Tao Tao', 'M', 20, 'Yes', 'Singapore'], index=original_df.columns), ignore_index=True)
            right_answer_text = 'expected_output.append(pd.Series([11,\'Tao Tao\', \'M\', 20, \'Yes\', \'Singapore\'], index=original_df.columns), ignore_index=True)'
            if(right_answer.equals(expected_output)):
                status_check[6]=1
                isComplete = 1
        elif questionName == 'Deleting Rows':#Q8
            right_answer = default_df.drop(original_df.index[[4,9]])
            right_answer_text = 'expected_output.drop(original_df.index[[4,9]])'
            if(right_answer.equals(expected_output)):
                status_check[7]=1
                isComplete = 1
        elif questionName == 'Finding Min and Max':#Q9
            right_answer = default_df['NAME'].min()
            right_answer_text = 'expected_output[\'NAME\'].min()'
            if(right_answer.equals(expected_output)):
                status_check[8]=1
                isComplete = 1
        elif questionName == 'Multiplying and Dividing Column Values':#Q10
            right_answer = 10*default_df.iloc[:,3]
            right_answer_text = '10*expected_output.iloc[:,3]'
            if(right_answer.equals(expected_output)):
                status_check[9]=1
                isComplete = 1
        
        theMessage = ''
        if isComplete:
            theMessage = "Yay! You got it right!"
        else:
            theMessage = "Incorrect. Please try again."
        
        progress = status_check.count(1)
        print("Status Check", status_check)
        print("Progress", progress)
        
        ### Pull the contents back into a string and close the stream
        log_contents = log_capture_string.getvalue()
        log_capture_string.close()
        
        return {
            "statusCode": 200,
            "headers": {
            "Content-Type": "application/json",
                },
            "body":  json.dumps({
                "isComplete":isComplete,
                "pythonFeedback": log_contents.lower(),
                "htmlFeedback": theMessage + "\n\n" + userHtmlFeedback,
                "textFeedback": right_answer_text,
                "progress": progress,
                "questionStatus":status_check
            })
        }
