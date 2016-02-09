import logging
from pkg_resources import iter_entry_points

log = logging.getLogger(__name__)
SCANNERS = {}


def scan_path(store, parent, path):
    if not len(SCANNERS):
        for ep in iter_entry_points('datasurvey.scanners'):
            SCANNERS[ep.name] = ep.load()

    best_scanner = None
    best_bid = 0
    for scanner_cls in SCANNERS.values():
        scanner = scanner_cls(store, parent, path)
        bid = scanner.bid()
        if bid is None:
            continue
        if bid > best_bid:
            best_bid = bid
            best_scanner = scanner
    if best_scanner is None:
        log.warning("Cannot find a scanner for: %r", path)
    else:
        return best_scanner.scan()
