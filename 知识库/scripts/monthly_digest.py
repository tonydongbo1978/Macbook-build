#!/usr/bin/env python3
"""把 时事速递/ 下某个月的所有日报汇总成一份月度汇总 Markdown。

用法:
    python3 知识库/scripts/monthly_digest.py            # 当前月
    python3 知识库/scripts/monthly_digest.py 2026-10    # 指定月份

输出:
    知识库/01-IT知识/时事速递/月度汇总/月度汇总-YYYY-MM.md
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, OrderedDict
from datetime import date
from pathlib import Path

KB_DIR = Path(__file__).resolve().parent.parent
DIGEST_DIR = KB_DIR / "01-IT知识" / "时事速递"
ROLLUP_DIR = DIGEST_DIR / "月度汇总"

FILENAME_RE = re.compile(r"^IT重大事件-(\d{4}-\d{2}-\d{2})$")
WEEKDAYS = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]

# 中文数字，用于月度汇总的章节编号
CN_NUMS = ["", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十",
           "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九"]

# 「## 一句话总结」正文
SUMMARY_RE = re.compile(r"^##\s*一句话总结\s*$")
TREND_RE = re.compile(r"^##\s*一句话趋势判断\s*$")
KEYWORDS_RE = re.compile(r"^##\s*关键词总结\s*$")
VERIFY_RE = re.compile(r"^##\s*[⚠\s]*核实说明\s*$")
# 「### 1️⃣ 标题」——仅匹配带圈数字编号的标题，避免把「🔑 核心关键词」误当作事件
EVENT_RE = re.compile(r"^###\s*([1-9]️⃣)\s*(.+?)\s*$")
# 关键词表格行： | 1 | **关键词** | 场景 |
KEYWORD_ROW_RE = re.compile(r"^\|\s*\d+\s*\|\s*(.+?)\s*\|\s*(.*?)\s*\|\s*$")
HEADING_RE = re.compile(r"^#{2,3}\s")


def clean(text: str) -> str:
    """去掉 Markdown 强调符号与多余空白。"""
    text = text.strip()
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"`(.+?)`", r"\1", text)
    return text.strip()


# 模板占位符：命中则视为「未填写」
PLACEHOLDERS = (
    "（用一句话概括当天的主线）",
    "（一句话说明当天的技术/产业动向指向哪里）",
    "标题",
)


def is_placeholder(text: str) -> bool:
    t = clean(text)
    return (not t) or t in PLACEHOLDERS


def collect_section(lines: list, start: int, stop_patterns: list) -> str:
    """收集 start 之后的正文，直到遇到下一个二级标题或匹配 stop_patterns。"""
    out = []
    for line in lines[start:]:
        s = line.strip()
        if s.startswith("## "):
            break
        if s.startswith("---") and out:
            break
        if any(p.match(s) for p in stop_patterns):
            break
        if s:
            out.append(s)
    return " ".join(out).strip()


def parse_digest(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    data = {
        "date": path.stem.replace("IT重大事件-", ""),
        "summary": "",
        "trend": "",
        "keywords": [],   # [(关键词, 场景)]
        "events": [],     # [(序号, 标题)]
        "verifications": [],
        "status": "草稿" if "状态：草稿" in text else "完成",
    }

    for i, line in enumerate(lines):
        s = line.strip()

        if SUMMARY_RE.match(s):
            body = clean(collect_section(lines, i + 1, []))
            data["summary"] = "" if is_placeholder(body) else body
        elif TREND_RE.match(s):
            body = clean(collect_section(lines, i + 1, []))
            data["trend"] = "" if is_placeholder(body) else body
        elif KEYWORDS_RE.match(s):
            pass
        elif VERIFY_RE.match(s):
            body = collect_section(lines, i + 1, [])
            for part in re.split(r"(?<=。)\s*", body):
                part = part.strip()
                if part and not part.startswith("#"):
                    data["verifications"].append(part)
        else:
            m = EVENT_RE.match(s)
            if m:
                title = clean(m.group(2))
                if not is_placeholder(title):
                    idx = m.group(1).strip("️⃣")
                    data["events"].append((idx, title))
                continue

            m = KEYWORD_ROW_RE.match(s)
            if m:
                kw = clean(m.group(1))
                # 跳过表头分隔与空行
                if kw and not set(kw) <= set("-: "):
                    data["keywords"].append((kw, clean(m.group(2))))

    return data


def build_markdown(days: list, month: str) -> str:
    n = len(days)
    total_events = sum(len(d["events"]) for d in days)

    # 关键词词频
    counter = Counter()
    for d in days:
        for kw, _scene in d["keywords"]:
            # 按分隔符拆开并列关键词
            for piece in re.split(r"[/、·]| vs ", kw):
                piece = piece.strip()
                if piece:
                    counter[piece] += 1

    out = []
    sec = iter(range(1, 20))   # 章节号自增，保证「一、二、三…」连续
    out.append("---")
    out.append("分类: 01-IT知识/时事速递")
    out.append("标签: [汇总, 月度]")
    out.append("创建: {}-01".format(month))
    out.append("更新: {}".format(date.today().isoformat()))
    out.append("---")
    out.append("")
    out.append("# IT 时事速递 · {} 月度汇总".format(month))
    out.append("")
    out.append("> 覆盖 {} 天日报 · 收录 {} 条事件".format(n, total_events))
    out.append("> 生成时间：{}".format(date.today().isoformat()))
    out.append("")
    out.append("---")
    out.append("")

    # ---- 1. 本月主线 ----
    out.append("## {}、本月主线".format(CN_NUMS[next(sec)]))
    out.append("")
    completed = [d for d in days if d["summary"]]
    if completed:
        for d in completed:
            out.append("- **{}**（{}）：{}".format(d["date"], WEEKDAYS[date.fromisoformat(d["date"]).weekday()], d["summary"]))
    else:
        out.append("- *（本月暂无已完成总结的日报）*")
    pending = [d["date"] for d in days if not d["summary"]]
    if pending:
        out.append("")
        out.append("> 待填写：{}".format("、".join(pending)))
    out.append("")

    # ---- 2. 高频关键词 ----
    # ---- 2. 高频关键词 ----
    out.append("## {}、高频关键词".format(CN_NUMS[next(sec)]))
    out.append("")
    if counter:
        out.append("| 排名 | 关键词 | 出现天数 |")
        out.append("|:---:|---|:---:|")
        for i, (kw, cnt) in enumerate(counter.most_common(15), start=1):
            out.append("| {} | **{}** | {} |".format(i, kw, cnt))
    else:
        out.append("*（暂无关键词数据）*")
    out.append("")

    # ---- 3. 每日事件清单 ----
    out.append("## {}、每日事件清单".format(CN_NUMS[next(sec)]))
    out.append("")
    for d in days:
        wd = WEEKDAYS[date.fromisoformat(d["date"]).weekday()]
        out.append("### {}（{}）".format(d["date"], wd))
        out.append("")
        if d["events"]:
            for idx, title in d["events"]:
                out.append("{}. {}".format(idx, title))
        else:
            out.append("*（无记录）*")
        out.append("")
        out.append("[查看日报](IT重大事件-{}.md)".format(d["date"]))
        out.append("")

    # ---- 4. 趋势判断汇总 ----
    trends = [d for d in days if d["trend"]]
    if trends:
        out.append("## {}、趋势判断汇总".format(CN_NUMS[next(sec)]))
        out.append("")
        for d in trends:
            out.append("- **{}**：{}".format(d["date"], d["trend"]))
        out.append("")

    # ---- 5. 核实记录 ----
    verifs = [(d["date"], v) for d in days for v in d["verifications"]]
    if verifs:
        out.append("## {}、核实与存疑记录".format(CN_NUMS[next(sec)]))
        out.append("")
        for dt, v in verifs:
            out.append("- `{}` {}".format(dt, v))
        out.append("")

    # ---- 6. 统计 ----
    out.append("## {}、月度统计".format(CN_NUMS[next(sec)]))
    out.append("")
    done = sum(1 for d in days if d["status"] == "完成")
    out.append("| 指标 | 数值 |")
    out.append("|---|---|")
    out.append("| 日报天数 | {} |".format(n))
    out.append("| 已定稿天数 | {} |".format(done))
    out.append("| 收录事件总数 | {} |".format(total_events))
    out.append("| 日均事件数 | {:.1f} |".format(total_events / n if n else 0))
    out.append("| 不同关键词数 | {} |".format(len(counter)))
    out.append("")
    out.append("> 「收录事件总数」仅统计带圈数字标题（1️⃣–5️⃣），未填写的草稿不计入。")
    out.append("")

    return "\n".join(out)


def main(argv: list = None) -> int:
    parser = argparse.ArgumentParser(description="汇总月度 IT 时事速递")
    parser.add_argument("month", nargs="?", help="月份，格式 YYYY-MM，默认当前月")
    args = parser.parse_args(argv)

    month = args.month or date.today().strftime("%Y-%m")
    if not re.fullmatch(r"\d{4}-\d{2}", month):
        print("月份格式错误：{}（应为 YYYY-MM）".format(month), file=sys.stderr)
        return 2

    files = []
    for p in sorted(DIGEST_DIR.glob("*.md")):
        m = FILENAME_RE.match(p.stem)
        if m and p.stem.startswith("IT重大事件-" + month):
            files.append(p)

    if not files:
        print("{} 没有找到任何日报（{}/IT重大事件-YYYY-MM-DD.md）".format(month, DIGEST_DIR), file=sys.stderr)
        return 1

    days = [parse_digest(p) for p in files]
    text = build_markdown(days, month)

    ROLLUP_DIR.mkdir(parents=True, exist_ok=True)
    out = ROLLUP_DIR / "月度汇总-{}.md".format(month)
    out.write_text(text, encoding="utf-8")

    total_events = sum(len(d["events"]) for d in days)
    print("已生成：{}".format(out))
    print("覆盖 {} 天，{} 条事件".format(len(days), total_events))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
