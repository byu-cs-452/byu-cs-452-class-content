-- 100,000 papers, 1,000,000 citations (each paper cites 10 distinct others).
-- Same pairs as measure_neo4j.cypher.
--
--   docker run -d --name pgsize -e POSTGRES_PASSWORD=pw postgres:16
--   docker exec -i pgsize psql -U postgres -q < measure_postgres.sql
\timing off
DROP TABLE IF EXISTS cites, papers, cites_u, papers_u;

-- Variant A: auto-incrementing BIGINT ids (the common case)
CREATE TABLE papers (id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY);
INSERT INTO papers OVERRIDING SYSTEM VALUE SELECT g FROM generate_series(0, 99999) g;
CREATE TABLE cites (
  citing_id BIGINT NOT NULL REFERENCES papers(id),
  cited_id  BIGINT NOT NULL REFERENCES papers(id),
  PRIMARY KEY (citing_id, cited_id)
);
INSERT INTO cites
SELECT i / 10, ((i / 10) + 1 + (i % 10) * 9973) % 100000
FROM generate_series(0, 999999) i;
CREATE INDEX cites_cited_idx ON cites (cited_id);   -- for "who cites me?"

-- Variant B: UUID ids
CREATE TABLE papers_u (id UUID PRIMARY KEY);
INSERT INTO papers_u SELECT md5(g::text)::uuid FROM generate_series(0, 99999) g;
CREATE TABLE cites_u (
  citing_id UUID NOT NULL REFERENCES papers_u(id),
  cited_id  UUID NOT NULL REFERENCES papers_u(id),
  PRIMARY KEY (citing_id, cited_id)
);
INSERT INTO cites_u
SELECT md5(((i / 10))::text)::uuid, md5((((i / 10) + 1 + (i % 10) * 9973) % 100000)::text)::uuid
FROM generate_series(0, 999999) i;
CREATE INDEX cites_u_cited_idx ON cites_u (cited_id);

VACUUM ANALYZE;
SELECT count(*) AS citations FROM cites;

SELECT c.relname AS object,
       CASE c.relkind WHEN 'r' THEN 'table' ELSE 'index' END AS kind,
       pg_relation_size(c.oid) AS bytes,
       pg_size_pretty(pg_relation_size(c.oid)) AS size
FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname = 'public' AND c.relkind IN ('r','i')
ORDER BY c.relname;
