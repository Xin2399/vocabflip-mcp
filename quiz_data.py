# Tab 4 知识题 - PCT / US / EP / 常用国家地区
# 全部选择题，4选1，含解析

QUIZ_QUESTIONS = [
  # ── PCT ──────────────────────────────────────────────────────
  {
    "id": "pct_001",
    "category": "PCT",
    "question": "PCT申请的国际公开通常在优先权日后多少个月进行？",
    "options": ["12个月", "18个月", "24个月", "30个月"],
    "answer": 1,
    "explanation": "PCT申请在优先权日起18个月后由国际局公开，这是PCT体系的标准时间节点。"
  },
  {
    "id": "pct_002",
    "category": "PCT",
    "question": "PCT申请进入国家阶段的标准期限是优先权日起多少个月？",
    "options": ["20个月", "25个月", "30个月", "36个月"],
    "answer": 2,
    "explanation": "PCT申请进入各指定国的国家阶段，标准期限为优先权日起30个月。部分国家有所不同，但30个月是最普遍的基准。"
  },
  {
    "id": "pct_003",
    "category": "PCT",
    "question": "以下哪个机构负责发布国际检索报告（ISR）？",
    "options": ["国际局（IB）", "受理局（RO）", "国际检索机构（ISA）", "指定局（DO）"],
    "answer": 2,
    "explanation": "国际检索机构（ISA，如USPTO、EPO、CNIPA等）负责检索并出具国际检索报告（ISR）和书面意见（WO-ISA）。"
  },
  {
    "id": "pct_004",
    "category": "PCT",
    "question": "PCT申请中，申请人可依据哪个条款在收到ISR后修改权利要求？",
    "options": ["Article 6", "Article 19", "Article 28", "Article 41"],
    "answer": 1,
    "explanation": "Article 19允许申请人在收到国际检索报告后一个月内（或优先权日起16个月，取较晚者）向国际局提交权利要求修改。"
  },
  {
    "id": "pct_005",
    "category": "PCT",
    "question": "PCT申请中，\"receiving Office\"指的是？",
    "options": ["负责初步审查的机构", "接收PCT申请的机构", "发布公告的机构", "颁发专利证书的机构"],
    "answer": 1,
    "explanation": "受理局（RO, Receiving Office）是接收PCT国际申请的机构，通常是申请人所在国的专利局，也可以直接向WIPO国际局（RO/IB）提交。"
  },
  {
    "id": "pct_006",
    "category": "PCT",
    "question": "申请人提交PCT申请后，如未在通知期限内纠正签名缺陷，申请将被视为？",
    "options": ["暂时搁置", "转为实用新型", "considered withdrawn（视为撤回）", "自动转入国家阶段"],
    "answer": 2,
    "explanation": "依据PCT Article 14(1)(b)，若申请人未在规定期限内纠正缺陷，受理局将宣布该申请视为撤回（considered withdrawn）。"
  },
  {
    "id": "pct_007",
    "category": "PCT",
    "question": "PCT申请的国际申请号格式是？",
    "options": ["WO/2024/123456", "PCT/CN2024/123456", "IB/2024/CN/123456", "US2024/PCT/123456"],
    "answer": 1,
    "explanation": "国际申请号格式为 PCT/[受理局代码][年份]/[序号]，例如PCT/CN2024/098765。WO开头的是国际公开号，两者不同。"
  },
  # ── US（美国）──────────────────────────────────────────────
  {
    "id": "us_001",
    "category": "US",
    "question": "美国专利审查机构的英文缩写是？",
    "options": ["USPTO", "USGOV", "USIP", "USOIP"],
    "answer": 0,
    "explanation": "USPTO即United States Patent and Trademark Office（美国专利商标局），负责审查和授予美国专利和商标。"
  },
  {
    "id": "us_002",
    "category": "US",
    "question": "美国发明专利（Utility Patent）的保护期限是自申请日起多少年？",
    "options": ["14年", "17年", "20年", "25年"],
    "answer": 2,
    "explanation": "美国发明专利保护期为申请日起20年，与大多数PCT成员国一致。设计专利为15年，植物专利为20年。"
  },
  {
    "id": "us_003",
    "category": "US",
    "question": "美国AIA（America Invents Act）实施后，美国专利制度采用的是？",
    "options": ["先发明制（FTI）", "先申请制（FTF）", "混合制", "注册制"],
    "answer": 1,
    "explanation": "2013年3月16日起，美国AIA将专利制度从传统的先发明制（First to Invent）改为先申请制（First to File），与全球大多数国家接轨。"
  },
  {
    "id": "us_004",
    "category": "US",
    "question": "美国专利申请中，\"Office Action\"指的是？",
    "options": ["专利授权通知", "审查员的审查意见/驳回通知", "缴费通知", "公开通知"],
    "answer": 1,
    "explanation": "Office Action是USPTO审查员在审查过程中发出的官方审查意见，通常包含驳回理由或要求修改的意见，申请人需在期限内答复。"
  },
  {
    "id": "us_005",
    "category": "US",
    "question": "通过PCT进入美国国家阶段时，通常需要在优先权日起多少个月内完成？",
    "options": ["20个月", "25个月", "30个月", "35个月"],
    "answer": 2,
    "explanation": "美国作为PCT指定国，进入国家阶段的期限为优先权日起30个月，与PCT标准一致。"
  },
  # ── EP（欧洲）──────────────────────────────────────────────
  {
    "id": "ep_001",
    "category": "EP",
    "question": "欧洲专利局的英文缩写是？",
    "options": ["EUIP", "EPA", "EPO", "EUPO"],
    "answer": 2,
    "explanation": "EPO即European Patent Office（欧洲专利局），负责受理和审查欧洲专利申请。注意EUIPO是欧盟知识产权局，主要负责商标和外观设计。"
  },
  {
    "id": "ep_002",
    "category": "EP",
    "question": "欧洲专利授权后，需要在各成员国进行什么操作才能在该国生效？",
    "options": ["重新申请", "提交翻译并缴纳国家费用（Validation）", "通知欧洲专利局", "无需任何操作"],
    "answer": 1,
    "explanation": "EPO授权的欧洲专利需要在每个希望保护的成员国进行\"Validation\"（确认/生效），通常需要提交译文并缴纳国家维持费。未在规定期限内确认的国家将失去保护。"
  },
  {
    "id": "ep_003",
    "category": "EP",
    "question": "欧洲专利申请中，\"examining division\"指的是？",
    "options": ["申请受理部门", "实质审查部门", "异议审查部门", "上诉委员会"],
    "answer": 1,
    "explanation": "Examining Division（审查部）是EPO负责对欧洲专利申请进行实质审查的部门，判断申请是否满足新颖性、创造性等授权条件。"
  },
  # ── 常用国家/地区 ─────────────────────────────────────────
  {
    "id": "int_001",
    "category": "国际通用",
    "question": "\"prior art\"在知识产权语境中指的是？",
    "options": ["已授权的专利", "现有技术（申请日前公开的一切技术）", "优先权文件", "申请人的早期作品"],
    "answer": 1,
    "explanation": "Prior art（现有技术）是指在专利申请日（或优先权日）之前已经公开的全部技术知识，是判断专利新颖性和创造性的基准。"
  },
  {
    "id": "int_002",
    "category": "国际通用",
    "question": "\"priority claim\"（优先权主张）允许申请人享有什么好处？",
    "options": [
      "免缴申请费",
      "以最早申请日作为后续申请的有效申请日",
      "延长专利保护期",
      "跳过审查程序"
    ],
    "answer": 1,
    "explanation": "基于巴黎公约，申请人在一个成员国提出申请后，可在12个月内（专利/实用新型）向其他成员国主张优先权，以最早申请日作为后续申请的评判基准日。"
  },
  {
    "id": "int_003",
    "category": "国际通用",
    "question": "商标的马德里体系（Madrid System）主要由哪个机构管理？",
    "options": ["WTO", "WIPO", "EPO", "INTA"],
    "answer": 1,
    "explanation": "WIPO（世界知识产权组织）管理马德里体系，允许商标申请人通过一次申请、一种语言、一种货币，向多个成员国/地区寻求商标保护。"
  },
  {
    "id": "int_004",
    "category": "国际通用",
    "question": "\"non-disclosure agreement\"（保密协议）在知产流程中主要用于？",
    "options": ["申请专利前公开技术", "防止在提交申请前技术内容被公开泄露", "替代专利申请", "申请商标注册"],
    "answer": 1,
    "explanation": "NDA（保密协议）用于保护在合作洽谈、技术转让等场景中需要披露但尚未申请专利的技术内容，防止其成为影响新颖性的公开现有技术。"
  },
  {
    "id": "int_005",
    "category": "国际通用",
    "question": "\"designated Office\"（指定局）在PCT体系中指的是？",
    "options": [
      "发出通知的受理局",
      "申请人希望获得专利保护的国家/地区的专利局",
      "进行国际检索的机构",
      "WIPO国际局"
    ],
    "answer": 1,
    "explanation": "指定局（DO, Designated Office）是申请人在PCT申请中指定的、希望在该国获得专利保护的国家专利局。申请人需在30个月内向各指定局进入国家阶段。"
  }
]
