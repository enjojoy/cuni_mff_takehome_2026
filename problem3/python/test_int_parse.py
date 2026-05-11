import pytest


def test_int_parses_string_variable():
    value = "123"

    assert int(value) == 123


def test_int_parses_zero_string():
    assert int("0") == 0


def test_int_parses_string_with_leading_zeros():
    assert int("00123") == 123


def test_int_parses_string_with_plus_sign():
    value = "+123"

    assert int(value) == 123


def test_int_parses_string_with_minus_sign():
    value = "-123"

    assert int(value) == -123


def test_int_rejects_float_string():
    with pytest.raises(ValueError):
        int("12.5")


def test_int_rejects_text_string():
    with pytest.raises(ValueError):
        int("hello")


def test_int_rejects_empty_string():
    with pytest.raises(ValueError):
        int("")


def test_int_rejects_whitespace_only_string():
    with pytest.raises(ValueError):
        int("   ")


def test_int_parses_string_with_spaces():
    assert int("   123   ") == 123


def test_int_rejects_string_with_internal_spaces():
    with pytest.raises(ValueError):
        int("12 3")


def test_int_parses_string_with_tabs_and_newlines_around_digits():
    assert int("\t\n123\n") == 123


def test_int_rejects_plus_sign_without_digits():
    with pytest.raises(ValueError):
        int("+")


def test_int_rejects_minus_sign_without_digits():
    with pytest.raises(ValueError):
        int("-")


def test_int_rejects_sign_separated_from_digits():
    with pytest.raises(ValueError):
        int("+ 123")


def test_int_parses_string_with_underscores_between_digits():
    assert int("1_000") == 1000


def test_int_rejects_string_starting_with_underscore():
    with pytest.raises(ValueError):
        int("_1000")


def test_int_rejects_string_ending_with_underscore():
    with pytest.raises(ValueError):
        int("1000_")


def test_int_rejects_string_with_repeated_underscores():
    with pytest.raises(ValueError):
        int("1__000")


def test_int_rejects_different_base_string_by_default():
    with pytest.raises(ValueError):
        int("0x10")


def test_int_parses_very_large_integer_string():
    assert int("999999999999999999999999999999") == 999999999999999999999999999999
