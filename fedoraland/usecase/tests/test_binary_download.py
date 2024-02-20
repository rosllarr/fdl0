import os
import unittest
from fedoraland.lib.util import move_to_destination, remove_file
from fedoraland.usecase.binary_download import BinaryDownload


class TestInstallPass(unittest.TestCase):
    def setUp(self):
        # backup existing binary file
        src = "/usr/local/bin/kubectl"
        dest = "/usr/local/bin/kubectl.bak"
        move_to_destination(src, dest)

    def tearDown(self):
        # remove downloaded binary file
        path = "/usr/local/bin/kubectl"
        remove_file(path)
        # used backup file
        src = "/usr/local/bin/kubectl.bak"
        dest = "/usr/local/bin/kubectl"
        move_to_destination(src, dest)

    def test_install_pass(self):
        attr = {
            "name": "kubectl",
            "binaries": ["kubectl"],
            "downloadUrl": "https://dl.k8s.io/release/v1.29.2/bin/linux/amd64/kubectl",
            "downloadTo": "/usr/local/bin/",
        }
        app = BinaryDownload(**attr)
        app.install()

        path = "/usr/local/bin/kubectl"
        self.assertTrue(os.path.exists(path))


class TestInstallSkipWithExistingFile(unittest.TestCase):
    def test_install_skip(self):
        attr = {
            "name": "kubectl",
            "binaries": ["kubectl"],
            "downloadUrl": "https://dl.k8s.io/release/v1.29.2/bin/linux/amd64/kubectl",
            "downloadTo": "/usr/local/bin/",
        }
        app = BinaryDownload(**attr)

        self.assertEqual(
            app.install(), "/usr/local/bin/kubectl file is already exists")
