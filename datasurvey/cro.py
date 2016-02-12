import os
import logging

from unidecode import unidecode
from normality import slugify
from cronos import parse
from datasurvey.scanner import DirectoryScanner

log = logging.getLogger(__name__)


class CronosScanner(DirectoryScanner):

    FILES = ['CroBank.dat', 'CroBank.tad', 'CroStru.dat']

    def bid(self):
        if super(CronosScanner, self).bid():
            if self.name.lower().strip() == 'voc':
                return
            for fn in self.FILES:
                path = os.path.join(self.real_path, fn)
                if not os.path.isfile(path):
                    return
            return 100

    def scan(self):
        log.info('Cronos extract: %s', self.path_name)
        target_dir = os.environ.get('CRONOS_OUTDIR')
        if target_dir is None:
            log.warning('No CRONOS_OUTDIR is set.')
            return
        sub_dir = slugify(unidecode(self.path_name), '_')
        target_dir = os.path.join(target_dir, sub_dir)
        try:
            os.makedirs(target_dir)
        except:
            pass
        try:
            parse(self.real_path, target_dir)
        except Exception as ex:
            log.exception(ex)
