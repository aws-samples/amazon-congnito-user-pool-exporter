# Pooltool.py: Cognito User Pool Exporter

This script that leverages the AWS Boto API to export a cognito user pool to a CSV file.  The CSV file can then be used to re-hydrate another Cognito user pool with users.

## What do I do with a user pool csv file?

You can use this csv file as a way to backup your user pool and restore it into recovered user pool or into a user pool in another account or region.

Details on how to import users from a csv to a user pool can be found in the AWS developer guide under [Cognito User Pools Using Import Tool](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-using-import-tool.html)

# Requirements

## Python
This CLI is built with Python 3.7.  Install Python on your machine and install pip to get started.

## PIP Requirements
The requirements.txt file can be used to setup your Python environment via pip.  Simply call pip install -r requirements.txt to install the required modules.

## Install AWS CLI
To use this script, you'll need to install the AWS CLI on your machine.  Detailed instructions can be found here: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html

## Create an AWS Credentials File With Profile
You'll need to create an AWS credentials file with a profile entry for the account that you want to connect to.

Detailed information can be found here: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html

## [Optional] Modify the settings.txt file located in src
If you do not wish to provide profile and region information as arguments to the Pooltool, you can save them to a settings.txt file.

Modify the settings.txt file located in the src folder to align with the profile you created in the previous step and the region in which the Cognito user pool that you want to export is located.

# Usage
For up-to-date inline help documentation type the following:

```python pooltool.py --help```

## Export
Currently, the only supported action is a userpool export.

```
usage: pooltool.py export userpool [-h] --file FILE --id ID [--verbose]
                                   [--format FORMAT] [--region REGION]
                                   [--profile PROFILE]

optional arguments:
  -h, --help         show this help message and exit
  --file FILE        [Required] output file path
  --id ID            [Required] userpool id
  --verbose          display json output of user pool
  --format FORMAT    output file type [json or csv]; defaults to csv
  --region REGION    region name; overrides value from settings.txt
  --profile PROFILE  aws profile name; overrides value from settings.txt
  ```

For example, the command to export a user pool with id ```us-west-2_Qiq9DIvhR``` in ```us-west-2``` connecting via profile ```test_account```, would look like this:

```python pooltool.py export userpool --file backup.csv --id us-west-2_Qiq9DIvhR --region us-west-2 --profile test_account```