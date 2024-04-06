from neo4j import GraphDatabase, Transaction
from src.utils.parsing import format_dict_for_cypher
from src.utils.handlers import handle_db_operations


class Neo4jDB:
    """
    A class to manage the database operations for Neo4j.
    """

    def __init__(self, uri, username, password):
        """
        Initialize the database driver.
        """
        self._driver = GraphDatabase.driver(uri, auth=(username, password))

    def close(self):
        """
        Close the database connection.
        """
        self._driver.close()

    def execute_write(self, func, **kwargs):
        with self._driver.session() as session:
            return session.execute_write(func, **kwargs)

    def execute_read(self, func, **kwargs):
        with self._driver.session() as session:
            result = session.execute_read(func, **kwargs)
            # Vérifier si le résultat est vide
            if not result:
                return None
            return result


    @handle_db_operations
    def drop(self, label=None):
        """
        Delete all or certains nodes and relationships.

        Args:
            tx (Transaction): Neo4j transaction.
            label (str): Label for the node.

        Returns:
            dict: The result of the operation.
        """

        def delete_all(tx: Transaction):
            query = f"MATCH (n) DETACH DELETE n"
            result = tx.run(query)
            return result.consume().counters

        def delete_label(tx: Transaction, label: str):
            query = f"MATCH (n:{label}) DETACH DELETE n"
            result = tx.run(query)
            return result.consume().counters

        if label:
            result = self.execute_write(delete_label, label=label)
            return result
        else:
            result = self.execute_write(delete_all)
            return result

    @handle_db_operations
    def create_index(self, node_label: str, property_name: str) -> dict:
        """
        Create a unique index on a node.

        Args:
            tx (Transaction): Neo4j transaction.
            node_label (str): Label for the node.
            property_name (str): Property to index.

        Returns:
            dict: The result of the operation.
        """

        def create_node_index(tx: Transaction, node_label: str, property_name: str):
            query = f"CREATE CONSTRAINT FOR (a:{node_label}) REQUIRE a.{property_name} IS UNIQUE"
            result = tx.run(query)
            return result.consume().counters

        index = self.execute_write(
            create_node_index, node_label=node_label, property_name=property_name
        )
        return index

    def create_node(
        self, tx: Transaction, node_label: str, properties: dict, identifier: str = "id"
    ) -> dict:
        """
        Create a node with given label and properties.

        Args:
            tx (Transaction): Neo4j transaction.
            node_label (str): Label for the node.
            properties (dict): Properties for the node.

        Returns:
            dict: The result of the operation.
        """
        # TODO: Student: Create node
        # (fixme, neo4j): Build a Cypher query to create a node with a specific label and properties.
        # The identifier is the property that will be used to identify the node.
        # The method format_dict_for_cypher is used to format the properties.
        # Example: format_dict_for_cypher({"name": "John Doe"}) -> "{name: 'John Doe'}"
        
        identifier_value = properties.get(identifier)
        properties = format_dict_for_cypher(properties)
        query = f"CREATE (n:{node_label} {properties}) RETURN n"

        result = tx.run(query, identifier_value=identifier_value, properties=properties)

        return result.single()

    def read_node(
        self,
        tx: Transaction,
        node_label: str,
        properties: dict,
        many: bool = False,
        limit: int = None,
        sort: tuple = None,
    ) -> dict:
        """
        Read nodes with the given label and properties, with optional sorting and limiting.
        """
        properties = format_dict_for_cypher(properties)
        
        # Construction de la requête Cypher
        query = f"MATCH (u:{node_label} {properties}) RETURN u"
        print(query)
        # Ajout des fonctionnalités de tri et de limitation
        if sort is not None:
            field, order = sort
            query += f" ORDER BY u.{field} {order.upper()}"
        if limit is not None:
            query += f" LIMIT {limit}"

        # Exécution de la requête
        result = tx.run(query)
        result_data = result.data()

        # Formatage du résultat
        if many:
            result_to_return = {"result": [record['u'] for record in result_data]}
        else:
            # Accès direct aux propriétés du premier nœud
            result_to_return = result_data[0]['u'] if result_data else {}

        return result_to_return




    def update_node(
        self,
        tx: Transaction,
        node_label: str,
        match_properties: dict,
        set_properties: dict,
    ) -> dict:
        """
        Update nodes with the given label and matching properties.
        """

        # Utiliser format_dict_for_cypher pour formater les propriétés
        formatted_match = format_dict_for_cypher(match_properties)
        formatted_set = format_dict_for_cypher(set_properties)

        #Construire les parties de la clause SET de manière dynamique
        set_clauses = []
        for key, value in set_properties.items():
            # Si la valeur est un nombre, la traiter comme telle, sinon la traiter comme une chaîne
            if isinstance(value, (int, float)):
                set_clauses.append(f"n.{key} = {value}")
            else:
                set_clauses.append(f"n.{key} = '{value}'")

        set_clause = ', '.join(set_clauses)

        # Construire la requête Cypher
        query = (
            f"MATCH (n:{node_label} {formatted_match}) "
            f"SET {set_clause} "
            f"RETURN n AS a"
        )

        # Exécuter la requête et retourner le résultat
        result = tx.run(query)
        return result.data()

   
    def delete_node(self, tx: Transaction, node_label: str, properties: dict) -> dict:

        # Formater les propriétés pour la requête Cypher
        formatted_properties = format_dict_for_cypher(properties)
    
        # Construire la requête Cypher
        query = (
            f"MATCH (n:{node_label} {formatted_properties}) "
            "WITH n "
            "ORDER BY ID(n) "
            "LIMIT 1 "
            "OPTIONAL MATCH (n)-[r]-() "
            "DELETE r, n "
            "RETURN COUNT(n) AS nodes_deleted"
        )

    
        # Exécuter la requête et obtenir le résultat
        result = tx.run(query)
        counters_dict = result.consume().counters
 
        print(counters_dict)
        return counters_dict

    def create_relationship(
        self,
        tx: Transaction,
        start_node_label,
        start_node_properties,
        end_node_label,
        end_node_properties,
        relation_type,
    ) -> dict:
        # Formater les propriétés pour la requête Cypher
        formatted_start_node_properties = format_dict_for_cypher(start_node_properties)
        formatted_end_node_properties = format_dict_for_cypher(end_node_properties)

        # Vérifier l'existence des nœuds et les créer si nécessaire
        query_check_create_start = (
            f"MERGE (a:{start_node_label} {formatted_start_node_properties}) "
            "RETURN a"
        )
        query_check_create_end = (
            f"MERGE (b:{end_node_label} {formatted_end_node_properties}) "
            "RETURN b"
        )
        tx.run(query_check_create_start)
        tx.run(query_check_create_end)

        # Construire la requête Cypher pour créer la relation
        query_create_relation = (
            f"MATCH (a:{start_node_label} {formatted_start_node_properties}), "
            f"(b:{end_node_label} {formatted_end_node_properties}) "
            f"CREATE (a)-[r:{relation_type}]->(b) "
            "RETURN a, type(r) AS relationType, b"
        )

        # Exécuter la requête et obtenir le résultat
        result = tx.run(query_create_relation)
        result_data = result.data()


        # Extraire et retourner les informations pertinentes
        if result_data:
            start_node, relation_type, end_node = result_data[0]['a'], result_data[0]['relationType'], result_data[0]['b']
            return (start_node, relation_type, end_node)
        else:
            return None


    def read_relationship(
        self,
        tx: Transaction,
        start_node_label,
        start_node_properties,
        end_node_label,
        end_node_properties,
        relation_type,
        many=False,
        sort: tuple = None,
    ) -> dict:
        """
        Read a relationship between two nodes.

        Args:
            tx (Transaction): Neo4j transaction.
            start_node_label (str): Label for the starting node.
            start_node_properties (dict): Properties for the starting node.
            end_node_label (str): Label for the ending node.
            end_node_properties (dict): Properties for the ending node.
            relation_type (str): Type of relationship.

        Returns:
            dict: The relationship read.
        """
        # TODO: Read Relationship
        # (fixme, neo4j): Build a Cypher query to read a relationship between two nodes.
        # You can use the `format_dict_for_cypher` method to format the properties.
        # Make sure to manage the case where we want to return many relationships or just one relationship.
        start_node_properties = format_dict_for_cypher(start_node_properties)
        end_node_properties = format_dict_for_cypher(end_node_properties)
    
        query = (
            f"MATCH (a:{start_node_label} {start_node_properties})-"
            f"[r:{relation_type}]->(b:{end_node_label} {end_node_properties}) "
            "RETURN a, type(r) AS relationType, b"
        )

        print(query)

        result = tx.run(query)

        if many:
            return [record for record in result]
        else:
            record = result.single()
            if record:
                return (record['a'], record['relationType'], record['b'])
            else:
                return None

    def update_relationship(
        self,
        tx: Transaction,
        start_node_label,
        start_node_properties,
        end_node_label,
        end_node_properties,
        relation_type,
        new_properties,
    ) -> dict:
        """
        Update a relationship between two nodes.

        Args:
            tx (Transaction): Neo4j transaction.
            start_node (dict): Starting node properties.
            end_node (dict): Ending node properties.
            relationship_type (str): Type of relationship.
            properties (dict): New properties for the relationship.

        Returns:
            dict: The relationship updated.
        """
        # TODO: Update Relationship
        # (fixme, neo4j): Build a Cypher query to update a relationship between two nodes.
        # You can use the `format_dict_for_cypher` method to format the properties.
        formatted_start_node_properties = format_dict_for_cypher(start_node_properties)
        formatted_end_node_properties = format_dict_for_cypher(end_node_properties)
        formatted_new_properties = format_dict_for_cypher(new_properties)

        # Construire la requête Cypher avec LIMIT pour cibler une seule relation
        query = (
            f"MATCH (a:{start_node_label} {formatted_start_node_properties})-"
            f"[r:{relation_type}]->(b:{end_node_label} {formatted_end_node_properties}) "
            "WITH r LIMIT 1 "
            f"SET r += {formatted_new_properties} "
            "RETURN r"
        )

        # Exécution de la requête et récupération du résultat
        result = tx.run(query)
        record = result.single()

        # Préparation et retour des informations de mise à jour
        if record:
            counters_dict = result.consume().counters
            return counters_dict
        else:
            return None



    def delete_relationship(
        self,
        tx: Transaction,
        start_node_label,
        start_node_properties,
        end_node_label,
        end_node_properties,
        relation_type,
    ) -> dict:
        # Assurez-vous que start_node_properties et end_node_properties sont correctement formatés pour être utilisés dans une clause WHERE.
          
        start_node_properties = format_dict_for_cypher(start_node_properties)
        end_node_properties = format_dict_for_cypher(end_node_properties)
 
        query = (
            f"MATCH (a:{start_node_label} {start_node_properties})-[r:{relation_type}]->(b:{end_node_label} {end_node_properties}) "
            "WITH r LIMIT 1 " 
            "DELETE r "
            "RETURN COUNT(r) AS relationships_deleted"
        )

        result = tx.run(query)
        counters_dict = result.consume().counters

        return counters_dict




    @handle_db_operations
    def create(self, tx_type: str, **kwargs):
        """
        Create a node with the given label and properties.

        Args:
            tx (Transaction): Neo4j transaction.
            node_label (str): Label for the node.
            properties (dict): Properties for the node.

        Returns:
            dict: The result of the operation.
        """
        
        if tx_type == "node":
            return self.execute_write(
                self.create_node,
                node_label=kwargs["node_label"],
                properties=kwargs["properties"],
                identifier=kwargs["identifier"],
            )
        if tx_type == "relationship":
            return self.execute_write(
                self.create_relationship,
                start_node_label=kwargs["start_node_label"],
                start_node_properties=kwargs["start_node_properties"],
                end_node_label=kwargs["end_node_label"],
                end_node_properties=kwargs["end_node_properties"],
                relation_type=kwargs["relation_type"],
            )

    @handle_db_operations
    def read(self, tx_type: str, custom_query=None, **kwargs):
        """
        Read nodes or relationships with the given label and properties,
        or execute a custom Cypher query.

        Args:
            tx (Transaction): Neo4j transaction.
            tx_type (str): Type of transaction ('node' or 'relationship').
            custom_query (str, optional): Custom Cypher query to execute.
            kwargs: Other parameters for the node or relationship query.

        Returns:
            dict: The result of the operation.
        """
        if custom_query:
            return self.execute_read(
                lambda tx: tx.run(custom_query).data()
            )
        
        if tx_type == "node":
            return self.execute_read(
                self.read_node,
                node_label=kwargs["node_label"],
                properties=kwargs["properties"],
                many=kwargs.get("many", False),
                limit=kwargs.get("limit", None),
                sort=kwargs.get("sort", None),
            )

        if tx_type == "relationship":
            return self.execute_read(
                self.read_relationship,
                start_node_label=kwargs["start_node_label"],
                start_node_properties=kwargs["start_node_properties"],
                end_node_label=kwargs["end_node_label"],
                end_node_properties=kwargs["end_node_properties"],
                relation_type=kwargs["relation_type"],
                many=kwargs.get("many", False),
            )


    @handle_db_operations
    def update(self, tx_type: str, **kwargs):
        """
        Update nodes with the given label and matching properties.

        Args:
            tx (Transaction): Neo4j transaction.
            node_label (str): Label for the node.
            match_properties (dict): Properties to match.
            set_properties (dict): Properties to set.

        Returns:
            dict: The result of the operation.
        """
        if tx_type == "node":
            return self.execute_write(
                self.update_node,
                node_label=kwargs["node_label"],
                match_properties=kwargs["match_properties"],
                set_properties=kwargs["set_properties"],
            )
        if tx_type == "relationship":
            return self.execute_write(
                self.update_relationship,
                start_node_label=kwargs["start_node_label"],
                start_node_properties=kwargs["start_node_properties"],
                end_node_label=kwargs["end_node_label"],
                end_node_properties=kwargs["end_node_properties"],
                relation_type=kwargs["relation_type"],
                new_properties=kwargs["new_properties"],
            )

    @handle_db_operations
    def delete(self, tx_type: str, **kwargs):
        """
        Delete nodes with the given label and properties.

        Args:
            tx (Transaction): Neo4j transaction.
            node_label (str): Label for the node.
            properties (dict): Properties for the node.

        Returns:
            dict: The result of the operation.
        """
        if tx_type == "node":
            return self.execute_write(
                self.delete_node,
                node_label=kwargs["node_label"],
                properties=kwargs["properties"],
            )
        if tx_type == "relationship":
            return self.execute_write(
                self.delete_relationship,
                start_node_label=kwargs["start_node_label"],
                start_node_properties=kwargs["start_node_properties"],
                end_node_label=kwargs["end_node_label"],
                end_node_properties=kwargs["end_node_properties"],
                relation_type=kwargs["relation_type"],
            )
