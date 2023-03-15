# Disaster recovery with dynamic reservation strategy PoC

This Proof of Concept (PoC) repository demonstrates how VM reservations can be
used to ensure capacity in the event of a disaster while minimising costs. We
attempt to demonstrate how idle reserved capacity can be utilized by
non-critical workloads (e.g. dev, staging, pre-production environments) and
then replaced with critical workloads as part of a Disaster Recovery Plan (DRP).

**Highest-level DR strategy overview**

1. Detect disaster and alert (using dual mode redundancy to reduce false
   positives)
2. Workload matching mechanism - how to identify critical workloads in a
   disaster region and match them with non-critical workloads in another
   recovery region (with reserved capacity)
3. Workload migration and reservation usage mechanism

**Out of scope**

- The specifics of the application and automated deployment/IaC tooling
- The specifics of the database of running workloads (BQ, Asset inventory,
  `gcloud` API, self-managed database...)
- The specifics of how the application and application data is backed-up (which
  will affect your RPO)
  <!-- TODO: This needs to be looked into further? Using Turboreplication to
  maintain freshness of backups across regions -->

## Background

In order to demonstrate how different workloads can be switched to use shared
reserved capacity, the PoC contains a `dummy-critical-app` which is a Python
Flask application recording the amount of page views in a `count.txt` file
(gives a sense of persistent state). The application runs on a VM as daemon
process registered with `systemd` in order to ensure the process is maintained
(even at startup). The whole application and `systemd` configuration is present
in the customised base image: `critical-app-python-debian`.

The `dummy-non-critical-app` is a simple 'Hello world!' Flask application with
an open SSH firewall policy to allow developers to access the machine.

Both application infrastructure is described in their respective Terraform
configuration files.

## Setting up GCP for the demo

Configure three projects in GCP to be used:

- A 'Reservation mother project' (similar to shared CUD management we typically
  use an independent project to manage all the multi-project reservations).
- Two other projects, for the Critical app and the Non-critical app, setup in
  different regions.
- Update the Terraform `variables.tf` and `terraform.tfvars` in each of the
  dummy application directories to ensure the correct project IDs and regions
  are configured.

## Demo

### Pre-demo setup

- Run `terraform apply` from the `dummy-critical-app` directory to bring up the
  application in the default region (`europe-west-3`). Make sure that the
  recovery regions are commented out in the `terraform.tfvars` file (they will
  be used to migrate the workload when disaster strikes)
- Run `terraform apply` from the `dummy-non-critical-app` directory to bring up
  the non-critical application

### Demo path

<!-- for tmr (do intro + workload migration and then show workload identification and matching) -->

- Intro
  - Show critical application running in its region (demonstrate in browser +
    VM console)
  - Show non-critical application running in its region (VM consoles)
  - Show 100% reservation utilization in reservation mother project (show the two associated projects)
- Disaster strikes!
  - Workload identification and matching
    - Show the matching mechanism script with valid matching workloads
      - Go through each of the functions - focus on the highest level region_to_region and region_to_many recovery
    - Also show identification of unmatched critical workloads
  - Workload migration (prove that we get to use the reserved capacity)
    - Take down non-critical application running in region designated for
      disaster recovery
    - Migrate the critical application to the disaster recovery region by enabling
      the tfvars
    - Show the critical application running
    - Show 100% reservation utilization

## Open questions

- How to prevent people from creating VMs in a region when there is a disaster
  recovery status?
  - Turn off automatic reservation in the case of a disaster (hardcode the
    reservation to be taken on a workload by workload basis)
  - Rule in the centralized VM management system to prevent creation of VMs in
    the region where DR is occurring with reservation
- Explore edge case where there are no non-critical workloads in the recovery
  region (try another region)

<!--
PoC (proof of concept MVP)
Supprimer le workload non critique
Récupérer la réservation et l’associer à un projet cible
Déployer la prod dans le projet & la nouvelle région up (mettre a jour le DNS) -->
