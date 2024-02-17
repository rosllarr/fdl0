import unittest

from fedoraland.usecase.parser import Parser


class TestPackageManagerParser(unittest.TestCase):
    def test_pass(self):
        app = {
            "name": "Docker",
            "kind": "packageManager",
            "packages": [
                "docker-ce",
                "docker-ce-cli",
                "containerd.io",
                "docker-buildx-plugin",
                "docker-compose-plugin",
            ],
            "repositoryExternal": {
                "name": "docker-ce-stable",
                "url": "https://download.docker.com/linux/fedora/docker-ce.repo",
            }
        }
        parser = Parser([app])
        package_manager = parser.apps[0]

        self.assertEqual(app.get("name"), package_manager.name)
        self.assertEqual(app.get("packages"), package_manager.packages)
        self.assertEqual(
            app.get("repositoryExternal"),
            package_manager.repository_external
        )

    def test_no_name(self):
        app = {
            "kind": "packageManager",
        }

        with self.assertRaisesRegex(ValueError, "Name is required"):
            Parser([app])

    def test_no_packages(self):
        app = {
            "name": "Docker",
            "kind": "packageManager",
        }

        with self.assertRaisesRegex(ValueError, "Packages is required"):
            Parser([app])

    def test_no_repository(self):
        app = {
            "name": "Docker",
            "kind": "packageManager",
            "packages": [
                "docker-ce",
                "docker-ce-cli",
                "containerd.io",
                "docker-buildx-plugin",
                "docker-compose-plugin",
            ],
        }

        with self.assertRaisesRegex(
            ValueError,
            """
                You aren't specify both repositoryCopr and repositoryExternal
                Please specify either repositoryCopr or repositoryExternal
            """
        ):
            Parser([app])

    def test_both_repository(self):
        app = {
            "name": "Docker",
            "kind": "packageManager",
            "packages": [
                "docker-ce",
                "docker-ce-cli",
                "containerd.io",
                "docker-buildx-plugin",
                "docker-compose-plugin",
            ],
            "repositoryCopr": "not None",
            "repositoryExternal": "not None",
        }

        with self.assertRaisesRegex(
            ValueError,
            """
                You specified both repositoryCopr and repositoryExternal
                Please specify either repositoryCopr or repositoryExternal
            """
        ):
            Parser([app])


class TestBinaryDownloadParser(unittest.TestCase):
    def test_pass(self):
        app = {
            "name": "kubectl",
            "kind": "binaryDownload",
            "binaries": ["kubectl"],
            "downloadUrl": "https://dl.k8s.io/release/v1.29.2/bin/linux/amd64/kubectl",
            "downloadTo": "/usr/local/bin/",
        }
        parser = Parser([app])
        binary_download = parser.apps[0]

        self.assertEqual(app.get("name"), binary_download.name)
        self.assertEqual(app.get("binaries"), binary_download.binaries)
        self.assertEqual(app.get("downloadUrl"), binary_download.download_url)
        self.assertEqual(app.get("downloadTo"), binary_download.download_to)

    def test_no_name(self):
        app = {
            "kind": "binaryDownload",
        }

        with self.assertRaisesRegex(ValueError, "Name is required"):
            Parser([app])

    def test_no_binaries(self):
        app = {
            "name": "kubectl",
            "kind": "binaryDownload",
        }

        with self.assertRaisesRegex(ValueError, "Binaries is required"):
            Parser([app])

    def test_no_downloadUrl(self):
        app = {
            "name": "kubectl",
            "kind": "binaryDownload",
            "binaries": ["kubectl"],
        }

        with self.assertRaisesRegex(ValueError, "DownloadUrl is required"):
            Parser([app])

    def test_no_downloadTo(self):
        app = {
            "name": "kubectl",
            "kind": "binaryDownload",
            "binaries": ["kubectl"],
            "downloadUrl": "https://dl.k8s.io/release/v1.29.2/bin/linux/amd64/kubectl",
        }

        with self.assertRaisesRegex(ValueError, "DownloadTo is required"):
            Parser([app])

    def test_downloadTo_without_last_slash(self):
        app = {
            "name": "kubectl",
            "kind": "binaryDownload",
            "binaries": ["kubectl"],
            "downloadUrl": "https://dl.k8s.io/release/v1.29.2/bin/linux/amd64/kubectl",
            "downloadTo": "/usr/local/bin",
        }

        parser = Parser([app])
        binary_download = parser.apps[0]

        self.assertEqual("/usr/local/bin/", binary_download.download_to)


class TestGitCloneParser(unittest.TestCase):
    def test_pass(self):
        app = {
            "name": "git",
            "kind": "gitClone",
            "binaries": ["git"],
            "repoUrl": "https://github.com/git/git.git",
            "cloneTo": "/usr/local/bin/",
            "linkTo": "/usr/local/bin/",
        }
        parser = Parser([app])
        git_clone = parser.apps[0]

        self.assertEqual(app.get("name"), git_clone.name)
        self.assertEqual(app.get("binaries"), git_clone.binaries)
        self.assertEqual(app.get("repoUrl"), git_clone.repo_url)
        self.assertEqual(app.get("cloneTo"), git_clone.clone_to)
        self.assertEqual(app.get("linkTo"), git_clone.link_to)

    def test_no_name(self):
        app = {
            "kind": "gitClone",
        }

        with self.assertRaisesRegex(ValueError, "Name is required"):
            Parser([app])

    def test_no_binaries(self):
        app = {
            "name": "git",
            "kind": "gitClone",
        }

        with self.assertRaisesRegex(ValueError, "Binaries is required"):
            Parser([app])

    def test_no_repoUrl(self):
        app = {
            "name": "git",
            "kind": "gitClone",
            "binaries": ["git"],
        }

        with self.assertRaisesRegex(ValueError, "RepoUrl is required"):
            Parser([app])

    def test_no_cloneTo(self):
        app = {
            "name": "git",
            "kind": "gitClone",
            "binaries": ["git"],
            "repoUrl": "https://github.com/git/git.git",
        }

        with self.assertRaisesRegex(ValueError, "CloneTo is required"):
            Parser([app])

    def test_no_linkTo(self):
        app = {
            "name": "git",
            "kind": "gitClone",
            "binaries": ["git"],
            "repoUrl": "https://github.com/git/git.git",
            "cloneTo": "/usr/local/bin/",
        }

        with self.assertRaisesRegex(ValueError, "LinkTo is required"):
            Parser([app])

    def test_linkTo_without_last_slash(self):
        app = {
            "name": "git",
            "kind": "gitClone",
            "binaries": ["git"],
            "repoUrl": "https://github.com/git/git.git",
            "cloneTo": "/usr/local/bin",
            "linkTo": "/usr/local/bin",
        }

        parser = Parser([app])
        git_clone = parser.apps[0]

        self.assertEqual("/usr/local/bin/", git_clone.link_to)
