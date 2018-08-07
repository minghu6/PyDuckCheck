# -*- coding:utf-8 -*-

from inspect import signature
from collections import namedtuple


class MissRequiredMethodsError(Exception):
    def __init__(self, methods):
        self.methods = unify_to_iterable(methods)

    def __str__(self):
        msg = ['\n']
        for method in self.methods:
            msg.append('lack method: %s params: %s' % (method.name, str(method.params)))

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


def flatten(items, class_type):
    """Yield items from any nested iterable; see REF."""
    for x in items:
        if not isinstance(x, class_type):
            yield from flatten(x, class_type)
        else:
            yield x


def unify_to_iterable(var):
    if isiterable(var):
        return var

    return [var]


REQUIRED = 'required'
MethodTuple = namedtuple('MethodTuple', ['name', 'params'])


def required(f):
    setattr(f, REQUIRED, True)

    return f


def get_required_methods(cls):
    required_methods = []
    for attr_s in dir(cls):
        attr = getattr(cls, attr_s)
        if callable(attr) and getattr(attr, REQUIRED, False) and len(signature(attr).parameters)>0:
            # print(MethodTuple(attr_s, signature(attr).parameters))
            required_methods.append(MethodTuple(attr_s, signature(attr).parameters))

    return required_methods


def _check_required_method(cls, method):
    method_name, params = method.name, method.params
    attr = getattr(cls, method_name, False)

    if not attr:
        return False
    if not callable(attr):
        return False

    #print(params, signature(attr).parameters, method_name, cls)

    return params.items() == signature(attr).parameters.items()


def check_required_methods(cls, required_methods):
    lacked_methods = [method for method in required_methods if not _check_required_method(cls, method)]

    if lacked_methods:
        raise MissRequiredMethodsError(lacked_methods)


def check_duck(duck, target_cls):
    if isiterable(duck):
        required_methods = flatten(map(get_required_methods, duck), MethodTuple)
    else:
        required_methods = get_required_methods(duck)

    check_required_methods(target_cls, required_methods)


def protocol(*duck_feature_cls):
    def class_wrapper_func(cls):
        check_duck(duck_feature_cls, cls)

        return cls
        # class WrapperClass:
        #     def __init__(self, *args, **kwargs):
        #         check_duck(duck_feature_cls, cls)
        #         print('hi?????????????', cls, duck_feature_cls)
        #         self.__wrapped = cls(*args, **kwargs)
        #
        #     def __getattr__(self, name):
        #         return getattr(self.__wrapped, name)
        #
        # return WrapperClass
    return class_wrapper_func


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

    class Speak:
        @required
        def blabla(self, words):
            pass

    try:
        check_duck(GreenDuck, A)
    except Exception as ex:
        print(ex)


    @protocol(Duck, Speak)
    class B:
        def fly(self):
            return 'fly fly'

        def guagua(self):
            return 'gua gua'

        def blabla(self):
            return 'words'

    @protocol(Duck, Speak)
    class B2:
        def fly(self):
            return 'fly fly'

        def guagua(self):
            return 'gua gua'

        def blabla(self, words):
            return 'words'

    print('check B')
    #B()
    # try:
    #     check_duck([Duck, Speak], B)
    # except MissRequiredMethodsError as ex:
    #     print(ex)
    #
    # try:
    #     check_duck([Duck, Speak], B2)
    # except MissRequiredMethodsError as ex:
    #     print(ex)
    # else:
    #     print('B2 ok')

    #B
