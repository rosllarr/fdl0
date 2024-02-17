import os
from fedoraland.util import (
    download_binary_file,
    enable_repository,
    enable_copr_repository,
    is_file_exists,
    is_repository_exists,
    make_file_executable,
    move_to_destination,
    skip_text,
    done_text,
    is_package_exists,
    install_package,
    remove_package,
)


class Software:
    def __init__(self, name, kind, packages,
                 repositoryCopr=None, repositoryExternal=None,
                 binaryDownload=None):
        self.name = name
        self.kind = kind
        self.packages = packages
        self.repository_copr = repositoryCopr
        self.repository_external = repositoryExternal
        self.binary_download = binaryDownload

    def _dnf_install(self, package):
        """
        Install dnf packages
        """
        # if package is already installed, Don't do any further action
        if is_package_exists(package):
            skip_text(f"{package} is already installed")
            return

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

    # def _binary_install(self, )

    def install(self):
        # Install binary file
        # --------------------------
        if self.binary_download is not None:
            if is_file_exists(self.binary_download.get("dest")):
                skip_text(f"{self.binary_download.get(
                    "dest")} binary file is already exists")
            else:
                file_path = f"{os.getcwd()}/.downloads/{self.name}"
                download_binary_file(
                    self.binary_download.get("url"), file_path)
                make_file_executable(file_path)
                move_to_destination(
                    file_path, self.binary_download.get("dest"))
                done_text(f"{self.name} download to {
                          self.binary_download.get('dest')}")
        # --------------------------

        for package in self.packages:
            if self.kind == "packageManager":
                self._dnf_install(package)

            # if self.kind == "binaryDownload":

    def remove(self):
        for package in self.packages:
            if not is_package_exists(package):
                skip_text(f"{package} doesn't exist")
                continue
            remove_package(package)
            done_text(f"{self.name} is removed")
