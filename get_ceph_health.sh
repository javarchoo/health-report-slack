#!/bin/bash

# Set Env
WORK_DIR=/opt/ceph-health
DATA_DIR=$WORK_DIR/data

# Get Ceph Status
for HOSTS in cicd dev stg prd
do ssh ceph-$HOSTS 'ceph -s' > $DATA_DIR/ceph-$HOSTS
done

# Get Status list
grep health -H -r $DATA_DIR | awk -F/ '{print $NF}' | awk '{print $1 "\t" $3}' > $WORK_DIR/cephstatuslist
#cat $WORK_DIR/cephstatuslist

python $WORK_DIR/post.py $1 $2
