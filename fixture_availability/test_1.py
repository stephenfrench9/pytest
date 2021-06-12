"""
When a test searches for a fixture, it searches
- function-scope
- class-scope
- module (file) scope
- package (directory) scope
"""
import pytest


"""
This fixture is scoped to the function
This fixture is defined in a module-scope
"""
@pytest.fixture
def order():
    return []


"""
1. This fixture is scoped to the function (default behaviour). 
    1. The fixture will appear in function scopes (aka function scopes)
1. This fixture is defined in the module-scope called test_1.py 
1. When this fixture is instantiated, how 'big' will it be? It will function-sized. 
1. Where does this fixture appear? 
It appears in function scopes. Every function has its own scope (scope), 
and this fixture will appear in those function scopes.
1. Where is this fixture defined? It is defined in the test_1.py-module scope.
The fixture is defined within a module scope, this governs how it will
be discovered. When the fixture is instantiated it, since it is scoped to the function
(people will say because it has function scope), it will be instantiated within function
scopes

One interesting thing - this fixture will request three different fixtures
during the session. TestOne:inner, TestTwo:inner, and order.  
"""
@pytest.fixture
def outer(order, inner):
    order.append("outer")


class TestOne:
    """
    This fixture is scoped to the function (default)
    This fixture is defined in the class=TestOne scope
    """
    @pytest.fixture
    def inner(self, order):
        order.append("one")

    """
    The order fixture and outer fixture are defined in a larger scope 
        (module over class over function) so it is discoverable
    These fixtures have function scope, so the logic for these fixtures will
        run once and then any results will be cached. Stated differently,
        this function will have its own fixtures. 
    This test directly requests a fixture at a higher scope, and then that fixture
        requests a fixture back at the scope of the test (a lower scope). But which
        lower scope does this fixture look into? There are two in this case! There
        could be more. It looks into the lower scope which requested it. It looks
        at the only special scope below it that there is. 
    """
    def test_order(self, order, outer):
        assert order == ["one", "outer"]


class TestTwo:
    """
    This fixture is scoped to the function (default)
    This fixture is defined in the class=TestTwo scope
    """
    @pytest.fixture
    def inner(self, order):
        order.append("two")

    def test_order(self, order, outer):
        assert order == ["two", "outer"]
