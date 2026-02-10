from unittest.mock import MagicMock

import pytest
from providers.dependency_resolver import DependencyResolver


@pytest.fixture
def mock_apt():
    provider = MagicMock()
    # Mock data tree:
    # A -> B, C
    # B -> D
    # C -> E
    # D (installed)
    # E (missing)
    data = {
        "pkg-a": {"Version": "1.0", "Depends": "pkg-b, pkg-c"},
        "pkg-b": {"Version": "2.0", "Depends": "pkg-d"},
        "pkg-c": {"Version": "1.5", "Depends": "pkg-e"},
        "pkg-d": {"Version": "3.0"},
    }
    provider.get_package_info.side_effect = lambda name: data.get(name)
    return provider


def test_resolve_graph(mock_apt):
    resolver = DependencyResolver(apt_provider=mock_apt)
    result = resolver.resolve("pkg-a")

    assert result["package"] == "pkg-a"
    assert "pkg-b" in result["dependencies"]
    assert "pkg-c" in result["dependencies"]
    assert result["total_packages"] == 5  # a, b, c, d, e
    assert "pkg-e" in result["missing"]


def test_parse_dependencies():
    resolver = DependencyResolver(apt_provider=MagicMock())
    deps = "liba (>= 1.0), libb | libc, libd"
    parsed = resolver._parse_dependencies(deps)
    assert parsed == ["liba", "libb", "libd"]
