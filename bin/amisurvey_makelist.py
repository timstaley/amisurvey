#!/usr/bin/env python
import click
from chimenea.obsinfo import ObsInfo
import glob
import os
import json


def main(fits_or_ms, groupname, outfile):
    paths = fits_or_ms
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
    json.dump(obsinfo_list, outfile, cls=ObsInfo.Encoder, indent=2)
    return obsinfo_list


@click.command()
@click.argument('fits_or_ms', nargs=-1, type=click.Path(exists=True))
@click.option('-g','--groupname', default='NOGROUP')
@click.option('-o', '--outfile', type=click.File(mode='w'), default='-')
def cli(fits_or_ms, groupname, outfile):
    obslist = main(fits_or_ms,groupname,outfile)
    click.echo("Wrote list of {} observations".format(len(obslist)))

if __name__ == '__main__':
    cli()