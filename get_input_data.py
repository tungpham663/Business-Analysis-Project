from graph import Neo4jGraph
from paragraphs_db import search_samples_by_keyword, connect_to_db

def get_input_data(keywords):
    #graph initialization
    URI = "bolt://localhost:7687"  # Replace with your Neo4j URI
    USERNAME = "neo4j"             # Default username
    PASSWORD = "12345678"     # Replace with your Neo4j password
    graph = Neo4jGraph(URI, USERNAME, PASSWORD)
    #connect to paragraphs database
    connect_to_db()
    paragraphs =''
    relationships =[]
    for keyword in keywords:
        paragraphs += search_samples_by_keyword(keyword)
        relationships += graph.get_rel_depth2(keyword)['relationships_depth_2']
    graph.close()
    return paragraphs, relationships