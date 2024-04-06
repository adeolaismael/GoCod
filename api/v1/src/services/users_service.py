"""
User Service
"""
# pylint: disable=W0212
import logging
from bson.objectid import ObjectId
from pymongo import errors
from src.db.mongo_db import MongoDB
from src.utils.handlers import handle_db_operations


class UserService:
    """
    Class to manage user operations.
    """
    def __init__(self, db):
        self.db = db
    
    @handle_db_operations
    def create_user(self, user_data: dict):
        """
        Create a user with the `user_data` object.
        An org with the name of the user should be created if an organization
        is not provided in registration.

        Args:
            user_data (dict): The user data to be inserted.

        Returns:
            str: The ID of the inserted user.
        """
        # TODO(mongo): Create a new user.
        # If "org_name" is not in user_data, create an organization with the name of the user.
        # Create the user with the organization ID.
        # Refer to MongoDB documentation: https://docs.mongodb.com/manual/tutorial/insert-documents/

        # Supprimer le champ 'org_name' s'il existe dans les données de l'utilisateur
        if "org_name" not in user_data.keys():
            # If "org_name" is not present, use the username as the organization name
            org_name = user_data.get("username")
            org_data = {"org_name": org_name}
            org_id = self.db.create(org_data, "orgs").get("result")
        else:
            # Remove the "org_name" field from user_data
            org_name = user_data.pop("org_name", None)

        # Insert the user data into the "users" collection
        user_id = self.db.create(user_data, "users").get("result")

        return user_id
    
    @handle_db_operations
    def authenticate_user(self, username: str, password: str):
        """
        Authenticate a user by username and password.

        Args:
            username (str): The username of the user to be authenticated.
            password (str): The password of the user to be authenticated.

        Returns:
            Union[dict, None]: Les données de l'utilisateur si l'authentification est réussie,
                            ou None si l'authentification échoue.
        """
        # Tentez de lire les données de l'utilisateur dans la base de données en utilisant le nom d'utilisateur comme clé de recherche.
        try:
            user_data = self.db.read({"username": username}, "users")
        except Exception as e:
            # Gérer l'exception si la lecture de la base de données échoue.
            return {"error": str(e)}

        # Vérifiez si les données de l'utilisateur ont été trouvées.
        if user_data:
            # Accédez au dictionnaire imbriqué 'result' dans 'user_data'.
            user_info = user_data.get("result", {})
            # Obtenez le mot de passe stocké du dictionnaire.
            stored_password = user_info.get("password")

            # Définir une valeur par défaut pour 'org_id' si elle n'existe pas
            default_org_id = "valeur_par_defaut"  # Remplacez ceci par la valeur par défaut souhaitée
            user_info.setdefault('org_id', default_org_id)

            # Si le mot de passe stocké existe et correspond au mot de passe fourni, renvoyez les données de l'utilisateur.
            if stored_password and stored_password == password:
                return user_info  # Retournez directement le dictionnaire de l'utilisateur.
            else:
                # Si l'authentification échoue, renvoyez None.
                return None
        else:
            # Si les données de l'utilisateur n'ont pas été trouvées, renvoyez None.
            return None

    @handle_db_operations
    def read_user(self, user_id: str):
        """
        Read a user with the `user_id` object.

        Args:
            user_id (str): The user id to be read.

        Returns:
            dict: The user data or None if the user is not found.
        """
        try:
            # Convertir la chaîne en ObjectId
            user_id = ObjectId(user_id)
        except bson.errors.InvalidId:
            print("L'ID utilisateur fourni n'est pas valide.")
            return None

        # Utiliser l'ObjectId pour obtenir le document de l'utilisateur
        user = self.db.read(
            query={"_id": user_id},
            collection_name="users",
            many=False  # Assurez-vous que cette option est gérée correctement dans la méthode `read`
        ).get("result")

        # Imprimer le résultat pour le débogage
        #print(user)
        return user 
    pass

    @handle_db_operations
    def get_user_by_username(self, username: str, projection: dict = None):
        """
        Get a user by username.

        Args:
            username (str): The username of the user to be returned.

        Returns:
            dict: The user data, with 'org_id' field included.
        """
        projection = projection or {}
        default_org_id = "valeur_par_defaut"  # Remplacez ceci par la valeur par défaut souhaitée

        user_data = self.db.read(
            query={"username": username},
            collection_name="users",
            projection=projection
        ).get("result")

        if user_data:
            user_data.setdefault('org_id', default_org_id)

        return user_data
