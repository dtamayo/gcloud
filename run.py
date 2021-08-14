import os
import argparse
from subprocess import call
import rebound

def _parse_args():
    parser = argparse.ArgumentParser('run', 
                                     description='submit runs to cluster')

    parser.add_argument('-b', 
                        '--bucketname', 
                        required=True, 
                        help='Google Cloud bucketname used to store data')
    
    parser.add_argument('-o', 
                        '--orbmax', 
                        required=True, 
                        help='Maximum number of orbits before we move binary to finished folder')

    return parser.parse_args()


def main():
    args = _parse_args()
    bucketname = args.bucketname
    orbmax = float(args.orbmax)

    call("gsutil -m cp gs://{0}/data/unfinished/*.bin gs://{0}/data/backup/".format(bucketname), shell=True)
    call("mkdir {0}".format(bucketname), shell=True)
    call("gsutil -m cp gs://{0}/data/unfinished/*.bin {0}/".format(bucketname), shell=True)

    for root, dirs, files in os.walk('{0}/'.format(bucketname)):
        for file in files:
            if 'run' in file:
                sa = rebound.SimulationArchive('{0}/{1}'.format(bucketname, file))
                sim = sa[0]
                P0 = sim.particles[1].P
                sim = sa[-1]
                if sim.t/P0 > orbmax or sim._status == 7: # exceeded max # of orbits or status=7 means had a collision this dt
                    print('Binary {0} finished'.format(file))
                    call("gsutil mv gs://{0}/data/unfinished/{1} gs://{0}/data/finished/".format(bucketname, file), shell=True)
                    call("gsutil rm {0}/{1}".format(bucketname, file)

    for root, dirs, files in os.walk('{0}/'.format(bucketname)):
        for file in files:
            if 'run' in file:
                run_num = file[3:7]
                
                with open("submit-job", "w") as of:
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
