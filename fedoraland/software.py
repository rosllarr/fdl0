from fedoraland.util import (
    enable_repository,
    is_repository_exists,
    done_text,
    enable_copr_repository,
    install_package,
    remove_package,
    skip_text,
    is_package_exists
)


# Remove
def podman():
    if is_package_exists("podman"):
        remove_package("podman")
        done_text("Podman is removed")
    skip_text("Podman is already removed")
    return 0


# Install
def alacritty():
    if is_package_exists("alacritty"):
        skip_text("Alacritty is already installed")
        return 0

    if is_repository_exists("atim"):
        skip_text("Copr repository 'atim/alacritty' is already enabled")
    else:
        enable_copr_repository("atim/alacritty")

    install_package("alacritty")
    done_text("Alacritty is installed")


def cargo():
    package_name = "cargo"
    if is_package_exists(package_name):
        skip_text(f"{package_name} is already installed")
        return 0

    install_package(package_name)
    done_text(f"{package_name} is installed")


def docker():
    package_list = ["docker-ce", "docker-ce-cli", "containerd.io",
                    "docker-buildx-plugin", "docker-compose-plugin"]

    if is_repository_exists("docker-ce-stable"):
        skip_text("docker-ce-stable repository is already enabled")
    else:
        enable_repository("https://download.docker.com/linux/fedora/docker-ce.repo")

    for package in package_list:
        if is_package_exists(package):
            skip_text(f"{package} is already installed")
            break
        else:
            install_package(package)
            done_text(f"{package} is installed")


def fish():
    if is_package_exists("fish"):
        skip_text("Fish is already installed")
        return 0

    if is_repository_exists("shells_fish"):
        skip_text("shells_fish repository is already enabled")
    else:
        enable_repository(
            "https://download.opensuse.org/repositories/shells:fish/Fedora_39/shells:fish.repo")

    install_package("fish")
    done_text("Fish is installed")


def tmux():
    if is_package_exists("tmux"):
        skip_text("Tmux is already installed")
        return 0

    install_package("tmux")
    done_text("Tmux is installed")
