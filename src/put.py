import utils
import os
import click


class Put:
    def __init__(self, key, directory='code', origin_path=None):
        self.key = key
        self.directory = directory
        self.origin_path = origin_path

    def recreate_share(self, file_service):
        file_service.create_share(self.key)

    def recursive_put(self, path, file_service):
        for file_path in os.listdir(path):
            _file_path = os.path.join(path, file_path)

            if os.path.isdir(_file_path):
                self.recursive_put(_file_path, file_service)
            else:
                self.put_file(_file_path, file_service)

    def put(self, path, is_directory=False):
        if os.path.isdir(path) and not is_directory:
            click.echo("please add -f or --folder parameters to upload folder.")
        else:

            self.origin_path = path

            file_service = utils.init_file_server_by_key(self.key)

            self.recreate_share(file_service)

            file_service.create_directory(self.key, self.directory)

            if is_directory:
                self.recursive_put(path, file_service)
            else:
                self.put_file(path, file_service)

    def put_file(self, file_path, file_service):
        sub_dir = os.path.dirname(os.path.relpath(file_path, self.origin_path))
        upload_directory = self.directory
        if sub_dir:
            upload_directory = "%s/%s" % (upload_directory, sub_dir)
            directories = upload_directory.split('/')
            temp_directory = ''
            for directory in directories:
                temp_directory += directory + '/'
                file_service.create_directory(self.key, temp_directory)

        upload_result = file_service.create_file_from_path(self.key, upload_directory, os.path.basename(file_path),
                                                           file_path)
        if upload_result is None:
            click.echo("%s upload success ." % os.path.basename(file_path))
        else:
            click.echo("%s upload fail ." % os.path.basename(file_path))
