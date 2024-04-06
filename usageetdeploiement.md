**Titre : Rapport d'Activité  Déploiement MongoDB, Neo4j,API et Frontend**

**Date : 29/11/2023**

**Objectifs :**

- **Deployer les bases de données MongoDB et Neo4j**
  
  -Déploiement de la base de donnée MongoDB sur GCP:
     -URI: mongodb://teamizaga:izagamongodb@34.155.173.177:27017
     -Procédure de déploiement:
        -Modification du fichier dev.tfars pour configurer les ressources à utiliser dans GCP en utilisant Terraform
        -Création d'un fichier mongo.ini dans le dossier ansible avec les adressses IP externes des instances GCP crées
        -Création d'un fichier mongo.yml(script ansible) pour déployer et configurer un service MongoDB sur un cluster (ou ensemble d'instances), en utilisant Docker
        -Exécution des commandes terraform init et terraform apply -var-file="environments/dev.tfvars"  pour initialiser un répertoire de travail contenant les fichiers de configuration Terraform et  pour appliquer les changements spécifiés dans les fichiers de configuration Terraform
        -Exécution de la commande ansible-playbook -i mongo.ini tasks/docker.yml pour installer et configurer Docker
        -Exécution de la commande ansible-playbook -i mongo.ini tasks/mongo.yml pour installer et démarrer MongoDB en utilisant Docker sur les instances GCP
  -Déploiement de base de données Neo4j sur GCP:
     -URI: neo4j://34.163.193.20:7687
     -USER:neo4j
     -PASSWORD:izaga_neo4j
     -Procédure de déploiement:
        -Modification du fichier dev.tfars pour configurer les ressources à utiliser dans GCP en utilisant Terraform
        -Création d'un fichier neo4j.ini dans le dossier ansible avec les adressses IP externes des instances GCP crées
        -Création d'un fichier neo4j.yml(script ansible) pour déployer et configurer un service neo4j sur un cluster (ou ensemble d'instances), en utilisant Docker
        -Exécution des commandes terraform init et terraform apply -var-file="environments/dev.tfvars"  pour initialiser un répertoire de travail contenant les fichiers de configuration Terraform et  pour appliquer les changements spécifiés dans les fichiers de configuration Terraform
        -Exécution de la commande ansible-playbook -i neo4j.ini tasks/dockerneo.yml pour installer et configurer Docker
        -Exécution de la commande ansible-playbook -i neo4j.ini tasks/neo4j.yml pour installer et démarrer neo4j en utilisant Docker sur les instances GCP
    -Déploiement frontend :
        -Utilisation de cli Google sdk pour exécuter des commandes gcp pour se connecter au projet à partir du shell
        -Exécution de la commande gcloud init pour se connecter au compte Google cloud à partir du shell
        -Création et configuration du fichier app.yaml pour le déploiement du front end
        -Exécution de la commande gcloud app deploy dans le répertoire front end, pour déployer le front end
    -Déploiement API :
        -Exécution de la commande gcloud run deploy apikikissgocod --port  --source pour déployer l'API
