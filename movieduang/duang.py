#!/usr/bin/env python3
import sys
import os


def main():
    duang_path = os.environ.get('DUANGPATH')
    if duang_path is not None:  # you can add your own special effect here
        sys.path.append(duang_path)
    sys.path.append(os.path.dirname(os.path.realpath(__file__)))
    me = sys.argv.pop(0)
    if len(sys.argv) == 0:
        me = os.path.split(me)[-1]
        print("Usage: %s cmd" % me)
        print("For more details, use %s cmd -h." % me)
    else:
        cmd = sys.argv[0]
        sys.argv[0] = me + " " + sys.argv[0]
        module = __import__(cmd)
        module.main()


if __name__ == '__main__':
    main()
