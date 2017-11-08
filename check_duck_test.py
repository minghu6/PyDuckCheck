# -*- coding:utf-8 -*-

import os
import sys

package_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(package_dir)

from check_duck import required, get_required_methods, check_required_methods, check_duck

def test_get_required_methods():
    class RequiredMethods:
        @required
        def append(self):pass

    check_duck(RequiredMethods, get_required_methods(None))


if __name__ == '__main__':
    test_get_required_methods()