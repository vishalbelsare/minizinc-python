#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.

from support import InstanceTestCase

from minizinc import Solver
from minizinc.helpers import check_solution
from minizinc.instance import Method


class CheckResults(InstanceTestCase):
    code = """
        array[1..2] of var 1..10: x;
        constraint x[1] + 1 = x[2];
    """
    other_solver = Solver.lookup("chuffed")

    def test_correct(self):
        assert self.instance.method == Method.SATISFY
        result = self.instance.solve()
        assert check_solution(self.instance, result, self.other_solver)

    def test_incorrect(self):
        assert self.instance.method == Method.SATISFY
        result = self.instance.solve()
        result.solution = self.instance.output_type(x=[2, 1])
        assert not check_solution(self.instance, result, self.other_solver)

    def test_check_all(self):
        assert self.instance.method == Method.SATISFY
        result = self.instance.solve(all_solutions=True)
        assert check_solution(
            self.instance, result, self.other_solver, range(len(result.solution))
        )

    def test_check_specific(self):
        assert self.instance.method == Method.SATISFY
        result = self.instance.solve(nr_solutions=5)
        assert check_solution(self.instance, result, self.other_solver, [1, 2])
