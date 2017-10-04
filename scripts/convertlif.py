
import os
import shlex
import shutil
import argparse
import tempfile
import subprocess

from dtoolcore import DataSet, ProtoDataSet

from dtoolutils import temp_working_dir, stage_outputs


def convert_lif_file(dataset, identifier, output_directory):

    lif_file_path = dataset.item_content_abspath(identifier)
    output_file_template = os.path.join(output_directory, '%n.tif')

    base_command = '/opt/tools/bftools/bfconvert'

    # docker_command = ['docker', 'run', '--rm']
    # docker_command += ['-v', '{}:{}'.format(lif_file_path, '/input.lif')]
    # docker_command += ['-v', '{}:{}'.format(output_directory, '/output')]
    # docker_command += ['-e', '"BF_MAX_MEM=6g"']
    # docker_command += [container]
    # docker_command += [base_command, '/input.lif', output_file_template]

    command = [base_command, lif_file_path, output_file_template]
    subprocess.call(command)

    # print ' '.join(docker_command)
    # returncode = subprocess.call(docker_command)
    # print("Returned {}".format(returncode))

    output_file_list = os.listdir(output_directory)
    outputs = [(filename, {}) for filename in output_file_list]

    return outputs


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

    input_dataset = DataSet.from_uri(args.dataset)

    output_dataset = ProtoDataSet.from_uri(args.output_dataset)

    tmpdir_prefix = os.path.join(os.path.expanduser("~"), 'tmp', 'tmp')

    with temp_working_dir() as working_dir:
        outputs = convert_lif_file(input_dataset, args.identifier, working_dir)
        stage_outputs(
            outputs,
            working_dir,
            input_dataset,
            output_dataset,
            [],
            args.identifier
        )


if __name__ == '__main__':
    main()
