def package_dependency_resolver(packages: dict[str, list[str]]) -> list[str]:
    res = []

    initial_packages = []
    for pkg, deps in packages.items():
        if not deps:
            initial_packages.append(pkg)
    initial_packages.sort()
    res.extend(initial_packages)

    if not res:
        return []
        
    added = True
    while added:
        added = False

        candidates = []
        for package_name, dependecies in packages.items():
            if package_name not in res:
                all_deps_met = True

                for dep in dependecies:
                    if dep not in res:
                        all_deps_met = False
                        break

                if all_deps_met:
                    candidates.append(package_name)

        if candidates:
            candidates = sorted(candidates)
            res.extend(candidates)
            added = True
    
    return res


print(package_dependency_resolver({"app": ["database"], "database": ["driver"], "driver": []}))  # Expected: ["driver", "database", "app"]
print(package_dependency_resolver({"A": [], "B": ["C"], "C": ["A", "B"]}))  # Expected: ["A", "B", "C"]
print(package_dependency_resolver({}))  # Expected: []
print(package_dependency_resolver({"X": ["Y"], "Y": ["X"]}))  # Expected: []
print(package_dependency_resolver({"web": [], "api": [], "frontend": ["web"], "backend": ["api"]}))  # Expected: ["api", "web", "backend", "frontend"]