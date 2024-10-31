from flask import Flask
from flask_graphql import GraphQLView
from graphene import Schema

from app.gql.mutations import Mutation
from app.gql.query import Query

app = Flask(__name__)

schema = Schema(query=Query, mutation=Mutation)

app.add_url_rule(
   '/graphql',
   view_func=GraphQLView.as_view(
       'graphql',
       schema=schema,
       graphiql=True
   )
)
if __name__ == '__main__':
    app.run(port=5009)