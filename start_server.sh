#!/bin/bash
cd /home/ec2-user
source environment/bin/activate
supervisord supervisord.conf