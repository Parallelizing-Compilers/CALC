import pytest
from calc.calc_lang import Add, CalcLangInterpreter, Literal, Sub, Mul, Pow, Variable

class TestCalcLangNormalization:
    """Test normalization of calc_lang expressions."""

    @pytest.mark.parametrize(
        "program",
        [
            Add(Literal(2), Literal(3)),
            Mul(Literal(4), Literal(7)),
            Pow(Literal(2), Literal(3)),
            Add(Mul(Variable("x"), Literal(2)), Literal(3)),
            Mul(Add(Variable("x"), Literal(2)), Literal(3)),
            Mul(Sub(Variable("x"), Literal(2)), Literal(3)),
            Pow(Variable("x"), Literal(3)),
            Pow(Add(Variable("x"), Literal(2)), Literal(3)),
            Pow(Mul(Add(Variable("x"), Literal(2)), Add(Variable("x"), Literal(3))), Literal(2)),
            Sub(Mul(Add(Literal(2), Variable("x")), Add(Literal(8), Pow(Variable("x"), Literal(2)))), Sub(Literal(3), Pow(Mul(Variable("x"), Literal(4)), Literal(2)))),
        ]
    )
    def test_normalization(self, program):
        from calc.normalize import normalize, is_normalized
        program2 = normalize(program)
        for x in range(-10, 10):
            bindings = {"x": x}
            interp = CalcLangInterpreter()
            result1 = interp(program, bindings=bindings)
            result2 = interp(program2, bindings=bindings)
            assert result1 == result2, f"normalization changed the value of the program for x={x}: {program} -> {program2}, expected {result1}, got {result2}"
        assert is_normalized(program2), f"non-normal {program2}, expected ... ((a * x^2) + ((b * x) + c))"