import os
import subprocess
import shutil
import urllib.request


TERMINAL_WIDTH = shutil.get_terminal_size().columns


def is_package_exists(package_name):
    command = f"rpm -qa | grep {package_name} | wc -l"
    result = subprocess.run(command, shell=True, capture_output=True)
    if int(result.stdout, 10) != 0:
        # package exist
        return True

    return False


def is_repository_exists(repository):
    command = f"dnf repolist | grep {repository} | wc -l"
    result = subprocess.run(command, shell=True, capture_output=True)
    if int(result.stdout, 10) != 0:
        # package exist
        return True

    return False


def is_file_exists(file_path):
    return os.path.isfile(file_path)


def enable_repository(repository_url):
    command = f"sudo dnf config-manager --add-repo {repository_url}"
    result = subprocess.run(command, shell=True)
    result.check_returncode()


def enable_copr_repository(repository):
    command = f"sudo dnf copr enable {repository} -y"
    result = subprocess.run(command, shell=True)
    result.check_returncode()


def remove_package(package_name):
    command = f"sudo dnf remove {package_name} -y"
    result = subprocess.run(command, shell=True)
    result.check_returncode()


def install_package(package_name):
    command = f"sudo dnf install {package_name} -y"
    result = subprocess.run(command, shell=True)
    result.check_returncode()


def done_text(message):
    print("Done!")
    print(message)
    print("-" * TERMINAL_WIDTH)


def skip_text(message):
    print("Skipping...")
    print(message)
    print("-" * TERMINAL_WIDTH)


def download_binary_file(url, file_path):
    urllib.request.urlretrieve(url, file_path)


def make_file_executable(file_path):
    os.chmod(file_path, 0o755)


def move_to_destination(src, dest):
    command = f"sudo mv -v {src} {dest}"
    result = subprocess.run(command, shell=True)
    result.check_returncode()
