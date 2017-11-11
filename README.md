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


    class A:
        def fly(self):
            return 'I can fly'


    check_duck(GreenDuck, A)

Output:
raise MissRequiredMethodsError(lacked_methods):
lack method: green
lack method: guagua

```