import os
from fedoraland.util import done_text


class Config:
    def __init__(self, name, src, dest):
        self.name = name
        self.src = src
        self.dest = dest

    def overwrite_or_create(self):
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
