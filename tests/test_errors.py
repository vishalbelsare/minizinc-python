import pytest
from minizinc.error import (Location, MiniZincAssertionError,
                            MiniZincSyntaxError, MiniZincTypeError)
from test_case import InstanceTestCase


class AssertionTest(InstanceTestCase):
    code = """
        array [1..10] of int: a = [i | i in 1..10];
        constraint assert(forall (i in 1..9) (a[i] > a[i + 1]), "a not decreasing");
        var 1..10: x;
        constraint a[x] = max(a);
        solve satisfy;
    """

    def test_assert(self):
        with pytest.raises(MiniZincAssertionError, match="a not decreasing") as error:
            self.solver.solve(self.instance)
        loc = error.value.location
        assert str(loc.file).endswith(".mzn")
        assert loc.line == 3
        assert loc.columns == Location.unknown().columns


class TypeErrorTest(InstanceTestCase):
    code = """
        array[1..2] of var int: i;
        constraint i = 1.5;
    """

    def test_assert(self):
        with pytest.raises(MiniZincTypeError, match="No matching operator found") as error:
            self.solver.solve(self.instance)
        loc = error.value.location
        assert str(loc.file).endswith(".mzn")
        assert loc.line == 3
        assert loc.columns == range(20, 26)


class SyntaxErrorTest(InstanceTestCase):
    code = """
        constrain true;
    """

    def test_assert(self):
        with pytest.raises(MiniZincSyntaxError, match="unexpected bool literal") as error:
            self.solver.solve(self.instance)
        loc = error.value.location
        assert str(loc.file).endswith(".mzn")
        assert loc.line == 2
        assert loc.columns == range(19, 22)