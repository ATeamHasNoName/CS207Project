from pytest import raises
from timeseries import TimeSeries
from lazy import lazy, lazy_add, lazy_mul, LazyOperation

@lazy
def lazy_kwargs_mul(a, b, optional = 1):
    """
        Test LazyOperation.eval() to verify functionality of self._kwargs.items()

        Returns
        -------
        a * b : the product of the two provided values
        a * b * optional : the product of the three provided values, if a value is provided for optional

        Notes
        -----
        PRE: if a value is provided for 'optional', the operation is altered
    """
    if optional != 1:
        return a * b * optional
    return a * b

@lazy
def lazy_kwargs_add(a, b, optional = 0):
    """
        Test LazyOperation.eval() to verify functionality of self._kwargs.items()

        Returns
        -------
        a + b : the sum of the two provided values
        a + b + optional : the sum of the three provided values, if a value is provided for optional

        Notes
        -----
        PRE: if a value is provided for 'optional', the operation is altered
    """
    if optional != 0:
        return a + b + optional
    return a + b

def test_isinstance():
    assert isinstance(lazy_add(1,1), LazyOperation) == True
    assert isinstance(lazy_mul(5,1), LazyOperation) == True

def test_add():
    assert lazy_add(1,1).eval() == 2
    assert lazy_add(2,8).eval() == 10

def test_mul():
    assert lazy_mul(5,1).eval() == 5

def test_multiple_operations():
    assert lazy_mul(4, lazy_add(-2,4)).eval() == 8
    assert lazy_add(100, lazy_mul(5, 4)).eval() == 120

def test_lazy_kwargs_add():
    assert lazy_kwargs_add(2, 3).eval() == 5
    assert lazy_kwargs_add(1, 5, optional = 50).eval() == 56

def test_lazy_kwargs_mul():
    assert lazy_kwargs_mul(5, 2).eval() == 10
    assert lazy_kwargs_mul(1, 5, optional = 10).eval() == 50

def test_lazy_interpolate():
    ts = TimeSeries([1,2,3,4,5], [0,5,10,15,20])
    assert ts.interpolate([-100, 100]).lazy.eval() == TimeSeries([1,5],[-100,100])