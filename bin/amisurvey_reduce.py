#!/usr/bin/env python
from __future__ import absolute_import
import argparse
import os
import sys
import logging
import logging.handlers
import datetime
import json
from amisurvey.dataflow import process_obsinfo_list
from amisurvey.utils import ami_info_to_obsinfo
import driveami
from driveami.environments import default_output_dir
from chimenea.obsinfo import ObsInfo



def handle_args():
    """
    Defines command line arguments.

    Default values can be tweaked here.
    """
    default_casa_dir = None

    parser = argparse.ArgumentParser()

    parser.add_argument('calfiles_list',
                         help="Path to listing of pre-calibrated datafiles")

    default_outfile_stem = "amisurvey_results"
    parser.add_argument('-o', '--outfile', nargs='?',
                        default=default_outfile_stem,
                    help='Specify filename stem for output listing of imaged '
                         'data, default: '+default_outfile_stem )

    parser.add_argument("-t", "--topdir", default=default_output_dir,
                    help="Top level data-output directory, default is : " +
                        default_output_dir)

    parser.add_argument("--casa-dir", default=default_casa_dir,
                      help="Path to CASA directory, default: " +
                           str(default_casa_dir))

    parser.add_argument('-m', '--monitor',
                      help="""Path to JSON-encoded dictionary mapping group-name
                                to monitoring co-ordinates, e.g.
                                {"TARGETFOO":[[268.1,55.2],[270.3,55.5]]}
                                """,
                      default=None)

    options = parser.parse_args()
    options.topdir = os.path.expanduser(options.topdir)
    return options


def setup_logging(reduction_timestamp):
    """
    Set up basic (INFO level) and debug logfiles
    """
    log_filename = 'amisurvey_log_'+reduction_timestamp
    date_fmt = "%y-%m-%d (%a) %H:%M:%S"

    from colorlog import ColoredFormatter

    std_formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s',
                                      date_fmt)


    debug_formatter = logging.Formatter(
                            '%(asctime)s:%(name)s:%(levelname)s:%(message)s',
                            # '%(asctime)s:%(levelname)s:%(message)s',
                            date_fmt)

    color_formatter = ColoredFormatter(
            "%(log_color)s%(asctime)s:%(levelname)-8s%(reset)s %(blue)s%(message)s",
            datefmt=date_fmt,
            reset=True,
            log_colors={
                    'DEBUG':    'cyan',
                    'INFO':     'green',
                    'WARNING':  'yellow',
                    'ERROR':    'red',
                    'CRITICAL': 'red',
            }
    )

    #Get to the following size before splitting log into multiple files:
    log_chunk_bytesize = 5e6

    info_logfile = logging.handlers.RotatingFileHandler(log_filename,
                            maxBytes=log_chunk_bytesize, backupCount=10)
    info_logfile.setFormatter(std_formatter)
    info_logfile.setLevel(logging.INFO)
    debug_logfile = logging.handlers.RotatingFileHandler(log_filename + '.debug',
                            maxBytes=log_chunk_bytesize, backupCount=10)
    debug_logfile.setFormatter(debug_formatter)
    debug_logfile.setLevel(logging.DEBUG)

    stdout_log = logging.StreamHandler()
    stdout_log.setFormatter(color_formatter)
    stdout_log.setLevel(logging.INFO)
    stdout_log.setLevel(logging.DEBUG)

    #Set up root logger
    logger = logging.getLogger()
    logger.handlers=[]
    logger.setLevel(logging.DEBUG)
    logger.addHandler(info_logfile)
    logger.addHandler(debug_logfile)
    logger.addHandler(stdout_log)
    logging.getLogger('drivecasa').setLevel(logging.INFO) #Suppress drivecasa debug log.
    logging.getLogger('tkp').setLevel(logging.ERROR) #Suppress SF / coords debug log.


def main(options, logging_timestamp):
    logger=logging.getLogger(__name__)

    monitor_coords_dict = {}
    if options.monitor:
        with open(options.monitor) as f:
            monitor_coords_dict =json.load(f)
    #Quick check to see if monitor-coords list appears sanely formatted:
    for coord_list in monitor_coords_dict.values():
        for coords in coord_list:
            if len(coords)!=2:
                raise ValueError(
                    'Please supply monitoring-coords in following dict syntax: '
                    '{"TARGETFOO":[[268.1,55.2],[270.3,55.5]]}')

    logger.info( "Processing all_obs in: %s", options.calfiles_list)
    with open(options.calfiles_list) as f:
        ami_uvfits_list,_ = driveami.load_listing(f,
                       expected_datatype=driveami.Datatype.ami_la_calibrated)

    all_obs = []
    for rawfile_name, rawfile_info in ami_uvfits_list.iteritems():
        all_obs.append(ami_info_to_obsinfo(rawfile_info))

    processed, rejected, concat = process_obsinfo_list(all_obs,
                         output_dir=options.topdir,
                         monitor_coords_dict=monitor_coords_dict,
                         logging_timestamp=logging_timestamp)

    outfile_processed = options.outfile+"_processed.json"
    outfile_rejected = options.outfile+"_rejected.json"
    outfile_concat = options.outfile+"_concat.json"
    with open(outfile_processed, 'w') as f:
        json.dump(processed, f, cls=ObsInfo.Encoder,
                  indent=2, sort_keys=True)
    with open(outfile_rejected, 'w') as f:
        json.dump(rejected, f, cls=ObsInfo.Encoder,
                  indent=2, sort_keys=True)
    with open(outfile_concat, 'w') as f:
        json.dump(concat, f, cls=ObsInfo.Encoder,
                  indent=2, sort_keys=True)


    sys.exit(0)


if __name__ == "__main__":
    timestamp = datetime.datetime.now().strftime("%y-%m-%dT%H%M%S")
    options = handle_args()
    setup_logging(timestamp)
    main(options, timestamp)


