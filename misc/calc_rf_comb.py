import logging
import math
import sys

from enum import Enum
from pathlib import Path
from typing import Callable


class Coefficient(Enum):
    ALPHA = 1.8
    BETA = 1.4

def create_logger(log_file:Path) -> logging.Logger:

    logger = logging.getLogger('Logger')
    logger.setLevel(logging.DEBUG)
    # logging handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    
    #formatter
    debug_formatter = logging.Formatter('%(asctime)s: %(name)s[%(levelname)s]: %(message)s', datefmt='%d.%m.%Y %H:%M:%S')
    info_formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(message)s', datefmt='%d.%m.%Y %H:%M:%S')

    ch.setFormatter(info_formatter)
    fh.setFormatter(debug_formatter)

    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger

def calc_rf_combined(a:float, b:float, c:float=0) -> Callable|float:
    if not c:
        c = min(a, b)/2
    r = (c/a)**Coefficient.ALPHA.value + (c/b)**Coefficient.BETA.value
    if math.isclose(r, 1, rel_tol=1e-04):
        return c
    return calc_rf_combined(a, b, c+(1-r)/2)


def main(input_data:list) -> None:
    
    log = create_logger(Path('./log_file.txt'))
    log.debug(f'Start of RF_C calculation with {input_data=}')

    try:
        rf_s, rf_t = tuple(map(float, input_data))
        rf_c = calc_rf_combined(rf_s, rf_t)
        log.info(f'Calculation successfull. RF_C = {int(rf_c*100)/100}')
    except ValueError as e:
        e.add_note('Input not valid. Please provide RF_S and RF_T as numerical values for the calculation.')
        log.error(e.__notes__[0])


if __name__ == '__main__':
    
    main(sys.argv[1:3])
