from __future__ import annotations
import ast
import sys
from ast import Attribute, Name, Subscript
from pathlib import Path
from typing import Any
from typing_extensions import TypeAlias
AliasInfo: TypeAlias = dict[str, str]
AliasCategoryDict: TypeAlias = dict[str, AliasInfo]
ModuleLevelAliasDict: TypeAlias = dict[str, AliasCategoryDict]
ModuleTypeVarDict: TypeAlias = dict[str, str]
AliasDocsDict: TypeAlias = dict[str, ModuleLevelAliasDict]
DataDict: TypeAlias = dict[str, list[str]]
TypeVarDict: TypeAlias = dict[str, ModuleTypeVarDict]
ALIAS_DOCS_DICT: AliasDocsDict = {}
DATA_DICT: DataDict = {}
TYPEVAR_DICT: TypeVarDict = {}
MANIM_ROOT = Path(__file__).resolve().parent.parent.parent

def parse_module_attributes() -> tuple[AliasDocsDict, DataDict, TypeVarDict]:
    global ALIAS_DOCS_DICT
    global DATA_DICT
    global TYPEVAR_DICT
    if ALIAS_DOCS_DICT or DATA_DICT or TYPEVAR_DICT:
        return (ALIAS_DOCS_DICT, DATA_DICT, TYPEVAR_DICT)
    for module_path in MANIM_ROOT.rglob('*.py'):
        module_name_t1 = module_path.resolve().relative_to(MANIM_ROOT)
        module_name_t2 = list(module_name_t1.parts)
        module_name_t2[-1] = module_name_t2[-1].removesuffix('.py')
        module_name = '.'.join(module_name_t2)
        module_content = module_path.read_text(encoding='utf-8')
        module_dict: ModuleLevelAliasDict = {}
        category_dict: AliasCategoryDict | None = None
        alias_info: AliasInfo | None = None
        module_typevars: ModuleTypeVarDict = {}
        data_list: list[str] = []
        data_name: str | None = None
        for node in ast.iter_child_nodes(ast.parse(module_content)):
            if type(node) is ast.Expr and type(node.value) is ast.Constant and (type(node.value.value) is str):
                string = node.value.value.strip()
                section_str = '[CATEGORY]'
                if string.startswith(section_str):
                    category_name = string[len(section_str):].strip()
                    module_dict[category_name] = {}
                    category_dict = module_dict[category_name]
                    alias_info = None
                elif alias_info:
                    alias_info['doc'] = string
                elif data_name:
                    data_list.append(data_name)
                continue
            if type(node) is ast.If and (type(node.test) is ast.Name and node.test.id == 'TYPE_CHECKING' or (type(node.test) is ast.Attribute and type(node.test.value) is ast.Name and (node.test.value.id == 'typing') and (node.test.attr == 'TYPE_CHECKING'))):
                inner_nodes: list[Any] = node.body
            else:
                inner_nodes = [node]
            for node in inner_nodes:
                is_type_alias = sys.version_info >= (3, 12) and type(node) is ast.TypeAlias
                is_annotated_assignment_with_value = type(node) is ast.AnnAssign and type(node.annotation) is ast.Name and (node.annotation.id == 'TypeAlias') and (type(node.target) is ast.Name) and (node.value is not None)
                if is_type_alias or is_annotated_assignment_with_value:
                    alias_name = node.name.id if is_type_alias else node.target.id
                    definition_node = node.value
                    if type(definition_node) is ast.Subscript and type(definition_node.value) is ast.Name and (definition_node.value.id == 'Union'):
                        union_elements = definition_node.slice.elts
                        definition = ' | '.join((ast.unparse(elem) for elem in union_elements))
                    else:
                        definition = ast.unparse(definition_node)
                    definition = definition.replace('npt.', '')
                    if category_dict is None:
                        module_dict[''] = {}
                        category_dict = module_dict['']
                    category_dict[alias_name] = {'definition': definition}
                    alias_info = category_dict[alias_name]
                    continue
                elif type(node) is ast.Assign and type(node.targets[0]) is ast.Name and (type(node.value) is ast.Call) and (type(node.value.func) is ast.Name) and node.value.func.id.endswith('TypeVar'):
                    module_typevars[node.targets[0].id] = ast.unparse(node.value).replace('_', '\\_')
                    continue
                alias_info = None
                if type(node) is ast.AnnAssign:
                    target: Name | Attribute | Subscript | ast.expr | None = node.target
                elif type(node) is ast.Assign and len(node.targets) == 1:
                    target = node.targets[0]
                else:
                    target = None
                if type(target) is ast.Name and (not (type(node) is ast.Assign and target.id not in module_typevars)):
                    data_name = target.id
                else:
                    data_name = None
        if len(module_dict) > 0:
            ALIAS_DOCS_DICT[module_name] = module_dict
        if len(data_list) > 0:
            DATA_DICT[module_name] = data_list
        if module_typevars:
            TYPEVAR_DICT[module_name] = module_typevars
    return (ALIAS_DOCS_DICT, DATA_DICT, TYPEVAR_DICT)