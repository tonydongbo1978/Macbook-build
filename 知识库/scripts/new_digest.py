#!/usr/bin/env python3
"""新建一天的 IT 时事速递文件（基于 时事速递/_模板.md）。

用法:
    python3 知识库/scripts/new_digest.py                # 今天
    python3 知识库/scripts/new_digest.py 2026-10-14     # 指定日期
    python3 知识库/scripts/new_digest.py --yesterday    # 昨天
    python3 知识库/scripts/new_digest.py --force        # 已存在时覆盖

输出:
    知识库/01-IT知识/时事速递/IT重大事件-YYYY-MM-DD.md
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

KB_DIR = Path(__file__).resolve().parent.parent
DIGEST_DIR = KB_DIR / "01-IT知识" / "时事速递"
TEMPLATE = DIGEST_DIR / "_模板.md"

WEEKDAYS = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]

# 计算时间窗口：前一天 09:00 → 当天 09:00
WINDOW_START_HOUR = 9


def build(target: date, force: bool = False) -> Path:
    dest = DIGEST_DIR / "IT重大事件-{}.md".format(target.isoformat())
    if dest.exists() and not force:
        print("已存在，未覆盖：{}".format(dest))
        return dest

    window_start = (target - timedelta(days=1)).isoformat()
    window_end = target.isoformat()
    weekday = WEEKDAYS[target.weekday()]
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    if TEMPLATE.exists():
        text = TEMPLATE.read_text(encoding="utf-8")
        text = text.replace("YYYY-MM-DD", target.isoformat())
        text = re.sub(r"（星期X）", "（{}）".format(weekday), text)
        # 时间窗口：前一日的 09:00 到目标日 09:00
        text = re.sub(
            r"时间窗口：\S+ 09:00 ~ 次日 09:00（北京时间）",
            "时间窗口：{} 09:00 ~ {} 09:00（北京时间）".format(window_start, window_end),
            text,
        )
        text = re.sub(r"整理时间：\S+ \S+ CST", "整理时间：{} CST".format(now), text)
    else:
        # 模板缺失时回退到内置结构
        text = (
            "---\n"
            "分类: 01-IT知识/时事速递\n"
            "标签: []\n"
            "创建: {d}\n"
            "更新: {d}\n"
            "---\n\n"
            "# IT 领域重大事件 · {d}（{w}）\n\n"
            "> 时间窗口：{s} 09:00 ~ {e} 09:00（北京时间）\n"
            "> 整理时间：{now} CST\n"
            "> 状态：草稿\n\n"
            "---\n\n"
            "## 一句话总结\n\n\n\n"
            "---\n\n"
            "## TOP 5 事件\n\n"
            "### 1️⃣ \n\n- **时间**：\n- **来源**：\n\n\n"
            "### 2️⃣ \n\n- **时间**：\n- **来源**：\n\n\n"
            "### 3️⃣ \n\n- **时间**：\n- **来源**：\n\n\n"
            "### 4️⃣ \n\n- **时间**：\n- **来源**：\n\n\n"
            "### 5️⃣ \n\n- **时间**：\n- **来源**：\n\n\n"
            "---\n\n"
            "## 关键词总结\n\n\n"
            "## 一句话趋势判断\n\n\n"
            "## ⚠️ 核实说明\n\n-\n"
        ).format(d=target.isoformat(), w=weekday, s=window_start, e=window_end, now=now)

    DIGEST_DIR.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding="utf-8")
    print("已创建：{}".format(dest))
    return dest


def main(argv: list = None) -> int:
    parser = argparse.ArgumentParser(description="新建一天的 IT 时事速递")
    parser.add_argument("date", nargs="?", help="日期，格式 YYYY-MM-DD，默认今天")
    parser.add_argument("--yesterday", action="store_true", help="使用昨天的日期")
    parser.add_argument("--force", action="store_true", help="已存在时覆盖")
    args = parser.parse_args(argv)

    if args.yesterday:
        target = date.today() - timedelta(days=1)
    elif args.date:
        try:
            target = date.fromisoformat(args.date)
        except ValueError:
            print("日期格式错误：{}（应为 YYYY-MM-DD）".format(args.date), file=sys.stderr)
            return 2
    else:
        target = date.today()

    build(target, force=args.force)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
