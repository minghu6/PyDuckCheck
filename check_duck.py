# -*- coding:utf-8 -*-

from inspect import signature


class MissRequiredMethodsError(Exception):
    def __init__(self, attrs):
        self.attrs = unify_to_iterable(attrs)

    def __str__(self):
        msg = ['\n']
        for attr in self.attrs:
            msg.append('lack method: %s' % attr)

        return '\n'.join(msg)


def isiterable(obj, but_str_bytes=True):
    """
    :param obj:
    :param but_str_bytes: most of time, we don't need str and bytes
    :return:
    """
    from collections import Iterable
    if but_str_bytes and isinstance(obj, (str, bytes, bytearray)):
        return False
    else:
        return isinstance(obj, Iterable)


def unify_to_iterable(var):
    if isiterable(var):
        return var

    return [var]


REQUIRED = 'required'


def required(f):
    def wrapper_func(*args, **kwasrgs):
        raise NotImplementedError

    setattr(wrapper_func, REQUIRED, True)

    return wrapper_func


def get_required_methods(cls):
    required_methods = []
    for attr_s in dir(cls):
        attr = getattr(cls, attr_s)
        if callable(attr) and getattr(attr, REQUIRED, False) and len(signature(attr).parameters)>0:
            required_methods.append(attr_s)

    return required_methods


def check_required_methods(cls, required_methods):
    lacked_methods = []
    for attr_s in required_methods:
        if not getattr(cls, attr_s, False):
            lacked_methods.append(attr_s)

    if lacked_methods:
        raise MissRequiredMethodsError(lacked_methods)


def check_duck(duck, target_cls):
    required_methods = get_required_methods(duck)
    check_required_methods(target_cls, required_methods)


if __name__ == '__main__':
    class Duck:
        @required
        def fly(self):
            pass

        @required
        def guagua(self):
            pass


    class GreenDuck(Duck):
        @required
        def green(self):
            return 'green'


    class A:
        def fly(self):
            return 'I can fly'


    check_duck(GreenDuck, A)