import warnings

from .stack import DefaultStack


class _DefaultContextMixin(object):
    def as_default(self):
        return self.__class__.set_default(self)

    @classmethod
    def get_default(cls):
        instance = cls._default_stack.get_default()
        if instance is None and cls._global_default_factory is not None:
            factory = cls._global_default_factory
            try:
                instance = factory()
            except TypeError:
                # Fix for unbounded method error in Python 2
                instance = factory.__func__()

        return instance

    @classmethod
    def set_default(cls, instance):
        return cls._default_stack.get_context_manager(instance)

    @classmethod
    def reset_stack(cls):
        cls._default_stack.reset()


def optional_arg_class_decorator(fn):
    """
    Based on:
    https://stackoverflow.com/questions/3888158/python-making-decorators-with-optional-arguments
    """
    def wrapped_decorator(*args, **kwargs):
        if len(args) == 1 and isinstance(args[0], type) and not kwargs:
            return fn(args[0])
        else:
            def real_decorator(decoratee):
                return fn(decoratee, *args, **kwargs)
            return real_decorator
    return wrapped_decorator


@optional_arg_class_decorator
def with_default_context(cls, use_empty_init=False, factory=None):
    """
    :param use_empty_init: If set to True, object constructed without
            arguments will be an initial default object of the class.
    :param factory: Function that constructs an initial global default object
            on the stack.

    N.B. Either `use_empty_init` should be set to True, or the `factory`
    should be passed, but not both.
    """

    if use_empty_init:
        if factory is not None:
            warnings.warn('Either factory or use_empty_init should be set. '
                          'Assuming use_empty_init=True.')
        factory = cls

    default_stack = DefaultStack()
    class_attrs = dict(
            _default_stack=default_stack,
            _global_default_factory=factory)
    return type(cls.__name__, (cls, _DefaultContextMixin), class_attrs)

