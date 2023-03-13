"""This script implements the workload identification and matching mechanism."""

from ast import literal_eval
import pandas as pd


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

# TODO: Clean this up

# get all projects in a region/zone

# For a given project and zone, list the critical workloads and migrate them to another zone replacing the non-critical workloads (if needed)


# FEATURE: DO THIS AS TOP PRIORITY (not python script)
# 1. Have a terraform for the non-critical workloads
# 2. and show that you can destroy non-critical with terraform destroy, replace reservation by applying critical terraform with terrorm apply


# Should work in rounds as long as no critical workloads remain in the disaster zone

# read in csv file as data frame
# in practice this could be the GCP API, Cloud Asset Inventory, BQ or another database...
df = pd.read_csv("workloads.csv")


df['tags'] = df['tags'].apply(lambda x: literal_eval(x) if "[" in x else x)

# print(df.head())

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
    disaster_region_critical_workloads = get_critical_workloads_in_region(
        disaster_region)
    recovery_region_non_critical_workloads = get_non_critical_workloads_in_region(
        recovery_region)

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

disaster_region_critical_workloads = get_critical_workloads_in_region(
    "europe-west3")
recovery_region_non_critical_workloads = get_non_critical_workloads_in_region(
    "europe-west4")

# for each critical workload in the disaster region data frame find a non-critical workload in the recovery region data frame with the same machine type
# match the workloads in the disaster region with the workloads in the recovery region in a new data frame

# new data frame with the critical workloads in the disaster region and the non-critical workloads in the recovery region
workload_mapping = disaster_region_critical_workloads.merge(
    recovery_region_non_critical_workloads, on='instance_type', how='inner')

# get all the critical workloads in the disaster region that do not have a match in the recovery region
non_mapped_critical_workloads = disaster_region_critical_workloads.merge(
    recovery_region_non_critical_workloads, on='instance_type', how='outer', indicator=True).loc[lambda x: x['_merge'] == 'left_only']
print(workload_mapping)
print(non_mapped_critical_workloads)

# Next step - try map the failed mapped critical workloads to another region/zone - rerun the script

# TODO: Explore edge case where there are no non-critical workloads in the recovery region
