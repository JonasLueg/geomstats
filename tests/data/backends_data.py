import geomstats.backend as gs
from geomstats.geometry.matrices import Matrices
from geomstats.geometry.spd_matrices import SPDMatrices
from geomstats.geometry.special_orthogonal import SpecialOrthogonal
from geomstats.geometry.symmetric_matrices import SymmetricMatrices
from tests.data_generation import TestData

rand = gs.random.rand


class BackendsTestData(TestData):
    def _array_data(self):
        func_name = "array"

        args = [
            ([],),
            (1.5,),
            (gs.array(1.5),),
            ([gs.ones(2), gs.ones(2)],),
            ([gs.ones(1), gs.ones(1)],),
            ([gs.ones(2), [0, 0]],),
        ]

        return [{"func_name": func_name, "args": args_} for args_ in args]

    def _additional_array_data(self):

        data = [
            dict(func_name="zeros", args=(2,)),
            dict(func_name="zeros", args=((2, 2),)),
            dict(func_name="ones", args=(2,)),
            dict(func_name="ones", args=((2, 2),)),
        ]

        return data

    def array_like_np_test_data(self):
        smoke_data = []

        smoke_data += self._array_data()
        smoke_data += self._additional_array_data()

        return self.generate_tests(smoke_data)

    def _einsum_data(self):
        func_name = "einsum"

        args = [
            ("...i,...i->...", rand(2, 2), rand(2, 2)),
            ("...i,...i->...", rand(2, 2), rand(2)),
            ("...i,...i->...", rand(2), rand(2, 2)),
            ("...i,...i->...", rand(2), rand(2)),
            ("...,...i->...i", rand(1), rand(1, 3)),
            ("...,...i->...i", rand(1), rand(3)),
            ("...,...i->...i", 5.0, rand(1, 3)),
            ("...,...i->...i", 5.0, rand(3)),
            ("...,...i->...i", rand(3), rand(1, 3)),
            ("...,...i->...i", rand(3), rand(3)),
            ("...ij,...ik->...jk", rand(3, 2, 2), rand(3, 2, 2)),
            ("...ij,...ik->...jk", rand(2, 2), rand(3, 2, 2)),
            ("...ij,...ik->...jk", rand(3, 2, 2), rand(2, 2)),
            ("...ij,...ik->...jk", rand(2, 2), rand(2, 2)),
            ("...i,...ijk->...jk", rand(3), rand(3, 3, 3)),
            ("...i,...ijk->...jk", rand(3), rand(1, 3, 3, 3)),
            ("...i,...ijk->...jk", rand(2, 3), rand(2, 3, 3, 3)),
            ("...i,...ijk->...jk", rand(2, 3), rand(3, 3, 3)),
            ("...k,...j,...i->...kji", rand(3), rand(3), rand(3)),
            ("...k,...j,...i->...kji", rand(2, 3), rand(3), rand(3)),
        ]
        return [{"func_name": func_name, "args": args_} for args_ in args]

    def _logm_expm_data(self, func_name="linalg.logm"):
        arrays = [
            Matrices.to_diagonal(rand(3, 3)),
            # TODO: uncomment or delete?
            # Matrices.to_symmetric(rand(3, 3)),
            # rand(3, 3),
        ]
        return [dict(func_name=func_name, a=array) for array in arrays]

    def func_like_np_test_data(self):
        smoke_data = []
        smoke_data += self._einsum_data()

        return self.generate_tests(smoke_data)

    def unary_op_like_np_test_data(self):
        smoke_data = [
            dict(func_name="trace", a=rand(2, 2)),
            dict(func_name="trace", a=rand(3, 3)),
            dict(func_name="linalg.cholesky", a=SPDMatrices(3).random_point()),
            dict(func_name="linalg.eigvalsh", a=SymmetricMatrices(3).random_point()),
        ]
        return self.generate_tests(smoke_data)

    def unary_op_like_scipy_test_data(self):
        smoke_data = []
        smoke_data += self._logm_expm_data()
        smoke_data += self._logm_expm_data("linalg.expm")

        return self.generate_tests(smoke_data)

    def unary_op_vec_test_data(self):
        smoke_data = [
            dict(func_name="trace", a=rand(3, 3)),
            dict(func_name="linalg.cholesky", a=SPDMatrices(3).random_point()),
            dict(func_name="linalg.eigvalsh", a=SymmetricMatrices(3).random_point()),
        ]
        smoke_data += self._logm_expm_data()
        smoke_data += self._logm_expm_data("linalg.expm")

        return self.generate_tests(smoke_data)

    def binary_op_like_np_test_data(self):
        smoke_data = [
            dict(func_name="matmul", a=rand(2, 2), b=rand(2, 2)),
            dict(func_name="matmul", a=rand(2, 3), b=rand(3, 2)),
            dict(func_name="outer", a=rand(3), b=rand(3)),
            dict(func_name="outer", a=rand(3), b=rand(4)),
            dict(func_name="dot", a=rand(3), b=rand(3)),
            dict(func_name="cross", a=rand(3), b=rand(3)),
        ]

        return self.generate_tests(smoke_data)

    def binary_op_like_einsum_test_data(self):
        smoke_data = [
            dict(func_name="matvec", a=rand(3, 3), b=rand(3), einsum_expr="ij,j->i")
        ]

        return self.generate_tests(smoke_data)

    def binary_op_vec_test_data(self):
        smoke_data = [
            dict(func_name="matmul", a=rand(3, 4), b=rand(4, 3)),
            dict(func_name="matmul", a=rand(3, 3), b=rand(3, 3)),
            dict(func_name="outer", a=rand(3), b=rand(3)),
            dict(func_name="outer", a=rand(3), b=rand(4)),
            dict(func_name="matvec", a=rand(3, 3), b=rand(3)),
            dict(func_name="matvec", a=rand(4, 3), b=rand(3)),
            dict(func_name="dot", a=rand(3), b=rand(3)),
            dict(func_name="cross", a=rand(3), b=rand(3)),
        ]

        return self.generate_tests(smoke_data)

    def binary_op_vec_raises_error_test_data(self):
        return self.binary_op_vec_test_data()

    def binary_op_raises_error_test_data(self):
        smoke_data = [
            dict(func_name="matmul", a=rand(1), b=rand(1)),
            dict(func_name="matmul", a=rand(2, 3, 3), b=rand(2, 3)),
            dict(func_name="matmul", a=rand(2, 3, 3), b=rand(3, 3, 3)),
            dict(func_name="matvec", a=rand(3, 2), b=rand(3)),
            dict(func_name="dot", a=rand(4), b=rand(3)),
            dict(func_name="dot", a=rand(3, 4), b=rand(3)),
            dict(func_name="cross", a=rand(4), b=rand(4)),
        ]

        return self.generate_tests(smoke_data)

    def binary_op_runs_test_data(self):
        smoke_data = []

        return self.generate_tests(smoke_data)

    def _pad_data(self):
        func_name = "pad"

        n, m = 2, 3
        args = [
            (gs.ones((n, n)), [[0, 1], [0, 1]]),
            (gs.ones((n, n)), [[0, 1], [0, 0]]),
            (gs.ones((m, n, n)), [[0, 0], [0, 1], [0, 1]]),
        ]
        expected = [(n + 1, n + 1), (n + 1, n), (m, n + 1, n + 1)]

        return [
            {"func_name": func_name, "args": args_, "expected": expected_}
            for args_, expected_ in zip(args, expected)
        ]

    def func_out_shape_test_data(self):
        smoke_data = []

        smoke_data += self._pad_data()

        return self.generate_tests(smoke_data)

    def func_out_type_test_data(self):
        smoke_data = [
            dict(func_name="shape", args=(gs.ones(3),), expected=tuple),
        ]

        return self.generate_tests(smoke_data)

    def func_out_bool_test_data(self):
        smoke_data = [
            dict(func_name="is_array", args=[gs.ones(2)], expected=True),
            dict(func_name="is_array", args=([1, 2],), expected=False),
            dict(func_name="is_array", args=(1,), expected=False),
        ]

        return self.generate_tests(smoke_data)

    def _take_data(self):
        func_name = "take"

        vec = gs.array([0, 1])
        indices = gs.array([0, 0, 1])
        # mat = gs.array(
        #     [
        #         [0, 1],
        #         [2, 3],
        #     ]
        # )
        data = [
            dict(func_name=func_name, args=[vec, indices], expected=indices),
            # TODO: uncomment after test refactor merge
            # dict(func_name=func_name, args=[mat, indices],
            #      expected=gs.array([[0, 1]] * 2 + [[2, 3]]),
            #      axis=0),
            # dict(func_name=func_name, args=[mat, indices],
            #      expected=gs.transpose(gs.array([[0, 2]] * 2 + [[1, 3]])),
            #      axis=1),
            # dict(func_name=func_name, args=[mat, 0], expected=gs.array([0, 2]),
            #      axis=1)
        ]

        return data

    def func_out_allclose_test_data(self):
        smoke_data = [
            dict(
                func_name="linalg.logm",
                args=[gs.array([[2.0, 0.0, 0.0], [0.0, 3.0, 0.0], [0.0, 0.0, 4.0]])],
                expected=gs.array(
                    [
                        [0.693147180, 0.0, 0.0],
                        [0.0, 1.098612288, 0.0],
                        [0.0, 0.0, 1.38629436],
                    ]
                ),
            ),
            dict(
                func_name="linalg.logm",
                args=[gs.array([[1.0, 0.0, 0.0], [0.0, 5.0, 0.0], [0.0, 0.0, 6.0]])],
                expected=gs.array(
                    [[0.0, 0.0, 0.0], [0.0, 1.609437912, 0.0], [0.0, 0.0, 1.79175946]]
                ),
            ),
            dict(
                func_name="linalg.expm",
                args=[
                    gs.array(
                        [[2.0, 0.0, 0.0], [0.0, 3.0, 0.0], [0.0, 0.0, 4.0]],
                    )
                ],
                expected=gs.array(
                    [
                        [7.38905609, 0.0, 0.0],
                        [0.0, 20.0855369, 0.0],
                        [0.0, 0.0, 54.5981500],
                    ]
                ),
            ),
            # TODO: uncomment or delete?
            # dict(
            #     func_name="linalg.expm",
            #     args=[gs.array([[1.0, 0.0, 0.0], [0.0, 5.0, 0.0], [0.0, 0.0, 6.0]])],
            #     expected=gs.array(
            #         [
            #             [2.718281828, 0.0, 0.0],
            #             [0.0, 148.413159, 0.0],
            #             [0.0, 0.0, 403.42879349],
            #         ],
            #     ),
            # ),
        ]
        smoke_data += self._take_data()

        return self.generate_tests(smoke_data)

    def func_out_equal_test_data(self):
        smoke_data = [
            dict(func_name="shape", args=(1,), expected=()),
            dict(func_name="shape", args=([1, 2],), expected=(2,)),
            dict(func_name="shape", args=(gs.ones(3),), expected=(3,)),
            dict(func_name="shape", args=(gs.ones((3, 3)),), expected=(3, 3)),
            dict(func_name="take", args=[gs.array([0, 1]), 0], expected=0),
        ]

        return self.generate_tests(smoke_data)

    def compose_with_inverse_test_data(self):
        smoke_data = [
            dict(
                func_name_1="linalg.logm",
                func_name_2="linalg.expm",
                a=Matrices.to_diagonal(rand(3, 3)),
            ),
            dict(
                func_name_1="linalg.expm",
                func_name_2="linalg.logm",
                a=Matrices.to_diagonal(rand(3, 3)),
            ),
            dict(
                func_name_1="linalg.logm",
                func_name_2="linalg.expm",
                a=SpecialOrthogonal(n=3).random_point(2),
            ),
        ]
        return self.generate_tests(smoke_data)
