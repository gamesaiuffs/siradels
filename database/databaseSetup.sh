#!/bin/bash
#!/bin/bash
docker run --name postgres-pesquisa-ia \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_DB=ia \
  -p 5432:5432 \
  -v pgdata-ia:/var/lib/postgresql/data \
  -v "${pwd}../backup/":/backup \
  -d postgres:15-alpine