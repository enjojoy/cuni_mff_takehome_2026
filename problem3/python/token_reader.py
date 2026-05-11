from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Protocol


class TokenType(Enum):
    END_OF_INPUT = auto()
    WORD = auto()
    END_OF_LINE = auto()
    END_OF_PARAGRAPH = auto()


@dataclass(frozen=True)
class Token:
    type: TokenType
    value: Optional[str] = None

    @classmethod
    def word(cls, value: str) -> "Token":
        return cls(TokenType.WORD, value)


class TokenReader(Protocol):
    def read_token(self) -> Token:
        ...


class ParagraphDetectingTokenReaderDecorator:
    def __init__(self, reader: TokenReader):
        self.reader = reader
        self._next_token: Optional[Token] = None

    def read_token(self) -> Token:
        if self._next_token is not None:
            token = self._next_token
            self._next_token = None
            return token

        new_lines_found = 0
        token = self.reader.read_token()

        while token.type == TokenType.END_OF_LINE:
            new_lines_found += 1
            token = self.reader.read_token()

        if new_lines_found > 1:
            self._next_token = token
            return Token(TokenType.END_OF_PARAGRAPH)

        return token
