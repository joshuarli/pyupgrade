import ast
from typing import Iterable
from typing import List
from typing import Tuple

from tokenize_rt import Offset
from tokenize_rt import Token

from pyupgrade._ast_helpers import ast_to_offset
from pyupgrade._ast_helpers import is_name_attr
from pyupgrade._data import register
from pyupgrade._data import State
from pyupgrade._data import TokenFunc
from pyupgrade._token_helpers import find_open_paren
from pyupgrade._token_helpers import find_token


def _remove_call(i: int, tokens: List[Token]) -> None:
    i = find_open_paren(tokens, i)
    j = find_token(tokens, i, ')')
    del tokens[i:j + 1]


@register(ast.Call)
def visit_Call(
        state: State,
        node: ast.Call,
) -> Iterable[Tuple[Offset, TokenFunc]]:
    if (
            state.min_version >= (3, 8) and
            not node.args and
            not node.keywords and
            is_name_attr(
                node.func,
                state.from_imports,
                'functools',
                ('lru_cache',),
            )
    ):
        yield ast_to_offset(node), _remove_call
