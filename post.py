#!/usr/bin/env python
"""Post slack message."""

# https://github.com/os/slacker
# https://api.slack.com/methods

import os
import sys
from slacker import Slacker


def post_slack():
    """Post slack message."""
    try:

        token=sys.argv[2]
        slack = Slacker(token)

        work_dir="/opt/ceph-health"
        data_dir=work_dir+"/data"

        dic = {}
        sr = {}

        lines = open(work_dir+"/cephstatuslist", "r").readlines()
        for line in lines:
            site = line.split('\t')[0].replace(":", "")
            result = line.split('\t')[1].replace("\n","")

            dic[site] = result

            if result in sr:
                sr[result] = sr[result] + ", " + site
            else:
                sr[result] = site

        body = ""
        if len(sr.keys()) == 1 and "HEALTH_OK" in sr.keys():
            body += ""
        else:
            body += "*_# Ceph Health Check Detail_*\n"
            files = ["cicd", "dev", "stg", "prd"]
            for f in files:
                if 'HEALTH_OK' != dic["ceph-"+f]:
                    f_name = data_dir + "/ceph-" + f
                    tf = open(f_name,"r")
                    body += ">*ceph-" + f + "*\n"
                    body += ">```\n"
                    body += tf.read()
                    body += "```\n\n"

        body += "*_# Ceph Health Check Simple_*\n"
        body += ">```\n"
        for k in ["OK", "WARN", "ERROR"]:
            if "HEALTH_"+k in sr.keys():
               body += ((k + ":").ljust(8) + sr["HEALTH_"+k]+"\n")
        body+="```"

        channel = "#" + sys.argv[1]
        obj = slack.chat.post_message(channel, body)
#        print(obj.successful, obj.__dict__['body']['channel'], obj.__dict__[
#            'body']['ts'])
    except KeyError as ex:
        print('Environment variable %s not set.' % str(ex))

if __name__ == '__main__':
    post_slack()
