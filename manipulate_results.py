import neo4j
import pyvis
from neo4j_driver import Neo4jConnection


def transform_to_df():
    # Create connection
    neo4j_conn = Neo4jConnection()
    
    try:
        # Verify connectivity
        driver = neo4j_conn._Neo4jConnection__driver
        driver.verify_connectivity()

        pandas_df = driver.execute_query(
            "UNWIND range(1, 10) AS n RETURN n, n+1 AS m",
            database_="neo4j",
            result_transformer_=neo4j.Result.to_df
        )
        print(pandas_df)
    finally:
        # Always close the connection
        neo4j_conn.close()
        print("Connection closed.")

def transform_to_graph(query_graph, nodes_text_properties):
    visual_graph = pyvis.network.Network()

    for node in query_graph.nodes:
        node_label = list(node.labels)[0]
        node_text = node[nodes_text_properties[node_label]]
        visual_graph.add_node(node.element_id, node_text, group=node_label)

    for relationship in query_graph.relationships:
        visual_graph.add_edge(
            relationship.start_node.element_id,
            relationship.end_node.element_id,
            title=relationship.type
        )

    visual_graph.show('network.html', notebook=False)

if __name__ == "__main__":
    transform_to_df()