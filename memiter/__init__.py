"""
A generator that extends the functionality of a generator. simplifying pagination and data access.

License: MIT
Author: Udi Shalev <azsd91@gmail.com>
Version: 0.1.0
"""

from copy import deepcopy
from itertools import islice
from typing import Callable, Generic, Iterable, TypeVar

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
        self._first_iteration = True
        self._generator_copy = iter(iterable)

        self.data: list[T] = []
        self.original_iterable = iterable
        self.generator = self._generator_copy

    def __iter__(self) -> "memiter[T]":
        """Return the generator itself."""
        return self

    def __next__(self) -> T:
        """Return the next value from the generator."""
        if self._first_iteration:
            self._generator_copy = deepcopy(self.generator)
            self._add_pagination(self.generator)
            self._first_iteration = False

        try:
            value = next(self.generator)
            self.data.append(value)
        except StopIteration:
            self.generator = self._generator_copy
            self._first_iteration = True
            raise

        return value

    def _add_pagination(self, iterable: Iterable[T]) -> None:
        """Reset the generator according to the current limit and page."""
        start = (self._page - 1) * self._limit if self._limit is not None else 0
        stop = start + self._limit if self._limit is not None else None
        self.generator = islice(iterable, start, stop)

    def _reset_from_copy(self) -> None:
        """Reset the generator from the copy."""
        self.generator = self._generator_copy
        self._first_iteration = True

    ## Altering Methods
    def reset(self) -> "memiter[T]":
        """Reset the generator to the original iterable."""
        self._page = 1
        self._limit = None
        self._first_iteration = True
        self.generator = iter(self.original_iterable)
        self._add_pagination(self.original_iterable)
        self.data.clear()
        return self

    def limit(self, n: int) -> "memiter[T]":
        """Limit the number of elements that are generated.

        ### Note:
        ----

        - Resets the previous generator data. meaning it is recommended to use this method once for each memiter instance.
        - - - if you want to limit and swap page in the generator again, wrap it to a new memiter instance.
        - `self`.data will hold the last data that was generated.

        ### Example:
        ----

        Usage of the limit method.

        >>> from memiter import memiter
        >>> my_gen = memiter(range(100))
        >>> _ = list(my_gen.limit(5))
        >>> my_gen.data
        [0, 1, 2, 3, 4]

        >>> _ = list(my_gen.limit(3))
        >>> my_gen.data
        [0, 1, 2]

        - if you want to limit and swap page in the generator again, wrap it to a new memiter instance.
        >>> my_gen2 = memiter(my_gen).limit(2)
        [0, 1]

        ### Args:
        ----
            n (int): The number of elements to generate.

        ### Returns
        -------
            memiter[T]: The current memiter instance.

        """
        assert isinstance(n, int), "number must be an integer."
        assert n > 0, "number must be greater than 0."

        self._limit = n
        self.data.clear()
        return self

    def page(self, n: int) -> "memiter[T]":
        """Set the current page. (1-indexed), default page is 1.

        ### Note:
        ----
        - Has no meaning without the limit method.
        - Resets the previous generator data. meaning it is recommended to use this method once for each memiter instance.
        - - if you want to limit and swap page in the generator again, wrap the memiter instance with another memiter instance.
        - `self`.data will hold the last data that was generated.

        ### Example:

        >>> from memiter import memiter
        >>> my_gen = memiter(range(10))
        >>> _ = list(my_gen.limit(2).page(1))
        >>> my_gen.data
        [0, 1]
        >>> _ = list(my_gen.limit(2).page(2))
        >>> my_gen.data
        [2, 3]

        - if you want to limit and swap page in the generator again, wrap it to a new memiter instance.

        >>> my_gen2 = memiter(my_gen).limit(1).page(2)
        >>> list(my_gen2)
        [3]

        ### Args:
        ----
            n (int): The page number to set.

        ### Returns:
        -------
            memiter[T]: The current memiter instance.

        """
        assert isinstance(n, int), "number must be an integer."
        assert n > 0, "number must be greater than 0."

        self._page = n
        self.data.clear()
        return self

    def filter(self, func: Callable[[T], bool] = lambda x: True) -> "memiter[T]":  # noqa: ARG005
        """Filter the elements that are generated.

        ### Note:
        ----
        - Resets the previous generator data.
        - `self`.data will hold the last data that was generated.

        ### Example:
        ----

        - Filter the even numbers from the generator.

        >>> from memiter import memiter
        >>> my_gen = memiter(range(10))
        >>> _ = list(my_gen.filter(lambda x: x % 2 == 0))
        >>> my_gen.data
        [0, 2, 4, 6, 8]

        ### Args:
        ----
            func (Callable[[T], bool]): The function to filter the elements.

        ### Returns:
        -------
            memiter[T]: The current memiter instance.

        """
        assert callable(func), "func must be a callable."

        self.generator = filter(func, self.generator)
        return self

    def map(self, func: Callable[[T], T] = lambda x: x) -> "memiter[T]":
        """Map the elements that are generated.

        ### Example:
        ----

        - Multiply each element by 2.

        >>> from memiter import memiter
        >>> my_gen = memiter(range(10))
        >>> _ = list(my_gen.map(lambda x: x * 2))
        >>> my_gen.data
        [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

        ### Args:
        ----
            func (Callable[[T], T]): The function to map the elements.

        ### Returns:
        -------
            memiter[T]: The current memiter instance.

        """
        assert callable(func), "func must be a callable."

        self.generator = map(func, self.generator)
        return self

    def order_by(self, func: Callable[[T], T] = lambda x: x) -> "memiter[T]":
        """Order the elements that are generated.


        ### Note:
        ----

        - Resets the previous generator data.
        - `self`.data will hold the last data that was generated.
        - Consumes to the end of the generator.

        ### Example:
        ----

        - Order the elements in descending order.

        >>> from memiter import memiter
        >>> my_gen = memiter(range(10))
        >>> _ = list(my_gen.order_by(lambda x: -x))
        >>> my_gen.data
        [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

        ### Args:
        ----
            func (Callable[[T], T]): The function to order the elements.

        ### Returns:
        -------
            memiter[T]: The current memiter instance.

        """
        assert callable(func), "func must be a callable."

        self.data.clear()

        for _ in self:
            continue

        self.generator = iter(sorted(self.data, key=func))  # type: ignore [arg-type]

        return self

    ## Access Methods
    def first(self) -> T | None:
        """Return the first element of the generator.

        ### Note:
        ----

        - Resets the generator data.
        - `self`.data will hold the first element only.

        ### Example:
        ----

        - Get the first element of the generator.

        >>> from memiter import memiter
        >>> my_gen = memiter(range(10))
        >>> _ = list(my_gen.limit(5))
        >>> my_gen.first()
        0
        >>> my_gen.data
        [0]

        ### Returns:
        -------
            T | None: The first element of the generator. If the generator is empty, returns None.

        """
        self.data.clear()

        try:
            first_item = next(self)
        except StopIteration:
            first_item = None

        self._reset_from_copy()
        return first_item

    def last(self) -> T | None:
        """Return the last element of the generator.

        ### Note:
        ----

        - Resets the generator data.
        - `self`.data will hold the last elements that were generated.


        ### Example:
        ----

        - Get the last element of the generator.

        >>> from memiter import memiter
        >>> my_gen = memiter(range(10))
        >>> _ = list(my_gen.limit(5))
        >>> my_gen.last()
        4
        >>> my_gen.data
        [0, 1, 2, 3, 4]

        ### Returns:
        -------
            T | None: The last element of the generator. If the generator is empty, returns None.

        """
        self.data.clear()

        last_item = None
        for item in self:
            last_item = item

        return last_item
