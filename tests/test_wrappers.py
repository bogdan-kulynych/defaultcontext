import pytest

from defaultcontext.wrappers import with_default_context, _DefaultContextMixin


class Named(object):
    """Test class."""
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


@with_default_context
class NoFactory(Named):
    """Class with no default factory."""
    pass


def default_name_factory():
    return WithFactory(name='default')


@with_default_context(global_default_factory=default_name_factory)
class WithFactory(Named):
    """Class with default factory."""
    pass


@with_default_context(use_empty_init=True)
class WithEmptyInit(Named):
    """Class with default factory being empty __init__."""
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
        with_default_context(
                global_default_factory=Named('default'),
                use_empty_init=True)(Named)


def test_no_global_default():
    assert NoFactory.get_default() is None


@pytest.mark.parametrize('cls', [WithFactory, WithEmptyInit])
def test_global_default(cls):
    assert str(cls.get_default()) == 'default'


@pytest.mark.parametrize('cls', [WithFactory, WithEmptyInit])
def test_global_default_is_singleton(cls):
    id(cls.get_default()) == id(cls.get_default())


@pytest.mark.parametrize('cls', [WithFactory, WithEmptyInit])
def test_global_default_reset(cls):
    default1 = cls.get_default()
    cls.reset_defaults()
    default2 = cls.get_default()
    assert id(default1) != id(default2)


@pytest.mark.parametrize('cls,default', classes_with_defaults)
def test_preserves_doc(cls, default):
    assert cls.__doc__ is not None
    assert cls.__doc__ == globals()[cls.__name__].__doc__


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
def test_set_global_default(cls, default):
    instance = cls(name='custom')
    assert str(cls.get_default()) == default
    cls.set_global_default(instance)
    assert str(cls.get_default()) == 'custom'
    cls.reset_defaults()


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
