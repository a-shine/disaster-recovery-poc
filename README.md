# Disaster recovery with dynamic VM (GCE) reservation strategy - PoC

**Disclaimer**: This is not an officially supported Google product. The project
is intended to explore the feasibility of a dynamic VM reservation strategy for
use in disaster recovery. This is a PoC and not a production ready
implementation of a dynamic matching disaster recovery mechanism.

## Problem statement and proposed solution

Aim to demonstrate how VM reservations, on Google Cloud Platform (GCP) Compute
Engine (GCE) can be used to ensure capacity in the event of a disaster while
also minimising costs.

During a zonal or regional disaster, it may be necessary to move workloads to
another functioning zone/region in order to meet Service level metrics (SLOs,
SLAs). However, there is no guarantee that the necessary capacity will be
available (risk of stockout). This risk is further exasperated during a
zonal/regional failure as many users are likely to be migrating their workloads
to neighbouring zones/regions to recover from the disaster.

This justifies the need for reservations, however, reserved GCE capacity is
billed as full VMs (as the capacity, whether idle or not, is reserved for
exclusive use). Using reservations, hence, may be out of reach for certain
businesses, making a robust DRP unachievable.

The solution is to show how idle reserved capacity can be utilized by
non-critical workloads (e.g. dev, staging, pre-production environments) and then
replaced with critical workloads as part of a Disaster Recovery Plan (DRP).
Hence, we speak of dynamic reservation utilisation.

This process is similar to Pod priority in Kubernetes where certain workloads
take precedence over others conditionally (also known as workload
preemptability).

## Overview of Disaster Recovery Planning (DRP)

High-level overview of the DRP process:

1. Detect disaster and alert (using dual/triple mode redundancy to reduce false
   positives)
2. Workload matching mechanism - Identifying critical workloads in a disaster
   region and matching them with non-critical workloads one or more recovery
   regions (with reserved capacity)
3. Workload migration orchestration mechanism

We look to formalise and automate each step (most likely semi-automate as it
tends to be necessary to have some human validation), then the Recovery Point
Objective (RPO) and Recovery Time Objective (RTO) can be significantly improved.
This can enable an organisation to better maintain its service level metrics
(SLOs, SLAs).

## The strategy

The proposed strategy focuses on Stage 2 of the above high-level DRP process.

1. Disaster alert system triggers starting the dynamic matching Disaster
   recovery process (DR process).
2. DR process looks for critical workloads in the provided disaster region and
   matches each critical workload with a non-critical workload in non-disaster
   region.
  
   The match is constrained on the machine type (needs to be of the same or a
   similar machine type) and recovery region scope (for compliance).
3. On completion the DR process outputs:
    1. The successful pair matchings
    2. Warns of any critical workloads that have no match

## The PoC

This PoC uses the GCE
[Reservations](https://cloud.google.com/compute/docs/instances/reservations-overview)
and [Shared
reservations](https://cloud.google.com/compute/docs/instances/reservations-shared)
features on GCP.

In order to demonstrate how different workloads can be switched to use shared
reserved capacity, the PoC contains a `dummy-critical-app` which is a Python
Flask application recording the amount of page views in a `count.txt` file
(which is there to give a sense of persistent state).

The application should run on a VM and be configured as an autostarting process
(start the application on VM boot). It may be necessary to create a custom image
with a preconfigured `systemd` entry for the critical application.

The `dummy-non-critical-app` is a simple 'Hello world!' Flask application with
an open SSH firewall policy to allow developers to access the machine.

Both application infrastructure is described in their respective Terraform
configuration files.

### Setting up GCP environment for the demo

**Pre-requisites**:

- Standard Python 3 installation with `pip` and `virtualenv` (you will need to
  install the dependencies in the `requirements.txt` file)
- Terraform
- GCP account with billing enabled
- A basic understanding of the above tools

1. Configure three projects in GCP to be used:
    1. A reservation management project. Similar to shared Committed Use
       Discounts (CUD) management, we typically use an independent project to
       manage all the multi-project reservations in a centralised place.
    2. Two other projects, for the critical app and the non-critical app.
       Specify different regions for each of the projects.
2. Create a shared reservation in the reservation management project between the
   critical and non-critical project. Reserve one Compute Engine instance of
   type `e2-medium` in the zone of the non-critical application. Configure
   reservation to "Use reservation automatically".
3. Configure the Terraform `variables.tf` in both the `dummy-critical-app` and
   `dummy-non-crticial-app` with the respective critical and recovery
   zones/regions.
4. Update the Terraform `terraform.tfvars` in both the `dummy-critical-app` and
   `dummy-non-crticial-app` with the respective Project IDs.
5. Update the `terraform.tfvars` in the `dummy-critical-app` directory to ensure
   the correct recovery regions are configured. Make sure to keep them commented
   out as they will be used later to migrate the critical workload using
   Terraform.
6. Run `terraform apply` from the `dummy-critical-app` directory to bring up the
  application in the default region. Make sure that the recovery regions are
  commented out in the `terraform.tfvars` file. They will be used to migrate the
  workload when disaster strikes!
7. Run `terraform apply` from the `dummy-non-critical-app` directory to bring up
  the non-critical application.
8. Overwrite the `example_workload_db.csv` file by adding the necessary
   information as specified by each of the column headers.

### Demo walkthrough

- Observe critical application running in its region (navigate to Flask
  application endpoint and GCP Compute Engine console).
- Observe non-critical application running in its region.
- Notice 100% reservation utilisation in reservation management project (the
  single reserved e2-medium instance is being used by the non-critical
  application).
- Imaginary disaster strikes!
  - Workload identification and matching process. Run the DR dynamic matching
    process by executing the python `main.py` specifying the disaster region.
  - Observe output: workload pairs and unmatched critical workloads.
  - Demonstrate switched reservation utilisation during workload migration
    - Take down non-critical application running in region designated for
      disaster recovery (simulate a disaster).
    - Migrate the critical application to the disaster recovery region by
      uncommenting the recovery regions as specified in the `dummy-critical-app`
      `terraform.tfvars` file.
    - Show the critical application running once again, this time in the
      recovery region.
    - Show 100% reservation utilisation.

### Clean-up

Run `terraform destroy` for both the `dummy-critical-app` and
`dummy-non-critical-app`.

## Open questions

- How to prevent people from creating VMs in a region when there is a disaster
  recovery status?
  - Turn off automatic reservation in the case of a disaster (hardcode the
    reservation to be taken on a workload by workload basis)
  - Rule in the centralized VM management system to prevent creation of VMs in
    the region where DR is occurring with reservation
