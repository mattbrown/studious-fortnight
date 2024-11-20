# studious-fortnight


## Testing locally
- `poetry shell` will put your shell in the Python virtual env
- `poetry install` will install python dependancies

### Run unit tests 
`poetry run pytest`

### Start and setup database
1. `docker-compose up`
   1. Starts a postgresql DB running on port `5432`
2. [Login to the pgadmin portal](http://localhost:5050/) 
   - Username: `admin@admin.com`
   - Pass: `root`
3. In the portal, Create a new service. Name it `microblog`
   1. set the *host name* to `postgres`
   2. The service password is `root`
4. Repeat step 3 for a database named `test`
4. In the admin console, create a new database named `microblog`
