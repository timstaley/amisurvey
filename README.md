#AMIsurvey

An end-to-end calibration and imaging pipeline for data from the 
[AMI-LA](http://www.mrao.cam.ac.uk/telescopes/ami/) radio observatory. 


**Currently a work in progress.**

Builds upon:
* [drive-ami](https://github.com/timstaley/drive-ami), for interfacing with the
  AMI-Reduce calibration pipeline.
* [drive-casa](https://github.com/timstaley/drive-casa), for interfacing with 
the NRAO [CASA](http://casa.nrao.edu) image-synthesis routines.
* [chimenea](https://github.com/timstaley/chimenea), which implements a 
  simple iterative algorithm for automated imaging of multi-epoch radio 
  observations.
  
##Installation

    pip install -r requirements.txt
    pip install -r binstar-requirements.txt
    pip install .

##Usage

    amisurvey_reduce.py --help