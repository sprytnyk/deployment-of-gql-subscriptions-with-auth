from graphql.backend import GraphQLCoreBackend


class GraphQLCustomCoreBackend(GraphQLCoreBackend):
    """Custom GQL back-end that enables subscriptions."""

    def __init__(self, executor=None):
        super().__init__(executor)
        self.execute_params['allow_subscriptions'] = True
