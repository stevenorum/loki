#!/usr/bin/env python

from loki.ec2_utils import *

access_key = None # use .boto or instance metadata
secret_key = None # use .boto or instance metadata
ssh_key = None # already in EC2

#lokis_to_launch = 4 - len(get_regions_with_loki_instances(access_key,secret_key))

#empty_regions = get_regions_with_no_instances(access_key,secret_key)

#if len(empty_regions) >= lokis_to_launch:
#    for region in empty_regions[0:lokis_to_launch]:
#        print dir(ensure_keypair_exists(ssh_key,'loki',region,access_key,secret_key))
#        launch_loki(ssh_key,'loki',region, access_key, secret_key)
#else:
#    regions = get_regions_sorted_by_most_instances(access_key,secret_key)
#    for region in regions[0:lokis_to_launch]:
#        print dir(ensure_keypair_exists(ssh_key,'loki',region,access_key,secret_key))
#        launch_loki(ssh_key,'loki',region, access_key, secret_key)
#region='us-east-1'
#launch_loki(public_key=ssh_key,keyname='loki',region=region,access_key=access_key,secret_key=secret_key)
print get_unencoded_userdata()

#for region in get_all_regions():
#    print region
#    print "Instances: " + str(get_instance_count(region, access_key, secret_key))
#    print "Lokis: " + str(get_loki_count(region, access_key, secret_key))

