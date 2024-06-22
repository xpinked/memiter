from dataclasses import dataclass

import pytest

from memiter import memiter


@dataclass
class TestDeck:
    """Dataclass to hold the deck of cards."""

    suits: list[str]
    ranks: list[str]
    deck: list[str]


@pytest.fixture()
def deck() -> TestDeck:
    """Set up a standard deck of cards for testing."""
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    deck = [f"{rank} of {suit}" for suit in suits for rank in ranks]
    return TestDeck(suits=suits, ranks=ranks, deck=deck)


def test_limit_functionality(deck: TestDeck) -> None:
    """Test the limit functionality of memiter."""
    deck_gen = memiter(deck.deck).limit(5)
    output = list(deck_gen)
    expected_output = ["2 of Hearts", "3 of Hearts", "4 of Hearts", "5 of Hearts", "6 of Hearts"]
    assert output == expected_output, f"Expected {expected_output}, but got {output}"
    assert deck_gen.data == expected_output, f"Expected {expected_output}, but got {deck_gen.data}"


def test_page_functionality(deck: TestDeck) -> None:
    """Test the page functionality of memiter."""
    deck_gen = memiter(deck.deck).limit(5).page(2)
    output = list(deck_gen)
    expected_output = ["7 of Hearts", "8 of Hearts", "9 of Hearts", "10 of Hearts", "J of Hearts"]
    assert output == expected_output, f"Expected {expected_output}, but got {output}"
    assert deck_gen.data == expected_output, f"Expected {expected_output}, but got {deck_gen.data}"


def test_reset_generator(deck: TestDeck) -> None:
    """Test resetting the generator with different limits and pages."""
    deck_gen = memiter(deck.deck).limit(10).page(1)
    output = list(deck_gen)
    expected_output = [
        "2 of Hearts",
        "3 of Hearts",
        "4 of Hearts",
        "5 of Hearts",
        "6 of Hearts",
        "7 of Hearts",
        "8 of Hearts",
        "9 of Hearts",
        "10 of Hearts",
        "J of Hearts",
    ]
    assert output == expected_output, f"Expected {expected_output}, but got {output}"
    assert deck_gen.data == expected_output, f"Expected {expected_output}, but got {deck_gen.data}"

    deck_gen.limit(5).page(2)
    output = list(deck_gen)
    expected_output = ["7 of Hearts", "8 of Hearts", "9 of Hearts", "10 of Hearts", "J of Hearts"]
    assert output == expected_output, f"Expected {expected_output}, but got {output}"
    assert deck_gen.data == expected_output, f"Expected {expected_output}, but got {deck_gen.data}"


def test_large_pagination(deck: TestDeck) -> None:
    """Test pagination with a larger page number."""
    deck_gen = memiter(deck.deck).limit(5).page(10)
    output = list(deck_gen)
    expected_output = ["8 of Spades", "9 of Spades", "10 of Spades", "J of Spades", "Q of Spades"]
    assert output == expected_output, f"Expected {expected_output}, but got {output}"
    assert deck_gen.data == expected_output, f"Expected {expected_output}, but got {deck_gen.data}"


def test_generator_exhaustion(deck: TestDeck) -> None:
    """Test exhaustion of the generator."""
    deck_gen = memiter(deck.deck).limit(53).page(1)
    output = list(deck_gen)
    expected_output = deck.deck
    assert output == expected_output, f"Expected {expected_output}, but got {output}"
    assert deck_gen.data == expected_output, f"Expected {expected_output}, but got {deck_gen.data}"


def test_invalid_limit(deck: TestDeck) -> None:
    """Test setting an invalid limit."""
    with pytest.raises(AssertionError):
        memiter(deck.deck).limit(0)


def test_invalid_page(deck: TestDeck) -> None:
    """Test setting an invalid page."""
    with pytest.raises(AssertionError):
        memiter(deck.deck).page(0)
