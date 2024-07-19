from memiter import memiter


def test_limit() -> None:
    gen = memiter(range(10))
    gen.limit(5)
    assert len(list(gen)) == 5, f"Expected 5 items, but got {len(list(gen))}"


def test_page() -> None:
    gen = memiter(range(10))
    gen.limit(3).page(2)
    assert list(gen) == [3, 4, 5], f"Expected [3, 4, 5], but got {list(gen)}"


def test_filter() -> None:
    gen = memiter(range(10))
    gen.filter(lambda x: x % 2 == 0)
    assert list(gen) == [0, 2, 4, 6, 8], f"Expected [0, 2, 4, 6, 8], but got {list(gen)}"


def test_map() -> None:
    gen = memiter(range(5))
    gen.map(lambda x: x * 2)
    assert list(gen) == [0, 2, 4, 6, 8], f"Expected [0, 2, 4, 6, 8], but got {list(gen)}"


def test_order_by() -> None:
    gen = memiter([3, 1, 4, 1, 5])
    gen.order_by(lambda x: -x)
    assert list(gen) == [5, 4, 3, 1, 1], f"Expected [5, 4, 3, 1, 1], but got {list(gen)}"


def test_first() -> None:
    gen = memiter(range(10))
    gen.limit(5)
    assert gen.first() == 0, f"Expected 0, but got {gen.first()}"


def test_last():
    gen = memiter(range(10))
    gen.limit(5)
    assert gen.last() == 4, f"Expected 4, but got {gen.last()}"


def test_long_query_simulation__order_by_last() -> None:
    # Simulate a long query by chaining operations
    # [4, 1, 6, 8, 3, 6, 7, 5] - > [4, 6, 8, 6] -> [12, 8] -> [8, 12] -> [12, 8]

    gen = memiter([4, 1, 6, 8, 3, 6, 7, 5])
    result = gen.filter(lambda x: x % 2 == 0).map(lambda x: x * 2).limit(2).order_by(lambda x: -x)
    assert list(result) == [12, 8], f"Expected [12, 8], but got {list(result)}"


def test_long_query_simulation__order_by_first() -> None:
    # Simulate a long query by chaining operations
    # [4, 1, 6, 8, 3, 6, 7, 5] -> [8, 7, 6, 6, 5, 4, 3, 1] -> [8, 6, 6, 4] -> [16, 12, 12, 8] -> [16, 12]

    gen = memiter([4, 1, 6, 8, 3, 6, 7, 5])
    result = gen.order_by(lambda x: -x).filter(lambda x: x % 2 == 0).map(lambda x: x * 2).limit(2)
    assert list(result) == [16, 12]


def test_wrapping_instances():
    # Test wrapping a memiter instance with another memiter instance
    gen = memiter(range(10))
    paged = gen.limit(2).page(5)
    wrapped_gen = memiter(paged).limit(1).page(2)
    assert list(wrapped_gen) == [9], "Expected [9], but got {wrapped_gen}"
