Assumption:
===========
AWS account
AWS CLI package is installed and configured with ACCESS_KEY and SECRET_KEY
Permission to create S3 buckets, S3 objects, user roles, policies

Steps:
=========
Convert your iso to ova with required packages, number of interfaces, root access enabled

Upload the ova file to S3 bucket

Git clone this repo

Edit role-policy.json file, to change the bucketname

Edit image.json file, to correct bucketname and ova file name

aws iam create-role --role-name vmimport --assume-role-policy-document file://trust-policy.json

aws iam put-role-policy --role-name vmimport --policy-name vmimport --policy-document file://role-policy.json

aws ec2 import-image --cli-input-json file://image.json

Watch the progress by running the below command:

aws ec2 describe-import-image-tasks
