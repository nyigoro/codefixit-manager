touch cfm/engine/__init__.py
touch cfm/utils/__init__.py
try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version

__version__ = version("codefixit-manager")
