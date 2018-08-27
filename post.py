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

        work_dir="/root/ceph-health"
        data_dir="/root/ceph-health/data"


        dic = {}
        lines = open("/root/ceph-health/cephstatuslist", "r").readlines()
        for line in lines:
            dic[line.split('\t')[0].replace(":", "")] = line.split('\t')[1].replace("\n","")

        body = "#" * 30 + "\n# Ceph Health Check Detail\n" + "#" * 30 + "\n"
        files = ["cicd", "dev", "stg", "prd"]
        for f in files:
            if 'HEALTH_OK' != dic["ceph-"+f]:
                f_name = data_dir + "/ceph-" + f
                tf = open(f_name,"r")
                body+="ceph-" + f + "\n"
                body+="```\n"
                body+=tf.read()
                body+="```\n\n"

        body += "#" * 30 + "\n# Ceph Health Check Simple\n" + "#" * 30 + "\n"
        body+="```\n"
        f_name = work_dir + "/cephstatuslist"
        body += open(f_name, "r").read()
        body+="```"

        channel = "#" + sys.argv[1]
        obj = slack.chat.post_message(channel, body)
#        print(obj.successful, obj.__dict__['body']['channel'], obj.__dict__[
#            'body']['ts'])
    except KeyError as ex:
        print('Environment variable %s not set.' % str(ex))

if __name__ == '__main__':
    post_slack()
