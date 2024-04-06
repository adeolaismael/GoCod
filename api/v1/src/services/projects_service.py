"""
Project Service
"""
# pylint: disable=W0212
import logging
from bson.objectid import ObjectId
from src.utils.parsing import parse_mongo_id
from src.db.mongo_db import MongoDB
from src.db.neo4j_db import Neo4jDB
from src.utils.handlers import handle_db_operations

class ProjectService:
    """
    Class to manage project operations.
    """

    def __init__(self, mongo: MongoDB = None, neo4j: Neo4jDB = None):  # type: ignore
        self.mongo = mongo
        self.neo4j = neo4j

    @handle_db_operations
    def create_project(self, project_data: dict):
        """
        Create a project with the `project_data` object.

        Args:
            project_data (dict): The project data to be inserted.

        Returns:
            str: The ID of the inserted project.
        """
        insert_result = self.mongo.create(project_data, "projects").get("result")
        project_data = parse_mongo_id(project_data, "project")
        project_data["id"] = project_data["pid"]
        
        project_id = project_data["id"]

        print(project_data["id"])
        
                # Insertion dans Neo4j
        if self.neo4j:
            # Assurez-vous que cette méthode existe et fonctionne correctement
            self.neo4j.create(tx_type="node", node_label="Project", properties=project_data, identifier=str(project_id))

        print("Created Verification Result from Neo4j:", project_id)

        return str(project_id)

    @handle_db_operations
    def read_project(self, project_id: str):
        """
        Read a project with the `project_id` object.

        Args:
            project_id (str): The project id to be read.

        Returns:
            str: The ID of the inserted project.
        """
        project = self.mongo.read(
            query={"_id": ObjectId(project_id)}, collection_name="projects"
        ).get("result")
        return project

    @handle_db_operations
    def update_project(self, project_id: str, project_data: dict):
        """
        Update a project with the `project_data` object.

        Args:
            project_data (dict): The project data to be updated.

        Returns:
            str: The ID of the updated project.
        """
        # TODO(mongo): Update project
        # (fixme, mongo): Update the project given their id and the data.
        # Refer to MongoDB documentation: https://docs.mongodb.com/manual/tutorial/update-documents/
        update_result = self.mongo.update(
            query={"_id": ObjectId(project_id)},
            document_data=project_data,
            collection_name="projects",
        ).get("result")
        return str(update_result)



    @handle_db_operations
    def delete_project(self, project_id: str):
        """
        Delete a project with the `project_id` object.

        Args:
            project_id (str): The project id to be deleted.

        Returns:
            str: The ID of the deleted project.
        """
        # Delete Project from MongoDB
        delete_result = self.mongo.delete(
            query={"_id": ObjectId(project_id)}, collection_name="projects"
        ).get("result")

        # Deletion from Neo4j
        delete_result_neo4j = None
        if self.neo4j:
            delete_result_neo4j = self.neo4j.delete(
                tx_type="node",
                node_label="Project",
                properties={"id": project_id}  # Ensure 'id' is the correct property
            )

        # Print the deletion results
        #print("MongoDB Deletion Result:", delete_result)
        #print("Neo4j Deletion Result:", delete_result_neo4j)

        # Post-deletion verification for Neo4j
        verification_result = None
        if self.neo4j:
            verification_query = "MATCH (p:Project {id: $project_id}) RETURN p"
            verification_result = self.neo4j.read(
                tx_type="node",
                node_label="Project",
                properties={"id": project_id},
                query=verification_query
            ).get("result")

            # Transform an empty dictionary to None
            #if verification_result == {}:
                #verification_result = None

            # Print the verification result
            print("Post-Deletion Verification Result from Neo4j:", verification_result)

        return str(delete_result)


    @handle_db_operations
    def list_projects(self, user_id: str):
        """
        List all projects for a user.

        Args:
            user_id (str): The ID of the user to list projects for.

        Returns:
            list: A list of projects.
        """
        #TODO(mongo): List projects
        # (fixme, mongo): Implement the listing of projects for a user.
        # You can use the `read` method of the MongoDB class.
        # Refer to MongoDB documentation: https://docs.mongodb.com/manual/tutorial/query-documents/
        projects = self.mongo.read(
            query={"created_by": user_id}, collection_name="projects", many=True
        ).get("result")
        return projects


    @handle_db_operations
    def select_template(self, project_id: str, template_id: str):
        """
        Select a public template for a project.

        Args:
            template_id (str): The ID of the template to select.
            project_id (str): The ID of the project to select the template for.

        Returns:
            str: The ID of the selected template.
        """
        # Vérifier l'existence du projet
        project = self.mongo.read(
            query={"_id": ObjectId(project_id)}, collection_name="projects"
        ).get("result")
        if project is None:
            raise Exception("Project not found")

        # Vérifier l'existence du template
        template = self.mongo.read(
            query={"_id": ObjectId(template_id)}, collection_name="templates"
        ).get("result")
        if template is None:
            raise Exception("Template not found")

        # Créer une relation entre le projet et le template dans Neo4j
        create_relation_select = self.neo4j.create(
            tx_type="relationship",
            relation_type="SELECTED",
            start_node_label="Project",
            end_node_label="Template",
            start_node_properties={"id": project_id},
            end_node_properties={"tid": template_id}
        )

            # Vérifier que la relation a été créée
        #verification_query = "MATCH (p:Project {id: $project_id})-[r:SELECTED]->(t:Template {tid: $template_id}) RETURN r"
        projects = self.neo4j.read(
            tx_type="relationship",
            relation_type="SELECTED",
            start_node_label="Project",
            end_node_label="Template",
            start_node_properties={"id": project_id},
            end_node_properties={}
        ).get("result")

        print(projects)

        return projects


    @handle_db_operations
    def get_recommended_templates(self, project_id: str):
        """
        Get recommended templates for a project.

        Args:
            project_id (str): The ID of the project to get the recommended templates for.

        Returns:
            list: A list of recommended templates.
        """
        # TODO(neo4j): Get recommended templates
        def find_recommended_templates(tx, project_id):
            # (fixme, neo4j): Implement this method to get recommended templates for a project.
            # Write the Cypher query to get recommended templates for a project.
            # Order the templates by the relevance score.
            query = """
            MATCH (p:Project {id: $project_id})
            WITH p, toLower(p.project_type) AS projectType

            MATCH (o:Option)
            WHERE toLower(o.text) = projectType

            WITH p, COLLECT(o) AS options

            MATCH (t:Template)
            WHERE ANY(o IN options WHERE ANY(tag IN o.tags WHERE toLower(tag) IN [ttag IN t.template_tags | toLower(ttag)]))

            WITH t, COUNT(DISTINCT options) AS relevanceScore
            RETURN t.template_name AS template_name
            ORDER BY relevanceScore DESC
            LIMIT 1

            """
            params = {'project_id': project_id}
            result = tx.run(query, params)
            print(query)
            return result.data()

        templates = self.neo4j.execute_read(find_recommended_templates, project_id=project_id)
        print(templates)
        return templates