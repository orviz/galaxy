"""Work around for gross circular dependency between galaxy.util and galaxy.web_stack.

Provide a function that will delay until a server forks but runs immediately
otherwise.
"""
try:
    from galaxy.web_stack import register_postfork_function
except ImportError:

    def register_postfork_function(f, *args, **kwargs):
        f(*args, **kwargs)
