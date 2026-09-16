"""通用示例工具：计算器（阶段 ① 的最小工具）。

展示确定性优先原则（已锁决策 ②）：LLM 只产出工具调用，
数值计算由代码完成。表达式求值用 ast 白名单，只允许数字与四则运算。
"""

import ast
import operator
from typing import Any

_BIN_OPS: dict[type[ast.operator], Any] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}
_UNARY_OPS: dict[type[ast.unaryop], Any] = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _safe_eval(node: ast.AST) -> float:
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _BIN_OPS:
        return _BIN_OPS[type(node.op)](_safe_eval(node.left), _safe_eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPS:
        return _UNARY_OPS[type(node.op)](_safe_eval(node.operand))
    raise ValueError(f"unsupported expression node: {type(node).__name__}")


def calculator(expression: str) -> str:
    """求值四则运算表达式，返回字符串结果。"""
    try:
        result = _safe_eval(ast.parse(expression, mode="eval"))
    except (SyntaxError, ValueError, ZeroDivisionError) as exc:
        return f"error: {exc}"
    if isinstance(result, float) and result.is_integer():
        return str(int(result))
    return str(result)


TOOLS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "计算四则运算表达式，如 (3+5)*2。",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "四则运算表达式"}
                },
                "required": ["expression"],
            },
        },
    }
]

_TOOL_FUNCTIONS: dict[str, Any] = {"calculator": calculator}


def execute_tool(name: str, arguments: dict[str, Any]) -> str:
    """按名字执行工具并返回字符串结果。"""
    fn = _TOOL_FUNCTIONS.get(name)
    if fn is None:
        return f"error: unknown tool {name}"
    return fn(**arguments)
