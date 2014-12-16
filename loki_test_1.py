#!/usr/bin/env python

from creds.creds import *
from loki.ec2_utils import *

access_key = get_access_key()
secret_key = get_secret_key()
ssh_key = get_ssh_public_key()

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
region='us-east-1'
launch_loki(public_key=ssh_key,keyname='loki',region=region,access_key=access_key,secret_key=secret_key)


#for region in get_all_regions():
#    print region
#    print "Instances: " + str(get_instance_count(region, access_key, secret_key))
#    print "Lokis: " + str(get_loki_count(region, access_key, secret_key))

