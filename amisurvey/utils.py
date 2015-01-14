import simplejson as json
from chimenea.obsinfo import ObsInfo

import logging
logger = logging.getLogger()

from driveami import keys as meta_keys
from chimenea.obsinfo import ObsInfo

def parse_monitoringlist_positions(opts):
    """Loads a list of monitoringlist (RA,Dec) tuples from cmd line opts object.

    Processes the flags "--monitor-coords" and "--monitor-list"
    NB This is just a dumb function that does not care about units,
    those should be matched against whatever uses the resulting values...
    """
    monitor_coords = []
    if opts.monitor_coords:
        try:
            monitor_coords.extend(json.loads(opts.monitor_coords))
        except ValueError:
            logger.error("Could not parse monitor-coords from command line:"
                         "string passed was:\n%s", opts.monitor_coords
                         )
            raise
    if opts.monitor_list:
        try:
            mon_list = json.load(open(opts.monitor_list))
            monitor_coords.extend(mon_list)
        except ValueError:
            logger.error("Could not parse monitor-coords from file: "
                              + opts.monitor_list)
            raise
    return monitor_coords


def ami_info_to_obsinfo(ami_info_dict):
    """
    Load the relevant attributes from a dict of AMI-dataset metadata.
    """
    d = ami_info_dict
    return ObsInfo(name = d[meta_keys.obs_name],
                   group= d[meta_keys.group_name],
                   metadata=d,
                   uvfits=d[meta_keys.target_uvfits])


def load_listings(listings_path):
    """
    Loads a list of ObsInfo objects from a json file
    """
    # simplejson loads plain strings as simple 'str' objects:
    ami_listings = json.load(open(listings_path))
    all_obs = []
    for ami_rawfile, ami_obs in ami_listings.iteritems():
        all_obs.append(ami_info_to_obsinfo(ami_obs))
    return all_obs


def get_grouped_file_listings(all_obs):
    """
    Groups a list of ObsInfo objects by ``group`` attribute.

    Returns: Dict mapping groupname -> list of ObsInfo
    """
    grp_names = list(set([obs.group for obs in all_obs]))
    groups_dict = {}
    for g_name in grp_names:
        grp = [obs for obs in all_obs if obs.group == g_name]
        groups_dict[g_name] = grp
    return groups_dict



