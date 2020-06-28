
"""Snapped

Usage:
  snapped analyse <index>

Description:
"""

from docopt import docopt
from snapped import snapped

if __name__ == '__main__':
  arguments = docopt(__doc__, version='0.1.0')
  snapped(arguments)
