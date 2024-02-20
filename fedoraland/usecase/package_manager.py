from fedoraland.lib.log import Log
from fedoraland.lib.util import (
    enable_copr_repository,
    enable_repository,
    install_package,
    is_package_exists,
    is_repository_exists,
    remove_package,
    skipped_text,
)


class PackageManager:

    def __init__(
        self,
        name,
        packages,
        repositoryCopr=None,
        repositoryExternal=None,
        call_stack=None,
    ):
        self.name = name
        self.packages = packages
        self.repository_copr = repositoryCopr
        self.repository_external = repositoryExternal
        self.call_stack = call_stack

    def install(self):

        for package in self.packages:
            log = {
                "name": package,
                "status": "",
                "messages": []
            }

            # if package is already installed, Don't do any further action
            if is_package_exists(package):
                log["status"] = "skipped"
                log["messages"].append(skipped_text(
                    f"{package} is already installed"
                ))
                continue

            if self.repository_copr is not None:
                if is_repository_exists(self.repository_copr.get("user")):
                    log["messages"].append(skipped_text(
                        f"{self.repository_copr.get(
                            "user")} repository is already enabled"
                    ))
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
