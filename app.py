# HERBY V0.8 - MINDSET ENGINE
# Streamlit application - full file for copy/paste

import streamlit as st

st.set_page_config(
    page_title="Herby V0.8",
    page_icon="❤️",
    layout="centered",
)


# ============================================================
# MASTER DATA
# ============================================================

ASSET_GROUPS = {
    "safety": {"เงินฝาก", "พันธบัตร", "ตราสารหนี้"},
    "balanced": {"กองทุนรวม", "RMF / SSF", "REIT", "ทองคำ"},
    "growth": {"ETF", "หุ้นไทย", "หุ้นต่างประเทศ"},
    "speculative": {"Bitcoin", "Cryptocurrency"},
    "uncertain": {"ยังไม่แน่ใจ"},
}

ASSET_OPTIONS = [
    "เงินฝาก",
    "พันธบัตร",
    "ตราสารหนี้",
    "กองทุนรวม",
    "RMF / SSF",
    "REIT",
    "ทองคำ",
    "ETF",
    "หุ้นไทย",
    "หุ้นต่างประเทศ",
    "Bitcoin",
    "Cryptocurrency",
    "ยังไม่แน่ใจ",
]

AGE_OPTIONS = [
    "18-24 ปี",
    "25-34 ปี",
    "35-44 ปี",
    "45-54 ปี",
    "55 ปีขึ้นไป",
]

GOAL_OPTIONS = [
    "เกษียณ",
    "อิสรภาพทางการเงิน",
    "สร้างความมั่งคั่งระยะยาว",
    "ซื้อบ้าน",
    "การศึกษาบุตร",
    "อื่น ๆ",
]

TIMELINE_OPTIONS = [
    "น้อยกว่า 3 ปี",
    "3-5 ปี",
    "5-10 ปี",
    "10-20 ปี",
    "มากกว่า 20 ปี",
]

EXPERIENCE_OPTIONS = [
    "ยังไม่เคยลงทุน",
    "น้อยกว่า 1 ปี",
    "1-3 ปี",
    "3-10 ปี",
    "มากกว่า 10 ปี",
]

FEELING_OPTIONS = [
    "กังวลมากและอยากขายออกทันที",
    "กังวล แต่คงขายบางส่วน",
    "ไม่สบายใจ แต่ยังถือไว้ได้",
    "มองว่าเป็นเรื่องปกติของการลงทุน",
    "มองว่าอาจเป็นโอกาสในการซื้อเพิ่ม",
]


# ============================================================
# SESSION STATE
# ============================================================

def initialize_session_state():
    defaults = {
        "started": False,
        "show_results": False,
        "confirmed": False,
        "analysis_result": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def clear_results():
    st.session_state.show_results = False
    st.session_state.confirmed = False
    st.session_state.analysis_result = None


# ============================================================
# NORMALIZATION AND CLASSIFICATION
# ============================================================

def classify_assets(selected_assets):
    selected = set(selected_assets)
    groups = {
        group: sorted(selected.intersection(items))
        for group, items in ASSET_GROUPS.items()
    }

    active_groups = [
        group for group in ["safety", "balanced", "growth", "speculative"]
        if groups[group]
    ]

    if not selected or selected == {"ยังไม่แน่ใจ"}:
        dominant_group = "uncertain"
    elif len(active_groups) == 1:
        dominant_group = active_groups[0]
    elif len(active_groups) >= 2:
        dominant_group = "mixed"
    else:
        dominant_group = "uncertain"

    return {
        "selected": sorted(selected),
        "groups": groups,
        "active_groups": active_groups,
        "dominant_group": dominant_group,
        "has_safety": bool(groups["safety"]),
        "has_balanced": bool(groups["balanced"]),
        "has_growth": bool(groups["growth"]),
        "has_speculative": bool(groups["speculative"]),
        "has_uncertain": bool(groups["uncertain"]),
        "only_safety": active_groups == ["safety"],
        "only_high_variation": bool(active_groups) and all(
            group in {"growth", "speculative"} for group in active_groups
        ),
    }


def evaluate_growth_desire(goal, timeline):
    high_growth_goals = {
        "อิสรภาพทางการเงิน",
        "สร้างความมั่งคั่งระยะยาว",
    }

    if goal in high_growth_goals:
        level = "high"
    elif goal in {"เกษียณ", "การศึกษาบุตร"}:
        level = "medium"
    else:
        level = "medium"

    if timeline in {"น้อยกว่า 3 ปี", "3-5 ปี"}:
        time_constraint = "short"
    elif timeline == "5-10 ปี":
        time_constraint = "medium"
    else:
        time_constraint = "long"

    return {
        "level": level,
        "time_constraint": time_constraint,
    }


def evaluate_risk_tolerance(volatility):
    if volatility <= 3:
        return "low"
    if volatility <= 6:
        return "medium"
    return "high"


def evaluate_stress_behavior(feeling):
    mapping = {
        "กังวลมากและอยากขายออกทันที": "escape",
        "กังวล แต่คงขายบางส่วน": "reduce",
        "ไม่สบายใจ แต่ยังถือไว้ได้": "endure",
        "มองว่าเป็นเรื่องปกติของการลงทุน": "accept",
        "มองว่าอาจเป็นโอกาสในการซื้อเพิ่ม": "actively_add",
    }
    return mapping[feeling]


def evaluate_learning_stage(experience):
    if experience in {"ยังไม่เคยลงทุน", "น้อยกว่า 1 ปี"}:
        return "emerging"
    if experience == "1-3 ปี":
        return "developing"
    if experience == "3-10 ปี":
        return "experienced"
    return "seasoned"


def evaluate_safety_need(timeline, risk_tolerance, stress_behavior, asset_profile):
    signals = 0

    if asset_profile["only_safety"]:
        signals += 2
    elif asset_profile["has_safety"]:
        signals += 1

    if timeline in {"น้อยกว่า 3 ปี", "3-5 ปี"}:
        signals += 1

    if risk_tolerance == "low":
        signals += 1

    if stress_behavior in {"escape", "reduce"}:
        signals += 1

    if signals >= 3:
        return "high"
    if signals >= 1:
        return "medium"
    return "low"


# ============================================================
# RELATIONSHIP ENGINE
# ============================================================

def add_relationship(relationships, code, observation, interpretation, priority=1):
    if any(item["code"] == code for item in relationships):
        return
    relationships.append(
        {
            "code": code,
            "observation": observation,
            "interpretation": interpretation,
            "priority": priority,
        }
    )


def detect_mindset_relationships(answers, mindsets, asset_profile):
    relationships = []
    growth = mindsets["growth_desire"]["level"]
    time_constraint = mindsets["growth_desire"]["time_constraint"]
    safety = mindsets["safety_need"]
    risk = mindsets["risk_tolerance"]
    behavior = mindsets["stress_behavior"]
    learning = mindsets["learning_stage"]

    if growth == "high" and safety == "high":
        add_relationship(
            relationships,
            "growth_safety_tension",
            "เป้าหมายของคุณต้องการการเติบโต แต่คำตอบหลายส่วนสะท้อนว่าคุณให้ความสำคัญกับความมั่นคงสูง",
            "คุณอาจกำลังอยู่ระหว่างความต้องการให้เงินเติบโตกับความสบายใจจากการรักษาเงินต้น",
            3,
        )

    if risk == "low" and behavior in {"accept", "actively_add"}:
        add_relationship(
            relationships,
            "risk_behavior_tension_low_active",
            f"คุณระบุว่ารับความผันผวนได้ {answers['volatility']} จาก 10 แต่คาดว่าจะรับมือเชิงรุกเมื่อมูลค่าลดลง 30%",
            "คุณอาจเข้าใจแนวคิดการถือผ่านความผันผวนหรือ Buy the Dip แต่ยังไม่แน่ใจว่าความรู้สึกในสถานการณ์จริงจะตรงกับสิ่งที่คาดไว้หรือไม่",
            3,
        )

    if risk == "high" and behavior in {"escape", "reduce"}:
        add_relationship(
            relationships,
            "risk_behavior_tension_high_defensive",
            f"คุณระบุว่ารับความผันผวนได้ {answers['volatility']} จาก 10 แต่คาดว่าจะลดความเสี่ยงอย่างรวดเร็วเมื่อมูลค่าลดลง 30%",
            "ความเสี่ยงที่คุณเชื่อว่ารับได้กับพฤติกรรมภายใต้แรงกดดันอาจยังไม่ตรงกัน",
            3,
        )

    if asset_profile["only_safety"] and behavior == "actively_add":
        add_relationship(
            relationships,
            "safety_asset_active_add_tension",
            "คุณเลือกสินทรัพย์ที่เน้นความมั่นคง แต่ตอบว่าจะซื้อเพิ่มเมื่อมูลค่าการลงทุนลดลงมาก",
            "คุณอาจชอบแนวคิดซื้อเมื่อราคาลดลง แต่เหตุการณ์ลดลง 30% อาจไม่ได้เกิดกับเงินฝากหรือพันธบัตรในลักษณะเดียวกับหุ้นและสินทรัพย์ดิจิทัล",
            3,
        )

    if asset_profile["only_high_variation"] and behavior == "escape":
        add_relationship(
            relationships,
            "high_variation_asset_escape_tension",
            "คุณสนใจสินทรัพย์ที่อาจผันผวนสูง แต่ตอบว่าจะขายออกทันทีเมื่อมูลค่าลดลงมาก",
            "ความสนใจในโอกาสผลตอบแทนอาจนำหน้าความพร้อมรับช่วงขาดทุน",
            3,
        )

    if learning == "emerging" and asset_profile["has_speculative"]:
        if behavior in {"escape", "reduce"} or risk == "low":
            interpretation = (
                "คุณเปิดรับโอกาสจากสินทรัพย์ผันผวนสูง แต่ประสบการณ์และความพร้อมรับการขาดทุนยังมีจำกัด "
                "ความสนใจในผลตอบแทนอาจนำหน้าความพร้อมรับความเสี่ยงเล็กน้อย"
            )
        else:
            interpretation = (
                "คุณเปิดรับสินทรัพย์รูปแบบใหม่และเชื่อว่าตัวเองรับความผันผวนได้ "
                "แต่คำตอบยังสะท้อนความตั้งใจมากกว่าพฤติกรรมที่ผ่านการทดสอบในตลาดจริง"
            )
        add_relationship(
            relationships,
            "emerging_speculative",
            "คุณยังมีประสบการณ์ลงทุนไม่มาก และสนใจ Bitcoin หรือ Cryptocurrency ซึ่งอาจมีความผันผวนสูง",
            interpretation,
            2,
        )

    growth_sensitive_goal = answers["goal"] in {
        "อิสรภาพทางการเงิน",
        "สร้างความมั่งคั่งระยะยาว",
    }
    if growth_sensitive_goal and time_constraint == "short":
        add_relationship(
            relationships,
            "short_timeline_growth_goal",
            "เป้าหมายของคุณต้องการการเติบโต แต่ระยะเวลาที่คาดว่าจะใช้เงินค่อนข้างสั้น",
            "เวลารอให้สินทรัพย์ฟื้นตัวมีจำกัด ทำให้ความพร้อมใช้เงินอาจสำคัญกว่าการเร่งผลตอบแทน",
            3,
        )

    if answers["goal"] == "เกษียณ" and answers["timeline"] in {"น้อยกว่า 3 ปี", "3-5 ปี"}:
        add_relationship(
            relationships,
            "retirement_near_term",
            "คุณระบุเป้าหมายเกษียณและคาดว่าจะเริ่มใช้เงินในช่วงไม่เกิน 5 ปี",
            "เวลารอการฟื้นตัวของสินทรัพย์มีจำกัดกว่าการลงทุนระยะยาวทั่วไป ดังนั้นความพร้อมใช้เงินอาจมีน้ำหนักมากขึ้น",
            2,
        )

    if asset_profile["has_uncertain"]:
        add_relationship(
            relationships,
            "uncertain_asset_preference",
            "คุณเลือกว่ายังไม่แน่ใจเกี่ยวกับสินทรัพย์ที่สนใจ",
            "คุณอาจอยู่ในช่วงสำรวจทางเลือก หรือยังไม่แน่ใจว่าระดับความเสี่ยงแบบใดเหมาะกับตัวเอง",
            1,
        )

    if not answers["assets"]:
        add_relationship(
            relationships,
            "no_asset_preference",
            "คุณยังไม่ได้เลือกสินทรัพย์ที่สนใจ",
            "ความสนใจด้านสินทรัพย์ยังไม่ชัด จึงควรอ่านผลลัพธ์นี้เป็นภาพเบื้องต้น",
            1,
        )

    # Alignment is added only when no major tension has been found.
    major_tensions = [item for item in relationships if item["priority"] >= 3]
    aligned_behavior = (
        risk == "low" and behavior in {"escape", "reduce"}
    ) or (
        risk == "medium" and behavior in {"reduce", "endure", "accept"}
    ) or (
        risk == "high" and behavior in {"endure", "accept", "actively_add"}
    )

    if not major_tensions and aligned_behavior:
        add_relationship(
            relationships,
            "risk_behavior_alignment",
            "ระดับความผันผวนที่คุณคิดว่ารับได้ไปในทิศทางเดียวกับวิธีที่คุณคาดว่าจะตอบสนองเมื่อมูลค่าลดลง",
            "คำตอบด้านความรู้สึกและการรับความผันผวนสนับสนุนกัน",
            1,
        )

    if (
        not major_tensions
        and time_constraint == "long"
        and asset_profile["has_growth"]
        and risk in {"medium", "high"}
        and behavior in {"endure", "accept", "actively_add"}
    ):
        add_relationship(
            relationships,
            "long_term_growth_alignment",
            "เป้าหมาย ระยะเวลา สินทรัพย์ที่สนใจ และวิธีรับมือความผันผวนของคุณไปในทิศทางเดียวกัน",
            "คุณมีองค์ประกอบหลายด้านที่สนับสนุนการเติบโตระยะยาว",
            1,
        )

    return sorted(relationships, key=lambda item: item["priority"], reverse=True)


# ============================================================
# HUMAN INTERPRETATION AND STYLE
# ============================================================

def build_human_interpretation(answers, mindsets, asset_profile, relationships):
    codes = {item["code"] for item in relationships}
    paragraphs = []

    if "growth_safety_tension" in codes:
        paragraphs.append(
            "Herby มองว่าคุณต้องการให้เงินเติบโตเพื่อไปถึงเป้าหมาย "
            "แต่ในเวลาเดียวกันคุณให้ความสำคัญกับความปลอดภัยและการรักษาเงินต้นค่อนข้างมาก"
        )
    elif asset_profile["only_safety"]:
        paragraphs.append(
            "Herby สังเกตว่าคุณให้ความสำคัญกับความมั่นคงเป็นหลัก "
            "จากสินทรัพย์ที่สนใจและคำตอบเกี่ยวกับระดับความผันผวน"
        )
    elif asset_profile["has_growth"] or asset_profile["has_speculative"]:
        paragraphs.append(
            "Herby มองว่าคุณเปิดรับโอกาสให้เงินเติบโต และสนใจสินทรัพย์ที่อาจมีความผันผวน"
        )
    else:
        paragraphs.append(
            "Herby เริ่มเห็นว่าคุณกำลังสำรวจความสัมพันธ์ระหว่างเป้าหมาย ความมั่นคง และโอกาสเติบโต"
        )

    if "risk_behavior_tension_low_active" in codes:
        paragraphs.append(
            "อย่างไรก็ตาม คุณระบุว่ารับความผันผวนได้น้อย แต่กลับมองการลดลง 30% ว่าอาจเป็นโอกาสซื้อเพิ่ม "
            "คำตอบนี้อาจสะท้อนว่าคุณเข้าใจแนวคิด Buy the Dip หรือเชื่อในการฟื้นตัวระยะยาว "
            "แต่ยังไม่แน่ใจว่าความรู้สึกจริงเมื่อเห็นมูลค่าลดลงจะตรงกับสิ่งที่คาดไว้หรือไม่"
        )
    elif "risk_behavior_tension_high_defensive" in codes:
        paragraphs.append(
            "อย่างไรก็ตาม ระดับความเสี่ยงที่คุณคิดว่ารับได้กับพฤติกรรมที่คาดว่าจะเกิดขึ้นเมื่อขาดทุนยังไปคนละทาง "
            "คุณอาจรับแนวคิดเรื่องความผันผวนได้ แต่ยังต้องการทางออกเมื่อเผชิญแรงกดดันจริง"
        )

    if "safety_asset_active_add_tension" in codes:
        paragraphs.append(
            "นอกจากนี้ แนวคิดซื้อเพิ่มเมื่อมูลค่าลดลงมากมักเกี่ยวข้องกับสินทรัพย์ที่มีราคาเคลื่อนไหวชัดเจน "
            "จึงอาจไม่ตรงกับธรรมชาติของเงินฝากหรือพันธบัตรที่คุณสนใจทั้งหมด"
        )

    if "high_variation_asset_escape_tension" in codes:
        paragraphs.append(
            "ความสนใจในสินทรัพย์ผันผวนสูงจึงอาจนำหน้าความพร้อมรับช่วงขาดทุน "
            "ซึ่งเป็นจุดสำคัญที่ควรทำความเข้าใจก่อนตัดสินใจลงทุนจริง"
        )

    if "emerging_speculative" in codes:
        paragraphs.append(
            "เนื่องจากประสบการณ์ลงทุนของคุณยังมีไม่มาก คำตอบบางข้ออาจสะท้อนสิ่งที่คาดว่าจะทำ "
            "มากกว่าพฤติกรรมที่เคยผ่านการทดสอบในตลาดจริง"
        )

    if "short_timeline_growth_goal" in codes or "retirement_near_term" in codes:
        paragraphs.append(
            "ระยะเวลาที่คาดว่าจะใช้เงินยังทำให้ความสามารถรอการฟื้นตัวมีจำกัด "
            "ดังนั้นความพร้อมใช้เงินอาจมีความสำคัญพอ ๆ กับความต้องการผลตอบแทน"
        )

    if "long_term_growth_alignment" in codes:
        paragraphs.append(
            "คำตอบหลายส่วนสนับสนุนกัน ทั้งระยะเวลาที่ยาว ความสนใจในสินทรัพย์เติบโต "
            "และความพร้อมถือผ่านความผันผวน"
        )
    elif "risk_behavior_alignment" in codes and not any(
        item["priority"] >= 3 for item in relationships
    ):
        paragraphs.append(
            "วิธีที่คุณคาดว่าจะตอบสนองเมื่อมูลค่าลดลงสอดคล้องกับระดับความผันผวนที่คุณบอกว่ารับได้"
        )

    major_tensions = [item for item in relationships if item["priority"] >= 3]
    if len(major_tensions) >= 2:
        paragraphs.append(
            "เมื่อมองรวมกัน คุณอาจกำลังอยู่ระหว่างความต้องการหลายด้าน "
            "และยังค้นหาว่าความเสี่ยงระดับใดเหมาะกับตัวเองในสถานการณ์จริง"
        )
    elif not major_tensions:
        paragraphs.append(
            "ภาพรวมปัจจุบันจึงเริ่มมีทิศทางที่ชัดขึ้น แต่สไตล์นี้ยังเปลี่ยนแปลงได้เมื่อประสบการณ์และสถานการณ์ชีวิตเปลี่ยนไป"
        )

    if answers["age"] == "55 ปีขึ้นไป" and answers["timeline"] in {"น้อยกว่า 3 ปี", "3-5 ปี"}:
        paragraphs.append(
            "ช่วงอายุไม่ได้กำหนดว่าคุณควรรับความเสี่ยงเท่าใด แต่เมื่อพิจารณาร่วมกับระยะเวลาใช้เงินที่ค่อนข้างสั้น "
            "ความพร้อมของเงินและเวลารอการฟื้นตัวควรถูกนำมาคิดร่วมกัน"
        )

    return "\n\n".join(paragraphs)


def determine_current_style(mindsets, asset_profile, relationships):
    codes = {item["code"] for item in relationships}
    major_tensions = [item for item in relationships if item["priority"] >= 3]
    growth = mindsets["growth_desire"]["level"]
    safety = mindsets["safety_need"]
    risk = mindsets["risk_tolerance"]
    behavior = mindsets["stress_behavior"]
    learning = mindsets["learning_stage"]

    if len(major_tensions) >= 2 or (
        growth == "high" and safety == "high"
    ) or any(
        code in codes
        for code in {
            "risk_behavior_tension_low_active",
            "risk_behavior_tension_high_defensive",
        }
    ):
        return {
            "name": "🧭 ผู้กำลังค้นหาจุดสมดุล",
            "description": (
                "คุณมีความต้องการมากกว่าหนึ่งด้านที่ยังดึงไปคนละทาง "
                "และกำลังค้นหาว่าความเสี่ยงแบบใดสอดคล้องกับเป้าหมายและความสบายใจจริง"
            ),
        }

    if learning == "emerging" and (
        asset_profile["dominant_group"] == "uncertain" or not asset_profile["selected"]
    ):
        return {
            "name": "🌱 ผู้เริ่มสำรวจโลกการลงทุน",
            "description": (
                "คุณกำลังสร้างความเข้าใจพื้นฐานและค้นหาว่าสินทรัพย์ ระยะเวลา "
                "และความเสี่ยงแบบใดเหมาะกับตัวเอง"
            ),
        }

    if safety == "high" and risk == "low" and behavior in {"escape", "reduce", "endure"}:
        return {
            "name": "🛡️ ผู้รักษาความมั่นคง",
            "description": (
                "คุณให้ความสำคัญกับการรักษาเงินต้นและความแน่นอน "
                "มากกว่าการไล่ตามผลตอบแทนสูง"
            ),
        }

    if (
        mindsets["growth_desire"]["time_constraint"] == "long"
        and asset_profile["has_growth"]
        and risk in {"medium", "high"}
        and behavior in {"endure", "accept"}
    ):
        return {
            "name": "📈 ผู้สร้างการเติบโตอย่างมีวินัย",
            "description": (
                "คุณต้องการให้เงินเติบโตและพร้อมยอมรับความผันผวน "
                "ในระดับที่สอดคล้องกับเป้าหมายและระยะเวลาลงทุน"
            ),
        }

    if (
        growth == "high"
        and (asset_profile["has_growth"] or asset_profile["has_speculative"])
        and risk == "high"
        and behavior in {"accept", "actively_add"}
    ):
        return {
            "name": "🚀 ผู้เปิดรับโอกาส",
            "description": (
                "คุณเปิดรับโอกาสการเติบโตและพร้อมพิจารณาใช้ความผันผวนเป็นโอกาส "
                "โดยยังควรแยกโอกาสออกจากความเสี่ยงที่เกินความพร้อม"
            ),
        }

    return {
        "name": "⚖️ ผู้แสวงหาสมดุล",
        "description": (
            "คุณต้องการการเติบโตควบคู่กับการควบคุมความเสี่ยง "
            "และคำตอบส่วนใหญ่เริ่มไปในทิศทางเดียวกัน"
        ),
    }


def analyze_answers(answers):
    asset_profile = classify_assets(answers["assets"])
    growth_desire = evaluate_growth_desire(answers["goal"], answers["timeline"])
    risk_tolerance = evaluate_risk_tolerance(answers["volatility"])
    stress_behavior = evaluate_stress_behavior(answers["feeling"])
    learning_stage = evaluate_learning_stage(answers["experience"])
    safety_need = evaluate_safety_need(
        answers["timeline"],
        risk_tolerance,
        stress_behavior,
        asset_profile,
    )

    mindsets = {
        "growth_desire": growth_desire,
        "safety_need": safety_need,
        "risk_tolerance": risk_tolerance,
        "stress_behavior": stress_behavior,
        "learning_stage": learning_stage,
    }

    relationships = detect_mindset_relationships(
        answers,
        mindsets,
        asset_profile,
    )
    insight = build_human_interpretation(
        answers,
        mindsets,
        asset_profile,
        relationships,
    )
    style = determine_current_style(
        mindsets,
        asset_profile,
        relationships,
    )

    return {
        "answers": answers,
        "asset_profile": asset_profile,
        "mindsets": mindsets,
        "relationships": relationships,
        "observations": [item["observation"] for item in relationships],
        "insight": insight,
        "style": style,
    }


# ============================================================
# USER INTERFACE
# ============================================================

def render_welcome_screen():
    st.title("❤️ Herby")
    st.subheader("Your Digital Financial Mentor")
    st.markdown(
        """
### เราไม่ได้ช่วยคุณเลือกสินทรัพย์
### เราช่วยให้คุณเข้าใจตัวเองมากขึ้น
        """
    )

    if st.button("🚀 เริ่มต้นกับ Herby", type="primary", use_container_width=True):
        st.session_state.started = True
        st.rerun()


def render_questionnaire():
    st.title("👋 ยินดีต้อนรับ")

    with st.form("mindset_questionnaire"):
        name = st.text_input(
            "คุณอยากให้ Herby เรียกคุณว่าอะไร?",
            key="q_name",
        )

        if name.strip():
            st.success(f"สวัสดี {name.strip()} 👋 ยินดีต้อนรับสู่ Herby")

        age = st.selectbox(
            "คุณอยู่ในช่วงอายุใด?",
            AGE_OPTIONS,
            key="q_age",
        )

        goal = st.selectbox(
            "เป้าหมายหลักในการลงทุนของคุณคืออะไร?",
            GOAL_OPTIONS,
            key="q_goal",
        )

        timeline = st.selectbox(
            "คุณคาดว่าจะใช้เงินก้อนนี้เมื่อไร?",
            TIMELINE_OPTIONS,
            key="q_timeline",
        )

        experience = st.selectbox(
            "คุณมีประสบการณ์การลงทุนมากแค่ไหน?",
            EXPERIENCE_OPTIONS,
            key="q_experience",
        )

        assets = st.multiselect(
            "คุณสนใจสินทรัพย์ประเภทใดเป็นพิเศษ?",
            ASSET_OPTIONS,
            key="q_assets",
            help="เลือกได้มากกว่าหนึ่งประเภท หากยังไม่แน่ใจสามารถเลือก 'ยังไม่แน่ใจ' ได้",
        )

        feeling = st.radio(
            "คุณรู้สึกอย่างไร หากมูลค่าการลงทุนของคุณลดลง 30%?",
            FEELING_OPTIONS,
            key="q_feeling",
        )

        volatility = st.slider(
            "คุณยอมรับความผันผวนได้มากแค่ไหน?",
            min_value=1,
            max_value=10,
            value=5,
            key="q_volatility",
        )

        submitted = st.form_submit_button(
            "🔍 วิเคราะห์สไตล์การลงทุน",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        if not name.strip():
            st.error("กรุณาใส่ชื่อที่ต้องการให้ Herby เรียก")
            clear_results()
            return

        answers = {
            "name": name.strip(),
            "age": age,
            "goal": goal,
            "timeline": timeline,
            "experience": experience,
            "assets": assets,
            "feeling": feeling,
            "volatility": volatility,
        }

        st.session_state.analysis_result = analyze_answers(answers)
        st.session_state.show_results = True
        st.session_state.confirmed = False
        st.rerun()


def render_results(result):
    st.divider()
    st.caption(f"ผลสะท้อนสำหรับ {result['answers']['name']}")

    st.header("🔎 สิ่งที่ Herby สังเกตเห็น")
    observations = result["observations"]

    if observations:
        for observation in observations:
            st.warning(observation)
    else:
        st.info(
            "Herby ยังไม่พบแรงดึงสำคัญจากคำตอบชุดนี้ "
            "แต่ผลลัพธ์ยังเป็นเพียงภาพสะท้อนจากข้อมูลที่คุณให้"
        )

    st.header("🌟 What Herby Learned About You")
    st.info(result["insight"])

    st.header("📈 สไตล์การลงทุนปัจจุบันของคุณ")
    st.subheader(result["style"]["name"])
    st.write(result["style"]["description"])

    st.caption(
        "ผลลัพธ์นี้เป็นภาพสะท้อนปัจจุบัน ไม่ใช่คำแนะนำให้ซื้อหรือขายสินทรัพย์ "
        "และสไตล์การลงทุนสามารถเปลี่ยนแปลงได้ตามประสบการณ์และสถานการณ์ชีวิต"
    )

    st.header("❓ Herby เข้าใจคุณถูกไหม?")
    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "🔄 ฉันว่ายังไม่ใช่ กลับไปแก้ไขคำตอบ",
            use_container_width=True,
        ):
            st.session_state.show_results = False
            st.session_state.confirmed = False
            st.rerun()

    with col2:
        if st.button(
            "✅ ฉันคิดว่าใช่ ไปขั้นตอนต่อไปกันเลย",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.confirmed = True
            st.rerun()

    if st.session_state.confirmed:
        st.success(
            "Herby เริ่มเข้าใจสไตล์การลงทุนปัจจุบันของคุณแล้ว\n\n"
            "การยืนยันนี้ไม่ได้ล็อกสไตล์ของคุณ เพราะมุมมองและพฤติกรรมการลงทุน "
            "สามารถเปลี่ยนแปลงได้ตามประสบการณ์และสถานการณ์ชีวิต"
        )


def main():
    initialize_session_state()

    if not st.session_state.started:
        render_welcome_screen()
        return

    render_questionnaire()

    if st.session_state.show_results and st.session_state.analysis_result:
        render_results(st.session_state.analysis_result)


if __name__ == "__main__":
    main()
