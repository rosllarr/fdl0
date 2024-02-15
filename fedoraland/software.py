from fedoraland.util import (
    enable_repository,
    enable_copr_repository,
    is_repository_exists,
    skip_text,
    done_text,
    is_package_exists,
    install_package,
    remove_package,
)


class Software:
    def __init__(self, name, packages,
                 repositoryCopr=None, repositoryExternal=None):
        self.name = name
        self.packages = packages
        self.repository_copr = repositoryCopr
        self.repository_external = repositoryExternal

    def install(self):
        for package in self.packages:
            # if package is already installed, Don't do any further action
            if is_package_exists(package):
                skip_text(f"{package} is already installed")
                continue

            if self.repository_copr is not None:
                if is_repository_exists(self.repository_copr.get("user")):
                    skip_text(f"{self.repository_copr.get(
                        "user")} repository is already enabled")
                else:
                    enable_copr_repository(self.repository_copr.get("name"))
            elif self.repository_external is not None:
                if is_repository_exists(self.repository_external.get("name")):
                    skip_text(f"{self.repository_external.get(
                        "name")} repository is already enabled")
                else:
                    enable_repository(self.repository_external.get("url"))

            install_package(package)
            done_text(f"{self.name} is installed")

    def remove(self):
        for package in self.packages:
            if not is_package_exists(package):
                skip_text(f"{package} doesn't exist")
                continue
            remove_package(package)
            done_text(f"{self.name} is removed")
