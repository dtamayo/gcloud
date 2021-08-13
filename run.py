import os
import argparse

def _parse_args():
    parser = argparse.ArgumentParser('run', 
                                     description='submit runs to cluster')

    parser.add_argument('-b', 
                        '--bucketname', 
                        required=True, 
                        help='Google Cloud bucketname used to store data')

    return parser.parse_args()


def main():
    args = _parse_args()
    bucketname = args.bucketname

    call("gsutil cp gs://{0}/data/unfinished/* gs://{0}/data/backup/".format(bucketname), shell=True)

    for root, dirs, files in os.walk('gs://{0}/data/unfinished/'.format(bucketname)):
        for file in files:
            if 'run' in file:
                call("gsutil cp gs://{0}/data/unfinished/* {0}/".format(bucketname), shell=True)
                run_num = file[3:7]

                with open("htcondor/submit-job", "w") as of:
                    of.write("#!/bin/bash -l\n")
                    of.write("executable\t\t\t\t= {0}.sh\n".format(bucketname))
                    of.write("arguments\t\t\t\t= {0}\n".format(file))
                    of.write("transfer_input_files\t= continue_sim.py, {0}.sh, {0}/{1}\n".format(bucketname, file))
                    of.write("should_transfer_files\t= IF_NEEDED\n")
                    of.write('Transfer_Output_Files\t= ""\n')
                    of.write("when_to_transfer_output\t= ON_EXIT\n")
                    of.write("log\t\t\t\t\t\t= {0}/run.{1}.log\n".format(bucketname, run_num))
                    of.write("Error\t\t\t\t\t= {0}/err.{1}\n".format(bucketname, run_num))
                    of.write("Output\t\t\t\t\t= {0}/out.{1}\n".format(bucketname, run_num))
                    of.write("queue")

                call("condor_submit submit-job", shell=True)
                call("gsutil mv gs://{0}/data/unfinished/{1} gs://{0}/data/queued/".format(bucketname, file), shell=True)

if __name__ == '__main__':
    main()
