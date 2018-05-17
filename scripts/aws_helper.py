#!/usr/bin/env /usr/bin/python

import logging
import json
import subprocess

def get_aws_route_table_subnets(route_table_id):
    ''' returns list of subnets in use '''
    try:
        res = subprocess.check_output(["aws", "ec2", "describe-route-tables", "--route-table-ids", route_table_id])
    except subprocess.CalledProcessError as e:
        logging.error(e)
        logging.error("Check AWS credentials are set")
        return None

    try:
        rt_table = json.loads(res)
    except ValueError as e:
        logging.error(e)
        logging.error("Error loading json output")
        return None

    routes = rt_table["Routetable"][0]["Routes"]
    return routes

def get_aws_route_table(subnet_id, vpc_id):
    ''' return dict of route_table_id '''

    try:
        res = subprocess.check_output(["aws", "ec2", "describe-route-tables", "--filters", "Name=association.subnet-id,Values={}".format(subnet_id)])
        if not json.loads(res)['RouteTables']:
            route_tables = subprocess.check_output(["aws", "ec2", "describe-route-tables", "--filters", 'Name=vpc-id,Values={}'.format(vpc_id), 'Name=association.main, Values=true'])

    except subprocess.CalledProcessError as e:
        logging.error(e)
        logging.error("Check AWS credentials are set")
        return None

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
