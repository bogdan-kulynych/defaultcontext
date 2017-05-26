import pytest

from defaultcontext.wrappers import with_default_context, _DefaultContextMixin


class Named(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


@with_default_context
class NoFactory(Named):
    pass


def default_name_factory():
    return WithFactory(name='default')


@with_default_context(factory=default_name_factory)
class WithFactory(Named):
    pass


@with_default_context(use_empty_init=True)
class WithEmptyInit(Named):
    def __init__(self, name='default'):
        self.name = name


default_instances = [
    NoFactory(name='default'),
    default_name_factory(),
    WithEmptyInit()
]


classes_with_defaults = [
    (NoFactory, 'None'),
    (WithFactory, 'default'),
    (WithEmptyInit, 'default')
]


@pytest.mark.parametrize('instance', default_instances)
def test_object_is_instance_of_global_context(instance):
    assert isinstance(instance, _DefaultContextMixin)


def test_both_empty_init_and_factory():
    with pytest.warns(UserWarning):
        with_default_context(factory=Named('default'), use_empty_init=True)(Named)


def test_no_factory_get_initial_default():
    assert NoFactory.get_default() is None


@pytest.mark.parametrize('cls', [WithFactory, WithEmptyInit])
def test_with_factory_get_initial_default(cls):
    assert str(cls.get_default()) == 'default'


@pytest.mark.parametrize('cls,default', classes_with_defaults)
def test_as_default(cls, default):
    custom = cls(name='custom')
    assert str(cls.get_default()) == default
    with custom.as_default():
        assert cls.get_default() == custom
    assert str(cls.get_default()) == default


@pytest.mark.parametrize('cls,default', classes_with_defaults)
def test_as_default_nested(cls, default):
    first = cls(name='first')
    second = cls(name='second')
    assert str(cls.get_default()) == default
    with first.as_default():
        assert str(cls.get_default()) == 'first'
        with second.as_default():
            assert str(cls.get_default()) == 'second'
        assert str(cls.get_default()) == 'first'
    assert str(cls.get_default()) == default


@pytest.mark.parametrize('cls,default', classes_with_defaults)
def test_set_default(cls, default):
    instance = cls(name='custom')
    assert str(cls.get_default()) == default
    with cls.set_default(instance):
        assert str(cls.get_default()) == 'custom'
    assert str(cls.get_default()) == default


@pytest.mark.parametrize('cls,default', classes_with_defaults)
def test_set_default_nested(cls, default):
    first = cls(name='first')
    second = cls(name='second')
    assert str(cls.get_default()) == default
    with cls.set_default(first):
        assert str(cls.get_default()) == 'first'
        with cls.set_default(second):
            assert str(cls.get_default()) == 'second'
        assert str(cls.get_default()) == 'first'
    assert str(cls.get_default()) == default
