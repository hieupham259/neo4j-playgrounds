from db.connection import Neo4jConnection


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