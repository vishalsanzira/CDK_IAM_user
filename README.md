# CDK_IAM_user

User And Email finding Script From IAM, Cognito, Appstream(find_IAM_user_cognito_appstream_username_new.py)

•	Change Your AWS account Profile where you want to run the script.
o	setx aws_profile profilename
•	your current AWS account Profile using command 
AWS configure list 
•	Change Cognito User PoolID (variable V_UserPoolID) as per AWS profile.
•	Run Python Script and that will create three Individual CSV file for IAM, Cognito, Appstream.


Now need to merge these three files in to single csv file(filter the Record that we want to delete)  and run below steps for that.


Deleting Account using IAM user and Cognito, Appstream Email.
(Final_combine_script_delete_user.py)
•	Check your file name that should be delete and format should be in CSV.
•	IAM user column header should be user and Appstream and Cognito Email column header should be useremail.
•	Run Python Script that will take Cognito UserpoolID as argument and will print all deleted user console on cmd.




