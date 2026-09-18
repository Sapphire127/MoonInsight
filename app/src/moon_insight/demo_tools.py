"""阶段验证用的演示工具（calculator）。

这是验证「工具调用链路」的脚手架，不属于框架业务（spec 用户拍板决策 5）：
框架自身不携带任何业务工具，本模块供测试与 interfaces 演示共用，业务工具到来时移除。
application 不依赖本模块——工具定义与执行器均由使用端注入。
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


def execute_demo_tool(name: str, arguments: dict[str, Any]) -> str:
    """演示工具的执行器：由使用端注入 pipeline 的 executor 参数。"""
    if name == "calculator":
        return calculator(arguments["expression"])
    return f"error: unknown tool {name}"
