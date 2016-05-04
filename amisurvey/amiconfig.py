"""Settings and routines specific to AMI-LA"""
from __future__ import absolute_import
from driveami import keys as meta_keys
from chimenea.config import SourcefinderConfig, CleanConfig, ChimConfig
import numpy as np

import logging
logger = logging.getLogger(__name__)

image_pixel_dim = 512

pixel_size_arcsec = 5.0


ami_clean_args= {
    "spw": '0:0~5',
    "imsize": [image_pixel_dim, image_pixel_dim],
    "cell": [str(pixel_size_arcsec)+'arcsec'],
    "pbcor": False,
    # "weighting": 'natural',
    "weighting": 'briggs',
    "robust": 0.5,
    #          "weighting":'uniform',
    "psfmode": 'clark',
    "imagermode": 'csclean',
}

clean_conf = CleanConfig(niter=500, sigma_threshold=3,
                         other_args=ami_clean_args)

sf_conf = SourcefinderConfig(detection_thresh=5., analysis_thresh=3.,
                             back_size=64,
                             margin=128,
                             radius=None)


default_ami_central_freq = 15.37e9

def ami_sigma_arcmin(freq_hz):
    return 24.905/(freq_hz*1e-9) + 0.79

arcmin_per_pix = pixel_size_arcsec/60
pb_sigma_arcmin = ami_sigma_arcmin(default_ami_central_freq)
sigma_pix = pb_sigma_arcmin/arcmin_per_pix

def ami_la_pbcor_curve(radius_pix):
    return np.exp( -(radius_pix/sigma_pix)**2 / 2.)

cutoff_radius = 3*sigma_pix

####################################################

ami_chimconfig = ChimConfig(clean_conf, sf_conf,
                            max_recleans=3,
                            reclean_rms_convergence=0.05,
                            mask_source_sigma = 5.5,
                            mask_ap_radius_degrees = 60./3600,
                            pb_correction_curve=ami_la_pbcor_curve,
                            pb_cutoff_pix=cutoff_radius
                            )




default_rain_min, default_rain_max = 0.8, 1.2


def reject_bad_obs(obs_list,
                   rain_min=default_rain_min,
                   rain_max=default_rain_max):
    """
    Run quality control on a list of ObsInfo.

    Currently just filters on rain gauge values.
    Returns 2 lists: [passed],[failed]
    """
    good_files = []
    rain_rejected = []
    for obs in obs_list:
        if not obs.meta:
            logger.warning("No metadata for file {}".format(obs.name))
            good_files.append(obs)
            continue
        rain_amp_mod = obs.meta[meta_keys.rain]
        if (rain_amp_mod > rain_min and rain_amp_mod < rain_max):
            good_files.append(obs)
        else:
            rain_rejected.append(obs)
            logger.info("Rejected file %s due to rain value %s" %
                        (obs.name,rain_amp_mod))
    return good_files, rain_rejected