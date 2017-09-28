
import os
import shlex
import shutil
import argparse
import tempfile
import subprocess

from contextlib import contextmanager

from dbluesea import AzureDataSet


@contextmanager
def tmp_working_dir(prefix):

    tmp_dir = tempfile.mkdtemp(prefix=prefix)

    yield tmp_dir

    shutil.rmtree(tmp_dir)


def convert_lif_file(dataset, identifier, output_directory):

    lif_file_path = dataset.abspath_from_identifier(identifier)
    output_file_template = os.path.join('/output', '%n.tif')

    container = "jicscicomp/bioformats"
    base_command = '/opt/tools/bftools/bfconvert'

    docker_command = ['docker', 'run', '--rm']
    docker_command += ['-v', '{}:{}'.format(lif_file_path, '/input.lif')]
    docker_command += ['-v', '{}:{}'.format(output_directory, '/output')]
    docker_command += ['-e', '"BF_MAX_MEM=6g"']
    docker_command += [container]
    docker_command += [base_command, '/input.lif', output_file_template]

    print ' '.join(docker_command)
    returncode = subprocess.call(docker_command)
    print("Returned {}".format(returncode))


def put_all_in_dir_to_dataset(dir, dataset, prefix=None):

    for filename in os.listdir(dir):

        if prefix is not None:
            remote_path = "{}/{}".format(prefix, filename)
        else:
            remote_path = "{}".format(filename)

        local_path = os.path.join(dir, filename)

        print("Put {} as {}".format(local_path, remote_path))

        dataset.put_from_local_path(local_path, remote_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d',
        '--dataset',
        help='UUID of input dataset'
    )
    parser.add_argument(
        '-i',
        '--identifier',
        help='Identifier (hash) to process'
    )
    parser.add_argument(
        '-o',
        '--output-dataset',
        help='UUID of output dataset'
    )

    args = parser.parse_args()

    input_dataset = AzureDataSet.from_uuid(args.dataset)

    output_dataset = AzureDataSet.from_uuid(args.output_dataset)

    tmpdir_prefix = os.path.join(os.path.expanduser("~"), 'tmp', 'tmp')

    with tmp_working_dir(tmpdir_prefix) as working_dir:
        convert_lif_file(input_dataset, args.identifier, working_dir)
        item_path = input_dataset.item_from_identifier(args.identifier)['path']
        name_stem, _ = os.path.splitext(item_path)
        put_all_in_dir_to_dataset(working_dir, output_dataset, name_stem)

if __name__ == '__main__':
    main()
