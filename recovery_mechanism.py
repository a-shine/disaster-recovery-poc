# Switch between two known regions e.g. eu-west3 and eu-west4
# Given a workload to move (machine type + region) find a cousin workload with the same machine type that is non-critical in a different region
# replace the workload

# Import the terraform conf file from the critical workload
# Get the machine type
# Get the region
# Get the project
# Get the zone

# Do for one specific workload and then could be generalized to do multiple workloads

# List the GCP GCE instances
# List the GCP GCE instances with a critical tag
# List the GCP GCE instances with a non-critical tag
# List the GCP GCE instances with a critical tag in a different region
# List the GCP GCE instances with a non-critical tag in a different region

import pandas as pd

def list_instances(project, zone):
    """Lists all instances in a project."""
    client = compute_v1.InstancesClient()
    instance_list = client.list(project=project, zone=zone)
    for instance in instance_list:
        print(instance.name)
        print(instance.tags.items)
        print(instance.machine_type)

# List all VMs in a zone with a specific tag
def list_instances_with_tag(project, zone, tag):
    """Lists all instances in a project."""
    client = compute_v1.InstancesClient()
    instance_list = client.list(project=project, zone=zone)
    for instance in instance_list:
        if tag in instance.labels:
            print(instance.name)
            print(instance.machine_type)


def recover_critical_workload(critical_workload):
    identify_workload_to_kill()
    kill_workload()
    apply_terraform()
    # update dns (maybe this is done inside the terraform)

# def move_critical_workloads_to_w4():
#     # Get all vms with critical tag (maybe need to have a database of this stored in a multregion)
#     # Find an equivalently sized non-critical worload
#     # take it down and replace reserved slot with critical load
#     pass

def identify_workload_to_kill(machine_type): # FEATURE: Read the machine type from the terraform file
    pass
    # Once we have identified workloads to kill - we can remove it 
    # and then run the terraform apply to bring up the critical workload

def kill_workload():
    pass

def apply_terraform():
    pass

# def move_critical_workloads_to_w3():
#     pass
    
# get all projects in a region/zone
def list_projects():
    client = resource_manager_v3.Client()
    for project in client.list_projects():
        print(project.project_id)

# list_projects()
# list_instances("long-grin-378416", "europe-west3-a")
# list_instances_with_tag("long-grin-378416", "europe-west3-a", "critical")

# Migrate all VMs with critical tag to a different region, replace non-critical VMs with critical VMs
# def migrate_critical_workloads_to_w4():


# For a given project and zone, list the critical workloads and migrate them to another zone replacing the non-critical workloads (if needed)


# Managed VMs - why is that important?

# FEATURE: DO THIS AS TOP PRIORITY (not python script)
# 1. Have a terraform for the non-critical workloads 
# 2. and show that you can destroy non-critical with terraform destroy, replace reservation by applying critical terraform with terrorm apply


# Should work in rounds as long as no critical workloads remain in the disaster zone

# read in csv file as data frame
df = pd.read_csv("workloads.csv") # in practice this could be the GCP API, Cloud Asset Inventory, BQ or another database...

from ast import literal_eval

df['tags'] = df['tags'].apply(lambda x: literal_eval(x) if "[" in x else x)

print(df.head())

# get all critical workloads in a region
def get_critical_workloads_in_region(region):
    return df.loc[(df['region'] == region) & (df['tags'].map(lambda x: 'critical' in x))]

# get all non-critical workloads in a region
def get_non_critical_workloads_in_region(region):
    # Get when the region matches and the tags array contains the non-critical tag
    return df.loc[(df['region'] == region) & (df['tags'].map(lambda x: 'non-critical' in x))]

def identify_workload_to_kill(machine_type):
    return recovery_region_non_critical_workloads.loc[(recovery_region_non_critical_workloads['instance_type'] == machine_type)]
    

# do this in rounds until all critical workloads are in the recovery region
def regional_disaster_recovery(disaster_region, recovery_region):
    disaster_region_critical_workloads = get_critical_workloads_in_region(disaster_region)
    recovery_region_non_critical_workloads = get_non_critical_workloads_in_region(recovery_region)

    # for each critical workload in the disaster region data frame find a non-critical workload in the recovery region data frame with the same machine type
    # disaster_region.apply(lambda x: identify_workload_to_kill(x['machine_type']), axis=1)
    disaster_region.apply(lambda x: x['instance_type'], axis=1)

    # for critical_workload in disaster_region:
        # print(critical_workload)
        # Find a non-critical workload in a different region with the same machine type
        # critical_workload_machine_type = critical_workload['machine_type']
        # for non_critical_workload in recovery_region:
        #     if non_critical_workload['machine_type'] == critical_workload_machine_type:
        #         # Destroy the non-critical workload
        #         # Replace the capacity previously occupied by the non-critical workload with the critical workload (Apply the critical workload)
        #         # Update the database so we know that the critical workload is now in the recovery region
        #         pass


# regional_disaster_recovery("europe-west3", "europe-west4")

disaster_region_critical_workloads = get_critical_workloads_in_region("europe-west3")
recovery_region_non_critical_workloads = get_non_critical_workloads_in_region("europe-west4")

# for each critical workload in the disaster region data frame find a non-critical workload in the recovery region data frame with the same machine type
# match the workloads in the disaster region with the workloads in the recovery region in a new data frame

# new data frame with the critical workloads in the disaster region and the non-critical workloads in the recovery region
workload_mapping = disaster_region_critical_workloads.merge(recovery_region_non_critical_workloads, on='instance_type', how='inner')

# get all the critical workloads in the disaster region that do not have a match in the recovery region
non_mapped_critical_workloads = disaster_region_critical_workloads.merge(recovery_region_non_critical_workloads, on='instance_type', how='outer', indicator=True).loc[lambda x : x['_merge']=='left_only']
print(workload_mapping)
print(non_mapped_critical_workloads)

# Next step - try map the failed mapped critical workloads to another region/zone - rerun the script

# TODO: Explore edge case where there are no non-critical workloads in the recovery region