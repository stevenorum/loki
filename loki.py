#!/usr/bin/env python
import base64, boto.ec2, sys

def get_boto_key(key):
    return [line.split('=')[1] for line in open('/etc/boto.cfg', 'r').read().split('\n') if line.startswith(key)][0]

def get_all_region_info():
    return [{'Name':'ap-northeast-1','ami':'ami-2385b022'},{'Name':'ap-southeast-1','ami':'ami-ba5c7ae8'},{'Name':'ap-southeast-2','ami':'ami-71f7954b'},{'Name':'eu-central-1','ami':'ami-a03503bd'},{'Name':'eu-west-1','ami':'ami-9c7ad8eb'},{'Name':'sa-east-1','ami':'ami-9137828c'},{'Name':'us-east-1','ami':'ami-246ed34c'},{'Name':'us-west-1','ami':'ami-9b6e64de'},{'Name':'us-west-2','ami':'ami-55a7ea65'}]

def get_ec2_conn(region='us-east-1',access_key=None,secret_key=None):
    return boto.ec2.connect_to_region(region_name=region,aws_access_key_id=access_key,aws_secret_access_key=secret_key)

def get_all_regions():
    return [region['Name'] for region in get_all_region_info()]

def get_all_instances(region='us-east-1',access_key=None,secret_key=None):
    return [reservation.instances[0] for reservation in get_ec2_conn(region,access_key,secret_key).get_all_instances(filters={"instance-state-name": "running"})]

def is_loki_instance(instance):
    return instance.tags.get('type', 'baldr') == 'loki' # Eventually this will be much more complex, but for now, let's be simple.

def get_instance_count(region='us-east-1',access_key=None,secret_key=None):
    return len(get_all_instances(region,access_key,secret_key))

def get_instance_count(region='us-east-1',access_key=None,secret_key=None):
    return len(get_all_instances(region,access_key,secret_key))

def get_loki_count(region='us-east-1',access_key=None,secret_key=None):
    return len([instance for instance in get_all_instances(region,access_key,secret_key) if is_loki_instance(instance)])

def get_regions_with_no_instances(access_key=None,secret_key=None):
    return [region for region in get_all_regions() if len(get_all_instances(region,access_key,secret_key)) == 0]

def get_regions_with_no_non_loki_instances(access_key=None,secret_key=None):
    return [region for region in get_all_regions() if get_instance_count(region,access_key,secret_key) - get_loki_count(region,access_key,secret_key) == 0]

def get_regions_with_loki_instances(access_key=None,secret_key=None):
    return [region for region in get_all_regions() if get_loki_count(region,access_key,secret_key) > 0]

def get_regions_sorted_by_most_instances(access_key=None,secret_key=None):
    return [region['Region'] for region in sorted([{'Region':region,'count':get_instance_count(region,access_key,secret_key)} for region in get_all_regions()], key=lambda k: k['count'], reverse=True)]



get_region_info_with_all_instances = lambda access_key=None,secret_key=None: {region['Name']:(lambda instances:{'ami':region['ami'],'instances':instances,'loki_count':len([instance for instance in instances if instance.tags.get('type', 'baldr') == 'loki'])})([reservation.instances[0] for reservation in get_ec2_conn(region['Name'],access_key,secret_key).get_all_instances(filters={"instance-state-name": "running"})]) for region in [{'Name':'ap-northeast-1','ami':'ami-2385b022'},{'Name':'ap-southeast-1','ami':'ami-ba5c7ae8'},{'Name':'ap-southeast-2','ami':'ami-71f7954b'},{'Name':'eu-central-1','ami':'ami-a03503bd'},{'Name':'eu-west-1','ami':'ami-9c7ad8eb'},{'Name':'sa-east-1','ami':'ami-9137828c'},{'Name':'us-east-1','ami':'ami-246ed34c'},{'Name':'us-west-1','ami':'ami-9b6e64de'},{'Name':'us-west-2','ami':'ami-55a7ea65'}]}

#[reservation.instances[0] for reservation in get_ec2_conn(region['Name'],access_key,secret_key).get_all_instances(filters={"instance-state-name": "running"})]

#empty_regions = [region for region in all_region_info.keys() if len(all_region_info[region]['instances']) == 0]
#sorted_regions = [region for region in sorted(all_region_info.keys(), key=lambda k: len(all_region_info[k]['instances']), reverse=True)]
#okis_to_launch = 4-len([region for region in all_region_info.keys() if all_region_info[region]['loki_count'] > 0])


# need to embed get_region_info_with_all_instances and the above three comprehensions into the below

launch_necessary_lokis = lambda: (lambda launch_loki: (lambda access_key, secret_key, ssh_key:(lambda lokis_to_launch,empty_regions,sorted_regions: [launch_loki(ssh_key,'loki',region, access_key, secret_key) for region in empty_regions[0:lokis_to_launch] if lokis_to_launch>0] if len(empty_regions) >= lokis_to_launch else [launch_loki(ssh_key,'loki',region, access_key, secret_key) for region in sorted_regions[0:lokis_to_launch] if lokis_to_launch>0])(lokis_to_launch = 2 - len(get_regions_with_loki_instances(access_key,secret_key)), empty_regions = get_regions_with_no_instances(access_key,secret_key), sorted_regions = get_regions_sorted_by_most_instances(access_key,secret_key)))(access_key=get_boto_key('aws_access_key_id'),secret_key=get_boto_key('aws_secret_access_key'),ssh_key='ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDe5LgFk3lB5LTwNL6AZ1NRRd6lpdrnJ8lCknPAJ+i485E2XsEMxEaPdod+63Q9CG7Hum0aU/8NK44dFn1T0J8hAscIzboSlGbElLrNQ6Vue+hQxrp6lNx4pYDwGFDfgksRvTuHxX0UqrI0yI9RevXgFAgYmyMNGjjAK0mrefDwzs34f2R+JNz8mB+ngMAXuq+ciZeh61LEswdBNfJ1jVVy38W+zU4FQLRIHQBDuMYYVOvo3j4b6OKgnXElN68JO36UJspoqPXOwfy06ZuZDVryi2kJn1gjq6c/+1gn35plOzuTEE0EC5/5dyRy1GqBjhGmFNRdDfx84B4rTwO8dsV1'))(lambda public_key,keyname='loki',region='us-east-1',access_key=None,secret_key=None:(lambda reservation: reservation.instances[0].add_tag('type','loki'))(get_ec2_conn(region,access_key,secret_key).run_instances(image_id=[_region['ami'] for _region in get_all_region_info() if _region['Name'] == region][0], key_name=(lambda public_key,keyname='loki',region='us-east-1',access_key=None,secret_key=None:(lambda conn: conn.get_key_pair(keyname) if conn.get_key_pair(keyname) else conn.import_key_pair(key_name=keyname, public_key_material=public_key))(get_ec2_conn(region,access_key,secret_key)))(public_key,'loki',region,access_key,secret_key).name, user_data=base64.b64encode("#!/bin/bash\ntouch /var/log/loki.log\nyum update -y\nyum install emacs -y\necho \"{0}\" | base64 --decode > /etc/boto.cfg\nmkdir -p /home/ec2-user/loki\nyum install python27 -y\nrm /usr/bin/python\nln -s /usr/bin/python2.7 /usr/bin/python\ncp /usr/bin/yum /usr/bin/_yum_before_27\nsed -i s/python/python2.6/g /usr/bin/yum\nsed -i s/python2.6/python2.6/g /usr/bin/yum\ncurl https://bootstrap.pypa.io/ez_setup.py > /tmp/ez_setup.py\n/usr/bin/python2.7 /tmp/ez_setup.py &> /home/ec2-user/install-easy-install.log\nrm /tmp/ez_setup.py\neasy_install-2.7 pip &> /home/ec2-user/install-pip.log\npip install boto --upgrade &> /home/ec2-user/pip-install-boto.log\necho \"{1}\" | base64 --decode > /home/ec2-user/loki/loki.py\nchmod +x /home/ec2-user/loki/loki.py\necho \"* * * * * root /home/ec2-user/loki/loki.py >> /var/log/loki.log 2>&1\" > /etc/cron.d/loki".format(base64.b64encode('[Credentials]\naws_access_key_id={0}\naws_secret_access_key={1}'.format(access_key,secret_key)),base64.b64encode(open('/home/ec2-user/loki/loki.py', 'r').read()))), instance_type='t1.micro', disable_api_termination=True, dry_run=False)))

check_for_orders = lambda: sys.stdout.write("Checking for orders from the master...\n") # just a placeholder right now

# Currently it won't self-replicate because I've commented out the cron job that runs the script.
# However, it should spin up the new instances.

# I'll put in the ssh_key when I get to the computer that has it but it'll work for now because it's already loaded into my EC2 account in the regions this is trying to launch in.

#check_for_orders()
#launch_necessary_lokis()

# Next steps: Find a better way to identify loki instances, have it perform some sort of check in the startup script to get orders from elsewhere, have it crawl github for new creds to launch with, and have it install a shutdown script that re-launches itself when the instance dies
