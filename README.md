loki is a program that self-replicates across EC2 regions in an AWS account.

loki's core is a 2-line python script that checks which regions have lokis running, and when the number of regions drops below a certain threshold, starts more.  It installs a cron job to run itself every minute, and installs a shutdown script to launch itself in a different region if its instance gets stopped or terminated.  It runs on a standard amazon linux AMI; it passes on its code through the userdata of the new instance.  This userdata is created dynamically by the python script and itself contains the python script as a base64-encoded blob that gets decoded and placed on disk on the new instance; it also puts a boto.cfg file, a cron job, and shutdown and reboot scripts into the proper locations.

There are no easily identifiable indicators in the console that an instance is a loki instance; lokis identify each other by examining the base64-encoded userdata script that contains all of their logic.

loki runs on user credentials, not the roles of the instances it launches, so it propagates using only ec2 permissions.  This means that a loki fleet can be disabled by deactivating the credential pair that it's using to make EC2 calls.
