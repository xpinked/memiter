from memiter import memiter


def test_limit():
    gen = memiter(range(10))
    gen.limit(5)
    assert len(list(gen)) == 5


def test_page():
    gen = memiter(range(10))
    gen.limit(3).page(2)
    assert list(gen) == [3, 4, 5]


def test_filter():
    gen = memiter(range(10))
    gen.filter(lambda x: x % 2 == 0)
    assert list(gen) == [0, 2, 4, 6, 8]


def test_map():
    gen = memiter(range(5))
    gen.map(lambda x: x * 2)
    assert list(gen) == [0, 2, 4, 6, 8]


def test_order_by() -> None:
    gen = memiter([3, 1, 4, 1, 5])
    gen.order_by(lambda x: -x)
    assert list(gen) == [5, 4, 3, 1, 1]


def test_first():
    gen = memiter(range(10))
    gen.limit(5)
    assert gen.first() == 0


def test_last():
    gen = memiter(range(10))
    gen.limit(5)
    assert gen.last() == 4


def test_long_query_simulation():
    # Simulate a long query by chaining operations
    gen = memiter([4, 1, 6, 8, 3, 6, 7, 5])
    result = gen.filter(lambda x: x % 2 == 0).map(lambda x: x * 2).limit(2).order_by(lambda x: -x)
    assert list(result) == [12, 8]


def test_wrapping_instances():
    # Test wrapping a memiter instance with another memiter instance
    gen = memiter(range(10))
    paged = gen.limit(2).page(5)
    wrapped_gen = memiter(paged).limit(1).page(2)
    assert list(wrapped_gen) == [9], "Expected [9], but got {wrapped_gen}"
