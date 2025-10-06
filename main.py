from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Neo4jConnection:
    def __init__(self):
        """Initialize Neo4j connection using environment variables"""
        uri = os.getenv("NEO4J_URI")
        user = os.getenv("NEO4J_USER")
        password = os.getenv("NEO4J_PASSWORD")
        
        if not all([uri, user, password]):
            raise ValueError("Missing required environment variables: NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD")
        
        self.__driver = GraphDatabase.driver(uri, auth=(user, password))
        
    def close(self):
        """Close the connection to Neo4j database"""
        if self.__driver:
            self.__driver.close()
            
    def query(self, query_string, parameters=None):
        """Execute a query string and return results"""
        with self.__driver.session() as session:
            result = session.run(query_string, parameters or {})
            return [record for record in result]
        
def query_graph(driver, query_string, parameters=None, database_name="neo4j"):
    """
    Execute a query using driver.execute_query and return records, summary, and keys
    
    Args:
        driver: Neo4j driver instance
        query_string: Cypher query string
        parameters: Dictionary of query parameters (optional)
        database_name: Name of the database to query (default: "neo4j")
    
    Returns:
        tuple: (records, summary, keys)
    """
    records, summary, keys = driver.execute_query(
        query_string,
        parameters or {},
        database_=database_name,
    )
    
    # Summary information
    print("The query `{query}` returned {records_count} records in {time} ms.".format(
        query=summary.query, 
        records_count=len(records),
        time=summary.result_available_after
    ))

    # Loop through results and do something with them
    for record in records:
        print(record.data())  # obtain record as dict

    return records, summary, keys

def get_all_nodes(driver, type="Person", database_name="neo4j"):
    """Fetch all nodes of a given type from the Neo4j database"""
    query_string = f"MATCH (n:{type}) RETURN n.name AS name"
    records, summary, keys = driver.execute_query(
        query_string,
        {},
        database_=database_name,
    )

    for i, record in enumerate(records):
        print(f"Record {i}: {record.data()}")

    return records, summary, keys


# Example usage of query_graph function
def example_query_graph(driver):
    """Example showing how to use the query_graph function"""    
    try:
        
        # Use query_graph function
        records, summary, keys = query_graph(
            driver=driver,
            query_string="""
                MATCH (p:Person)-[:KNOWS]->(:Person)
                RETURN p.name AS name
            """,
            database_name="neo4j"
        )
        
        # You can also work with the returned data
        print(f"\nKeys: {keys}")
        print(f"Total records: {len(records)}")
        
    finally:
        neo4j_conn.close()

# Usage example
if __name__ == "__main__":
    # Create connection
    neo4j_conn = Neo4jConnection()
    
    try:
        # Verify connectivity
        driver = neo4j_conn._Neo4jConnection__driver
        driver.verify_connectivity()
        print("Connected to Neo4j successfully!")
        
        # Execute query using query_graph function
        # records, summary, keys = query_graph(
        #     driver=driver,
        #     query_string="""
        #         CREATE (a:Person {name: $name})
        #         CREATE (b:Person {name: $friendName})
        #         CREATE (a)-[:KNOWS]->(b)
        #         RETURN a.name AS person1, b.name AS person2
        #     """,
        #     parameters={"name": "Bob 1", "friendName": "Bob 2"},
        #     database_name="neo4j"
        # )
        
        # print(f"\nQuery keys: {keys}")
        # print(f"Total records returned: {len(records)}")

        # example_query_graph(driver=driver)
        query_string = "MATCH (p:Person) RETURN p.name AS name"
        records, summary, keys = query_graph(driver=driver, query_string=query_string)
        
    finally:
        # Always close the connection
        neo4j_conn.close()
        print("Connection closed.")