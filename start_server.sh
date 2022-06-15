#!/bin/bash
cd /home/ec2-user
source environment/bin/activate
supervisorctl -c supervisord.conf