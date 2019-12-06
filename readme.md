# Cognito Export

This script will export the cognito user pool to a CSV file.  The CSV file can then be used to import the user pool to another instance of Congito.

# Requirements

## Python
This CLI is built with Python 3.7.  Install Python on your machine and install pip to get started

## PIP Requirements
The requirements.txt file can be used to setup your Python environment via pip.  Simply call pip install -r requirements.txt to install the pip requirements

## Install AWS CLI
To use this script, you'll need to install the AWS CLI on your machine.  Detailed instructions can be found here: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html

## Create an AWS Credentials File With Profile
You'll need to create an AWS credentials file with a profile entry for the account that you want to connect to.

Detailed information can be found here: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html

## Modify the settings.txt file located in src
You'll need to modify the settings.txt file located in the src folder to align with the profile you created in the previous step and the region in which the Cognito user pool that you want to export is located

# Usage
For up-to-date inline help documentation type the following:

'''python pooltool.py --help'''

## Export
Currently, the only supported action is a userpool export; type the following for help

'''python pooltool.py export userpool --help'''