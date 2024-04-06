"""
Section Service
"""
# pylint: disable=W0212
from src.db.neo4j_db import Neo4jDB


class SectionService:
    """
    Class to manage project operations.
    """

    def __init__(self, neo4j: Neo4jDB = None):
        self.neo4j = neo4j


    def get_options_for_question(self, question_id: str) -> list:
        """
        Get options for a question.

        Args:
            question_id (str): The question ID.

        Returns:
            List[dict]: The options.
        """
        # hint: This method can inspire you to implement some with relationships.
        options = self.neo4j.read(
            tx_type="relationship",
            start_node_label="Question",
            start_node_properties={"id": question_id},
            end_node_label="Option",
            end_node_properties={},
            relation_type="HAS_OPTION",
            many=True
        ).get("result")
        # the key 2 is the right part of the relationship where 0 is the left part and 1 is the relationship
        options = [option[2] for option in options]
        return options

    def get_sections(self) -> list:
        """
        Get all sections.
        """
        sort_criteria = ("order", "asc")
        sections = self.neo4j.read(tx_type="node", node_label="Section", properties={},many=True, sort=sort_criteria).get("result")

        print(sections)
        print(sections.get('result', []))

        return sections.get('result', [])

    def get_section_by_property(self, property: str, value: str) -> dict:
        """
        Get a section by a specific property.

        Args:

            property (str): The property to be used to get the section.
            value (str): The value of the property.

        Returns:
            dict: The section.
        """
        # TODO:(neo4j) Get Section Info by property
        # Implement this method to get a section from neo4j by a specific property.
        # (fixme, neo4j): You can use the `read` method of the Neo4jDB class to get a node of Label
        # Section by a specific property.
        dico = {property: value}
        section = self.neo4j.read(tx_type="node", node_label="Section", properties=dico).get("result")
        # placeholder

        return section

    def get_next_section(self, section_id: str) -> dict:
        # Query for the current section using its ID
        dico = {"id": section_id}
        current_section = self.neo4j.read(tx_type="node", node_label="Section", properties=dico).get("result")

        print(current_section)

        if not current_section:
            # Handle the case where the current section is not found
            print(f"Current section with ID {section_id} not found.")
            return {}

        # Get the order of the current section and determine the next section's order
        current_section_order = current_section['order']
        next_section_order = current_section_order + 1

        # Query for the next section
        dico_next = {"order": next_section_order}
        print(dico_next)
        next_section = self.neo4j.read(tx_type="node", node_label="Section", properties=dico_next).get("result")

        print(next_section)

        if not next_section:
            # Handle the case where the next section is not found
            print(f"Next section with order {next_section_order} not found.")
            return {}

        return next_section


    def get_questions_for_section(self, section_id: str) -> list:
        """
        Get all questions for a section.

        Args:
            section_id (str): The section ID.

        Returns:
            List[dict]: The questions.
        """
        # Get all Question nodes related to the section
        questions = self.neo4j.read(
            tx_type="relationship",
            start_node_label="Section",
            start_node_properties={"id": section_id},
            end_node_label="Question",
            end_node_properties={},
            relation_type="HAS_QUESTION",
            many=True,
        ).get("result")
        
        questions_processed = []
        for relation in questions:
            # Extract the Node object for the question
            question_node = relation[2]  # Adjust index based on the structure of your result

            # Convert the Node object to a dictionary
            question_dict = dict(question_node.items())

            questions_processed.append(question_dict)

        questions_processed = sorted(questions_processed, key=lambda x: x['order'])

        print(questions_processed)

        return questions_processed



    # Other class methods and attributes...



    def get_next_questions(self, question_id: str, option_text: str) -> list:
        # Dictionnaire pour faire correspondre le noeud de départ ('Option')
        start_node_properties = {"question_id": question_id, "text": option_text}

        try:
            related_questions_data = self.neo4j.read(
                tx_type="relationship",
                relation_type="LEADS_TO",
                start_node_label="Option",
                end_node_label="Question",
                start_node_properties=start_node_properties,
                end_node_properties={}
            ).get("result")
        except Exception as e:
            print(f"Erreur survenue lors de la récupération des questions liées : {e}")
            return []

        if not related_questions_data or not isinstance(related_questions_data, tuple):
            print("Aucune question liée trouvée ou format de données invalide.")
            return []

        next_questions = []

        if len(related_questions_data) >= 3 and hasattr(related_questions_data[2], '_properties'):
            question_node = related_questions_data[2]
            question_props = question_node._properties

            # Préparation de la requête Cypher personnalisée pour les options
            custom_query_options = f"MATCH (q:Question {{id: '{question_props['id']}'}})-[:HAS_OPTION]->(o:Option) RETURN o"
            try:
                options_data = self.neo4j.read(
                    tx_type="relationship",
                    custom_query=custom_query_options
                )
                options = [{"text": opt["o"]["text"]} for opt in options_data.get("result", [])]
                options.sort(key=lambda x: x["text"] != "React")
            except Exception as e:
                print(f"Erreur lors de la récupération des options pour la question {question_props['id']} : {e}")
                options = []

            # Ajouter les champs manquants
            next_questions.append({
                "id": question_props['id'],
                "statement": question_props.get("statement", "Statement not provided"),
                "question_type": question_props.get("question_type", "Type not provided"),
                "section_id": question_props.get("section_id", "Section ID not provided"),
                "order": question_props.get("order", 0),
                "options": options
            })
        else:
            print("Format de données related_questions_data inattendu")

        return next_questions
    
