import pytest

from src.utils.config.zyxel import range_formatter


# Тесты
def test_empty_list():
    assert range_formatter([]) == '""'


def test_single_element():
    assert range_formatter([5]) == "5"


def test_consecutive_numbers():
    assert range_formatter([1, 2, 3]) == "1-3"
    assert range_formatter([-2, -1, 0]) == "-2-0"


def test_non_consecutive_numbers():
    assert range_formatter([1, 3, 5]) == "1,3,5"
    assert range_formatter([10, 11, 13, 14]) == "10-11,13-14"


def test_mixed_ranges():
    assert range_formatter([1, 2, 4, 5, 7]) == "1-2,4-5,7"
    assert range_formatter([1, 2, 3, 5, 6, 8]) == "1-3,5-6,8"


def test_unsorted_list():
    # Если функция не обрабатывает сортировку, тест должен выявить ошибку
    with pytest.raises(AssertionError):
        assert range_formatter([3, 2, 1]) == "1-3"


if __name__ == "__main__":
    pytest.main()
