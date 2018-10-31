# http://docs.openstack.org/developer/python-novaclient/ref/v2/servers.html
import time, os, sys
import inspect
from os import environ as env

from  novaclient import client
import keystoneclient.v3.client as ksclient
from keystoneauth1 import loading
from keystoneauth1 import session

flavor = "ACCHT18.normal"
private_net = "SNIC 2018/10-30 Internal IPv4 Network"
floating_ip_pool_name = None
floating_ip = None
image_name = "Ubuntu 16.04 LTS (Xenial Xerus) - latest"
num_workers = 4



loader = loading.get_plugin_loader('password')

auth = loader.load_from_options(auth_url=env['OS_AUTH_URL'],
                                username=env['OS_USERNAME'],
                                password=env['OS_PASSWORD'],
                                project_name=env['OS_PROJECT_NAME'],
                                project_domain_name=env['OS_USER_DOMAIN_NAME'],
                                project_id=env['OS_PROJECT_ID'],
                                user_domain_name=env['OS_USER_DOMAIN_NAME'])

sess = session.Session(auth=auth)
nova = client.Client('2.1', session=sess)
print("user authorization completed.")

image = nova.glance.find_image(image_name)



flavor = nova.flavors.find(name=flavor)

if private_net != None:
    net = nova.neutron.find_network(private_net)
    nics = [{'net-id': net.id}]
else:
    sys.exit("private-net not defined.")

#print("Path at terminal when executing this file")
#print(os.getcwd() + "\n")
cfg_file_path =  os.getcwd()+'/cloud-cfg-worker.txt'
if os.path.isfile(cfg_file_path):
    userdata_worker = open(cfg_file_path)
else:
    sys.exit("cloud-cfg.txt is not in current working directory")

cfg_file_path =  os.getcwd()+'/cloud-cfg-master.txt'
if os.path.isfile(cfg_file_path):
    userdata_master = open(cfg_file_path)
else:
    sys.exit("cloud-cfg.txt is not in current working directory")

secgroups = ['default', 'Tor_security']

print("Creating master instance... ")
instance_master = nova.servers.create(name="group_18_master", image=image, flavor=flavor, userdata=userdata_master,
                                   nics=nics, security_groups=secgroups, key_name="group_18_kp")
inst_status = instance_master.status
time.sleep(10)
print("waiting for 10 seconds.. ")
while inst_status == 'BUILD':
    print("Instance: "+instance.name+" is in "+inst_status+" state, sleeping for 5 seconds more...")
    time.sleep(5)
    instance_master = nova.servers.get(instance_master.id)
print("Instance: "+ instance_master.name +" is in " + inst_status + "state")


print("Creating worker instance... ")
instance_worker = nova.servers.create(name="group_18_worker", image=image, flavor=flavor, userdata=userdata_worker,
                                   nics=nics, security_groups=secgroups, key_name="group_18_kp")
inst_status = instance_worker.status
time.sleep(10)
print("waiting for 10 seconds.. ")
while inst_status == 'BUILD':
    print("Instance: "+instance_worker.name+" is in "+inst_status+" state, sleeping for 5 seconds more...")
    time.sleep(5)
    instance_worker = nova.servers.get(instance_worker.id)

"""
for i in range(num_workers):
    print("Creating worker instance " + str(i) + " ... ")
    instance = nova.servers.create(name="group_18_worker " + str(i), image=image, flavor=flavor, userdata=userdata_worker,
                                   nics=nics, security_groups=secgroups, key_name="group_18_kp")
    inst_status = instance.status
    print("waiting for 10 seconds.. ")
    time.sleep(10)

    while inst_status == 'BUILD':
        print("Instance: "+instance.name+" is in "+inst_status+" state, sleeping for 5 seconds more...")
        time.sleep(5)
        instance = nova.servers.get(instance.id)
        inst_status = instance.status
"""

print("Instance: "+ instance.name +" is in " + inst_status + "state")