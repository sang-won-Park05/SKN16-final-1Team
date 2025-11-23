from models.llm.core import routers


def test_router_basic():
    assert routers.route_query("pain in chest") == "medical"
    assert routers.route_query("hello") == "general"
