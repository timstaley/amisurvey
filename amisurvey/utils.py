import simplejson as json
from driveami import keys as meta_keys
from chimenea.obsinfo import ObsInfo

import logging
logger = logging.getLogger()

def ami_info_to_obsinfo(ami_info_dict):
    """
    Load the relevant attributes from a dict of AMI-dataset metadata.
    """
    d = ami_info_dict
    return ObsInfo(name = d[meta_keys.obs_name],
                   group= d[meta_keys.group_name],
                   metadata=d,
                   uvfits=d[meta_keys.target_uvfits])


