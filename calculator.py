"""一个简单的命令行计算器。

支持 + - * / % ** 、括号、负数和小数，例如：
    (1 + 2) * 3 - 4 / 2
    -2 ** 2
    10 % 3

用法：
    python calculator.py              # 交互模式
    python calculator.py "1 + 2 * 3"  # 直接计算一个表达式
"""

import ast
import operator
import sys

_BINARY_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


class CalcError(Exception):
    """表达式不合法或无法计算时抛出。"""


def _eval_node(node):
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPS:
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > 1000:
            raise CalcError("指数太大")
        try:
            return _BINARY_OPS[type(node.op)](left, right)
        except ZeroDivisionError:
            raise CalcError("不能除以 0")
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPS:
        return _UNARY_OPS[type(node.op)](_eval_node(node.operand))
    raise CalcError("不支持的表达式")


def calculate(expression):
    """计算算术表达式并返回结果。

    只解析数字和算术运算符，不会执行任意代码。
    """
    if not expression.strip():
        raise CalcError("表达式为空")
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError:
        raise CalcError("语法错误")
    result = _eval_node(tree)
    if isinstance(result, float) and result.is_integer():
        return int(result)
    return result


def main(argv):
    if len(argv) > 1:
        try:
            print(calculate(" ".join(argv[1:])))
        except CalcError as e:
            print(f"错误：{e}", file=sys.stderr)
            return 1
        return 0

    print("简单计算器（输入 q 退出）")
    while True:
        try:
            line = input("> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if line.strip().lower() in ("q", "quit", "exit"):
            break
        if not line.strip():
            continue
        try:
            print(calculate(line))
        except CalcError as e:
            print(f"错误：{e}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
