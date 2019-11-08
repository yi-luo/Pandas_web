import json
import pandas as pd
import boto3 as bt3
import re

status_check = [0]*10    
def lambda_handler(event, context):
    
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
        
        # Evaluating User Inputs
        user_list = userSolution.splitlines()
        user_list = [x for x in user_list if not x.startswith('#')]
        for i in user_list:
            original_df = pd.eval(i)
            
        print("THIS IS STRING", original_df)
        
        if isinstance(original_df, str):
            userHtmlFeedback = original_df
        elif isinstance(original_df, pd.core.series.Series):
           original_df = original_df.to_frame()
           userHtmlFeedback = original_df.to_html()
        else:
            userHtmlFeedback = original_df.to_html()
        
        right_answer_text = "temp"
        isComplete = 0
        
        
        if questionName == 'Selecting Rows':#Q1
            right_answer = default_df.iloc[[1,4,9]]
            right_answer_text = 'original_df.iloc[[1,4,9]]'
            if(right_answer.equals(original_df)):
                status_check[0]=1
                isComplete = 1
        elif questionName == 'Selecting Columns':#Q2
            right_answer = default_df[['ID','NAME','RESIDENCE']]
            right_answer_text = 'original_df[[\'ID\',\'NAME\',\'RESIDENCE\']]'
            if(right_answer.equals(original_df)):
                status_check[1]=1
                isComplete = 1
        elif questionName == 'Selecting Specific Cells':#Q3
            right_answer = default_df.iloc[8]['NAME']
            right_answer_text = 'original_df.iloc[8][\'NAME\']'
            if(right_answer==(original_df)):
                status_check[2]=1
                isComplete = 1
        elif questionName == 'Replacing String Occurrences':#Q4
            right_answer = default_df.replace("USA","United States")
            right_answer_text = 'original_df.replace("USA","United States")'
            if(right_answer.equals(original_df)):
                status_check[3]=1
                isComplete = 1
        elif questionName == 'Filtering Data in Columns':#Q5
            right_answer = default_df[original_df['CHILDREN']=='Yes']
            right_answer_text = 'original_df[original_df[\'CHILDREN\']==\'Yes\']'
            if(right_answer.equals(original_df)):
                status_check[4]=1
                isComplete = 1
        elif questionName == 'Filtering Data based on Multiple Conditions':#Q6
            right_answer = default_df[(original_df['CHILDREN']=='Yes')|(original_df['RESIDENCE']=='China')]
            right_answer_text = 'original_df[(original_df[\'CHILDREN\']==\'Yes\')|(original_df[\'RESIDENCE\']==\'China\')]'
            if(right_answer.equals(original_df)):
                status_check[5]=1
                isComplete = 1
        elif questionName == 'Adding Rows':#Q7
            right_answer = default_df.append(pd.Series([11,'Tao Tao', 'M', 20, 'Yes', 'Singapore'], index=original_df.columns), ignore_index=True)
            right_answer_text = 'original_df.append(pd.Series([11,\'Tao Tao\', \'M\', 20, \'Yes\', \'Singapore\'], index=original_df.columns), ignore_index=True)'
            if(right_answer.equals(original_df)):
                status_check[6]=1
                isComplete = 1
        elif questionName == 'Deleting Rows':#Q8
            right_answer = default_df.drop(original_df.index[[4,9]])
            right_answer_text = 'original_df.drop(original_df.index[[4,9]])'
            if(right_answer.equals(original_df)):
                status_check[7]=1
                isComplete = 1
        elif questionName == 'Finding Min and Max':#Q9
            right_answer = default_df['NAME'].min()
            right_answer_text = 'original_df[\'NAME\'].min()'
            if(right_answer.equals(original_df)):
                status_check[8]=1
                isComplete = 1
        elif questionName == 'Multiplying and Dividing Column Values':#Q10
            right_answer = 10*default_df.iloc[:,3]
            right_answer_text = '10*original_df.iloc[:,3]'
            if(right_answer.equals(original_df)):
                status_check[9]=1
                isComplete = 1
        
        progress = status_check.count(1)
        print(status_check)
        print(progress)
        return {
            "statusCode": 200,
            "headers": {
            "Content-Type": "application/json",
                },
            "body":  json.dumps({
                "isComplete":isComplete,
                "pythonFeedback": "Hello",
                "htmlFeedback": userHtmlFeedback,
                "textFeedback": right_answer_text,
                "progress": progress,
                "questionStatus":status_check
            })
        }
