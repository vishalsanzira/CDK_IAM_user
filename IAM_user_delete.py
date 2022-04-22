import boto3
import json
import ast
import botocore
import csv
import pandas as pd
client = boto3.client('iam')
#users=["demo1"]
my_csv = pd.read_csv('delete.csv')
column = my_csv.user
users=column.values.tolist()
print(users)
for u in users:

    #deleteing access key from user
    try:
        access_keys = client.list_access_keys(UserName=u)
        #print(f"{access_keys=}")
        if access_keys['AccessKeyMetadata'] :
            for key in access_keys.get("AccessKeyMetadata"):
                v_AccessKeyId=key['AccessKeyId']
                print("use has {} accress key deleting  {} ..".format(u,v_AccessKeyId) )
                client.delete_access_key(UserName=u,AccessKeyId=v_AccessKeyId)
        else:
            print("No access key Present for user {}".format(u) )
    except client.exceptions.NoSuchEntityException:
        print("No  access key Presnet for user {}".format(u) )
    except Exception as e:
        print(e)

    #delete login profile from user
    try:
        response = client.get_login_profile(UserName=u)
        #print(f"{response=}")
        print ("User {} has password profile. Deleting..".format(u))
        client.delete_login_profile(UserName=u)
    except client.exceptions.NoSuchEntityException:
        print("No login profile  for user {}".format(u) )
    except Exception as e:
        print(e)

    #detach managed policies from user
    try:
        #print("manage policy")
        if client.list_attached_user_policies(UserName=u).get("AttachedPolicies"):
            for policy in client.list_attached_user_policies(UserName=u).get("AttachedPolicies"):
                #print(f"{policy=}")
                print ("User {} has managed policies Deleting..".format(u))
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
                #print(groupName['GroupName'])
                print ("User {} has attached with group {} detaching..".format(u,groupName))
                client.remove_user_from_group(GroupName=groupName['GroupName'], UserName=u)
        else:
            print("No group attached  for user {}".format(u) )
    except client.exceptions.NoSuchEntityException:
        print("No group attached  for user {}".format(u) )
    except Exception as e:
        #print("No group attached  for user {}".format(u) )
        print(e)

    #delete user
    try:
        client.delete_user(UserName=u)
        print("deleting user {}..".format(u))
    except client.exceptions.NoSuchEntityException:
        print("No user exist  for user {}".format(u) )
    except Exception as e:
        print(e)