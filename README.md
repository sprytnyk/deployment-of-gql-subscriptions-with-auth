# Deployment of GraphQL Subscriptions in Python (with auth)

It's an example of how to make more or less dockerised, production-ready
GraphQL Subscriptions in Python on top of NGINX, Daphne, Supervisor that
encompasses authentication process to GraphQL queries and mutations, the same
about subscriptions itself, so your websocket connection will require a JWT
token to be subscribed to something.

More sophisticated permissions checks can be done inside
[Django model signals](https://docs.djangoproject.com/en/2.2/topics/signals/),
Python subscriptions
([graphene-subscriptions](https://github.com/jaydenwindle/graphene-subscriptions)),
and [Django Channels consumer](https://channels.readthedocs.io/en/2.x/topics/consumers.html).

## Versions used in this example

- Python 3.9.4

- Redis 6.2.6

  If you use Redis below version 5 then you need to have inside *requirements.txt*
  `channels-redis` pinned to version 2.4.2 otherwise you will receive
  `ERR unknown command 'BZPOPMIN'`

- PostgreSQL 14.0

- Django 2.2.24 LTS

- Nginx 1.21.3

- Supervisor 3.3.5

## Requirements

In order to interact with this example you need the fowolloing things:

- [Docker](https://docs.docker.com/engine/install/) & [Docker Compose](https://docs.docker.com/compose/install/)
- [GraphQL Playground](https://github.com/graphql/graphql-playground)
- [curl](https://curl.se/download.html)

## Dive into example

### Step 1

Assuming you installed all above requirements clone this repo and launch
docker containers:

```sh
$ git clone https://github.com/vald-phoenix/deployment-of-gql-subscriptions-with-auth.git
$ cd deployment-of-gql-subscriptions-with-auth
$ docker-compose up --build -d
```

After successful run of docker containers we need to obtain an access token:

```sh
$ curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "letmein"}' \
  http://localhost:8000/api/token/
# this will return something like this
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYzNDcyOTUzMywianRpIjoiODJkMTUyYzdiNjI0NGQwNzlhMTcwNTU0ZDI1MTI0MmQiLCJ1c2VyX2lkIjoxfQ.Gstb6RX4ga5yp9eosAPhRGJo1iNemGywvQYQqm7ZSjc",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM0NjQzNDMzLCJqdGkiOiJlNGFiNjQyZDgyM2Q0NmNmYmE1YTRjZWNhNzAyNDhhNCIsInVzZXJfaWQiOjF9.g-qqbTJZ5HiCez8d_VgveMn4Z95oTLo9rtFev0aDWqA"
}
# you need only access token value
```

Open GraphQL Playground and type into the address bar
`http://localhost:8000/graphql/` and hit OPEN button.

![Step 1](media/step_1.png)

### Step 2

Use the access token to make a GraphQL query like on the screenshot below,
just update headers, provide the query, and hit play button. It should return
hi back.

Query:

```
{
  hi
}
```

HTTP Headers:

```
{
  "Authorization": "Bearer your_access_token"
}
```



![Step 2](media/step_2.png)

If you provide an ivalid or wrong token it will throw a coressponding message:
![Wrong or invalid token](media/gql_query_wrong_token.png)

The same applies if you try to make GraphQL Subscription:

![Subscription wrong token](media/gql_subscription_wrong_token.png)

### Step 3

If you changed your valid token to see if it returns an error message make
sure it's valid one because we're going to make our first subscription. This
will wait for the update on `Car` model instance with a primary key 1.

Query:

```
subscription {
  carModelUpdated(pk: 1) {
    make
    model
  }
}
```

HTTP Headers (merged with `connectionParams` for websocket type of a
connection by Apollo Client,
[see this](https://www.apollographql.com/docs/graphql-subscriptions/authentication/)):

```
{
  "Authorization": "Bearer your_access_token"
}
```

![Step 3](media/step_3.png)

### Step 4

Then we need to go inside a docker container and lauch a script that will do
an update to our model (picks randomly a make name). Navigate the root of the
example and type such commands:

```sh
$ docker-compose exec web bash
$ python trigger_event.py
```



![Step 4](media/step_4.png)

This will show an update inside GraphQL Playground.

![The first upate](media/first_update.png)

Repeat step 4 and you will see another update inside GraphQL Playground.

![The second update](media/second_update.png)

This example may help you tie-up everything, so you can intergrate
authentication for GraphQL queries, mutations, subscriptions, and deploy them.

## Additional notes

Make sure your load balancers don't strip *Connection* and *Upgrade* headers
and set reasonable timeouts for websockets (NGINX, Ingress, Gcloud, AWS), so
they don't reconnect every 30 seconds or so.
