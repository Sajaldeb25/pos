<h1 align="center">
  <img alt="cgapp logo" src="https://raw.githubusercontent.com/create-go-app/cli/master/.github/images/cgapp_logo%402x.png" width="224px"/><br/>
 Book and Author information GraphQL API
</h1>
<p align="center">A GraphQL server using <b>backend</b> (Golang) <b>database</b> (Postgres) containerised with (Docker)!</p>

<p align="center"><a href="#" 
target="_blank"><img src="https://img.shields.io/badge/Go-1.17+-00ADD8?style=for-the-badge&logo=go" alt="go version" /></a>&nbsp;<a href="#" target="_blank"><img src="https://img.shields.io/badge/-GraphQL-E10098?style=for-the-badge&logo=graphql&logoColor=white" alt="GraphQL" /></a>&nbsp;<a href="#" target="_blank"></a></p>

## 📖 Problem 

Build a simple graphql server with any database you prefer ( in-memory map[string]interface{} will do just fine ) that can perform this simple task. Finding books of all the authors and vice versa.
## ⚡️ Quick start
```shell
Using docker
     $ go test ./...  # run from root of the project directory 
     $ docker-compose down --volume # to make sure to remove shared volume
     $ docker-compose up --build --force-recreate # here --force-recreate is optional
```
🔔 `Note`If you interested to run it from locally without Docker please ensure database and .env properly configured
- >go run /cmd/app/main.go
>Example .env file
>>_GIN_PORT=8080 \
GIN_MODE=debug \
DB_HOST=localhost \
DB_PORT=5432 \
DB_USER=test \
DB_PASSWORD=test \
DB_NAME=test_

### ✍️ Populate demo data
> for populating demo data please visit `localhost:port/load-data`

🤾‍♂️ `Let's visit localhost:port and expolre my graphql api`
# 📋 Folder Structure 
```
book-info-graphql
├── build
│    ├── Dockerfile
│    ├── init.sql
├── cmd
│    ├── app
│    │    ├── config
│    │    │  └── loader.go
│    │    └── main.go
├── graph
│    ├── ***                  - All graph related code along with auto generated code
├── internal
│    └── app
│         ├── adapter         - Outer layer. All framework and external database and middlewares related code 
│         ├── application     - Middle layer. Usecase or buniness logic relaed code
│         │    └── usecase
│         └── domain          - Inner layer. Domain, interface and factory related code
│              ├── interface
│              └── factory
└── .env
```
# ❓ GraphQl query
![A test image](graph_ql_example.png)

```graphql
# For Getting author data
query{
    authors(name: "Hasan"){
        name, books{
            id, title
        }
    }
}
# For getting books data

query{
    books{
        id, title, authors{
            id, name
        }
    }
}
```