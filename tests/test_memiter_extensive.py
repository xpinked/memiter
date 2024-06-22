from memiter import memiter


def test_memiter_empty() -> None:
    # Test when the input iterable is empty
    iterable: list = []
    result = list(memiter(iterable))
    assert not result


def test_memiter_single_element() -> None:
    # Test when the input iterable has a single element
    iterable = [1]
    result = list(memiter(iterable))
    assert result == [1]


def test_memiter_multiple_elements() -> None:
    # Test when the input iterable has multiple elements
    iterable = [1, 2, 3, 4, 5]
    result = list(memiter(iterable))
    assert result == [1, 2, 3, 4, 5]


def test_memiter_nested_iterables():
    # Test when the input iterable contains nested iterables
    iterable = [[1, 2], [3, 4], [5, 6]]
    result = list(memiter(iterable))
    assert result == [[1, 2], [3, 4], [5, 6]]


def test_memiter_string() -> None:
    # Test when the input iterable is a string
    iterable = "hello"
    result = list(memiter(iterable))
    assert result == ["h", "e", "l", "l", "o"]


def test_memiter_generator() -> None:
    # Test when the input iterable is a generator
    iterable = iter(range(5))
    result = list(memiter(iterable))
    assert result == [0, 1, 2, 3, 4]


def test_memiter_custom_object() -> None:
    # Test when the input iterable contains custom objects
    class Person:
        def __init__(self, name: str) -> None:
            self.name = name

    iterable = [Person("Alice"), Person("Bob"), Person("Charlie")]
    result = list(memiter(iterable))
    assert result == iterable.copy()
