from token_reader import ParagraphDetectingTokenReaderDecorator, Token, TokenType


class FakeTokenReader:
    def __init__(self, tokens):
        self._tokens = list(tokens)
        self._index = 0

    def read_token(self):
        if self._index >= len(self._tokens):
            return Token(TokenType.END_OF_INPUT)

        token = self._tokens[self._index]
        self._index += 1
        return token


def test_word_helper_creates_word_token():
    assert Token.word("hello") == Token(TokenType.WORD, "hello")


def test_end_of_line_token_has_no_value_by_default():
    assert Token(TokenType.END_OF_LINE).value is None


def test_reader_returns_word_without_changes():
    reader = ParagraphDetectingTokenReaderDecorator(
        FakeTokenReader([Token.word("hello")])
    )

    assert reader.read_token() == Token.word("hello")


def test_empty_reader_returns_end_of_input():
    reader = ParagraphDetectingTokenReaderDecorator(FakeTokenReader([]))

    assert reader.read_token() == Token(TokenType.END_OF_INPUT)


def test_single_end_of_line_is_skipped():
    reader = ParagraphDetectingTokenReaderDecorator(
        FakeTokenReader([
            Token(TokenType.END_OF_LINE),
            Token.word("next"),
        ])
    )

    assert reader.read_token() == Token.word("next")


def test_single_end_of_line_before_end_of_input_is_not_paragraph():
    reader = ParagraphDetectingTokenReaderDecorator(
        FakeTokenReader([
            Token(TokenType.END_OF_LINE),
            Token(TokenType.END_OF_INPUT),
        ])
    )

    assert reader.read_token() == Token(TokenType.END_OF_INPUT)


def test_two_end_of_lines_create_paragraph_token():
    reader = ParagraphDetectingTokenReaderDecorator(
        FakeTokenReader([
            Token(TokenType.END_OF_LINE),
            Token(TokenType.END_OF_LINE),
            Token.word("next"),
        ])
    )

    assert reader.read_token() == Token(TokenType.END_OF_PARAGRAPH)


def test_token_after_paragraph_is_returned_on_next_call():
    reader = ParagraphDetectingTokenReaderDecorator(
        FakeTokenReader([
            Token(TokenType.END_OF_LINE),
            Token(TokenType.END_OF_LINE),
            Token.word("next"),
        ])
    )

    assert reader.read_token() == Token(TokenType.END_OF_PARAGRAPH)
    assert reader.read_token() == Token.word("next")


def test_more_than_two_end_of_lines_create_one_paragraph_token():
    reader = ParagraphDetectingTokenReaderDecorator(
        FakeTokenReader([
            Token(TokenType.END_OF_LINE),
            Token(TokenType.END_OF_LINE),
            Token(TokenType.END_OF_LINE),
            Token.word("next"),
        ])
    )

    assert reader.read_token() == Token(TokenType.END_OF_PARAGRAPH)
    assert reader.read_token() == Token.word("next")


def test_paragraph_before_end_of_input_buffers_end_of_input():
    reader = ParagraphDetectingTokenReaderDecorator(
        FakeTokenReader([
            Token(TokenType.END_OF_LINE),
            Token(TokenType.END_OF_LINE),
            Token(TokenType.END_OF_INPUT),
        ])
    )

    assert reader.read_token() == Token(TokenType.END_OF_PARAGRAPH)
    assert reader.read_token() == Token(TokenType.END_OF_INPUT)


def test_words_around_paragraph_are_not_lost():
    reader = ParagraphDetectingTokenReaderDecorator(
        FakeTokenReader([
            Token.word("first"),
            Token(TokenType.END_OF_LINE),
            Token(TokenType.END_OF_LINE),
            Token.word("second"),
            Token(TokenType.END_OF_INPUT),
        ])
    )

    assert reader.read_token() == Token.word("first")
    assert reader.read_token() == Token(TokenType.END_OF_PARAGRAPH)
    assert reader.read_token() == Token.word("second")
    assert reader.read_token() == Token(TokenType.END_OF_INPUT)


def test_end_of_input_can_be_read_repeatedly():
    reader = ParagraphDetectingTokenReaderDecorator(
        FakeTokenReader([Token(TokenType.END_OF_INPUT)])
    )

    assert reader.read_token() == Token(TokenType.END_OF_INPUT)
    assert reader.read_token() == Token(TokenType.END_OF_INPUT)
