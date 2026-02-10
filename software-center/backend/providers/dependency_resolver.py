import logging

import networkx as nx

logger = logging.getLogger("ctxos.dependency_resolver")


class DependencyResolver:
    """Resolves and analyzes package dependencies to prevent broken installations."""

    def __init__(self, apt_provider=None):
        from providers.apt import AptProvider

        self.apt = apt_provider or AptProvider()
        self.graph = nx.DiGraph()

    def resolve(self, package_name):
        """Builds a dependency graph for a package."""
        self.graph.clear()
        self._add_to_graph(package_name)

        return {
            "package": package_name,
            "dependencies": list(self.graph.successors(package_name)),
            "total_packages": len(self.graph.nodes),
            "conflicts": self._find_conflicts(),
            "missing": self._find_missing(),
        }

    def _add_to_graph(self, package_name):
        """Recursively adds dependencies to the graph."""
        if package_name in self.graph and "version" in self.graph.nodes[package_name]:
            return

        info = self.apt.get_package_info(package_name)
        if not info:
            logger.warning(f"Metadata not found for package: {package_name}")
            self.graph.add_node(package_name, missing=True)
            return

        self.graph.add_node(package_name, version=info.get("Version"))

        deps = self._parse_dependencies(info.get("Depends", ""))
        for dep in deps:
            self.graph.add_edge(package_name, dep)
            self._add_to_graph(dep)

    def _parse_dependencies(self, deps_string):
        """Parses APT dependency string into a list of package names."""
        if not deps_string:
            return []

        results = []
        # Depends: liba (>= 1.0), libb | libc, libd
        parts = deps_string.split(",")
        for part in parts:
            # Handle alternatives: libb | libc -> pick first for now
            pkg = part.split("|")[0].strip()
            # Remove version constraints: liba (>= 1.0) -> liba
            pkg_name = pkg.split("(")[0].strip()
            if pkg_name:
                results.append(pkg_name)
        return results

    def _find_conflicts(self):
        """Checks for known conflicts in the current graph."""
        # This would require checking 'Conflicts' or 'Breaks' fields
        # Simplified for now
        return []

    def _find_missing(self):
        """Returns packages that were not found in the provider."""
        return [n for n, d in self.graph.nodes(data=True) if d.get("missing")]
