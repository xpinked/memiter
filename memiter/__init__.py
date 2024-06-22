"""
A generator that extends the functionality of a generator. simplifying pagination and data access.

License: MIT
Author: Udi Shalev <azsd91@gmail.com>
Version: 0.1.0
"""

from itertools import islice
from typing import Generic, Iterable, TypeVar

T = TypeVar("T")


class memiter(Generic[T]):  # noqa: N801
    """Extends the functionality of a generator.

    ## Features:
    --------
    - Pagination:
        - Limit the number of elements that are generated.
        - Set the current page.

    - Access the data that has been generated.

    - Keeps the original generator. allowing to generate the data again.

    ## Example:
    -------
    Creating a memiter instance from a range generator.
    - Limit the number of elements to 5.
    - Setting the current page to 2.

    >>> from memiter import memiter
    >>> my_gen = memiter(range(100)).limit(5).page(2)
    >>> list(my_gen)
    [5, 6, 7, 8, 9]

    Access the data that has been generated as many times as needed.
    >>> my_gen.data
    [5, 6, 7, 8, 9]

    Reset the generator to generate the data again in a different way.
    - Limit the number of elements to 10.
    - Setting the current page to 1.

    >>> _ = list(my_gen.limit(10).page(1))
    >>> my_gen.data
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    """

    def __init__(self, iterable: Iterable[T]) -> None:
        """Initialize the memiter instance.

        ### Args:
        ----
            iterable (Iterable[T]): The iterable object to create a memiter instance from.

        """
        assert isinstance(iterable, Iterable), "Input must be an iterable."

        self._page = 1
        self._limit: int | None = None

        self.data: list[T] = []
        self.original_iterable = iterable
        self.generator = iter(iterable)

        self._reset_generator()

    def _reset_generator(self) -> None:
        """Reset the generator according to the current limit and page."""
        start = (self._page - 1) * self._limit if self._limit is not None else 0
        stop = start + self._limit if self._limit is not None else None
        self.generator = islice(self.original_iterable, start, stop)
        self.data = []

    def __iter__(self) -> "memiter[T]":
        """Return the generator itself."""
        return self

    def __next__(self) -> T:
        """Return the next value from the generator."""
        value = next(self.generator)
        self.data.append(value)
        return value

    def limit(self, n: int) -> "memiter[T]":
        """Limit the number of elements that are generated.

        ### Note:
        ----
        Resets the generator data.

        For example:

        >>> from memiter import memiter
        >>> my_gen = memiter(range(100))
        >>> _ = list(my_gen.limit(5))
        >>> my_gen.data
        [0, 1, 2, 3, 4]
        >>> _ = list(my_gen.limit(3))
        >>> my_gen.data
        [0, 1, 2]

        ### Args:
        ----
            n (int): The number of elements to generate.

        ### Returns
        -------
            memiter[T]: The current memiter instance.

        """
        assert isinstance(n, int), "Page number must be an integer."
        assert n > 0, "Page number must be greater than 0."

        self._limit = n
        self._reset_generator()
        return self

    def page(self, n: int) -> "memiter[T]":
        """Set the current page.

        ### Note:
        ----
        Resets the generator data.

        For example:

        >>> from memiter import memiter
        >>> my_gen = memiter(range(10))
        >>> _ = list(my_gen.limit(2).page(1))
        >>> my_gen.data
        [0, 1]
        >>> _ = list(my_gen.limit(2).page(2))
        >>> my_gen.data
        [2, 3]

        ### Args:
        ----
            n (int): The page number to set.

        ### Returns:
        -------
            memiter[T]: The current memiter instance.

        """
        assert isinstance(n, int), "Page number must be an integer."
        assert n > 0, "Page number must be greater than 0."

        self._page = n
        self._reset_generator()
        return self
