#!/usr/bin/env /usr/bin/python

import logging
import json
import subprocess


def get_aws_route_table_subnets(route_table_id):
    pass

def get_aws_route_table(subnet_id, vpc_id):
    pass

def get_ip_for_instance_name(instance_name):
    ''' return IP for specific instance '''

    instances = get_instances()
    for instance in instances:
        for tag in instance['Tags']:
            if tag['Key'] == "Name":
                if tag['Value'] == instance_name:
                    return instance['PublicIpAddress']

    return None

def get_instance_names():
    ''' return list of names of all the instances '''

    try:
        res = subprocess.check_output(["aws", "ec2", "describe-instances", "--query", "Reservations[].Instances[].Tags[?Key=='Name'].Value[]"])
        instance_names = json.loads(res)

    except subprocess.CalledProcessError as e:
        logging.error(e)
        logging.error("Check AWS credentials are set")
        return None

    return instance_names

def get_instances():
    ''' return dict with instance details '''
    try:
        res = subprocess.check_output(["aws", "ec2", "describe-instances", "--query", "Reservations[].Instances[]"])
        instances = json.loads(res)

    except subprocess.CalledProcessError as e:
        logging.error(e)
        logging.error("Check AWS credentials are set")
        return None

    return instances


if __name__ == "__main__":
    #inst = get_instances()
    #print inst
