# defaultcontext

Tiny util for creating tensorflow-like default context managers

Example usage:
```
from defaultcontext import with_default_context


@with_default_context
class Environment:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Environment %s' % self.name


test_env = Environment('test')
prod_env = Environment('prod')

with test_env.as_default():
    print(Environment.get_default())   # test

with prod_env.as_default():
    print(Environment.get_default())   # prod

print(Environment.get_default())       # None

```

