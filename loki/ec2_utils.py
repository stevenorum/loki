import boto.ec2


def get_all_region_info():
    return [{'Name':'ap-northeast-1','ami':'ami-2385b022'},{'Name':'ap-southeast-1','ami':'ami-ba5c7ae8'},{'Name':'ap-southeast-2','ami':'ami-71f7954b'},{'Name':'eu-central-1','ami':'ami-a03503bd'},{'Name':'eu-west-1','ami':'ami-9c7ad8eb'},{'Name':'sa-east-1','ami':'ami-9137828c'},{'Name':'us-east-1','ami':'ami-246ed34c'},{'Name':'us-west-1','ami':'ami-9b6e64de'},{'Name':'us-west-2','ami':'ami-55a7ea65'}]

def get_all_regions():
    return [region['Name'] for region in get_all_region_info()]

def get_ec2_conn(region='us-east-1',access_key=None,secret_key=None):
    return boto.ec2.connect_to_region(region_name=region,aws_access_key_id=access_key,aws_secret_access_key=secret_key)

def get_all_instances(region='us-east-1',access_key=None,secret_key=None):
    return [reservation.instances[0] for reservation in get_ec2_conn(region,access_key,secret_key).get_all_instances()]

def is_loki_instance(instance):
    return instance.tags.get('type', 'baldr') == 'loki' # Eventually this will be much more complex, but for now, let's be simple.

def print_instance(instance):
    print "Name: " + instance.tags.get('Name', '[none]') + "\n" + "Loki: " + str(is_loki_instance(instance))

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

def ensure_keypair_exists(public_key,keyname='loki',region='us-east-1',access_key=None,secret_key=None):
    return get_ec2_conn(region,access_key,secret_key).get_key_pair(keyname) if get_ec2_conn(region,access_key,secret_key).get_key_pair(keyname) else get_ec2_conn(region,access_key,secret_key).import_key_pair(key_name=keyname, public_key_material=public_key)

def launch_loki(public_key,keyname='loki',region='us-east-1',access_key=None,secret_key=None):
    return get_ec2_conn(region,access_key,secret_key).run_instances(image_id=[_region['ami'] for _region in get_all_region_info() if _region['Name'] == region][0], key_name=ensure_keypair_exists(public_key,'loki',region,access_key,secret_key).name, user_data=None, instance_type='t1.micro', disable_api_termination=True, dry_run=True)
