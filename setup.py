import boto3
import logging
from botocore.exceptions import ClientError
import os
import glob

logging.getLogger().setLevel(logging.INFO)
cloudformation_client = boto3.client('cloudformation')


def create_stack(stack_name, template_body, **kwargs):
    cloudformation_client.create_stack(
        StackName=stack_name,
        TemplateBody=template_body,
        Capabilities=['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM'],
        TimeoutInMinutes=30,
        OnFailure='ROLLBACK'
    )

    cloudformation_client.get_waiter('stack_create_complete').wait(
        StackName=stack_name,
        WaiterConfig={'Delay': 30, 'MaxAttempts': 120}
    )

    cloudformation_client.get_waiter('stack_exists').wait(StackName=stack_name)
    logging.info(f'CREATE COMPLETE')


def update_stack(stack_name, template_body, **kwargs):
    try:
        cloudformation_client.update_stack(
            StackName=stack_name,
            Capabilities=['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM'],
            TemplateBody=template_body
        )

    except ClientError as e:
        if 'No updates are to be performed' in str(e):
            logging.info(f'SKIPPING UPDATE: No updates to be performed at stack {stack_name}')
            return e

    cloudformation_client.get_waiter('stack_update_complete').wait(
        StackName=stack_name,
        WaiterConfig={'Delay': 30, 'MaxAttempts': 120}
    )

    cloudformation_client.get_waiter('stack_exists').wait(StackName=stack_name)
    logging.info(f'UPDATE COMPLETE')


def get_existing_stacks():
    response = cloudformation_client.list_stacks(
        StackStatusFilter=['CREATE_COMPLETE', 'UPDATE_COMPLETE', 'UPDATE_ROLLBACK_COMPLETE']
    )

    return [stack['StackName'] for stack in response['StackSummaries']]


def _get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)


def create_or_update_stack():
    # stack_name = 's3-bucket-ci'
    stacks = [
        # {
        #     "file_name": '1.networking.yml',
        #     "stack_name": 'networking'
        # },
        {
            "file_name": '1.networking.yml',
            "stack_name": 'networking'
        },
        {
            "file_name": '2.data_lake.yml',
            "stack_name": 'data-lake'
        },
        {
            "file_name": '3.load_data.yml',
            "stack_name": 'load-data'
        },
        {
            "file_name": '4.rds.yml',
            "stack_name": 'rds'
        },
        {
            "file_name": '5.dms.yml',
            "stack_name": 'dms'
        },
        {
            "file_name": '6.redshift.yml',
            "stack_name": 'redshift'
        },
        {
            "file_name": '7.emr.yml',
            "stack_name": 'emr'
        }
    ]

    for stack in stacks:
        with open(_get_abs_path(stack['file_name'])) as f:
            template_body = f.read()

        existing_stacks = get_existing_stacks()

        if stack['stack_name'] in existing_stacks:
            logging.info(f'UPDATING STACK {stack["stack_name"]}')
            update_stack(stack["file_name"], template_body)
        else:
            logging.info(f'CREATING STACK {stack["stack_name"]}')
            create_stack(stack['stack_name'], template_body)


if __name__ == '__main__':
    create_or_update_stack()
