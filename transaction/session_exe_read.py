from db.connection import Neo4jConnection


'''

Create a session. A single session can be the container for multiple queries. Unless created using the with construct, remember to close it when done.

The .execute_read() (or .execute_write()) method is the entry point into a transaction. It takes a callback to a transaction function and an arbitrary number of positional and keyword arguments which are handed down to the transaction function.

The transaction function callback is responsible of running queries.

Use the method Transaction.run() to run queries. Each query run returns a Result object.

Process the result using any of the methods on Result.
'''

def match_person_nodes(tx, name_filter):
    result = tx.run("""
        MATCH (p:Person) WHERE p.name STARTS WITH $filter
        RETURN p.name AS name ORDER BY name
        """, filter=name_filter)
    return list(result)  # a list of Record objects

if __name__ == "__main__":
    neo4j_conn = Neo4jConnection()
    driver = neo4j_conn._Neo4jConnection__driver  # access the underlying

    with driver.session(database="neo4j") as session:
        people = session.execute_read(
            match_person_nodes,
            "Bob",
        )
        for person in people:
            print(person.data())  # obtain dict representation