import sys
import argparse
import datetime
import time
import pyautogui

CONFIG = {
    'start': '08:00',
    'end': '17:00',
    'interval': '300',
    'nudge': '1',
    'verbose': 'False',
}

params = CONFIG.copy()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser()
        parser.add_argument('--start')
        parser.add_argument('--end')
        parser.add_argument('--interval')
        parser.add_argument('--nudge')
        parser.add_argument('--verbose')
        args = parser.parse_args()

        for key in args.__dict__:
            val = args.__dict__[key]
            if val is not None:
                params[key] = val
    else:
        print('  I will assume you typed this:')
        print('    python', sys.argv[0], '--start', CONFIG['start'], '--end', CONFIG['end'], '--interval',  CONFIG['interval'], '--nudge', CONFIG['nudge'], '--verbose', CONFIG['verbose'])
        print('  (all params are optional)')

try:
    params['interval'] = float(params['interval'])
    params['nudge'] = float(params['nudge'])
    params['verbose'] = params['verbose'].lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']

    start_time = datetime.datetime.strptime(params['start'], '%H:%M')
    start_time_val = start_time.hour + start_time.minute / 60

    end_time = datetime.datetime.strptime(params['end'], '%H:%M')
    end_time_val = end_time.hour + end_time.minute / 60
    
except ValueError as e:
    print('Bad user:', e)
    print('  Try something like:')
    print('    python', sys.argv[0], '--start', CONFIG['start'], '--end', CONFIG['end'], '--interval',  CONFIG['interval'], '--nudge', CONFIG['nudge'], '--verbose', CONFIG['verbose'])
    print('  (all params are optional)')
    exit(1)

if end_time_val > start_time_val:
    in_hours = lambda now_val: now_val > start_time_val and now_val < end_time_val
else:
    in_hours = lambda now_val: now_val > start_time_val or now_val < end_time_val

dist = params['nudge']
verbose = params['verbose']

while True:
    now = datetime.datetime.now()
    now_val = now.hour + now.minute / 60

    if in_hours(now_val):
        if verbose:
            print('jiggle', now)
        pyautogui.moveRel(dist, dist)
        pyautogui.moveRel(-2*dist, -2*dist)
        pyautogui.moveRel(dist, dist)

    time.sleep(params['interval'])
