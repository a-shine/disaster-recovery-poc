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

# from google.cloud import compute_v1
from google.cloud import resource_manager


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

list_projects()
list_instances("long-grin-378416", "europe-west3-a")
# list_instances_with_tag("long-grin-378416", "europe-west3-a", "critical")

# Migrate all VMs with critical tag to a different region, replace non-critical VMs with critical VMs
# def migrate_critical_workloads_to_w4():


# For a given project and zone, list the critical workloads and migrate them to another zone replacing the non-critical workloads (if needed)


# Managed VMs - why is that important?

# FEATURE: DO THIS AS TOP PRIORITY (not python script)
# 1. Have a terraform for the non-critical workloads 
# 2. and show that you can destroy non-critical with terraform destroy, replace reservation by applying critical terraform with terrorm apply