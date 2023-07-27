import click
from pathlib import Path
import sizebased_compress_lib.smart_compress as smart_compress
import cv2
import os
import logging

LoggingLevels = {'info': logging.INFO, 'error': logging.ERROR, 'warning': logging.WARNING, 'debug': logging.DEBUG} # ToDo: Try enum

@click.command()
@click.argument("src", type=click.Path(exists=True, dir_okay=False, readable=True ,path_type=Path))
@click.argument("dst", type=click.Path(dir_okay=False, writable=True ,path_type=Path))
@click.argument("size", type=int)
@click.option('--log', type=click.Choice(LoggingLevels.keys()) ,default='info', help='Set logging level')
@click.option('--overwrite/--no-overwrite', type=bool ,default=False, help='Overwrite if DST exists')
def compress_img(src :Path, dst :Path, size :int, log :str, overwrite :bool):
    logging.basicConfig(level=LoggingLevels[log])

    # Check
    src_size = os.path.getsize(src)
    if dst.exists():
        if overwrite:
            logging.debug('Target path already exist, overwriting...')
        else:
            logging.warning('Target path already exist, skipping...')
            return
    if size >= src_size:
        logging.info('Target size >= source file size, skipping...')
        return

    # Compress
    src_img = cv2.imread(str(src) ,cv2.IMREAD_UNCHANGED)
    try:
        quality,dst_bytes = smart_compress.smart_compress(src_img, size)
    except Exception as err:
        logging.error(err)

    dst_size = len(dst_bytes)

    with open(dst, 'wb') as dst_file:
        dst_file.write(dst_bytes)

    # Log result
    logging.info(f"Compressed {src} to {dst_size} Bytes, quality={quality}")

if __name__=='__main__':
    compress_img()