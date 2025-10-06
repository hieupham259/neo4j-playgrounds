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