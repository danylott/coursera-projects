class TestFactorize(unittest.TestCase):
    def test_wrong_types_raise_exception(self):
        self.cases = ('string', 1.5)

        for data in self.cases:
            with self.subTest(x=data):
                self.assertRaises(TypeError, factorize, data)

    def test_negative(self):
        self.cases = (-1, -10, -100)

        for data in self.cases:
            with self.subTest(x=data):
                self.assertRaises(ValueError, factorize, data)

    def test_zero_and_one_cases(self):
        self.cases = (
            (0, (0,)),
            (1, (1,)),
        )

        for data, result in self.cases:
            with self.subTest(x=data):
                self.assertEqual(factorize(data), result)

    def test_simple_numbers(self):
        self.cases = (
            (3, (3,)),
            (13, (13,)),
            (29, (29,))
        )

        for data, result in self.cases:
            with self.subTest(x=data):
                self.assertEqual(factorize(data), result)

    def test_two_simple_multipliers(self):
        self.cases = (
            (6, (2, 3)),
            (26, (2, 13)),
            (121, (11, 11))
        )

        for data, result in self.cases:
            with self.subTest(x=data):
                self.assertEqual(factorize(data), result)

    def test_many_multipliers(self):
        self.cases = (
            (1001, (7, 11, 13)),
            (9699690, (2, 3, 5, 7, 11, 13, 17, 19))
        )

        for data, result in self.cases:
            with self.subTest(x=data):
                self.assertEqual(factorize(data), result)
