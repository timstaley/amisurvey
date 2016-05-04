import click
from chimenea.obsinfo import ObsInfo
import glob
import os
import json


def main(glob_pattern, groupname, outfile):
    paths = glob.glob(glob_pattern)
    paths = [os.path.abspath(p) for p in paths]
    obsinfo_list = []
    for p in paths:
        basename = os.path.basename(p)
        if os.path.isdir(p):
            o = ObsInfo(name=basename, group=groupname,
                        uvms=p)
        else:
            o = ObsInfo(name=basename, group=groupname,
                        uvfits=p)
        obsinfo_list.append(o)
    print json.dumps(obsinfo_list, outfile, cls=ObsInfo.Encoder, indent=2)


@click.command()
@click.argument('glob_pattern')
@click.option('-g','--groupname', default='NOGROUP')
@click.option('-o', '--outfile', type=click.File(mode='w'), default='-')
def cli(glob_pattern, groupname, outfile):
    main(glob_pattern,groupname,outfile)

if __name__ == '__main__':
    cli()