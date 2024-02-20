import os
from fedoraland.lib.log import Log
from fedoraland.lib.util import (
    download_binary_file,
    installed_text,
    is_file_exists,
    make_file_executable,
    move_to_destination,
    skipped_text
)


class BinaryDownload:

    def __init__(
        self,
        name,
        binaries,
        downloadUrl,
        downloadTo,
        call_stack,
    ):
        self.name = name
        self.binaries = binaries
        self.download_url = downloadUrl
        self.download_to = downloadTo
        self.call_stack = call_stack

    def install(self, ):
        for binary in self.binaries:
            binary_path = f"{self.download_to}{binary}"
            if is_file_exists(binary_path):
                log = Log.create_instance(
                    name=binary,
                    status="skipped",
                    message=skipped_text(
                        f"{binary_path} file is already exists")
                )
                self.call_stack.append(log)
                continue
            else:
                home_directory = os.path.expanduser("~")
                download_path = f"{home_directory}/Downloads/{binary}"
                download_binary_file(self.download_url, download_path)
                make_file_executable(download_path)
                move_to_destination(download_path, self.download_to)
                log = Log.create_instance(
                    name=binary,
                    status="installed",
                    message=installed_text(
                        f"{binary} are installed to {self.download_to}"
                    ),
                )
                self.call_stack.append(log)

    def remove(self):
        pass
