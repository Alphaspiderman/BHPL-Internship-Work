from intranet.endpoints.index import Index
from intranet.app import appserver

appserver.add_route(Index.as_view(), "/")
