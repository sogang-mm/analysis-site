import os, hashlib, datetime


def from_sha256(instance, filename):
    contents = instance.image.read()
    instance_hash_value = hashlib.sha256(bytes(contents)).hexdigest()
    filename_extension = os.path.splitext(filename)[-1]
    update_filename = "{0}{1}".format(instance_hash_value, filename_extension)
    return update_filename


# def from_datetime(instance, filename):
#     update_filename = ''
#     return update_filename
