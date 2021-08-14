import argparse
from subprocess import call

def _parse_args():
    parser = argparse.ArgumentParser('move', 
                                     description='move successes and failures back into unfinished for rerunning')

    parser.add_argument('-b', 
                        '--bucketname', 
                        required=True, 
                        help='Google Cloud bucketname used to store data')

    return parser.parse_args()


def main():
    args = _parse_args()
    bucketname = args.bucketname

    call("gsutil -m mv gs://{0}/data/successes/*.bin gs://{0}/data/unfinished/".format(bucketname), shell=True)
    call("gsutil -m mv gs://{0}/data/failures/*.bin gs://{0}/data/unfinished/".format(bucketname), shell=True)

if __name__ == '__main__':
    main()
