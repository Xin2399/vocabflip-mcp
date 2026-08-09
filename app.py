#!/usr/bin/env python3
"""Vocab - 涉外知产英语学习小站  Flask 5002"""
import sqlite3, json
from datetime import date
from flask import Flask, request, jsonify, render_template

import os as _os
app = Flask(__name__, template_folder=_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "templates"))

@app.after_request
def no_cache(resp):
    resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    resp.headers["Pragma"] = "no-cache"
    return resp
DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vocab.db") if "DB_PATH" not in _os.environ else _os.environ["DB_PATH"]

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.executescript("""
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

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/words/active")
def get_active_words():
    today = date.today().isoformat()
    with get_db() as db:
        words = db.execute("""
            SELECT w.id, w.word, w.phonetic, w.meaning, w.example, w.batch,
                   sl.status as today_status
            FROM words w
            LEFT JOIN study_log sl ON sl.word_id=w.id AND sl.log_date=?
            WHERE w.is_active=1 ORDER BY w.id
        """, (today,)).fetchall()
    return jsonify([dict(r) for r in words])

@app.route("/api/study", methods=["POST"])
def mark_study():
    data = request.get_json()
    word_id = data.get("word_id")
    status  = data.get("status")
    today   = date.today().isoformat()
    if not word_id or status not in ("learned","review"):
        return jsonify({"error":"bad request"}), 400
    with get_db() as db:
        db.execute("""
            INSERT INTO study_log (word_id, status, log_date) VALUES (?,?,?)
            ON CONFLICT(word_id, log_date) DO UPDATE SET status=excluded.status
        """, (word_id, status, today))
    return jsonify({"ok": True})

@app.route("/api/progress")
def progress():
    today = date.today().isoformat()
    with get_db() as db:
        total   = db.execute("SELECT COUNT(*) FROM words WHERE is_active=1").fetchone()[0]
        learned = db.execute("SELECT COUNT(*) FROM study_log WHERE log_date=? AND status='learned'",(today,)).fetchone()[0]
        review  = db.execute("SELECT COUNT(*) FROM study_log WHERE log_date=? AND status='review'",(today,)).fetchone()[0]
    return jsonify({"date":today,"total":total,"learned":learned,"review":review,"untouched":total-learned-review})

@app.route("/api/phrases")
def get_phrases():
    """返回当前激活批次的全部例句，按 word_id 分组"""
    with get_db() as db:
        rows = db.execute("""
            SELECT p.id, p.word_id, p.scene, p.sentence, p.source,
                   w.word, w.meaning, w.phonetic
            FROM phrases p
            JOIN words w ON w.id=p.word_id
            WHERE w.is_active=1
            ORDER BY p.word_id, p.id
        """).fetchall()
    return jsonify([dict(r) for r in rows])

@app.route("/api/admin/add_words", methods=["POST"])
def add_words():
    data  = request.get_json()
    words = data.get("words", [])
    batch = data.get("batch", 1)
    if not words:
        return jsonify({"error":"empty"}), 400
    with get_db() as db:
        if data.get("deactivate_old", False):
            db.execute("UPDATE words SET is_active=0")
        for w in words:
            db.execute("INSERT INTO words (word,phonetic,meaning,example,batch,is_active) VALUES (?,?,?,?,?,1)",
                (w.get("word",""), w.get("phonetic",""), w.get("meaning",""), w.get("example",""), batch))
    return jsonify({"ok":True,"added":len(words)})

@app.route("/api/admin/add_phrases", methods=["POST"])
def add_phrases():
    data    = request.get_json()
    phrases = data.get("phrases", [])
    if not phrases:
        return jsonify({"error":"empty"}), 400
    with get_db() as db:
        for p in phrases:
            db.execute("INSERT INTO phrases (word_id,scene,sentence,source,batch) VALUES (?,?,?,?,?)",
                (p.get("word_id"), p.get("scene",""), p.get("sentence",""), p.get("source",""), p.get("batch",1)))
    return jsonify({"ok":True,"added":len(phrases)})

@app.route("/api/admin/set_batch", methods=["POST"])
def set_batch():
    data  = request.get_json()
    batch = data.get("batch")
    if not batch:
        return jsonify({"error":"batch required"}), 400
    with get_db() as db:
        db.execute("UPDATE words SET is_active=0")
        db.execute("UPDATE words SET is_active=1 WHERE batch=?", (batch,))
        count = db.execute("SELECT COUNT(*) FROM words WHERE is_active=1").fetchone()[0]
    return jsonify({"ok":True,"active_words":count})


# ── Tab 3: 阅读练习 ──────────────────────────────────────────
@app.route('/api/readings')
def get_readings():
    from reading_data import READING_PASSAGES
    batch = int(request.args.get('batch', 1))
    result = []
    for p in READING_PASSAGES:
        if p.get('batch', 1) != batch:
            continue
        result.append({
            'id': p['id'],
            'title': p['title'],
            'source': p['source'],
            'text': p['text'],
            'questions': [
                {'id': q['id'], 'ask': q['ask'], 'hint': q['hint']}
                for q in p['questions']
            ]
        })
    return jsonify(result)

@app.route('/api/readings/check', methods=['POST'])
def check_reading():
    from reading_data import READING_PASSAGES
    data    = request.get_json()
    p_id    = data.get('passage_id')
    q_id    = data.get('question_id')
    answer  = (data.get('answer') or '').strip().lower()
    for p in READING_PASSAGES:
        if p['id'] != p_id:
            continue
        for q in p['questions']:
            if q['id'] != q_id:
                continue
            correct = any(kw.lower() in answer for kw in q['answer_keywords'])
            return jsonify({
                'correct': correct,
                'answer_display': q['answer_display'],
                'feedback': '答对了！' if correct else '再想想，参考答案：' + q['answer_display']
            })
    return jsonify({'error': 'not found'}), 404


# ── Tab 4: 知识题 ──────────────────────────────────────────
import random as _random

@app.route('/api/quiz/questions')
def get_quiz():
    from quiz_data import QUIZ_QUESTIONS
    category = request.args.get('category', 'all')
    count = int(request.args.get('count', 8))
    pool = QUIZ_QUESTIONS if category == 'all' else [q for q in QUIZ_QUESTIONS if q['category'] == category]
    selected = _random.sample(pool, min(count, len(pool)))
    # 不传答案给前端
    result = []
    for q in selected:
        result.append({
            'id': q['id'],
            'category': q['category'],
            'question': q['question'],
            'options': q['options']
        })
    return jsonify(result)

@app.route('/api/quiz/check', methods=['POST'])
def check_quiz():
    from quiz_data import QUIZ_QUESTIONS
    data   = request.get_json()
    q_id   = data.get('question_id')
    chosen = data.get('chosen')  # index 0-3
    for q in QUIZ_QUESTIONS:
        if q['id'] != q_id:
            continue
        correct = (chosen == q['answer'])
        return jsonify({
            'correct': correct,
            'answer': q['answer'],
            'explanation': q['explanation']
        })
    return jsonify({'error': 'not found'}), 404

if __name__ == "__main__":
    init_db()
    with get_db() as db:
        cnt = db.execute("SELECT COUNT(*) FROM words").fetchone()[0]
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
        with get_db() as db2:
            for s in batch1:
                db2.execute("INSERT INTO words (word,phonetic,meaning,example,batch) VALUES (?,?,?,?,?)", s)
        print(f"Seeded {len(batch1)} words")
    # 写入第一批例句（phrases）
    with get_db() as db:
        pcnt = db.execute("SELECT COUNT(*) FROM phrases").fetchone()[0]
    if pcnt == 0:
        with get_db() as db:
            # 拿到word_id映射
            wmap = {r["word"]: r["id"] for r in db.execute("SELECT id, word FROM words WHERE batch=1").fetchall()}
        phrases = [
            # applicant
            (wmap.get("applicant"), "受理通知", "The applicant is hereby notified that the international filing date of 15 March 2024 has been accorded to the above-identified international application.", "PCT/RO/105", 1),
            (wmap.get("applicant"), "缺陷通知", "The applicant is invited to correct the following defects within a period of two months from the date of mailing of this notification.", "PCT/RO/106", 1),
            (wmap.get("applicant"), "撤回通知", "The applicant is hereby notified that the above-identified international application is considered withdrawn.", "PCT/RO/117", 1),
            # agent
            (wmap.get("agent"), "代理任命", "The agent appointed to act on behalf of the applicant before this receiving Office is identified in Box No. IV of the request.", "PCT/RO/101", 1),
            (wmap.get("agent"), "地址对应", "All correspondence will be sent to the address of the agent unless otherwise indicated.", "PCT/RO/101 Notes", 1),
            # file reference
            (wmap.get("file reference"), "标题行", "Applicant's or agent's file reference: ABC-2024-001 / International Application No.: PCT/CN2024/123456", "PCT form header", 1),
            (wmap.get("file reference"), "回信引用", "Please quote the above file reference in any reply to this notification.", "PCT/RO/105", 1),
            # international filing date
            (wmap.get("international filing date"), "授予通知", "The receiving Office hereby notifies the applicant that an international filing date of 15 March 2024 has been accorded to the international application.", "PCT/RO/105", 1),
            (wmap.get("international filing date"), "优先权计算", "The international filing date is the date from which the 30-month time limit for entering the national phase is calculated.", "PCT Applicant's Guide", 1),
            # receiving Office
            (wmap.get("receiving Office"), "受理局通知", "This receiving Office (RO/CN) has examined the international application and found it to be in order.", "PCT/RO/105", 1),
            # accorded
            (wmap.get("accorded"), "日期授予", "An international filing date has been accorded to the international application referred to above.", "PCT/RO/105", 1),
            # hereby notifies
            (wmap.get("hereby notifies"), "套语场景1", "The International Bureau hereby notifies the applicant that the record copy has been received.", "PCT/IB/301", 1),
            (wmap.get("hereby notifies"), "套语场景2", "This Authority hereby notifies the applicant that the demand has been received on the date indicated below.", "PCT/IPEA/402", 1),
            # defects
            (wmap.get("defects"), "缺陷列举", "The following defects have been found in the international application: (1) The request does not contain the signature of the applicant as required under Rule 26.3ter.", "PCT/RO/106", 1),
            # invited to correct
            (wmap.get("invited to correct"), "纠正邀请", "The applicant is invited to correct the above defects within TWO MONTHS from the date of mailing of this invitation.", "PCT/RO/106", 1),
            # time limit
            (wmap.get("time limit"), "期限警告", "Failure to comply with this requirement within the time limit may result in the international application being considered withdrawn.", "PCT/RO/106", 1),
            (wmap.get("time limit"), "时限说明", "The applicable time limit for entering the national phase before this Office is 30 months from the priority date.", "PCT Guide", 1),
            # considered withdrawn
            (wmap.get("considered withdrawn"), "撤回通知", "NOTIFICATION THAT INTERNATIONAL APPLICATION CONSIDERED WITHDRAWN — The applicant is hereby notified that the international application is considered withdrawn.", "PCT/RO/117", 1),
            # priority date
            (wmap.get("priority date"), "优先权声明", "The priority date claimed in the international application is 10 January 2024, based on national application No. CN202410012345.6.", "PCT/RO/101", 1),
            # designated Office
            (wmap.get("designated Office"), "进入国家阶段", "The applicant must take the necessary steps to enter the national phase before each designated Office within 30 months from the priority date.", "PCT Applicant's Guide", 1),
            # international search report
            (wmap.get("international search report"), "检索报告通知", "The international search report and the written opinion of the International Searching Authority have been established and are transmitted herewith.", "PCT/ISA/210", 1),
        ]
        with get_db() as db2:
            for p in phrases:
                if p[0]:  # word_id存在才插入
                    db2.execute("INSERT INTO phrases (word_id,scene,sentence,source,batch) VALUES (?,?,?,?,?)", p)
        print(f"Seeded {len([p for p in phrases if p[0]])} phrases")
    app.run(host="0.0.0.0", port=5002, debug=False)

# placeholder to trigger syntax error detection
