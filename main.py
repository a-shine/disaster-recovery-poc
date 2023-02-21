if __name__ == "__main__":
    print("Hello world")


# Dual mode redundancy
# Listen to service + database -> ping server ip and database liveness route
# Listen to GCP status (seperate threads)
# If both return failure -> bring up a workload with terraform

# have multiple regions running this server with ring leader election

# Disaster alerting system
# Automated DR implementation - mechanism to destroy (make sure current prod system is down + destroy non-critical workloads), then bring up new system, update data and then change DNS
# get a reservation (how does the terraform)

# PoC (proof of concept MVP)
# Supprimer le workload non critique
# Récupérer la réservation et l’associer à un projet cible
# Déployer la prod dans le projet & la nouvelle région up
