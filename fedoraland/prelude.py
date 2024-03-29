from fedoraland.software import Software
from fedoraland.lib.util import (
    done_text,
    enable_repository,
    install_package,
    is_repository_exists,
    skip_text
)

# Install dnf-plugins-core
dnf_plugins_core = Software(name="dnf-plugins-core",
                            packages=["dnf-plugins-core"])
dnf_plugins_core.install()


def enable_rpmfusion():
    free_rpm = "https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm"
    nonfree_rpm = "https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm"

    package_list = [
        {"package": free_rpm, "repository": "rpmfusion-free"},
        {"package": nonfree_rpm, "repository": "rpmfusion-nonfree"},
    ]

    for package in package_list:
        if is_repository_exists(package.get("repository")):
            index = package.get("package").find("rpmfusion-free")
            if index != -1:
                skip_text("rpmfusion-free is already enabled")
            else:
                skip_text("rpmfusion-nonfree is already enabled")
            continue
        else:
            install_package(package)
            index = package.get("package").find("rpmfusion-free")
            if index != -1:
                done_text("rpmfusion-free is enabled")
            else:
                done_text("rpmfusion-nonfree is enabled")


# Enable RPMFusion
enable_rpmfusion()

# Enable openh264 library
if is_repository_exists("fedora-cisco-openh264"):
    skip_text("fedora-cisco-openh264 is already enabled")
else:
    enable_repository("fedora-cisco-openh264")
    done_text("fedora-cisco-openh264 is enabled")

# Remove podman to prevent conflicts with docker
podman = Software(name="Podman", packages=["podman"])
podman.remove()

# Install essential packages
openssl = Software(name="openssl", packages=["openssl"])
openssl.install()

python3_pip = Software(name="python3-pip", packages=["python3-pip"])
python3_pip.install()

python3_devel = Software(name="python3-devel", packages=["python3-devel"])
python3_devel.install()

keepassxc = Software(name="keepassxc", packages=["keepassxc"])
keepassxc.install()

git = Software(name="git", packages=["git"])
git.install()
