import boto3
import json
import ast
import botocore
import sys
import csv
import pandas as pd
import math
client = boto3.client('iam')
#users=["demo1"]
my_csv = pd.read_csv('delete.csv')
column = my_csv.user
users=column.values.tolist()

column = my_csv.useremail
usersemail=column.values.tolist()

###IAM user delete start ###
print(users)
for u in users:
    if pd.isnull(u) == False:
    print('\n')
        #deleteing access key from user
        try:
            access_keys = client.list_access_keys(UserName=u)
            if access_keys['AccessKeyMetadata'] :
                for key in access_keys.get("AccessKeyMetadata"):
                    v_AccessKeyId=key['AccessKeyId']
                    #print("use has {} accress key deleting  {} ..".format(u,v_AccessKeyId) )
                    client.delete_access_key(UserName=u,AccessKeyId=v_AccessKeyId)
            else:
                print("No access key Present for user {}".format(u) )
        except client.exceptions.NoSuchEntityException:
            print("No  access key Present for user {}".format(u) )
        except Exception as e:
            print(e)

        #delete login profile from user
        try:
            response = client.get_login_profile(UserName=u) 
            #print ("User {} has password profile. Deleting..".format(u))
            client.delete_login_profile(UserName=u)
        except client.exceptions.NoSuchEntityException:
            print("No login profile  for user {}".format(u) )
        except Exception as e:
            print(e)

        #detach managed policies from user
        try:
            if client.list_attached_user_policies(UserName=u).get("AttachedPolicies"):
                for policy in client.list_attached_user_policies(UserName=u).get("AttachedPolicies"):
                    #print ("User {} has managed policies Deleting..".format(u))
                    client.detach_user_policy(UserName = u, PolicyArn=policy.get("PolicyArn"))
            else:
                print("No manages policy attached for user {}".format(u))
        except client.exceptions.NoSuchEntityException:
            print("No  manage policy exist  for user {}".format(u) )
        except Exception as e:
            print(e)

        #remove group from user
        try:
            userGroups = client.list_groups_for_user(UserName=u)
            if  userGroups['Groups']:
                for groupName in userGroups['Groups']:
                    #print ("User {} has attached with group {} detaching..".format(u,groupName))
                    client.remove_user_from_group(GroupName=groupName['GroupName'], UserName=u)
            else:
                print("No group attached  for user {}".format(u) )
        except client.exceptions.NoSuchEntityException:
            print("No group attached  for user {}".format(u) )
        except Exception as e:
            print("No group attached  for user {}".format(u) )
            print(e)

        #delete user
        try:
            client.delete_user(UserName=u)
            print("deleting user {}..".format(u))
        except client.exceptions.NoSuchEntityException:
            print("No user exist  for user {}".format(u) )
        except Exception as e:
            print(e)
###IAM user delete End  ###


## Cognito Useremail delete start #####
print('\n\n')
print(usersemail)
uPoolID = sys.argv[1]
for u in usersemail:
    if pd.isnull(u) == False:
        try:
            client = boto3.client('cognito-idp')
            client.admin_delete_user(UserPoolId=uPoolID,Username=u)
            print("deleting user {} from userpool".format(u))
        except client.exceptions.UserNotFoundException:
            print("no user {}  exists in userPool".format(u))
        except Exception as e:
            print(e)
## Cognito Useremail delete end  #####
        
### APPstream user email delete start###        
        try:
            client = boto3.client('appstream')
            client.delete_user(AuthenticationType='USERPOOL',UserName=u)
            print("deleting user {} from AppStream".format(u))
        except client.exceptions.ResourceNotFoundException:
            print("no user {}  exists in AppStream".format(u))
        except Exception as e:
            print(e)
### APPstream user email delete end ###                    