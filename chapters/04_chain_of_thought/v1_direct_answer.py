#!/usr/bin/env python3
"""Chapter 04 v1: direct answer baseline.

No explicit intermediate reasoning is shown.
"""


def answer_direct(error_text: str) -> str:
    text = error_text.lower()
    if "modulenotfounderror" in text:
        return "直接建议：运行 pip install 对应缺失包。"
    if "permission" in text:
        return "直接建议：检查文件权限后重试。"
    return "直接建议：请提供更完整日志以定位问题。"


if __name__ == "__main__":
    print(answer_direct("ModuleNotFoundError: requests"))
