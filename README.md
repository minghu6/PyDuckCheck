# PyDuckCheck

```python
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

    class Speak:
        @required
        def blabla(self, words):
            pass

    class A:
        def fly(self):
            return 'I can fly'


    check_duck(GreenDuck, A)


Output:
    raise MissRequiredMethodsError(lacked_methods):
    lack method: green
    lack method: guagua
```

```python
    class Duck:
        @required
        def fly(self):
            pass

        @required
        def guagua(self):
            pass
    
    class Speak:
        @required
        def blabla(self, words):
            pass

    @protocol(Duck, Speak)
    class B2:
        def fly(self):
            return 'fly fly'

        def guagua(self):
            return 'gua gua'

        def blabla(self):
            return 'words'

Output:
    lack method: blabla params: OrderedDict([('self', <Parameter "self">), ('words', <Parameter "words">)])
```
