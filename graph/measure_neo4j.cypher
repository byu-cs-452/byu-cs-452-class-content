// 100,000 papers, 1,000,000 CITES relationships (each paper cites 10 distinct others).
// Same pairs as measure_postgres.sql. Run against an EMPTY database so node ids are 0..99999.
//
//   docker run -d --name neosize -e NEO4J_AUTH=neo4j/password123 \
//     -e NEO4J_db_store_files_preallocate=false neo4j:5-community
//   docker exec -i neosize cypher-shell -u neo4j -p password123 < measure_neo4j.cypher
//   docker stop neosize      # flushes the store files to disk
//   docker cp neosize:/data/databases/neo4j - | tar tvf - | grep store.db
//
// db.store.files.preallocate=false stops Neo4j from growing files in big chunks ahead of time,
// so the file sizes show what the records actually use.

UNWIND range(0, 99999) AS i CREATE (:Paper);

UNWIND range(0, 999999) AS i
CALL {
  WITH i
  MATCH (a) WHERE id(a) = i / 10
  MATCH (b) WHERE id(b) = ((i / 10) + 1 + (i % 10) * 9973) % 100000
  CREATE (a)-[:CITES]->(b)
} IN TRANSACTIONS OF 50000 ROWS;

MATCH ()-[r:CITES]->() RETURN count(r) AS citations;
SHOW DATABASE neo4j YIELD name, store;
