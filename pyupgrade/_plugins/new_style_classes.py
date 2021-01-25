import ast
from typing import Iterable
from typing import Tuple

from tokenize_rt import Offset

from pyupgrade._ast_helpers import ast_to_offset
from pyupgrade._data import register
from pyupgrade._data import State
from pyupgrade._data import TokenFunc
from pyupgrade._token_helpers import remove_base_class


@register(ast.ClassDef)
def visit_ClassDef(
        state: State,
        node: ast.ClassDef,
) -> Iterable[Tuple[Offset, TokenFunc]]:
    if state.min_version >= (3,):
        for base in node.bases:
            if isinstance(base, ast.Name) and base.id == 'object':
                yield ast_to_offset(base), remove_base_class