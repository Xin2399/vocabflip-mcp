# Tab 3 阅读练习 - 题目数据
# 每道题：一段真实官文 + 若干"找点"任务 + 答案关键词

READING_PASSAGES = [
  {
    "id": 1,
    "title": "PCT/RO/105 — 国际申请号及申请日通知",
    "source": "PCT/RO/105",
    "batch": 1,
    "text": (
      "PATENT COOPERATION TREATY\n\n"
      "NOTIFICATION OF THE INTERNATIONAL APPLICATION NUMBER "
      "AND OF THE INTERNATIONAL FILING DATE\n\n"
      "Applicant's or agent's file reference: ABC-2024-001\n\n"
      "To: Example Technology Co., Ltd.\n"
      "    Shenzhen, China\n\n"
      "International Application No.: PCT/CN2024/098765\n"
      "International Filing Date: 15 March 2024\n"
      "Title of Invention: Method and System for Intelligent Document Processing\n\n"
      "The receiving Office hereby notifies the applicant that the above-mentioned "
      "international filing date has been accorded to the international application.\n\n"
      "From: China National Intellectual Property Administration (CNIPA) as receiving Office\n"
      "Date of mailing: 20 March 2024"
    ),
    "questions": [
      {
        "id": "q1_appno",
        "ask": "国际申请号是多少？",
        "hint": "格式：PCT/XX...",
        "answer_keywords": ["PCT/CN2024/098765"],
        "answer_display": "PCT/CN2024/098765"
      },
      {
        "id": "q1_filingdate",
        "ask": "国际申请日是哪天？",
        "hint": "格式：日 月 年",
        "answer_keywords": ["15 March 2024", "15 march 2024"],
        "answer_display": "15 March 2024"
      },
      {
        "id": "q1_ro",
        "ask": "受理局是哪个机构？（简称即可）",
        "hint": "缩写2-5个字母",
        "answer_keywords": ["CNIPA", "cnipa"],
        "answer_display": "CNIPA"
      }
    ]
  },
  {
    "id": 2,
    "title": "PCT/RO/106 — 邀请纠正缺陷通知",
    "source": "PCT/RO/106",
    "batch": 1,
    "text": (
      "IMPORTANT NOTIFICATION\n\n"
      "INVITATION TO CORRECT DEFECTS IN THE INTERNATIONAL APPLICATION\n"
      "(PCT Article 14(1)(b) and Rule 26.2)\n\n"
      "Applicant's or agent's file reference: ABC-2024-001\n"
      "International Application No.: PCT/CN2024/098765\n"
      "International Filing Date: 15 March 2024\n"
      "Date of mailing: 25 March 2024\n\n"
      "The applicant is hereby notified that the following defects have been found "
      "in the international application:\n\n"
      "1. The request does not contain the signature of the applicant or agent "
      "as required under Rule 26.3ter(a).\n\n"
      "The applicant is invited to correct the above defects within TWO MONTHS "
      "from the date of mailing of this notification.\n\n"
      "Failure to correct the defects within the time limit specified above will "
      "result in the international application being considered withdrawn under "
      "PCT Article 14(1)(b)."
    ),
    "questions": [
      {
        "id": "q2_defect",
        "ask": "邮件里提到了什么缺陷？（核心关键词即可）",
        "hint": "缺少什么？",
        "answer_keywords": ["signature", "签名"],
        "answer_display": "signature（签名）"
      },
      {
        "id": "q2_timelimit",
        "ask": "申请人有多长时间来纠正缺陷？",
        "hint": "数字+时间单位",
        "answer_keywords": ["two months", "2 months", "两个月", "2个月"],
        "answer_display": "TWO MONTHS（两个月）"
      },
      {
        "id": "q2_consequence",
        "ask": "如果没有在期限内纠正，会发生什么？",
        "hint": "看最后一段",
        "answer_keywords": ["withdrawn", "撤回"],
        "answer_display": "considered withdrawn（视为撤回）"
      }
    ]
  },
  {
    "id": 3,
    "title": "PCT/IB/301 — 原件副本收到通知",
    "source": "PCT/IB/301",
    "batch": 1,
    "text": (
      "PATENT COOPERATION TREATY\n\n"
      "NOTIFICATION CONCERNING THE RECORD COPY\n\n"
      "Applicant's or agent's file reference: ABC-2024-001\n"
      "International Application No.: PCT/CN2024/098765\n"
      "Priority Date: 10 January 2024\n"
      "Date of mailing: 02 April 2024\n\n"
      "The International Bureau hereby notifies the applicant that the record copy "
      "of the above-identified international application has been received by the "
      "International Bureau on 01 April 2024.\n\n"
      "The international application will be published on 10 July 2024, "
      "which is after the expiration of 18 months from the priority date.\n\n"
      "Note: The applicant may file amendments to the claims under PCT Article 19 "
      "within a time limit of one month from the date of transmittal of the "
      "international search report, or 16 months from the priority date, "
      "whichever time limit expires later."
    ),
    "questions": [
      {
        "id": "q3_priority",
        "ask": "优先权日是哪天？",
        "hint": "格式：日 月 年",
        "answer_keywords": ["10 January 2024", "10 january 2024"],
        "answer_display": "10 January 2024"
      },
      {
        "id": "q3_publish",
        "ask": "国际申请预计什么时候公开发布？",
        "hint": "看 will be published",
        "answer_keywords": ["10 July 2024", "10 july 2024"],
        "answer_display": "10 July 2024"
      },
      {
        "id": "q3_art19",
        "ask": "根据文本，申请人可以依据哪个条款修改权利要求？",
        "hint": "PCT Article ...",
        "answer_keywords": ["article 19", "19"],
        "answer_display": "PCT Article 19"
      }
    ]
  }
]
