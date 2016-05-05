#AMIsurvey

An end-to-end calibration and imaging pipeline for data from the 
[AMI-LA](http://www.mrao.cam.ac.uk/telescopes/ami/) radio observatory. 
For a full description, see the accompanying paper, 
[Staley and Anderson (in prep)](https://github.com/timstaley/automated-radio-imaging-paper). 


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
    pip install .

##Usage

    amisurvey_reduce.py --help
