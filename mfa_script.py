# Script to generate token for MFA login AWS.

"""
Note: In your .aws folder, in the 'credentials' file,
this must already exist. You can use 'aws configure' to set these

[default]
aws_access_key_id = ABCDST6TH4N4WBSOMEG
aws_secret_access_key = wPJLoUDpIZVlkjgr+/ilXxbueV5asve2u75xSaSu
aws_mfa_device = arn:aws:iam::123212341234:mfa/yourmail@domain.com

"""
from pathlib import Path
import boto3

client = boto3.client('sts')

dev_id = 123432981234
username = 'yourmail@domain.com'

# Get your device ARN from:
# Login to AWS site, click on your photo and click on 'Security Credentials'
MFA_DEVICE_ARN=f"arn:aws:iam::{dev_id}:mfa/{username}"

path_to_aws_dir =  Path.home() / '.aws'
token_duration_in_seconds=21600

# Keep your authenticator ready for this step.
mfa_code = input('Enter MFA Code:')

def get_token_for_session():
    dict_params = {
        'DurationSeconds':token_duration_in_seconds,
        'SerialNumber':MFA_DEVICE_ARN,
        'TokenCode':mfa_code
        }
    token = client.get_session_token(**dict_params)
    print(token)

    # Write them to your aws credential file
    with open(path_to_aws_dir / 'credentials', 'a') as fop:
        fop.write('\n')
        fop.write('[mfa]' + '\n')
        fop.write(f"aws_access_key_id = {token['Credentials']['AccessKeyId']}" + '\n')
        fop.write(f"aws_secret_access_key = {token['Credentials']['SecretAccessKey']}" + '\n')
        fop.write(f"aws_session_token = {token['Credentials']['SessionToken']}" + '\n')
    return token

def create_session(token):
    session = boto3.Session(
        aws_access_key_id=token['Credentials']['AccessKeyId'],
        aws_secret_access_key=token['Credentials']['SecretAccessKey'],
        aws_session_token=token['Credentials']['SessionToken'],
        profile_name='mfa'
    )
    return session

def main():
    token = get_token_for_session()
    session = create_session(token)
    print(session)

if __name__ == '__main__':
    main()
