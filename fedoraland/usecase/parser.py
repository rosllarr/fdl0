from fedoraland.usecase.binary_download import BinaryDownload
from fedoraland.usecase.git_clone import GitClone
from fedoraland.usecase.package_manager import PackageManager


class Parser:
    """
    Take a YAML file and convert it into a appropriate object
    """

    def __init__(self, contents):
        self.apps = list()
        for app in contents:
            kind = app.get("kind")

            if kind is None:
                raise ValueError("Kind is required")

            if kind == "packageManager":
                attr = self._check_packageManager_attr(app)
                self.apps.append((PackageManager(**attr)))

            if kind == "binaryDownload":
                attr = self._check_downloadBinary_attr(app)
                self.apps.append(BinaryDownload(**attr))

            if kind == "gitClone":
                attr = self._check_gitClone_attr(app)
                self.apps.append(GitClone(**attr))

    def _check_packageManager_attr(self, app):
        name = app.get("name")
        package = app.get("packages")
        repositoryCopr = app.get("repositoryCopr")
        repositoryExternal = app.get("repositoryExternal")

        if name is None:
            raise ValueError("Name is required")

        if package is None:
            raise ValueError("Packages is required")

        if (
            repositoryCopr is not None and
            repositoryExternal is not None
        ):
            raise ValueError(
                """
                You specified both repositoryCopr and repositoryExternal
                Please specify either repositoryCopr or repositoryExternal
                """
            )

        if (
            repositoryCopr is None and
            repositoryExternal is None
        ):
            raise ValueError(
                """
                You aren't specify both repositoryCopr and repositoryExternal
                Please specify either repositoryCopr or repositoryExternal
                """
            )

        return {
            "name": name,
            "packages": package,
            "repositoryCopr": repositoryCopr,
            "repositoryExternal": repositoryExternal,
        }

    def _check_downloadBinary_attr(self, app):
        name = app.get("name")
        binaries = app.get("binaries")
        downloadUrl = app.get("downloadUrl")
        downloadTo = app.get("downloadTo")

        if name is None:
            raise ValueError("Name is required")

        if binaries is None:
            raise ValueError("Binaries is required")

        if downloadUrl is None:
            raise ValueError("DownloadUrl is required")

        if downloadTo is None:
            raise ValueError("DownloadTo is required")
        else:
            if not downloadTo.endswith("/"):
                downloadTo = downloadTo + "/"

        return {
            "name": name,
            "binaries": binaries,
            "downloadUrl": downloadUrl,
            "downloadTo": downloadTo,
        }

    def _check_gitClone_attr(self, app):
        name = app.get("name")
        binaries = app.get("binaries")
        repoUrl = app.get("repoUrl")
        cloneTo = app.get("cloneTo")
        linkTo = app.get("linkTo")

        if name is None:
            raise ValueError("Name is required")

        if binaries is None:
            raise ValueError("Binaries is required")

        if repoUrl is None:
            raise ValueError("RepoUrl is required")

        if cloneTo is None:
            raise ValueError("CloneTo is required")

        if linkTo is None:
            raise ValueError("LinkTo is required")
        else:
            if not linkTo.endswith("/"):
                linkTo = linkTo + "/"

        return {
            "name": name,
            "binaries": binaries,
            "repoUrl": repoUrl,
            "cloneTo": cloneTo,
            "linkTo": linkTo,
        }
