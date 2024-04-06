"""
MongoDB database operations.

This module contains the database operations for the MongoDB database.

Classes:
    MongoDB: A class to manage the database operations.

"""

import logging
from typing import Optional, List, Union
import datetime
from bson.objectid import ObjectId
from pymongo import errors
import pymongo
from src.utils.handlers import handle_db_operations


class MongoDB:
    """
    A class to manage the database operations.
    """

    def __init__(self, db):
        """
        Initialize the database.
        """
        self.db = db

    @handle_db_operations
    def drop_collection(self, collection_name: str) -> dict:
        """
        Drop a collection from the database.

        Args:
            collection_name (str): The name of the collection to be dropped.

        Returns:
            dict: A dictionary containing the operation's success status, message, and result.
        """

        drop_result = self.db[collection_name].drop()
        return drop_result
    
    @handle_db_operations
    def drop_database(self, database_name: str) -> dict:
        """
        Drop a database from the database.

        Args:
            database_name (str): The name of the database to be dropped.

        Returns:
            dict: A dictionary containing the operation's success status, message, and result.
        """

        drop_result = self.db.drop()
        return drop_result

    @handle_db_operations
    def drop_index(self, collection_name: str, index_name: str) -> dict:
        """
        Drop an index from the collection.

        Args:
            collection_name (str): The name of the collection.
            index_name (str): The name of the index.

        Returns:
            dict: A dictionary containing the operation's success status, message, and result.
        """
        # Liste des index existants dans la collection
        existing_indexes = [idx['name'] for idx in self.db[collection_name].list_indexes()]
        
        # Vérifier si l'index spécifié existe
        if index_name in existing_indexes:
            drop_result=self.db[collection_name].drop_index(index_name)
            return drop_result
        else:
            pass

    
 
    @handle_db_operations
    def create_index(self, collection_name: str, field: Union[str, List[tuple]], unique: bool = False) -> str:
        """
        Create an index on the `collection` for the `field`.
 
        Args:
            collection_name (str): The collection name.
            field (Union[str, List[tuple]]): The field name or a list of tuples for a compound index.
            unique (bool, optional): Whether the index should be unique. Defaults to False.
 
        Returns:
            str: The name of the created index on success, or an error message on failure.
        """
        try:
            if isinstance(field, str):
                # Single field index
                index_name = self.db[collection_name].create_index([(field, 1)], unique=unique)
            elif isinstance(field, list):
                # Compound index
                index_name = self.db[collection_name].create_index(field, unique=unique)
            else:
                raise TypeError("Field must be a string or a list of tuples")
 
            return index_name
        except errors.PyMongoError as e:
            error_message = f"Error creating index: {e}"
            print(error_message)
            return error_message


    
    @handle_db_operations
    def create(self, document_data: dict, collection_name: str, many: bool = False) -> Union[str, List[str]]:
        """
        Create a document or documents in a collection in the database.

        Args:
            document_data (dict): The data to be inserted.
            collection_name (str): The name of the MongoDB collection to be inserted into.
            many (bool, optional): Whether to insert many documents. Defaults to False.

        Returns:
            Union[str, List[str]]: The inserted document's ID or list of IDs.
        """
        collection = self.db[collection_name]
        if many:
            # Insert multiple documents
            result = collection.insert_many(document_data)
            return [str(id) for id in result.inserted_ids]
        else:
            # Insert a single document
            result = collection.insert_one(document_data)
            return str(result.inserted_id)

    @handle_db_operations
    def read(
        self,
        query: dict,
        collection_name: str,
        many: bool = False,
        projection: Optional[dict] = None,
        sort: Optional[List[tuple]] = None,
        limit: int = 10,
        skip: Optional[int] = None,
    ) -> Union[dict, List[dict]]:
        """
        Read a document(s) from the specified collection based on the query.
        """
        collection = self.db[collection_name]
        documents = []

        if many:
            cursor = collection.find(query, projection)
            if sort:
                cursor = cursor.sort(sort)
            if skip is not None:
                cursor = cursor.skip(skip)
            cursor = cursor.limit(limit)

            documents = list(cursor)
        else:
            document = collection.find_one(query, projection)
            if document is None:
                print ("No document found matching the query: {query}")
            documents = document

        return documents




    @handle_db_operations
    def update(
            self,
            query: dict,
            document_data: dict,
            collection_name: str,
            update_type: str = "set",
            multi: bool = False
        ) -> int:
        """
        Update a document or multiple documents in a given collection in the database.
        """
        if update_type not in ["set", "push", "pull", "unset", "inc"]:
            raise ValueError("Invalid update type")

        collection = self.db[collection_name]
        
        # Définir l'opérateur de mise à jour approprié.
        update_data = {f"${update_type}": document_data}
        
        # Choisir entre la mise à jour d'un seul document ou de plusieurs documents.
        if multi:
            result = collection.update_many(query, update_data)
        else:
            result = collection.update_one(query, update_data)
        
        # Retourner le nombre de documents modifiés.
        return result.modified_count
        
    @handle_db_operations
    def delete(self, query: dict, collection_name: str, many: bool = False) -> int:
        """
        Delete document(s) from the given collection in the database.
        """
        collection = self.db[collection_name]
        
        if many:
            # Supprimer tous les documents correspondant à la requête
            result = collection.delete_many(query)
        else:
            # Supprimer un seul document correspondant à la requête
            result = collection.delete_one(query)
        
        # Le nombre de documents supprimés est disponible via la propriété deleted_count de l'objet résultant.
        documents_deleted_count = result.deleted_count
        
        return documents_deleted_count
