# Copyright (c) 2013-2016 Dassault Systemes. All rights reserved.

class DymolaException(Exception):
    """This is the base class for exceptions from Dymola."""
    pass

class DymolaConnectionException(DymolaException):
    """This exception is thrown when Dymola cannot be started
    and when connection to Dymola is dropped.
    """
    pass

class DymolaFunctionException(DymolaException):
    """This exception is thrown when a call to a function in Dymola fails
    in an unexpected way. The exception is not thrown if, e.g.,
    a model fails to translate. In that case the return code is used instead.
    """
    pass
