#!/usr/bin/env python
import base64, boto.ec2, sys, random, re, string

regions = ['ap-northeast-1','ap-southeast-1','ap-southeast-2','eu-central-1','eu-west-1','sa-east-1','us-east-1','us-west-1','us-west-2']

for region in regions:
    ec2_conn = boto.ec2.connect_to_region(region_name=region)
    instances = [reservation.instances[0] for reservation in ec2_conn.get_all_instances(filters={"instance-state-name": "running"}) + ec2_conn.get_all_instances(filters={"instance-state-name": "pending"})]
    loki_instances = [instance for instance in instances if 'loki' in (lambda userdata: base64.b64decode(userdata) if re.search('^[{0}]*$'.format(string.uppercase + string.lowercase + string.digits + '+/=='),userdata) else 'baldr')(base64.b64decode(instance.get_attribute('userData')['userData']))]
    if loki_instances:
        print region
        print loki_instances
        for instance in loki_instances:
            print "Killing " + str(instance)
            instance.terminate()
