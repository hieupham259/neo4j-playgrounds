import neo4j
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

if __name__ == "__main__":
    transform_to_df()