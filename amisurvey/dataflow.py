from __future__ import absolute_import
import os
import drivecasa
import chimenea
import driveami.keys as meta_keys
import amisurvey.amiconfig as amiconfig
import amisurvey.utils as utils

import logging
logger = logging.getLogger(__name__)


def output_preamble_to_log(groups):
    """
    Prettyprint the group listings
    """
    logger=logging.getLogger()
    logger.info("*************************")
    logger.info("Processing groups:")
    for key in sorted(groups.keys()):
        logger.info("%s:", key)

        pointings = [f.meta[meta_keys.pointing_degrees] for f in groups[key] ]
        pointings = set((i[0], i[1]) for i in pointings)
        logger.info("%s different pointings:" % len(pointings))
        logger.info(str(pointings))
        for f in groups[key]:
            pointing = f.meta[meta_keys.pointing_degrees]
            ra, dec = pointing[0], pointing[1]
            logger.info("\t %s,  (%.4f,%.4f)", f.name.ljust(24), ra, dec),
        logger.info("--------------------------------")
    logger.info("*************************")


def reduce_listings(listings_file, output_dir, monitor_coords,
                    reduction_timestamp):
    """
    Perform data reduction on observations listed in ``listings_file``.

    **Args:**

    - listings_file: Path to json file containing observations info.
    - output_dir: Outputs here, futher divided into 'casa' and 'images' folders.
    - monitor_coords: a list of (RA,Dec) tuples which we want to add to our clean
      mask.
    - reduction_timestamp: Timestamp used when naming logfiles.
    """

    logger = logging.getLogger()
    logger.info( "Processing all_obs in: %s", listings_file)
    all_obs = utils.load_listings(listings_file)
    groups = utils.get_grouped_file_listings(all_obs)
    output_preamble_to_log(groups)

    for group_name in sorted(groups.keys()):
        #Setup output directories:
        grp_dir = os.path.join(os.path.expanduser(output_dir), str(group_name))
        casa_output_dir = os.path.join(grp_dir, 'casa')
        fits_output_dir = os.path.join(grp_dir, 'images')
        casa_logfile = os.path.join(casa_output_dir,
                            'casalog_{}.txt'.format(reduction_timestamp))
        commands_logfile = os.path.join(casa_output_dir,
                             'casa_commands_{}.txt'.format(reduction_timestamp))
        casa = drivecasa.Casapy(casa_logfile=casa_logfile,
                                commands_logfile=commands_logfile,
                                working_dir=casa_output_dir,)
        logger.info("Processing %s", group_name)
        logger.info("CASA logfile at: %s",casa_logfile)
        logger.info("Commands logfile at: %s",commands_logfile)

        #Filter those obs with extreme rain values
        good_obs, rejected = amiconfig.reject_bad_obs(groups[group_name])
        chimenea.pipeline.process_observation_group(good_obs,
                                  amiconfig.ami_chimconfig,
                                  monitor_coords,
                                  casa_output_dir,
                                  fits_output_dir,
                                  casa)
    return groups


