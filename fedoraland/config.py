import os
import shutil
from fedoraland.util import done_text


class Config:
    def __init__(self, name, src, dest):
        self.name = name
        self.src = src
        self.dest = dest

    def overwrite_or_create(self):
        """
        Overwrite or create the destination file.
        If the destination directory doesn't exist, create it.
        """
        try:
            # Get the directory of the destination file
            dest_dir = os.path.dirname(self.dest)

            # Create the directory if it doesn't exist
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)

            with open(self.src, "r") as src_file:
                content = src_file.read()

            with open(self.dest, "w") as dest_file:
                dest_file.write(content)

            done_text(f"{self.src} overwritten to {self.dest}")
        except IOError as e:
            print(f"Unable to overwrite or create {self.dest} file")
            print(e)

    def sync(self):
        """
        Overwrite the source file to the destination file,
        if the source modified timestamp is newer than the destination
        modified timestamp, or

        Overwrite the destination file to the source file, If the destination
        modified timestamp is newer than the source modified timestamp.
        """
        src_time = os.path.getmtime(self.src)
        dest_time = os.path.getmtime(self.dest)

        if src_time < dest_time:
            # destination is newer
            shutil.copy(self.dest, self.src)
            done_text(f"{self.dest} overwritten to {self.src}")
        elif src_time > dest_time:
            # source is newer
            shutil.copy(self.src, self.dest)
            done_text(f"{self.src} overwritten to {self.dest}")
        else:
            print(
                f"The modification times of \
                {self.src} and {self.dest} are the same"
            )
