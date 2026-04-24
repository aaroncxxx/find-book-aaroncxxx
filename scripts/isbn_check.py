#!/usr/bin/env python3
"""ISBN 校验与格式化工具"""

import re
import sys


def validate_isbn(isbn: str) -> dict:
    """校验 ISBN-10 或 ISBN-13"""
    # 清理输入
    clean = re.sub(r'[-\s]', '', isbn.strip())
    
    result = {"original": isbn, "clean": clean, "valid": False, "type": None, "error": None}
    
    if len(clean) == 10:
        result["type"] = "ISBN-10"
        result["valid"] = _check_isbn10(clean)
    elif len(clean) == 13:
        result["type"] = "ISBN-13"
        result["valid"] = _check_isbn13(clean)
    else:
        result["error"] = f"长度错误: {len(clean)}位（应为10或13位）"
    
    return result


def _check_isbn10(s: str) -> bool:
    if not re.match(r'^\d{9}[\dXx]$', s):
        return False
    total = sum((10 - i) * (int(c) if c not in 'Xx' else 10) for i, c in enumerate(s))
    return total % 11 == 0


def _check_isbn13(s: str) -> bool:
    if not re.match(r'^\d{13}$', s):
        return False
    weights = [1, 3] * 6 + [1]
    total = sum(int(c) * w for c, w in zip(s, weights))
    return total % 10 == 0


def format_isbn(isbn: str) -> str:
    """格式化 ISBN 为标准连字符形式"""
    clean = re.sub(r'[-\s]', '', isbn.strip())
    if len(clean) == 13:
        # ISBN-13: 978-X-XXXX-XXXX-X
        return f"{clean[:3]}-{clean[3]}-{clean[4:8]}-{clean[8:12]}-{clean[12]}"
    elif len(clean) == 10:
        # ISBN-10: X-XXXX-XXXX-X
        return f"{clean[0]}-{clean[1:5]}-{clean[5:9]}-{clean[9]}"
    return isbn


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 isbn_check.py <ISBN> [ISBN2 ...]")
        print("示例: python3 isbn_check.py 978-7-100-05982-4 9780521585848")
        sys.exit(1)
    
    for arg in sys.argv[1:]:
        r = validate_isbn(arg)
        status = "✅" if r["valid"] else "❌"
        print(f"{status} {r['original']} → {r['type'] or 'N/A'} | 格式: {format_isbn(arg)}", end="")
        if r["error"]:
            print(f" | {r['error']}", end="")
        print()
