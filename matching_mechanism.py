'''This script implements the workload identification and matching mechanism. 
The idea is to find, for each critical workload in the disaster region or zone, 
a non-critical workload in a recovery region with an equivalent machine type'''

import pandas as pd
from ast import literal_eval

# Assume that all capacity is used with reservations ( each workload is
# associated with a reservation). The aim is to maximise reservation
# utilisation in order to minimise cost of idle reserved capacity.

# As a pre-requisite we need a database of all projects (and hence workloads)
# containing the following information: project_id/workload, region, zone,
# machine_type, tags.

# Read the CSV file into a Pandas Dataframe
# In practice this could be the GCP API, Cloud Asset Inventory, BQ or another
# database...
df = pd.read_csv("workloads.csv")

# Convert the tags list string column to a list
df['tags'] = df['tags'].apply(lambda x: literal_eval(x) if "[" in x else x)


def get_critical_workloads_in_region(region):
    '''Get all the critical workloads for a given region based on the region
    and tag columns'''
    return df.loc[(df['region'] == region) & (df['tags'].map(lambda x: 'critical' in x))]


def get_non_critical_workloads_in_region(region):
    '''Get all non-critical workloads in a given region. Non-critical workloads
    are identified if they contain the non-critical tag'''
    return df.loc[(df['region'] == region) & (df['tags'].map(lambda x: 'non-critical' in x))]


def get_all_non_critical_workloads_regional_disaster(disaster_region):
    '''Get all non-critical workloads except those in the disaster region. 
    Non-critical workloads are identified if they contain the non-critical tag'''
    return df.loc[(df['tags'].map(lambda x: 'non-critical' in x)) & (df['region'] != disaster_region)]


def get_all_non_critical_workloads_zonal_disaster(disaster_zone):
    '''Get all non-critical workloads except those in the disaster zone. 
    Non-critical workloads are identified if they contain the non-critical tag'''
    return df.loc[(df['tags'].map(lambda x: 'non-critical' in x)) & (df['zone'] != disaster_zone)]


def get_critical_workloads_in_zone(zone):
    '''Get all the critical workloads for a given zone based on the region and
    tag columns'''
    return df.loc[(df['zone'] == zone) & (df['tags'].map(lambda x: 'critical' in x))]


def get_non_critical_workloads_in_zone(zone):
    '''Get all non-critical workloads in a given zone. Non-critical workloads
    are identified if they contain the non-critical tag'''
    return df.loc[(df['zone'] == zone) & (df['tags'].map(lambda x: 'non-critical' in x))]


# BUG: re-uses noncritical workloads that have already been mapped
def possible_workload_mapping(disaster_critical_workload, recovery_non_critical_workload):
    '''Map critical workloads in the disaster region or zone to a non-critical
    workloads in the recovery region'''
    return disaster_critical_workload.merge(
        recovery_non_critical_workload, on='instance_type', how='inner')


def unmappable_critical_workloads(disaster_critical_workload, recovery_non_critical_workload):
    '''Get all the critical workloads in the disaster region or zone that do not have a match in the recovery region or zone'''
    return disaster_critical_workload.merge(
        recovery_non_critical_workload, on='instance_type', how='outer', indicator=True).loc[lambda x: x['_merge'] == 'left_only']


# Should work in rounds (best efforts) as long as critical workloads remain
# in the disaster zone
def region_to_region_recovery(disaster_region, recovery_region):
    '''Identify and match workloads in the disaster region to workloads in a 
    specified recovery region'''
    disaster_region_critical_workloads = get_critical_workloads_in_region(
        disaster_region)
    recovery_region_non_critical_workloads = get_non_critical_workloads_in_region(
        recovery_region)

    # For each critical workload in the disaster region dataframe find a
    # non-critical workload in the recovery region data frame with the same
    # machine type
    print("Mapping critical workloads in the disaster region to non-critical workloads in the recovery region")
    mapped_workloads = possible_workload_mapping(disaster_region_critical_workloads,
                                                 recovery_region_non_critical_workloads)
    print(mapped_workloads.head())

    print("Warning the following critical workloads in the disaster region do not have a match in the recovery region")
    unmapped_workloads = unmappable_critical_workloads(
        disaster_region_critical_workloads, recovery_region_non_critical_workloads)
    print(unmapped_workloads)


# TODO: A better way to do this is as a constraint satisfaction problem using a backtracking algorithm
def region_to_many_recovery(disaster_region):
    '''Identify and match workloads in the disaster region to all non-critical workloads'''
    disaster_region_critical_workloads = get_critical_workloads_in_region(
        disaster_region)
    all_non_critical_workloads = get_all_non_critical_workloads_regional_disaster(
        disaster_region)

    print("Mapping critical workloads in the disaster region to non-critical workloads in the recovery regions")
    mapped_workloads = possible_workload_mapping(disaster_region_critical_workloads,
                                                 all_non_critical_workloads)
    print(mapped_workloads.head())

    # Modify the dataframe to include one unique critical workload to non-critical workload mapping
    # for each row - if the workload has been matched remove any other matches
    # from the dataframe
    # mapped_workloads = mapped_workloads.drop_duplicates(
    #     subset=['project_y'], keep='first')
    # print(mapped_workloads.head())

    # First let us identify all unmappable critical workloads
    print("Warning the following critical workloads in the disaster region do not have a match in any recovery region")
    # unmapped_workloads = unmappable_critical_workloads(
    # disaster_region_critical_workloads, recovery_region_non_critical_workloads)  # BUG: fix this
    # print(unmapped_workloads)

    new_mapped_workloads = pd.DataFrame()
    # BUG: its the for loop that is causing the issue as mapped_workloads is being modified
    # BUG: Add the notion of correct machine type + if there is no match for the machine type
    for critical_workload in mapped_workloads['project_x'].unique():
        # find the first match for the critical workload
        first_match = mapped_workloads.loc[mapped_workloads['project_x']
                                           == critical_workload].iloc[0]
        # add the first match to the new dataframe
        new_mapped_workloads = new_mapped_workloads.append(first_match)
        # remove the first match from the original dataframe
        mapped_workloads = mapped_workloads[mapped_workloads['project_x']
                                            != critical_workload]
        # remove any other other rows containing the same project_y
        # print(first_match['project_y'])
        # print(mapped_workloads.head())
        mapped_workloads = mapped_workloads[mapped_workloads['project_y']
                                            != first_match['project_y']]
        # print(mapped_workloads.head())

    print(new_mapped_workloads.head())  # THIS WORKS! (I think)
