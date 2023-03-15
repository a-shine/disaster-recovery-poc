import matching_mechanism

if __name__ == "__main__":
    matching_mechanism.region_to_many_recovery("europe-west3")


# Disaster alerting system
# Automated DR implementation - mechanism to destroy (make sure current prod system is down + destroy non-critical workloads), then bring up new system, update data and then change DNS
# get a reservation (how does the terraform)

# PoC (proof of concept MVP)
# Supprimer le workload non critique
# Récupérer la réservation et l’associer à un projet cible
# Déployer la prod dans le projet & la nouvelle région up (mettre a jour le DNS)
