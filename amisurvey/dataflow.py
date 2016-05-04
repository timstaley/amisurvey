from __future__ import absolute_import
import os
from collections import defaultdict
import drivecasa
import chimenea.pipeline
import driveami.keys as meta_keys
import amisurvey.amiconfig as amiconfig


import logging
logger = logging.getLogger(__name__)

def process_obsinfo_list(all_obs, output_dir, monitor_coords_dict,
                         logging_timestamp):
    obs_groups = defaultdict(list)
    for obs in all_obs:
        obs_groups[obs.group].append(obs)
    logger.info("*************************")
    logger.info("Processing {} groups:".format(len(obs_groups)))
    output_preamble_to_log(obs_groups, monitor_coords_dict)
    logger.info("*************************")
    logger.info("")
    all_processed_obs = []
    all_rejected_obs = []
    all_concat_obs = []
    for groupname, obs in sorted(obs_groups.items()):
        logger.info("*************************")
        logger.info("Currently processing:")
        output_preamble_to_log({groupname:obs_groups[groupname]},
                               monitor_coords_dict)
        #Filter those obs with extreme rain values
        good_obs, rejected = amiconfig.reject_bad_obs(obs)
        all_rejected_obs.extend(rejected)
        if good_obs:
            try:
                processed_group_obs, group_concat_ob = image_group(good_obs, output_dir,
                            monitor_coords=monitor_coords_dict.get(groupname,None),
                            reduction_timestamp=logging_timestamp)
                all_processed_obs.extend(processed_group_obs)
                all_concat_obs.append(group_concat_ob)
                logger.info("Group processed successfully")
            except Exception as e:
                logger.exception("ERROR reducing group {}".format(groupname))
        else:
            logger.info("No good observations in group.")
        logger.info("*************************")
    return all_processed_obs, all_rejected_obs, all_concat_obs


def output_preamble_to_log(groups,monitor_coords_dict):
    """
    Prettyprint the group listings
    """
    for key in sorted(groups.keys()):
        logger.info("%s:", key)
        mc_list = monitor_coords_dict.get(key,None)
        pointings = [f.meta[meta_keys.pointing_degrees] for f in groups[key]
                     if f.meta]
        if pointings:
            pointings = set((i[0], i[1]) for i in pointings)
        logger.info("%s different pointings:" % len(pointings))
        logger.info(str(pointings))
        logger.info("Monitoring coords:")
        logger.info("{}".format(mc_list))
        for f in groups[key]:
            if f.meta:
                pointing = f.meta[meta_keys.pointing_degrees]
                ra, dec = pointing[0], pointing[1]
                logger.info("\t %s,  (%.4f,%.4f)", f.name.ljust(24), ra, dec),
        logger.info("--------------------------------")


def image_group(obs_list, output_dir, monitor_coords,
                    reduction_timestamp):
    """
    Perform image-synthesis of calibrated uvFITS listed in ``listings_file``.

    This routine sets up the CASA reduction environment,
    then kicks off the chimenea iterative-imaging routine with
    AMI-specific configuration.

    **Args:**

    - obs_group: List of ObsInfo representing calibrated epochs of observation
        (for a single target, i.e. all belonging to same groups)
    - output_dir: Outputs here, futher divided into 'casa' and 'images' folders.
    - monitor_coords: a list of (RA,Dec) tuples which we want to add to our clean
      mask.
    - reduction_timestamp: Timestamp used when naming logfiles.
    """
    group_name = obs_list[0].group
    for obs in obs_list:
        #sanity check:
        assert obs.group == group_name

    #Setup output directories:
    grp_dir = os.path.join(output_dir, str(group_name))
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
    obs_list, concat_ob = chimenea.pipeline.process_observation_group(obs_list,
                              amiconfig.ami_chimconfig,
                              monitor_coords,
                              casa_output_dir,
                              fits_output_dir,
                              casa)
    return obs_list, concat_ob


