
import boto3
import botocore
import csv

###IAM finding users ####
client1 = boto3.client('iam')
users = client1.list_users()
with open('IAM.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    for key in users['Users']:
        #print (key['UserName'])
        writer.writerow([key['UserName']])


###COgnito finding email #####
l=[]
V_UserPoolID='us-east-1_z4elHBR4L'
pagination_token = ""
client2 = boto3.client('cognito-idp')
while pagination_token is not None:
    if pagination_token:
        u = client2.list_users(UserPoolId=V_UserPoolID,Limit = 60,PaginationToken=pagination_token )
    else:
        u = client2.list_users(UserPoolId=V_UserPoolID,Limit = 60)
    #print(u['PaginationToken'])
    for d in u.values():
        #print(d)
        for i in d:
            #print(i.get('Username'))
            if isinstance(i, dict):
                #print(i)
                d=i.get('Username')
                #print(d)
                l.append(d)     
    if "PaginationToken" in u:
        pagination_token = u['PaginationToken']
    else:
        pagination_token = None
with open('cognito.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    for i in l:
        writer.writerow([i])
    f.close()           


##APPstream finding email ####
j=[]
pagination_token = ""
client2 = boto3.client('appstream')
while pagination_token is not None:
    if pagination_token:
        u = client2.describe_users(AuthenticationType='USERPOOL',limit=60,NextToken=pagination_token)
    else:
        u = client2.describe_users(AuthenticationType='USERPOOL')        
    for d in u.values():
        #print(d)
        for i in d:
            if isinstance(i, dict):
                #print(i)
                d=i.get('UserName')
                #print(d)
                j.append(d)
    if "PaginationToken" in u:
        pagination_token = u['PaginationToken']
    else:
        pagination_token = None            
with open('appstream.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    for i in j:
        writer.writerow([i])
    f.close() 