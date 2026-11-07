from distutils.core import setup # Need this to handle modules
import py2exe  # noqa: F401  (side effect: registers py2exe command)
setup(console=['chiffrement.py']) #making console based exe file