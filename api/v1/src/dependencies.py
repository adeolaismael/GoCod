import os
from dotenv import load_dotenv

from pymongo import MongoClient,errors
from pymongo.server_api import ServerApi
from src.db.mongo_db import MongoDB
from src.db.neo4j_db import Neo4jDB


load_dotenv()
mongo_uri = os.getenv("MONGO_URI", "mongodb://teamizaga:izagamongodb@34.155.173.177:27017")
#mongo_uri = os.getenv("MONGO_URI")

uri = os.getenv("URI","neo4j://34.163.193.20:7687")
user = os.getenv("USER", "neo4j")
password = os.getenv("PASSWORD","izaga_neo4j")

def get_neo4j_db():
    # TODO(neo4j): Create Neo4j database connection.
    # You can use the Neo4jDB class for this task.
    # Refer to Neo4j documentation: https://neo4j.com/docs/driver-manual/current/client-applications/
    # Crée une instance de la classe Neo4jDB
    db = Neo4jDB(uri, user, password)
    return db
    pass




def get_mongo_db(database_name="test_db"):
    if mongo_uri is None:
        raise EnvironmentError("La variable d'environnement 'MONGO_URI' n'est pas définie.")
    # Connexion au client MongoDB en utilisant l'URI
    client = MongoClient(mongo_uri, server_api=ServerApi('1'))
    
 
    # Tentative de récupération d'une liste de bases de données pour tester la connexion
    try:
        client.list_database_names()
        print("Connected successfully to MongoDB.")
    except Exception as e:
        print(f"An error occurred while trying to connect to MongoDB: {e}")
        raise
 
    # Sélection de la base de données
    db = client[database_name]
    dbs=MongoDB(db)
    
    return dbs
