from neo4j import GraphDatabase
from utils import calculate_months_difference


# Neo4j class to handle the graph operations
class Neo4jGraph:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self.driver.close()

    # Create nodes
    def create_nodes(self, entities):
        with self.driver.session() as session:
            for entity in entities:
                session.write_transaction(self._create_node, entity['Entity Name'], entity['Entity Type'])
    
    @staticmethod
    def _create_node(tx, name, entity_type):
        query = """
        MERGE (n:Entity {name: $name})
        ON CREATE SET n.type = $type
        """
        tx.run(query, name=name, type=entity_type)

    # Create relationships
    def create_relationships(self, relationships):
        with self.driver.session() as session:
            for rel in relationships:
                session.write_transaction(
                    self._create_relationship, 
                    rel['Entity 1'], 
                    rel['Entity 2'], 
                    rel['Relationship'], 
                    rel['Description'],
                    rel['Classification'], 
                    rel['Time']
                )
    
    @staticmethod
    def _create_relationship(tx, entity1, entity2, relationship, description, classification, time):
        query = """
        MATCH (a:Entity {name: $entity1})
        MATCH (b:Entity {name: $entity2})
        OPTIONAL MATCH (a)-[existing:RELATIONSHIP {name: $relationship}]->(b)
        FOREACH (_ IN CASE WHEN existing IS NULL THEN [1] ELSE [] END |
            MERGE (a)-[r:RELATIONSHIP {name: $relationship}]->(b)
            ON CREATE SET 
                r.description = $description,
                r.classification = $classification,
                r.time = $time,
                r.score = 1
            ON MATCH SET
                r.score = coalesce(r.score, 0) + 1, 
                r.description = r.description + ' | ' + $description
        )
        """
        tx.run(query, entity1=entity1, entity2=entity2, relationship=relationship, 
            description=description, classification=classification, time=time)


    # Delete a node by name
    def delete_node(self, node_name):
        with self.driver.session() as session:
            session.write_transaction(self._delete_node, node_name)

    @staticmethod
    def _delete_node(tx, node_name):
        query = """
        MATCH (n:Entity {name: $name})
        DETACH DELETE n
        """
        tx.run(query, name=node_name)
        print(f"Node '{node_name}' deleted successfully.")

    # Delete a relationship by type between two entities
    def delete_relationship(self, entity1, entity2, relationship_type):
        with self.driver.session() as session:
            session.write_transaction(self._delete_relationship, entity1, entity2, relationship_type)
    
    @staticmethod
    def _delete_relationship(tx, entity1, entity2, relationship_type):
        query = """
        MATCH (a:Entity {name: $entity1})-[r:RELATIONSHIP {type: $relationship_type}]->(b:Entity {name: $entity2})
        DELETE r
        """
        tx.run(query, entity1=entity1, entity2=entity2, relationship_type=relationship_type)
        print(f"Relationship '{relationship_type}' between '{entity1}' and '{entity2}' deleted successfully.")

    # Delete all nodes and relationships
    def delete_all(self):
        with self.driver.session() as session:
            session.write_transaction(self._delete_all)
    
    @staticmethod
    def _delete_all(tx):
        query = """
        MATCH (n)
        DETACH DELETE n
        """
        tx.run(query)
        print("All nodes and relationships have been deleted.")

    # Function to print all nodes and relationships using the driver
    def print_all(self):
        with self.driver.session() as session:
            session.read_transaction(self._print_all_nodes_and_relationships)

    @staticmethod
    def _print_all_nodes_and_relationships(tx):
        # Query to retrieve all nodes
        nodes_query = """
        MATCH (n)
        RETURN n.name AS name, n.type AS type
        """
        
        # Query to retrieve all relationships
        relationships_query = """
        MATCH (a)-[r]->(b)
        RETURN a.name AS Entity1, r.name AS Relationship, b.name AS Entity2, r.description AS Description
        """
        
        # Fetch and print nodes
        print("=== All Nodes ===")
        result_nodes = tx.run(nodes_query)
        for record in result_nodes:
            name = record["name"] or "N/A"
            type_ = record["type"] or "N/A"
            print(f"Node: Name='{name}', Type='{type_}'")
        
        # Fetch and print relationships
        print("\n=== All Relationships ===")
        result_relationships = tx.run(relationships_query)
        for record in result_relationships:
            entity1 = record["Entity1"] or "N/A"
            relationship = record["Relationship"] or "N/A"
            entity2 = record["Entity2"] or "N/A"
            description = record["Description"] or "N/A"
            print(f"Relationship: '{entity1}' -[{relationship}]-> '{entity2}' (Description: '{description}')")

    #Calculate node score
    def calculate_node_score(self):
        with self.driver.session() as session:
            session.write_transaction(self._calculate_node_score)
    
    @staticmethod
    def _calculate_node_score(tx, node_name):
        query = """
        MATCH (n:Entity {name: $name})-[r:RELATIONSHIP]->()
        RETURN r.classification AS classification, r.time AS time, r.score AS score
        """
        result = tx.run(query, name=node_name)
        score = 0

        for record in result:
            if record["classification"] == "Short-term":
                time = record["time"]
                months_gap = calculate_months_difference(time)
                if months_gap <= 3:
                    score += record["score"]
        return score

    # Function to find the node with the maximum score
    def find_node_with_max_score(self):
        with self.driver.session() as session:
            return session.read_transaction(self._find_node_with_max_score)

    @staticmethod
    def _find_node_with_max_score(tx):
        query = """
        MATCH (n:Entity)
        RETURN n.name AS name, n.type AS type
        """
        nodes = tx.run(query)
        max_score = -1
        max_score_node = None

        for record in nodes:
            node_name = record["name"]
            node_type = record["type"]
            score = Neo4jGraph._calculate_node_score(tx, node_name)

            if score > max_score:
                max_score = score
                max_score_node = {
                    "name": node_name,
                    "type": node_type,
                    "score": score
                }
        return max_score_node

    def get_rel_depth2(self, keyword=""):
        with self.driver.session() as session:
            return session.read_transaction(self._get_relationships_depth_2, keyword)
    
    @staticmethod
    def _get_relationships_depth_2(tx, keyword):
        # Step 1: Determine the node name based on the keyword
        if not keyword:
            node = Neo4jGraph._find_node_with_max_score(tx)
            node_name = node["name"]
            node_type = node["type"]
        else:
            query_node = """
            MATCH (n:Entity)
            WHERE n.name = $keyword OR n.name CONTAINS $keyword
            RETURN n.name AS name, n.type AS type
            """
            result = tx.run(query_node, keyword=keyword).single()
            node_name = result["name"] if result else None
            node_type = result["type"] if result else None

        if not node_name:
            return {"message": "No matching node found."}
        
        # Step 2: Fetch relationships up to depth 2 for the node
        query = """
        MATCH (n:Entity {name: $name})-[r1:RELATIONSHIP]-(m:Entity)
        OPTIONAL MATCH (m)-[r2:RELATIONSHIP]-(o:Entity)
        WHERE o <> n
        RETURN DISTINCT 
            m.name AS level1_node, 
            r1.name AS level1_relationship, 
            r1.description AS level1_description,
            o.name AS level2_node, 
            r2.name AS level2_relationship, 
            r2.description AS level2_description
        """
        result = tx.run(query, name=node_name)
        relationships = []

        for record in result:
            level1_node = record["level1_node"] 
            level1_relationship = record["level1_relationship"] 
            level1_description = record["level1_description"]
            level2_node = record["level2_node"] or "N/A"
            level2_relationship = record["level2_relationship"] or "N/A"
            level2_description = record["level2_description"] or "N/A"
            if f"Relationship: '{node_name}' -[{level1_relationship}]-> '{level1_node}' (Description: '{level1_description}')" not in relationships:
                relationships.append(f"Relationship: '{node_name}' -[{level1_relationship}]-> '{level1_node}' (Description: '{level1_description}')")
            if level2_node != "N/A" and f"Relationship: '{level1_node}' -[{level2_relationship}]-> '{level2_node}' (Description: '{level2_description}')" not in relationships:
                relationships.append(f"Relationship: '{level1_node}' -[{level2_relationship}]-> '{level2_node}' (Description: '{level2_description}')")
        
        return {
            "node_name": node_name,
            "node_type": node_type,
            "relationships_depth_2": relationships
        }
    
    # Function to check if a keyword exists within the 'name' property of any node
    def node_keyword_exists(self, keyword):
        with self.driver.session() as session:
            return session.read_transaction(self._node_keyword_exists, keyword)

    @staticmethod
    def _node_keyword_exists(tx, keyword):
        query = """
        MATCH (n:Entity)
        WHERE n.name CONTAINS $keyword
        RETURN COUNT(n) AS count
        """
        result = tx.run(query, keyword=keyword)
        record = result.single()
        return record["count"] > 0 if record else False



