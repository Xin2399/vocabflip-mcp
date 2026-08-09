#!/usr/bin/env python3
"""Vocab MCP - 词汇学习进度追踪  端口 8771  SSE传输"""
import sqlite3, json, os
from datetime import date
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("vocab", host="0.0.0.0", port=8771)

# 数据库路径：优先使用环境变量，默认使用当前目录下的 vocab.db
DB = os.environ.get("DB_PATH", os.path.join(os.path.dirname(os.path.abspath(__file__)), "vocab.db"))

def db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """初始化数据库：建表 + 种子数据"""
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    with db() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS words (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            word       TEXT NOT NULL,
            phonetic   TEXT DEFAULT '',
            meaning    TEXT NOT NULL,
            example    TEXT DEFAULT '',
            batch      INTEGER DEFAULT 1,
            is_active  INTEGER DEFAULT 1,
            created_at TEXT DEFAULT (date('now'))
        );
        CREATE TABLE IF NOT EXISTS study_log (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            word_id  INTEGER NOT NULL,
            status   TEXT NOT NULL,
            log_date TEXT NOT NULL DEFAULT (date('now','localtime')),
            UNIQUE(word_id, log_date)
        );
        CREATE TABLE IF NOT EXISTS phrases (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            word_id  INTEGER REFERENCES words(id),
            scene    TEXT DEFAULT '',
            sentence TEXT NOT NULL,
            source   TEXT DEFAULT '',
            batch    INTEGER DEFAULT 1
        );
        """)
        # 检查是否已有数据
        cnt = c.execute("SELECT COUNT(*) FROM words").fetchone()[0]
        if cnt == 0:
            batch1 = [
                ("applicant","/ˈæplɪkənt/","申请人","The applicant is hereby notified that the international filing date has been accorded.",1),
                ("agent","/ˈeɪdʒənt/","代理人","The agent filed the PCT application on behalf of the applicant.",1),
                ("file reference","/faɪl ˈrefərəns/","档案编号（内部编号）","Please quote your file reference in all correspondence.",1),
                ("international application No.","","国际申请号","International Application No.: PCT/CN2024/123456",1),
                ("international filing date","","国际申请日","The international filing date has been accorded as 15 March 2024.",1),
                ("receiving Office","/rɪˈsiːvɪŋ ˈɒfɪs/","受理局（缩写 RO）","The receiving Office hereby notifies the applicant of the filing date.",1),
                ("accorded","/əˈkɔːdɪd/","（正式）授予、认定","An international filing date has been accorded to this application.",1),
                ("hereby notifies","","特此通知（官文套语）","The receiving Office hereby notifies the applicant that...",1),
                ("defects","/dɪˈfekts/","缺陷、瑕疵","The following defects have been found in the international application.",1),
                ("invited to correct","","被要求纠正","The applicant is invited to correct the defects within two months.",1),
                ("time limit","/taɪm ˈlɪmɪt/","期限、截止时间","Failure to act within the time limit may result in loss of rights.",1),
                ("considered withdrawn","","视为撤回","The application will be considered withdrawn if no response is received.",1),
                ("priority date","/praɪˈɒrɪti deɪt/","优先权日","The priority date is the date of the earliest related application.",1),
                ("designated Office","/ˈdezɪɡneɪtɪd ˈɒfɪs/","指定局（缩写 DO）","The applicant must enter the national phase before each designated Office.",1),
                ("international search report","","国际检索报告（缩写 ISR）","The international search report will be issued within three months.",1),
            ]
            for s in batch1:
                c.execute("INSERT INTO words (word,phonetic,meaning,example,batch) VALUES (?,?,?,?,?)", s)
            print(f"Seeded {len(batch1)} words")

@mcp.tool()
def vocab_check_today() -> str:
    """查今天的学习情况"""
    today = date.today().isoformat()
    try:
        with db() as c:
            total   = c.execute("SELECT COUNT(*) FROM words WHERE is_active=1").fetchone()[0]
            learned = c.execute("SELECT COUNT(*) FROM study_log WHERE log_date=? AND status='learned'",(today,)).fetchone()[0]
            review  = c.execute("SELECT COUNT(*) FROM study_log WHERE log_date=? AND status='review'",(today,)).fetchone()[0]
            untouched = total - learned - review
            details = c.execute("""
                SELECT w.word, sl.status
                FROM study_log sl JOIN words w ON w.id=sl.word_id
                WHERE sl.log_date=? ORDER BY sl.id
            """, (today,)).fetchall()
        result = f"📅 {today} 学习报告\n"
        result += f"总词数: {total}  已学会: {learned}  需复习: {review}  未碰: {untouched}\n"
        if total > 0:
            pct = int(learned / total * 100)
            result += f"完成率: {pct}%\n"
        if details:
            result += "\n--- 今日记录 ---\n"
            for d in details:
                icon = "✓" if d["status"] == "learned" else "↻"
                result += f"  {icon} {d['word']}\n"
        else:
            result += "\n今天还没开始学习哦。"
        return result
    except Exception as e:
        return f"查询失败: {e}"

@mcp.tool()
def vocab_add_words(words_json: str, batch: int = 2, deactivate_old: bool = False) -> str:
    """
    批量添加新词（进入下一阶段学习时用）
    words_json: JSON字符串，格式 [{"word":"...","phonetic":"...","meaning":"...","example":"..."}]
    batch: 批次编号（第一批=1，第二批=2，以此类推）
    deactivate_old: 是否把之前的批次全部设为不激活
    """
    try:
        words = json.loads(words_json)
        with db() as c:
            if deactivate_old:
                c.execute("UPDATE words SET is_active=0")
            for w in words:
                c.execute(
                    "INSERT INTO words (word,phonetic,meaning,example,batch,is_active) VALUES (?,?,?,?,?,1)",
                    (w.get("word",""), w.get("phonetic",""), w.get("meaning",""), w.get("example",""), batch)
                )
        return f"已添加 {len(words)} 个词到第 {batch} 批。{'旧批次已停用。' if deactivate_old else ''}"
    except Exception as e:
        return f"添加失败: {e}"

@mcp.tool()
def vocab_get_all_progress() -> str:
    """查所有批次的整体进度"""
    try:
        with db() as c:
            batches = c.execute("SELECT DISTINCT batch FROM words ORDER BY batch").fetchall()
            result  = "=== 整体进度 ===\n"
            for b in batches:
                bn    = b["batch"]
                total = c.execute("SELECT COUNT(*) FROM words WHERE batch=?",(bn,)).fetchone()[0]
                activ = c.execute("SELECT COUNT(*) FROM words WHERE batch=? AND is_active=1",(bn,)).fetchone()[0]
                learned_ids = c.execute("""
                    SELECT DISTINCT word_id FROM study_log sl
                    JOIN words w ON w.id=sl.word_id
                    WHERE w.batch=? AND sl.status='learned'
                """,(bn,)).fetchall()
                result += f"  第{bn}批: {total}词，{'激活中' if activ else '已存档'}，历史学会{len(learned_ids)}词\n"
        return result
    except Exception as e:
        return f"查询失败: {e}"

if __name__ == "__main__":
    init_db()
    print(f"DB path: {DB}")
    mcp.run(transport="sse")
