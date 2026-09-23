# Create V1.0 Guide Me development baseline
# V1.0 Sprint 1 - Guide Me foundation

import streamlit as st
import pandas as pd
import json
import os
import hashlib
import requests
from datetime import datetime

st.set_page_config(
    page_title="Herby Your Digital Financial Mentor",
    page_icon="💚",
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
    "ขายออกทั้งหมดทันที",
    "ขายบางส่วนเพื่อลดความเสี่ยง",
    "ยังถือไว้ แม้จะไม่สบายใจ",
    "ถือไว้ เพราะมองว่าเป็นเรื่องปกติของการลงทุน",
    "ซื้อเพิ่ม เพราะมองว่าเป็นโอกาส",
]

GUIDE_ME_ASSET_PROFILES = {
    "เงินฝาก": {
        "icon": "💰",
        "risk_level": 1,
        "growth_level": 1,
        "minimum_timeline": 1,
        "experience_level": 1,
        "portfolio_role": "เงินสำรองและความมั่นคง",
        "strengths": [
            "มูลค่ามีความผันผวนต่ำ",
            "เข้าถึงเงินได้ง่าย",
            "เหมาะสำหรับเงินสำรองหรือเป้าหมายระยะสั้น",
        ],
        "weaknesses": [
            "โอกาสเติบโตในระยะยาวค่อนข้างจำกัด",
            "ผลตอบแทนอาจไม่ชนะเงินเฟ้อ",
        ],
        "general_cautions": [
            "ควรตรวจสอบอัตราดอกเบี้ยและเงื่อนไขการถอน",
            "ไม่ควรใช้เป็นสินทรัพย์หลักเพียงอย่างเดียวสำหรับเป้าหมายเติบโตระยะยาว",
        ],
    },
    "พันธบัตร / ตราสารหนี้": {
        "icon": "🛡️",
        "risk_level": 2,
        "growth_level": 2,
        "minimum_timeline": 2,
        "experience_level": 1,
        "portfolio_role": "ลดความผันผวนและสร้างความมั่นคง",
        "strengths": [
            "โดยทั่วไปมีความผันผวนต่ำกว่าหุ้น",
            "อาจช่วยลดความผันผวนของพอร์ตโดยรวม",
            "สามารถสร้างรายได้จากดอกเบี้ย",
        ],
        "weaknesses": [
            "ราคายังเปลี่ยนแปลงได้เมื่ออัตราดอกเบี้ยเปลี่ยน",
            "ผลตอบแทนระยะยาวอาจต่ำกว่าสินทรัพย์เติบโต",
        ],
        "general_cautions": [
            "ตราสารหนี้แต่ละประเภทมีความเสี่ยงเครดิตต่างกัน",
            "กองทุนตราสารหนี้ไม่ใช่เงินฝากและอาจขาดทุนได้",
        ],
    },
    "กองทุนผสม": {
        "icon": "⚖️",
        "risk_level": 3,
        "growth_level": 3,
        "minimum_timeline": 2,
        "experience_level": 1,
        "portfolio_role": "สร้างสมดุลระหว่างการเติบโตและความมั่นคง",
        "strengths": [
            "กระจายการลงทุนหลายประเภทในผลิตภัณฑ์เดียว",
            "เหมาะกับผู้ใช้ที่ต้องการความสมดุล",
            "ไม่ต้องเลือกสินทรัพย์ทุกส่วนด้วยตนเอง",
        ],
        "weaknesses": [
            "สัดส่วนสินทรัพย์อาจไม่ตรงกับความต้องการทั้งหมด",
            "อาจมีค่าธรรมเนียมการบริหาร",
        ],
        "general_cautions": [
            "ควรตรวจสอบนโยบายลงทุนและสัดส่วนสินทรัพย์",
            "ชื่อกองทุนเพียงอย่างเดียวไม่ได้บอกระดับความเสี่ยงทั้งหมด",
        ],
    },
    "REIT": {
        "icon": "🏢",
        "risk_level": 3,
        "growth_level": 3,
        "minimum_timeline": 3,
        "experience_level": 2,
        "portfolio_role": "รายได้และการกระจายสินทรัพย์",
        "strengths": [
            "มีโอกาสสร้างกระแสเงินสดจากอสังหาริมทรัพย์",
            "ช่วยกระจายพอร์ตจากหุ้นทั่วไป",
            "ซื้อขายง่ายกว่าการถืออสังหาริมทรัพย์โดยตรง",
        ],
        "weaknesses": [
            "อ่อนไหวต่ออัตราดอกเบี้ยและภาวะเศรษฐกิจ",
            "รายได้และเงินจ่ายอาจลดลงได้",
        ],
        "general_cautions": [
            "ควรตรวจสอบคุณภาพสินทรัพย์ ผู้เช่า และระดับหนี้",
            "อัตราผลตอบแทนสูงอาจมาพร้อมความเสี่ยงที่สูงขึ้น",
        ],
    },
    "ทองคำ": {
        "icon": "🪙",
        "risk_level": 3,
        "growth_level": 2,
        "minimum_timeline": 2,
        "experience_level": 1,
        "portfolio_role": "กระจายความเสี่ยงและรักษามูลค่า",
        "strengths": [
            "อาจช่วยกระจายความเสี่ยงในช่วงตลาดไม่แน่นอน",
            "มีบทบาทเป็นสินทรัพย์รักษามูลค่าในบางช่วงเวลา",
        ],
        "weaknesses": [
            "ไม่สร้างกำไรหรือกระแสเงินสดจากธุรกิจ",
            "ราคาอาจเคลื่อนไหวเป็นเวลานานโดยไม่สร้างผลตอบแทน",
        ],
        "general_cautions": [
            "ไม่ควรประเมินว่าทองคำไม่มีความผันผวน",
            "ผลตอบแทนขึ้นอยู่กับราคาและช่องทางการถือครอง",
        ],
    },
    "ETF หุ้น": {
        "icon": "📊",
        "risk_level": 4,
        "growth_level": 4,
        "minimum_timeline": 3,
        "experience_level": 1,
        "portfolio_role": "พอร์ตหลักเพื่อการเติบโตและการกระจาย",
        "strengths": [
            "กระจายความเสี่ยงได้มากกว่าการถือหุ้นเพียงตัวเดียว",
            "เข้าถึงตลาดหรือกลุ่มอุตสาหกรรมได้ง่าย",
            "เหมาะสำหรับการลงทุนระยะยาว",
        ],
        "weaknesses": [
            "ยังขาดทุนได้เมื่อตลาดลดลง",
            "ETF เฉพาะกลุ่มอาจกระจุกตัวและผันผวนสูง",
        ],
        "general_cautions": [
            "ควรตรวจสอบดัชนีอ้างอิง ค่าธรรมเนียม และการกระจุกตัว",
            "ETF ไม่ได้หมายความว่ามีความเสี่ยงต่ำเสมอไป",
        ],
    },
    "หุ้นไทย": {
        "icon": "📈",
        "risk_level": 4,
        "growth_level": 4,
        "minimum_timeline": 3,
        "experience_level": 2,
        "portfolio_role": "การเติบโตและการลงทุนในธุรกิจรายตัว",
        "strengths": [
            "มีโอกาสได้รับประโยชน์จากการเติบโตของธุรกิจ",
            "สามารถเลือกบริษัทตามคุณภาพและมูลค่าได้",
            "ติดตามข้อมูลในประเทศได้สะดวก",
        ],
        "weaknesses": [
            "หุ้นรายตัวอาจมีความผันผวนสูง",
            "มีความเสี่ยงจากการเลือกบริษัทผิดหรือกระจุกตัว",
        ],
        "general_cautions": [
            "ควรตรวจสอบกำไร หนี้ กระแสเงินสด และราคาที่จ่าย",
            "ควรกระจายความเสี่ยงและไม่พึ่งหุ้นตัวเดียวมากเกินไป",
        ],
    },
    "หุ้นต่างประเทศ": {
        "icon": "🌍",
        "risk_level": 4,
        "growth_level": 5,
        "minimum_timeline": 4,
        "experience_level": 2,
        "portfolio_role": "การเติบโตระยะยาวและการกระจายสู่ตลาดโลก",
        "strengths": [
            "เข้าถึงบริษัทและอุตสาหกรรมระดับโลก",
            "มีโอกาสเติบโตสูงในระยะยาว",
            "ช่วยกระจายออกจากเศรษฐกิจประเทศเดียว",
        ],
        "weaknesses": [
            "มีความเสี่ยงจากราคาและอัตราแลกเปลี่ยน",
            "หุ้นเติบโตบางกลุ่มอาจมีมูลค่าสูงและผันผวนมาก",
        ],
        "general_cautions": [
            "ควรตรวจสอบคุณภาพธุรกิจ หนี้ การเติบโต และมูลค่า",
            "ผู้ใช้ต้องพร้อมรับช่วงขาดทุนและเวลาฟื้นตัว",
        ],
    },
    "Bitcoin": {
        "icon": "₿",
        "risk_level": 5,
        "growth_level": 5,
        "minimum_timeline": 4,
        "experience_level": 3,
        "portfolio_role": "สินทรัพย์ทางเลือกหรือส่วนเสริมที่มีความเสี่ยงสูง",
        "strengths": [
            "มีโอกาสเติบโตสูงภายใต้ความต้องการและการยอมรับที่เพิ่มขึ้น",
            "มีลักษณะแตกต่างจากสินทรัพย์การเงินแบบดั้งเดิม",
        ],
        "weaknesses": [
            "ราคาอาจลดลงรุนแรงในช่วงเวลาสั้น",
            "ไม่มีรายได้หรือกระแสเงินสดจากธุรกิจรองรับ",
            "มีความเสี่ยงด้านกฎระเบียบ การเก็บรักษา และแพลตฟอร์ม",
        ],
        "general_cautions": [
            "ควรจำกัดสัดส่วนตามความสามารถรับความเสียหาย",
            "ไม่ควรใช้เงินฉุกเฉินหรือเงินที่ต้องใช้ในระยะสั้น",
            "การเคยซื้อเพิ่มเมื่อตลาดลดไม่ได้รับประกันว่าจะรับการขาดทุนจริงได้",
        ],
    },
}

STYLE_ASSET_MAPPING = {

    "🛡️ ผู้รักษาความมั่นคง": [
        "เงินฝาก",
        "พันธบัตร / ตราสารหนี้",
        "ทองคำ",
        "กองทุนผสม",
    ],

    "⚖️ ผู้แสวงหาสมดุล": [
        "กองทุนผสม",
        "ETF หุ้น",
        "REIT",
        "ทองคำ",
    ],

    "📈 ผู้สร้างการเติบโตอย่างมีวินัย": [
        "ETF หุ้น",
        "หุ้นต่างประเทศ",
        "หุ้นไทย",
        "REIT",
    ],

    "🚀 ผู้เปิดรับโอกาส": [
        "ETF หุ้น",
        "หุ้นต่างประเทศ",
        "Bitcoin",
        "หุ้นไทย",
    ],

    "🧭 ผู้กำลังค้นหาจุดสมดุล": [
        "ETF หุ้น",
        "กองทุนผสม",
        "หุ้นต่างประเทศ",
        "ทองคำ",
    ],

    "🌱 ผู้เริ่มสำรวจโลกการลงทุน": [
        "กองทุนผสม",
        "ETF หุ้น",
        "เงินฝาก",
        "ทองคำ",
    ],
}


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
        "ขายออกทั้งหมดทันที": "escape",
        "ขายบางส่วนเพื่อลดความเสี่ยง": "reduce",
        "ยังถือไว้ แม้จะไม่สบายใจ": "endure",
        "ถือไว้ เพราะมองว่าเป็นเรื่องปกติของการลงทุน": "accept",
        "ซื้อเพิ่ม เพราะมองว่าเป็นโอกาส": "actively_add",
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
            f"คุณระบุว่ารับความผันผวนได้ {answers['volatility']} จาก 10 แต่คาดว่าจะรับมือเชิงรุกเมื่อเงินลงทุน 1,000,000 บาท เหลือ 700,000 บาท",
            "คุณอาจเข้าใจแนวคิดการถือผ่านความผันผวนหรือ Buy the Dip แต่ยังไม่แน่ใจว่าความรู้สึกในสถานการณ์จริงจะตรงกับสิ่งที่คาดไว้หรือไม่",
            3,
        )

    if risk == "high" and behavior in {"escape", "reduce"}:
        add_relationship(
            relationships,
            "risk_behavior_tension_high_defensive",
            f"คุณระบุว่ารับความผันผวนได้ {answers['volatility']} จาก 10 แต่คาดว่าจะลดความเสี่ยงอย่างรวดเร็วเมื่อเงินลงทุน 1,000,000 บาท เหลือ 700,000 บาท",
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
            "อย่างไรก็ตาม คุณระบุว่ารับความผันผวนได้น้อย แต่กลับมองการลดลงจาก 1,000,000 บาท เหลือ 700,000 บาท ว่าอาจเป็นโอกาสซื้อเพิ่ม "
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
# ============================================================
# V0.9.1 SUPABASE PROFILE STORAGE
# ============================================================
# Configure these values in Streamlit Community Cloud > App settings > Secrets:
# SUPABASE_URL = "https://YOUR_PROJECT.supabase.co"
# SUPABASE_KEY = "sb_publishable_..."
#
# NOTE: The profiles table was created as "Profiles" (capital P), while
# assessments was created in lowercase. PostgREST table names are case-sensitive.
PROFILES_TABLE = "Profiles"
ASSESSMENTS_TABLE = "assessments"
REQUEST_TIMEOUT = 15


def normalize_nickname(value):
    return " ".join(value.strip().split())


def nickname_key(value):
    return normalize_nickname(value).casefold()


def hash_pin(pin):
    return hashlib.sha256(pin.encode("utf-8")).hexdigest()


def get_supabase_config():
    try:
        url = str(st.secrets["SUPABASE_URL"]).strip().rstrip("/")
        key = str(st.secrets["SUPABASE_KEY"]).strip()
    except (KeyError, FileNotFoundError):
        url = os.getenv("SUPABASE_URL", "").strip().rstrip("/")
        key = os.getenv("SUPABASE_KEY", "").strip()
    return url, key

def get_admin_password():
    try:
        return str(st.secret["ADMIN_PASSWORD"]).strip()
    except Exception:
        return os.getenv("ADMIN_PASSWORD", "").strip()

def supabase_headers(prefer=None):
    _, key = get_supabase_config()
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    if prefer:
        headers["Prefer"] = prefer
    return headers


def supabase_request(method, table, params=None, payload=None, prefer=None):
    url, key = get_supabase_config()
    if not url or not key:
        raise RuntimeError("ยังไม่ได้ตั้งค่า SUPABASE_URL และ SUPABASE_KEY ใน Streamlit Secrets")
    response = requests.request(
        method,
        f"{url}/rest/v1/{table}",
        headers=supabase_headers(prefer),
        params=params,
        json=payload,
        timeout=REQUEST_TIMEOUT,
    )
    if not response.ok:
        detail = response.text[:500]
        raise RuntimeError(f"Supabase error {response.status_code}: {detail}")
    if response.status_code == 204 or not response.text.strip():
        return None
    return response.json()


def find_profile(nickname):
    normalized = normalize_nickname(nickname)
    rows = supabase_request(
        "GET",
        PROFILES_TABLE,
        params={"select": "id,nickname,pin_hash,created_at", "nickname": f"ilike.{normalized}", "limit": "1"},
    ) or []
    return rows[0] if rows else None


def create_profile(nickname, pin):
    payload = {"nickname": normalize_nickname(nickname), "pin_hash": hash_pin(pin)}
    rows = supabase_request(
        "POST", PROFILES_TABLE, payload=payload, prefer="return=representation"
    ) or []
    return rows[0] if rows else None


def get_assessments(profile_id):
    rows = supabase_request(
        "GET",
        ASSESSMENTS_TABLE,
        params={
            "select": "id,profile_id,assessment_date,style_name,learning_stage,result_json",
            "profile_id": f"eq.{profile_id}",
            "style_name": "neq.GUIDE_ME_FEEDBACK",
            "order": "assessment_date.desc",
        },
    ) or []
    return rows


def assessment_to_record(row):
    return {
        "assessed_at": row.get("assessment_date", ""),
        "result": row.get("result_json") or {},
    }


def get_current_profile():
    profile_id = st.session_state.current_profile_id
    if not profile_id:
        return None
    rows = supabase_request(
        "GET", PROFILES_TABLE,
        params={"select": "id,nickname,pin_hash,created_at", "id": f"eq.{profile_id}", "limit": "1"},
    ) or []
    if not rows:
        return None
    profile = rows[0]
    assessments = get_assessments(profile_id)
    profile["assessment_history"] = [assessment_to_record(row) for row in reversed(assessments)]
    profile["latest_assessment"] = assessment_to_record(assessments[0]) if assessments else None
    return profile


def save_assessment(result):
    profile_id = st.session_state.current_profile_id
    if not profile_id:
        return False
    payload = {
        "profile_id": profile_id,
        "style_name": result.get("style", {}).get("name", ""),
        "learning_stage": result.get("mindsets", {}).get("learning_stage", ""),
        "result_json": result,
    }
    supabase_request("POST", ASSESSMENTS_TABLE, payload=payload, prefer="return=minimal")
    return True

def save_guide_me_feedback(feedback_data):

    try:

        profile_id = (
            st.session_state.current_profile_id
        )

        if not profile_id:
            return False

        payload = {
            "profile_id": profile_id,
            "style_name": "GUIDE_ME_FEEDBACK",
            "learning_stage": "",
            "result_json": {
                "feedback_type": "guide_me",
                "feedback": feedback_data,
            },
        }

        supabase_request(
            "POST",
            ASSESSMENTS_TABLE,
            payload=payload,
            prefer="return=minimal",
        )

        return True

    except Exception:

        return False


def database_health_check():
    supabase_request("GET", PROFILES_TABLE, params={"select": "id", "limit": "1"})
    supabase_request("GET", ASSESSMENTS_TABLE, params={"select": "id", "limit": "1"})
    return True
def safe_admin_data(loader_function):

    try:

        return loader_function()

    except Exception as error:

        st.error(
            "❌ ไม่สามารถเชื่อมต่อฐานข้อมูลได้"
        )

        st.caption(str(error))

        return None


# ============================================================
# SESSION AND NAVIGATION
# ============================================================
def initialize_session_state():
    defaults = {
        "page": "home",
        "current_profile_id": None,
        "analysis_result": None,
        "show_results": False,
        "confirmed": False,
        "admin_logged_in": False,
        "selected_admin_profile_id": None,
        "selected_admin_nickname": None,
        "guide_me_selected_asset": None,
        "guide_me_feedback_submitted": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def go_to(page):
    st.session_state.page = page
    st.rerun()

def clear_results():
    st.session_state.show_results = False
    st.session_state.confirmed = False
    st.session_state.analysis_result = None

def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def admin_logout():

    st.session_state.admin_logged_in = False

    st.session_state.selected_admin_profile_id = None

    st.session_state.selected_admin_nickname = None

    go_to("home")


def render_back_button(destination="home"):
    if st.button("⬅️ ย้อนกลับ"):
        go_to(destination)

# ============================================================
# USER INTERFACE
# ============================================================
def apply_green_theme():
    st.markdown("""
    <style>
    :root { --herby-green: #168a46; }
    .stButton > button[kind="primary"], .stFormSubmitButton > button {
        background-color: var(--herby-green); border-color: var(--herby-green);
    }
    .herby-card { padding: 1rem; border-radius: 14px; background: #effaf3; border: 1px solid #bde5ca; }
    </style>
    """, unsafe_allow_html=True)

def render_home():
    st.title("💚 Herby")
    st.subheader("Your Digital Financial Mentor")
    st.markdown("### เราไม่ได้ช่วยคุณเลือกสินทรัพย์\n### เราช่วยให้คุณเข้าใจตัวเองมากขึ้น")
    st.write("ก่อนถามว่า ‘ควรลงทุนอะไร?’ Herby อยากเข้าใจก่อนว่า คนที่จะลงทุนคือใคร")
    if st.button("💚 ฉันเป็นผู้ใช้ใหม่", type="primary", use_container_width=True):
        go_to("register")
    if st.button("💚 ฉันเคยทำแบบประเมินแล้ว", use_container_width=True):
        go_to("login")
    if st.button("🔐 Admin"):
        go_to("admin_login")

def render_register():
    render_back_button("home")
    st.title("💚 สร้างโปรไฟล์ Herby")
    with st.form("register_form"):
        nickname = st.text_input("Nickname", max_chars=40)
        pin = st.text_input("PIN ตัวเลข 4 หลัก", type="password", max_chars=4)
        consent = st.checkbox("ฉันยินยอมให้ Herby บันทึก Nickname, PIN แบบเข้ารหัส และผลการประเมิน เพื่อเรียกดูโปรไฟล์ภายหลัง")
        submitted = st.form_submit_button("💚 ตรวจสอบและสร้างโปรไฟล์", use_container_width=True)
    if submitted:
        nickname = normalize_nickname(nickname)
        if not nickname:
            st.error("กรุณาใส่ Nickname")
        elif len(pin) != 4 or not pin.isdigit():
            st.error("PIN ต้องเป็นตัวเลข 4 หลัก")
        elif not consent:
            st.error("กรุณายอมรับการบันทึกข้อมูลก่อนสร้างโปรไฟล์")
        else:
            try:
                if find_profile(nickname):
                    st.error("❌ ชื่อนี้ถูกใช้งานแล้ว กรุณาตั้งชื่อใหม่")
                else:
                    profile = create_profile(nickname, pin)
                    if not profile:
                        raise RuntimeError("Supabase ไม่ได้ส่งข้อมูลโปรไฟล์กลับมา")
                    st.session_state.current_profile_id = profile["id"]
                    clear_results()
                    go_to("questionnaire")
            except Exception as error:
                st.error(f"ไม่สามารถสร้างโปรไฟล์ได้: {error}")

def render_login():
    render_back_button("home")
    st.title("💚 ยินดีต้อนรับกลับ")
    with st.form("login_form"):
        nickname = st.text_input("Nickname")
        pin = st.text_input("PIN ตัวเลข 4 หลัก", type="password", max_chars=4)
        submitted = st.form_submit_button("💚 ให้ Herby จำฉัน", use_container_width=True)
    if submitted:
        try:
            profile = find_profile(nickname)
            if profile and profile.get("pin_hash") == hash_pin(pin):
                st.session_state.current_profile_id = profile["id"]
                assessments = get_assessments(profile["id"])
                st.session_state.analysis_result = assessments[0].get("result_json") if assessments else None
                st.session_state.show_results = False
                st.session_state.confirmed = False
                go_to("dashboard")
            else:
                st.error("ไม่พบ Nickname หรือ PIN ไม่ถูกต้อง")
        except Exception as error:
            st.error(f"ไม่สามารถเข้าสู่ระบบได้: {error}")

def render_questionnaire():
    profile = get_current_profile()
    if not profile:
        go_to("home")
    render_back_button("dashboard" if profile.get("latest_assessment") else "home")
    nickname = profile["nickname"]
    st.title("👋 ยินดีต้อนรับ")
    st.success(f"สวัสดี {nickname} 👋 ยินดีต้อนรับสู่ Herby")
    with st.form("mindset_questionnaire"):
        age = st.selectbox("คุณอยู่ในช่วงอายุใด?", AGE_OPTIONS, key="q_age")
        goal = st.selectbox("เป้าหมายหลักในการลงทุนของคุณคืออะไร?", GOAL_OPTIONS, key="q_goal")
        timeline = st.selectbox("คุณคาดว่าจะใช้เงินก้อนนี้เมื่อไร?", TIMELINE_OPTIONS, key="q_timeline")
        experience = st.selectbox("คุณมีประสบการณ์การลงทุนมากแค่ไหน?", EXPERIENCE_OPTIONS, key="q_experience")
        assets = st.multiselect(
            "คุณสนใจสินทรัพย์ประเภทใดเป็นพิเศษ?", ASSET_OPTIONS, key="q_assets",
            help="เลือกได้มากกว่าหนึ่งประเภท หากยังไม่แน่ใจสามารถเลือก 'ยังไม่แน่ใจ' ได้",
        )
        feeling = st.radio(
            "หากคุณซื้อหุ้นมูลค่า 1,000,000 บาท และเมื่อเปิดตลาดมามูลค่าเหลือ 700,000 บาท คุณคิดว่าตัวเองจะทำอย่างไร?",
            FEELING_OPTIONS, key="q_feeling",
        )
        volatility = st.slider("คุณยอมรับความผันผวนได้มากแค่ไหน?", 1, 10, 5, key="q_volatility")
        submitted = st.form_submit_button("🔍 วิเคราะห์สไตล์การลงทุน", type="primary", use_container_width=True)
    if submitted:
        answers = {
            "name": nickname, "age": age, "goal": goal, "timeline": timeline,
            "experience": experience, "assets": assets, "feeling": feeling,
            "volatility": volatility,
        }
        st.session_state.analysis_result = analyze_answers(answers)
        st.session_state.show_results = True
        st.session_state.confirmed = False
        st.rerun()
    if st.session_state.show_results and st.session_state.analysis_result:
        render_results(st.session_state.analysis_result)

def render_results(result):
    st.divider()
    st.caption(f"ผลสะท้อนสำหรับ {result['answers']['name']}")
    st.header("🔎 สิ่งที่ Herby สังเกตเห็น")
    if result["observations"]:
        for observation in result["observations"]:
            st.warning(observation)
    else:
        st.info("Herby ยังไม่พบแรงดึงสำคัญจากคำตอบชุดนี้ แต่ผลลัพธ์ยังเป็นเพียงภาพสะท้อนจากข้อมูลที่คุณให้")
    st.header("🌟 What Herby Learned About You")
    st.info(result["insight"])
    st.header("📈 สไตล์การลงทุนปัจจุบันของคุณ")
    st.subheader(result["style"]["name"])
    st.write(result["style"]["description"])
    st.caption("ผลลัพธ์นี้เป็นภาพสะท้อนปัจจุบัน ไม่ใช่คำแนะนำให้ซื้อหรือขายสินทรัพย์ และสไตล์สามารถเปลี่ยนแปลงได้")
    st.header("❓ Herby เข้าใจคุณถูกไหม?")

    feedback_accuracy = st.radio(
        "💚 ผลลัพธ์นี้ตรงกับตัวคุณมากแค่ไหน?",
        [
            "👍 ตรงมาก",
            "🙂 ค่อนข้างตรง",
            "😕 ยังไม่ค่อยตรง",
            "😣 ไม่ตรงเลย"
        ]
    )

    feedback_understanding = st.slider(
        "🧠 ผลลัพธ์นี้ช่วยให้คุณเข้าใจตัวเองมากขึ้นแค่ไหน?",
        1,
        5,
        3
    )

    feedback_comment = st.text_area(
        "💬 มีอะไรที่อยากให้ Herby ปรับปรุงเพิ่มเติมไหม?"
    )

    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 ฉันว่ายังไม่ใช่ กลับไปแก้ไขคำตอบ", use_container_width=True):
            st.session_state.show_results = False
            st.session_state.confirmed = False
            st.rerun()
    with col2:
        if st.button("✅ ฉันคิดว่าใช่ ไปขั้นตอนต่อไปกันเลย", type="primary", use_container_width=True):

            result["feedback"] = {
                "accuracy": feedback_accuracy,
                "understanding": feedback_understanding,
                "comment": feedback_comment
            }
            
            if save_assessment(result):
                st.session_state.show_results = False
                st.session_state.confirmed = True
                go_to("about")
            else:
                st.error("ไม่สามารถบันทึกโปรไฟล์ได้ กรุณาเข้าสู่ระบบใหม่")

def render_about():
    render_back_button("dashboard")
    st.title("❤️ ทำไม Herby ถึงถามคำถามเหล่านี้?")
    st.markdown("""
Herby ไม่ได้พยายามตัดสินคุณ และไม่ได้พยายามหาว่าคุณตอบถูกหรือผิด

Herby กำลังพยายามเข้าใจว่า:
- คุณต้องการอะไร
- คุณกังวลอะไร
- คุณให้ความสำคัญกับอะไร
- คุณพร้อมรับอะไรจริง ๆ

### 💚 ความเชื่อหลักของ Herby
ก่อนถามว่า **ควรลงทุนอะไร?** ต้องถามก่อนว่า **คนที่จะลงทุนคือใคร?**

### 🌱 จุดเริ่มต้นของ Herby
Founder ของ Herby เคยเป็นนักลงทุนประเภท:

ใครบอกว่าดี...ซื้อ 🤣  
ใครบอกว่ากำลังมา...ซื้อ 🤣  
ใครบอกว่าควรช้อน...ช้อน 🤣  
ใครบอกว่าห้ามพลาด...ซื้อเพิ่ม 🤣

Herby จึงเกิดขึ้นเพื่อช่วยให้เราเข้าใจตัวเอง ก่อนตัดสินใจเรื่องการลงทุน
    """)
    if st.button("💚 ไปที่ Dashboard", type="primary", use_container_width=True):
        go_to("dashboard")

def render_result_snapshot(result):
    st.header("🔎 สิ่งที่ Herby สังเกตเห็น")
    for observation in result.get("observations", []):
        st.warning(observation)
    st.header("🌟 What Herby Learned About You")
    st.info(result.get("insight", ""))
    st.header("📈 สไตล์การลงทุนปัจจุบันของคุณ")
    st.subheader(result.get("style", {}).get("name", "-"))
    st.write(result.get("style", {}).get("description", ""))

def get_risk_display(value):

    mapping = {
        "low": "ต่ำ",
        "medium": "ปานกลาง",
        "high": "สูง",
    }

    return mapping.get(value, value or "-")


def get_behavior_display(value):

    mapping = {
        "escape": "ขายออกทั้งหมดทันที",
        "reduce": "ขายบางส่วนเพื่อลดความเสี่ยง",
        "endure": "ถือต่อ แม้จะรู้สึกไม่สบายใจ",
        "accept": "ถือไว้ เพราะมองว่าเป็นความผันผวนตามปกติ",
        "actively_add": "พิจารณาซื้อเพิ่มเมื่อมองว่าเป็นโอกาส",
    }

    return mapping.get(value, value or "-")


def get_learning_stage_display(value):

    mapping = {
        "emerging": "กำลังเริ่มสำรวจ",
        "developing": "กำลังพัฒนา",
        "experienced": "มีประสบการณ์",
        "seasoned": "มีประสบการณ์สูง",
    }

    return mapping.get(value, value or "-")


def get_safety_need_display(value):

    mapping = {
        "low": "ต่ำ",
        "medium": "ปานกลาง",
        "high": "สูง",
    }

    return mapping.get(value, value or "-")


def get_growth_desire_display(value):

    mapping = {
        "low": "ต่ำ",
        "medium": "ปานกลาง",
        "high": "สูง",
    }

    return mapping.get(value, value or "-")

def get_risk_display(value):

    mapping = {
        "low": "ต่ำ",
        "medium": "ปานกลาง",
        "high": "สูง",
    }

    return mapping.get(value, value or "-")


def get_behavior_display(value):

    mapping = {
        "escape": "ขายออกทั้งหมดทันที",
        "reduce": "ขายบางส่วนเพื่อลดความเสี่ยง",
        "endure": "ถือต่อ แม้จะรู้สึกไม่สบายใจ",
        "accept": "ถือไว้ เพราะมองว่าเป็นความผันผวนตามปกติ",
        "actively_add": "พิจารณาซื้อเพิ่มเมื่อมองว่าเป็นโอกาส",
    }

    return mapping.get(value, value or "-")


def get_learning_stage_display(value):

    mapping = {
        "emerging": "กำลังเริ่มสำรวจ",
        "developing": "กำลังพัฒนา",
        "experienced": "มีประสบการณ์",
        "seasoned": "มีประสบการณ์สูง",
    }

    return mapping.get(value, value or "-")


def get_safety_need_display(value):

    mapping = {
        "low": "ต่ำ",
        "medium": "ปานกลาง",
        "high": "สูง",
    }

    return mapping.get(value, value or "-")


def get_growth_desire_display(value):

    mapping = {
        "low": "ต่ำ",
        "medium": "ปานกลาง",
        "high": "สูง",
    }

    return mapping.get(value, value or "-")

def get_profile_numeric_levels(result):

    answers = result.get("answers") or {}
    mindsets = result.get("mindsets") or {}

    risk_mapping = {
        "low": 1,
        "medium": 3,
        "high": 5,
    }

    behavior_mapping = {
        "escape": 1,
        "reduce": 2,
        "endure": 3,
        "accept": 4,
        "actively_add": 5,
    }

    timeline_mapping = {
        "น้อยกว่า 3 ปี": 1,
        "3-5 ปี": 2,
        "5-10 ปี": 3,
        "10-20 ปี": 4,
        "มากกว่า 20 ปี": 5,
    }

    experience_mapping = {
        "ยังไม่เคยลงทุน": 1,
        "น้อยกว่า 1 ปี": 1,
        "1-3 ปี": 2,
        "3-10 ปี": 3,
        "มากกว่า 10 ปี": 4,
    }

    growth_desire = (
        mindsets.get("growth_desire")
        or {}
    )

    growth_mapping = {
        "low": 1,
        "medium": 3,
        "high": 5,
    }

    safety_mapping = {
        "low": 1,
        "medium": 3,
        "high": 5,
    }

    return {
        "risk": risk_mapping.get(
            mindsets.get("risk_tolerance"),
            3,
        ),
        "behavior": behavior_mapping.get(
            mindsets.get("stress_behavior"),
            3,
        ),
        "timeline": timeline_mapping.get(
            answers.get("timeline"),
            3,
        ),
        "experience": experience_mapping.get(
            answers.get("experience"),
            1,
        ),
        "growth": growth_mapping.get(
            growth_desire.get("level"),
            3,
        ),
        "safety": safety_mapping.get(
            mindsets.get("safety_need"),
            3,
        ),
    }
def score_asset_suitability(
    asset_name,
    asset_profile,
    result,
):
    answers = result.get("answers") or {}
    mindsets = result.get("mindsets") or {}
    relationships = result.get("relationships") or []

    levels = get_profile_numeric_levels(result)

    asset_risk = asset_profile["risk_level"]
    asset_growth = asset_profile["growth_level"]
    minimum_timeline = asset_profile["minimum_timeline"]
    required_experience = asset_profile["experience_level"]

    score = 50
    alignments = []
    cautions = []

    style_name = result.get("style", {}).get("name", "")
    preferred_assets = STYLE_ASSET_MAPPING.get(style_name, [])

    if asset_name in preferred_assets:
        position = preferred_assets.index(asset_name)
        ranking_bonus = {0: 12, 1: 9, 2: 6, 3: 3}
        score += ranking_bonus.get(position, 0)
        alignments.append(
            f"สินทรัพย์นี้อยู่ในกลุ่มที่ Herby มองว่าสอดคล้องกับสไตล์ {style_name}"
        )

        risk_difference = abs(levels["risk"] - asset_risk)
        if risk_difference == 0:
            score += 18
            alignments.append("ระดับความเสี่ยงของสินทรัพย์สอดคล้องกับระดับที่คุณระบุว่ารับได้")
        elif risk_difference == 1:
            score += 10
            alignments.append("ระดับความเสี่ยงของสินทรัพย์อยู่ใกล้เคียงกับความพร้อมรับความผันผวนของคุณ")
        elif asset_risk > levels["risk"]:
            score -= 18
            cautions.append("สินทรัพย์นี้มีความเสี่ยงสูงกว่าระดับที่คุณระบุว่ารับได้")
        else:
            score -= 3
            cautions.append("สินทรัพย์นี้อาจมีโอกาสเติบโตต่ำกว่าความต้องการของคุณ")

    # … (โค้ดเงื่อนไขอื่น ๆ คงเดิม)

    score = max(0, min(100, round(score)))
    if score >= 85:
        label = "สอดคล้องสูงมาก"
    elif score >= 70:
        label = "สอดคล้อง"
    elif score >= 55:
        label = "สอดคล้องแบบมีเงื่อนไข"
    elif score >= 40:
        label = "ควรพิจารณาด้วยความระมัดระวัง"
    else:
        label = "สอดคล้องค่อนข้างต่ำ"

    return {
        "asset_name": asset_name,
        "icon": asset_profile["icon"],
        "score": score,
        "label": label,
        "portfolio_role": asset_profile["portfolio_role"],
        "alignments": alignments,
        "cautions": cautions,
        "strengths": asset_profile["strengths"],
        "weaknesses": asset_profile["weaknesses"],
        "general_cautions": asset_profile["general_cautions"],
    }

def build_asset_suitability_results(result):

    suitability_results = []

    for asset_name, asset_profile in (
        GUIDE_ME_ASSET_PROFILES.items()
    ):

        suitability = score_asset_suitability(
            asset_name,
            asset_profile,
            result,
        )

        suitability_results.append(
            suitability
        )

    return sorted(
        suitability_results,
        key=lambda item: item["score"],
        reverse=True,
    )

def render_asset_suitability_card(
    suitability,
    rank,
):

    asset_name = suitability["asset_name"]
    icon = suitability["icon"]
    score = suitability["score"]
    label = suitability["label"]

    with st.container(border=True):

        st.subheader(
            f"อันดับ {rank} • {icon} {asset_name}"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "🧭 Suitability Score",
                f"{score} / 100",
            )

        with col2:

            st.write(
                f"**ระดับความสอดคล้อง**  \n"
                f"{label}"
            )
            portfolio_role = suitability[
                "portfolio_role"
            ]

            if "ส่วนเสริม" in portfolio_role:

                st.warning(
                    "⚠️ แม้สินทรัพย์ประเภทนี้จะสอดคล้องกับ "
                    "โปรไฟล์ของคุณในหลายด้าน\n\n"
                    "Herby มองว่าสินทรัพย์ประเภทนี้ "
                    "เหมาะเป็นพอร์ตเสริมมากกว่าพอร์ตหลัก\n\n"
                    "เนื่องจากความผันผวนสูง "
                    "และการลดลงของมูลค่าอาจรุนแรง"
                )

                st.info(
                    "📌 บทบาทที่ Herby มองว่าเหมาะสม:\n"
                    "พอร์ตเสริม (Satellite Portfolio)"
                )

            elif (
                "Core" in portfolio_role
            ):

                st.success(
                "✅ สินทรัพย์ประเภทนี้สามารถเป็น "
                "หนึ่งในองค์ประกอบหลักของพอร์ตระยะยาวได้ "
                "หากสอดคล้องกับเป้าหมายและระดับความเสี่ยงของคุณ"
            )

            st.write(
                f"**บทบาทที่อาจเหมาะสม**  \n"
                f"{suitability['portfolio_role']}"
            )
            portfolio_role = suitability[
                "portfolio_role"
            ]

            if portfolio_role == "Satellite Opportunity Portfolio":

                st.warning(
                    "⚠️ แม้สินทรัพย์ประเภทนี้จะสอดคล้องกับ "
                    "โปรไฟล์ของคุณในหลายด้าน "
                    "Herby มองว่าสินทรัพย์ประเภทนี้ "
                    "เหมาะเป็นพอร์ตเสริมมากกว่าพอร์ตหลัก "
                    "เนื่องจากความผันผวนสูง "
                    "และการลดลงของมูลค่าอาจรุนแรง"
                )

            elif portfolio_role in [
                "Core Growth Portfolio",
                "Core Global Growth Portfolio",
            ]:

                st.success(
                    "✅ สินทรัพย์ประเภทนี้สามารถเป็น "
                    "หนึ่งในองค์ประกอบหลักของพอร์ตระยะยาวได้ "
                    "หากสอดคล้องกับเป้าหมายและระดับความเสี่ยงของคุณ"
                )

        st.progress(score / 100)
        
        if st.button(
            f"🔎 ดูรายละเอียด {asset_name}",
            key=f"detail_{asset_name}",
            use_container_width=True,
        ):

            st.session_state.guide_me_selected_asset = (
                asset_name
            )
        
            go_to("asset_detail")


        with st.expander(
            "🔎 ดูเหตุผล จุดแข็ง จุดอ่อน และข้อควรระวัง"
        ):

            st.markdown(
                "#### ✅ สิ่งที่สอดคล้องกับคุณ"
            )

            alignments = suitability[
                "alignments"
            ]

            if alignments:

                for item in alignments:
                    st.write(f"• {item}")

            else:

                st.caption(
                    "ยังไม่พบความสอดคล้องเด่นชัด"
                )

            st.markdown("#### 📈 จุดแข็ง")

            for item in suitability["strengths"]:
                st.write(f"• {item}")

            st.markdown("#### 📉 จุดอ่อน")

            for item in suitability["weaknesses"]:
                st.write(f"• {item}")

            all_cautions = (
                suitability["cautions"]
                + suitability["general_cautions"]
            )

            st.markdown("#### ⚠️ ข้อควรระวัง")

            for item in dict.fromkeys(all_cautions):
                st.write(f"• {item}")

def get_personalized_warning(
    style_name,
    asset_name,
):

    if asset_name != "Bitcoin":
        return None

    warning_map = {

        "🚀 ผู้เปิดรับโอกาส":
        (
            "⚠️ แม้ Bitcoin จะสอดคล้องกับโปรไฟล์ของคุณ\n\n"
            "Herby มองว่าสินทรัพย์ประเภทนี้ "
            "เหมาะเป็นพอร์ตเสริมมากกว่าพอร์ตหลัก\n\n"
            "เนื่องจากความผันผวนสูง "
            "และการลดลงของมูลค่าอาจรุนแรง"
        ),

        "🛡️ ผู้รักษาความมั่นคง":
        (
            "⚠️ Herby สังเกตว่า\n\n"
            "ความผันผวนของ Bitcoin "
            "อาจสูงกว่าระดับความเสี่ยง "
            "ที่คุณระบุว่ารับได้\n\n"
            "นอกจากนี้พฤติกรรมที่คุณคาดว่า "
            "จะใช้เมื่อขาดทุน\n\n"
            "อาจทำให้การถือสินทรัพย์นี้ "
            "เป็นเรื่องที่ท้าทาย"
        ),

        "⚖️ ผู้แสวงหาสมดุล":
        (
            "⚠️ Herby สังเกตว่า\n\n"
            "คุณให้ความสำคัญทั้ง "
            "การเติบโตและความมั่นคง\n\n"
            "ดังนั้นสินทรัพย์ประเภทนี้ "
            "อาจเหมาะในสัดส่วนที่จำกัด "
            "มากกว่าการเป็นพอร์ตหลัก"
        ),

        "📈 ผู้สร้างการเติบโตอย่างมีวินัย":
        (
            "⚠️ Bitcoin อาจสอดคล้องกับ "
            "เป้าหมายการเติบโตของคุณ\n\n"
            "อย่างไรก็ตาม\n\n"
            "Herby มองว่าการสร้างรากฐานพอร์ต "
            "ด้วยสินทรัพย์หลักที่หลากหลาย "
            "อาจมีความสำคัญไม่แพ้การแสวงหา "
            "ผลตอบแทนที่สูงขึ้น"
        ),
    }

    return warning_map.get(style_name)


def render_asset_detail():

    asset_name = (
        st.session_state.get(
            "guide_me_selected_asset"
        )
    )    

    if not asset_name:

        st.warning(
            "ไม่พบข้อมูลสินทรัพย์"
        )

        if st.button(
            "⬅️ กลับ Guide Me",
            use_container_width=True,
        ):
            go_to("guide_me")

        return

    profile = get_current_profile()

    latest = (
        profile.get(
            "latest_assessment"
        )
    )

    result = latest.get(
        "result",
        {},
    )
    style_name = (
        result.get(
            "style",
            {}
        ).get(
            "name",
            ""
        )
    )
    suitability_results = (
        build_asset_suitability_results(
            result
        )
    )

    suitability = None

    for item in suitability_results:

        if (
            item["asset_name"]
            == asset_name
        ):
            suitability = item
            break


    
    if not suitability:

        st.warning(
            "ไม่พบข้อมูลสินทรัพย์"
        )

        if st.button(
            "⬅️ กลับ Guide Me",
            use_container_width=True,
        ):
            go_to("guide_me")

        return

    st.title(
        f"{suitability['icon']} "
        f"{suitability['asset_name']}"
    )

    st.caption(
        "รายละเอียดสินทรัพย์ที่ Herby "
        "มองว่าสอดคล้องกับคุณ"
    )

    if st.button(
        "⬅️ กลับ Guide Me",
        use_container_width=True,
    ):
        go_to("guide_me")

    st.divider()

    st.header("📌 บทบาทในพอร์ต")

    st.info(
        suitability["portfolio_role"]
    )

    role = suitability[
        "portfolio_role"
    ]

    if "ส่วนเสริม" in role:

    personalized_warning = (
        get_personalized_warning(
            style_name,
            suitability["asset_name"],
        )
    )

    if personalized_warning:

        st.warning(
            personalized_warning
        )

    st.divider()

    st.header("✅ ทำไม Herby ถึงแนะนำ")

    for item in suitability["alignments"]:

        st.write(f"• {item}")

    st.divider()

    st.header("📈 จุดแข็ง")

    for item in suitability["strengths"]:

        st.success(item)

    st.divider()

    st.header("📉 จุดอ่อน")

    for item in suitability["weaknesses"]:

        st.error(item)

    st.divider()

    st.header("⚠️ ข้อควรระวัง")

    all_cautions = (
        suitability["cautions"]
        + suitability["general_cautions"]
    )

    for item in dict.fromkeys(
        all_cautions
    ):

        st.warning(item)

    st.divider()

    st.header("💬 Herby Reflection")

    asset_name = suitability[
        "asset_name"
    ]

    reflection_map = {

        "Bitcoin":
        (
            "หาก Bitcoin ลดลง 50% "
            "คุณยังเชื่อในเหตุผลเดิม "
            "ที่ทำให้คุณสนใจสินทรัพย์นี้อยู่หรือไม่?"
        ),

        "ETF หุ้น":
        (
            "คุณกำลังมองหา "
            "ความมั่งคั่งระยะยาว "
            "หรือกำลังมองหาผลตอบแทนระยะสั้น?"
        ),

        "หุ้นต่างประเทศ":
        (
            "หากตลาดโลกผันผวนต่อเนื่อง "
            "คุณยังสามารถถือสินทรัพย์นี้ "
            "ได้ตามแผนเดิมหรือไม่?"
        ),

        "ทองคำ":
        (
            "คุณเลือกทองคำ "
            "เพื่อกระจายความเสี่ยง "
            "หรือเพื่อหวังผลตอบแทน?"
        ),

    }

    reflection = reflection_map.get(
        asset_name,
        (
            "สินทรัพย์นี้มีบทบาทอย่างไร "
            "ต่อเป้าหมายทางการเงินของคุณ?"
        )
    )

    st.info(reflection)

    st.divider()

    st.button(
        "✅ ฉันสนใจสินทรัพย์นี้",
        use_container_width=True,
        disabled=True,
    )

    st.caption(
        "ปุ่มนี้จะเชื่อมกับ "
        "Portfolio Setup "
        "ใน Sprint ถัดไป"
    )


def render_guide_me():

    profile = get_current_profile()

    if not profile:
        st.warning(
            "Herby ยังไม่พบโปรไฟล์ของคุณ "
            "กรุณาเข้าสู่ระบบอีกครั้ง"
        )

        if st.button(
            "⬅️ กลับหน้าแรก",
            use_container_width=True,
        ):
            go_to("home")

        return

    latest = profile.get("latest_assessment")

    if not latest:

        st.title("📣 Guide Me")

        st.info(
            "Herby ต้องรู้จักคุณก่อน "
            "จึงจะสามารถนำเสนอสินทรัพย์ที่สอดคล้องกับคุณได้"
        )

        if st.button(
            "📝 เริ่มทำแบบประเมิน",
            type="primary",
            use_container_width=True,
        ):
            go_to("questionnaire")

        if st.button(
            "⬅️ กลับ Dashboard",
            use_container_width=True,
        ):
            go_to("dashboard")

        return

    result = latest.get("result") or {}
    answers = result.get("answers") or {}
    mindsets = result.get("mindsets") or {}
    style = result.get("style") or {}
    relationships = result.get("relationships") or []
    observations = result.get("observations") or []

    growth_desire = (
        mindsets.get("growth_desire")
        or {}
    )

    nickname = profile.get(
        "nickname",
        answers.get("name", "คุณ"),
    )

    st.title("📣 Guide Me")
    st.subheader("Herby แนะนำ")

    st.info(
        f"จากสิ่งที่ Herby ได้เรียนรู้เกี่ยวกับคุณ {nickname} "
        "Herby จะช่วยนำเสนอสินทรัพย์ที่อาจสอดคล้องกับ "
        "เป้าหมาย ระยะเวลา ระดับความเสี่ยง "
        "และพฤติกรรมการลงทุนของคุณ"
    )

    st.caption(
        "Herby จะอธิบายทั้งสิ่งที่สอดคล้อง "
        "จุดแข็ง จุดอ่อน และข้อควรระวัง "
        "โดยการตัดสินใจสุดท้ายยังเป็นของคุณเสมอ"
    )

    if st.button(
        "⬅️ กลับ Dashboard",
        use_container_width=True,
    ):
        go_to("dashboard")

    st.divider()
    st.header("👤 Herby รู้จักคุณอย่างไร")

    st.subheader(
        style.get(
            "name",
            "ยังไม่พบข้อมูลสไตล์",
        )
    )

    style_description = style.get("description")

    if style_description:
        st.write(style_description)

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**🎯 เป้าหมายหลัก**  \n"
            f"{answers.get('goal', '-')}"
        )

        st.write(
            f"**⏳ ระยะเวลาลงทุน**  \n"
            f"{answers.get('timeline', '-')}"
        )

        st.write(
            f"**🌱 ประสบการณ์**  \n"
            f"{answers.get('experience', '-')}"
        )

        st.write(
            f"**📚 Learning Stage**  \n"
            f"{get_learning_stage_display(
                mindsets.get('learning_stage')
            )}"
        )

    with col2:

        st.write(
            f"**🎯 การยอมรับความเสี่ยง**  \n"
            f"{get_risk_display(
                mindsets.get('risk_tolerance')
            )}"
        )

        st.write(
            f"**⚡ พฤติกรรมเมื่อขาดทุน**  \n"
            f"{get_behavior_display(
                mindsets.get('stress_behavior')
            )}"
        )

        st.write(
            f"**🛡️ ความต้องการความมั่นคง**  \n"
            f"{get_safety_need_display(
                mindsets.get('safety_need')
            )}"
        )

        st.write(
            f"**📈 ความต้องการการเติบโต**  \n"
            f"{get_growth_desire_display(
                growth_desire.get('level')
            )}"
        )

    interested_assets = (
        answers.get("assets")
        or []
    )

    st.markdown("### 💼 สินทรัพย์ที่คุณเคยระบุว่าสนใจ")

    if interested_assets:

        st.write(
            " • ".join(interested_assets)
        )

    else:

        st.caption(
            "คุณยังไม่ได้ระบุสินทรัพย์ที่สนใจ"
        )

    assessed_at = latest.get(
        "assessed_at",
        "",
    )

    if assessed_at:

        assessed_display = (
            assessed_at
            .replace("T", " ")
            [:16]
        )

        st.caption(
            f"อ้างอิงผลประเมินล่าสุด: "
            f"{assessed_display}"
        )

    st.divider()
    st.header("🌟 สิ่งที่ Herby เรียนรู้เกี่ยวกับคุณ")

    insight = result.get("insight")

    if insight:

        st.info(insight)

    else:

        st.caption(
            "ยังไม่มีข้อมูล Insight "
            "จากผลประเมินล่าสุด"
        )

    st.divider()
    st.header("🔎 สิ่งที่ Herby สังเกตเห็น")

    if observations:

        for observation in observations:
            st.warning(observation)

    else:

        st.success(
            "Herby ยังไม่พบแรงดึงหรือความขัดแย้งสำคัญ "
            "จากคำตอบชุดล่าสุดของคุณ"
        )

    important_relationships = [
        relationship
        for relationship in relationships
        if relationship.get("priority", 0) >= 2
    ]

    if important_relationships:

        with st.expander(
            "🧭 ดูความสัมพันธ์สำคัญที่ Herby ตรวจพบ"
        ):

            for relationship in important_relationships:

                interpretation = relationship.get(
                    "interpretation"
                )

                if interpretation:
                    st.write(
                        f"• {interpretation}"
                    )

    st.divider()
    st.header("🧭 สินทรัพย์ที่ Herby แนะนำให้พิจารณา")

    st.info(
        f"จากข้อมูลล่าสุดของคุณ {nickname} "
        "Herby ได้จัดอันดับประเภทสินทรัพย์ "
        "ตามความสอดคล้องกับเป้าหมาย ระยะเวลา "
        "ความเสี่ยง พฤติกรรม และประสบการณ์ของคุณ"
    )

    st.caption(
        "Suitability Score แสดงความสอดคล้องกับโปรไฟล์ "
        "ไม่ใช่การคาดการณ์ผลตอบแทนหรือคำสั่งซื้อ"
    )

    suitability_results = (
        build_asset_suitability_results(
            result
        )
    )

    top_results = suitability_results[:5]

    for rank, suitability in enumerate(
        top_results,
        start=1,
    ):

        render_asset_suitability_card(
            suitability,
            rank,
        )

    with st.expander(
        "📚 ดูสินทรัพย์ประเภทอื่นทั้งหมด"
    ):

        for rank, suitability in enumerate(
            suitability_results[5:],
            start=6,
        ):

            render_asset_suitability_card(
                suitability,
                rank,
            )

    st.divider()

    st.warning(
        "ผลลัพธ์นี้อ้างอิงจากคำตอบล่าสุดของคุณ "
        "และข้อมูลเชิงลักษณะของสินทรัพย์เท่านั้น "
        "ยังไม่ได้ประเมินผลิตภัณฑ์หรือหุ้นรายตัว "
        "ราคา มูลค่า ข่าว หรือจังหวะเข้าซื้อ"
    )

    st.divider()

    st.header("🧪 Guide Me Closed Alpha")

    st.info(
        "ผลลัพธ์นี้ประเมินความสอดคล้องระหว่าง "
        "ประเภทสินทรัพย์กับข้อมูลจากแบบประเมินล่าสุดของคุณ"
    )

    st.caption(
        "Herby ยังไม่ได้วิเคราะห์หุ้นรายตัว "
        "ราคา มูลค่า ข่าว หรือจังหวะเข้าซื้อ "
        "ผลลัพธ์นี้ไม่ใช่คำสั่งซื้อขาย"
    )
    st.divider()

    st.caption(
        "Herby ยังไม่ได้วิเคราะห์หุ้นรายตัว "
        "ราคา มูลค่า ข่าว หรือจังหวะเข้าซื้อ "
        "ผลลัพธ์นี้ไม่ใช่คำสั่งซื้อขาย"
    )

    guide_feedback_fit = st.radio(
    "📣 สินทรัพย์ที่ Herby นำเสนอ "
    "สอดคล้องกับตัวคุณแค่ไหน?",
    [
        "👍 สอดคล้องมาก",
        "🙂 ค่อนข้างสอดคล้อง",
        "😕 ยังไม่ค่อยสอดคล้อง",
        "👎 ไม่สอดคล้อง",
    ],
    )
    guide_feedback_ranking = st.text_area(
        "🧭 มีสินทรัพย์ใดที่คุณคิดว่า "
        "อันดับสูงหรือต่ำเกินไปหรือไม่?"
    )
    guide_feedback_understanding = st.text_area(
        "💬 มีอะไรที่ Herby "
        "เข้าใจคุณคลาดเคลื่อนหรือไม่?"
    )
    if not st.session_state.guide_me_feedback_submitted:

        if st.button(
            "📨 ส่ง Feedback ให้ Herby",
            type="primary",
            use_container_width=True,
        ):

            saved = save_guide_me_feedback(
                {
                    "fit": guide_feedback_fit,
                    "ranking_comment": (
                        guide_feedback_ranking
                    ),
                    "understanding_comment": (
                        guide_feedback_understanding
                    ),
                }
            )

            if saved:

                st.session_state.guide_me_feedback_submitted = True

                st.success(
                    "✅ Herby ได้รับ Feedback แล้ว"
                )

                st.rerun()

            else:

                st.error(
                    "ไม่สามารถบันทึก Feedback ได้"
                )
    else:

        st.success(
            "✅ คุณส่ง Feedback ให้ Herby แล้ว"
        )


def render_dashboard():
    profile = get_current_profile()
    if not profile:
        go_to("home")
    latest = profile.get("latest_assessment")
    st.title("📊 Dashboard")
    st.subheader(f"สวัสดี {profile['nickname']} 👋")
    st.success("Herby จำคุณได้")
    if latest:
        result = latest["result"]
        assessed = latest.get("assessed_at", "-").replace("T", " ")[:16]
        st.markdown(f"**📅 ประเมินล่าสุด:** {assessed}")
        st.markdown(f"**📈 สไตล์ล่าสุด:** {result['style']['name']}")
        st.markdown(f"**🌱 Learning Stage:** {result['mindsets']['learning_stage']}")
        st.divider()

        if st.button(
            "📣 Guide Me — Herby แนะนำ",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.guide_me_selected_asset = None
            go_to("guide_me")

        if st.button("💚 ทบทวนโปรไฟล์ของฉัน", use_container_width=True):
            st.session_state.review_result = result
            go_to("review")
        if st.button("💚 อัปเดตคำตอบใหม่", type="primary", use_container_width=True):
            clear_results()
            go_to("questionnaire")
        if st.button("💚 ดูประวัติการประเมิน", use_container_width=True):
            go_to("history")
    else:
        st.info("Herby จำโปรไฟล์ของคุณได้แล้ว แต่ยังไม่มีผลการประเมิน")
        if st.button("💚 เริ่มประเมินครั้งแรก", type="primary", use_container_width=True):
            go_to("questionnaire")
    if st.button("❤️ เรื่องราวของ Herby", use_container_width=True):
        go_to("about")
    if st.button("ออกจากระบบ", use_container_width=True):
        logout()

def render_review():
    render_back_button("dashboard")
    result = st.session_state.get("review_result")
    if not result:
        profile = get_current_profile() or {}
        latest = profile.get("latest_assessment")
        result = latest.get("result") if latest else None
    if not result:
        st.info("ยังไม่มีผลการประเมิน")
        return
    st.title("💚 โปรไฟล์ของฉัน")
    render_result_snapshot(result)

def render_history():
    render_back_button("dashboard")
    profile = get_current_profile() or {}
    history = profile.get("assessment_history", [])
    st.title("📚 ประวัติการประเมิน")
    if not history:
        st.info("ยังไม่มีประวัติการประเมิน")
        return
    for number, record in enumerate(reversed(history), 1):
        result = record.get("result", {})
        when = record.get("assessed_at", "-").replace("T", " ")[:16]
        style = result.get("style", {}).get("name", "-")
        with st.expander(f"ครั้งที่ {len(history)-number+1} • {when} • {style}"):
            render_result_snapshot(result)
def render_admin_login():
    render_back_button("home")
    st.title("🔐 Admin Login")
   
    password = st.text_input(
        "Admin Password",
        type="password"
    )
    
    if st.button("Login"):
        if password == get_admin_password():
            st.session_state.admin_logged_in = True
            go_to("admin_dashboard")
        else:
            st.error("Invalid Password")

def get_admin_stats():

    profiles = supabase_request(
        "GET",
        PROFILES_TABLE,
        params={
            "select": "id"
        }
    ) or []

    assessments = supabase_request(
        "GET",
        ASSESSMENTS_TABLE,
        params={
            "select": "profile_id,result_json"
        }
    ) or []

    total_users = len(profiles)

    total_assessments = len(assessments)

    assessment_count = {}

    understanding_scores = []

    for row in assessments:

        profile_id = row.get("profile_id")

        assessment_count[profile_id] = (
            assessment_count.get(profile_id, 0) + 1
        )

        feedback = (
            row.get("result_json", {})
            .get("feedback", {})
        )

        score = feedback.get("understanding")

        if isinstance(score, int):
            understanding_scores.append(score)

    returning_users = sum(
        1
        for count in assessment_count.values()
        if count > 1
    )

    average_understanding = (
        round(
            sum(understanding_scores)
            / len(understanding_scores),
            2
        )
        if understanding_scores
        else 0
    )

    return {
        "total_users": total_users,
        "total_assessments": total_assessments,
        "returning_users": returning_users,
        "average_understanding": average_understanding,
    }

def get_admin_users():

    profiles = supabase_request(
        "GET",
        PROFILES_TABLE,
        params={
            "select": "id,nickname,created_at",
            "order": "created_at.desc",
        },
    ) or []

    assessments = supabase_request(
        "GET",
        ASSESSMENTS_TABLE,
        params={
            "select": "profile_id,assessment_date,style_name,result_json",
            "order": "assessment_date.desc",
        },
    ) or []

    assessments_by_user = {}

    for assessment in assessments:

        profile_id = assessment.get("profile_id")

        if not profile_id:
            continue

        if profile_id not in assessments_by_user:
            assessments_by_user[profile_id] = []

        assessments_by_user[profile_id].append(assessment)

    users = []

    for profile in profiles:

        profile_id = profile.get("id")
        user_assessments = assessments_by_user.get(profile_id, [])

        latest_assessment = (
            user_assessments[0]
            if user_assessments
            else None
        )

        latest_style = "ยังไม่มีผลการประเมิน"
        latest_assessment_date = None

        if latest_assessment:

            latest_style = (
                latest_assessment.get("style_name")
                or latest_assessment.get("result_json", {})
                .get("style", {})
                .get("name")
                or "ไม่พบข้อมูลสไตล์"
            )

            latest_assessment_date = latest_assessment.get(
                "assessment_date"
            )

        users.append(
            {
                "id": profile_id,
                "nickname": profile.get("nickname", "-"),
                "created_at": profile.get("created_at"),
                "assessment_count": len(user_assessments),
                "latest_style": latest_style,
                "latest_assessment_date": latest_assessment_date,
            }
        )

    return users

def get_admin_user_assessments(profile_id):

    assessments = supabase_request(
        "GET",
        ASSESSMENTS_TABLE,
        params={
            "select": (
                "id,profile_id,assessment_date,"
                "style_name,learning_stage,result_json"
            ),
            "profile_id": f"eq.{profile_id}",
            "order": "assessment_date.desc",
        },
    ) or []

    return assessments

def get_admin_analytics():

    assessments = supabase_request(
        "GET",
        ASSESSMENTS_TABLE,
        params={
            "select": (
                "id,profile_id,assessment_date,"
                "style_name,learning_stage,result_json"
            ),
            "order": "assessment_date.desc",
        },
    ) or []

    latest_by_user = {}

    for assessment in assessments:

        profile_id = assessment.get("profile_id")

        if not profile_id:
            continue

        if profile_id not in latest_by_user:
            latest_by_user[profile_id] = assessment

    style_counts = {}
    risk_counts = {}
    behavior_counts = {}
    learning_counts = {}
    accuracy_counts = {}

    understanding_scores = []
    feedback_comments = []

    high_risk_users = 0
    defensive_high_risk_users = 0

    for assessment in latest_by_user.values():

        result = assessment.get("result_json") or {}

        style_name = (
            assessment.get("style_name")
            or result.get("style", {}).get("name")
            or "ไม่พบข้อมูล"
        )

        style_counts[style_name] = (
            style_counts.get(style_name, 0) + 1
        )

        mindsets = result.get("mindsets") or {}

        risk = (
            mindsets.get("risk_tolerance")
            or "ไม่พบข้อมูล"
        )

        behavior = (
            mindsets.get("stress_behavior")
            or "ไม่พบข้อมูล"
        )

        learning_stage = (
            assessment.get("learning_stage")
            or mindsets.get("learning_stage")
            or "ไม่พบข้อมูล"
        )

        risk_counts[risk] = (
            risk_counts.get(risk, 0) + 1
        )

        behavior_counts[behavior] = (
            behavior_counts.get(behavior, 0) + 1
        )

        learning_counts[learning_stage] = (
            learning_counts.get(learning_stage, 0) + 1
        )

        if risk == "high":

            high_risk_users += 1

            if behavior in {"escape", "reduce"}:
                defensive_high_risk_users += 1

    for assessment in assessments:

        result = assessment.get("result_json") or {}
        feedback = result.get("feedback") or {}

        accuracy = feedback.get("accuracy")

        if accuracy:

            accuracy_counts[accuracy] = (
                accuracy_counts.get(accuracy, 0) + 1
            )

        understanding = feedback.get(
            "understanding"
        )

        if isinstance(understanding, (int, float)):
            understanding_scores.append(
                understanding
            )

        comment = (
            feedback.get("comment")
            or ""
        ).strip()

        if comment:

            feedback_comments.append(
                {
                    "comment": comment,
                    "accuracy": accuracy or "-",
                    "understanding": understanding,
                    "assessment_date": (
                        assessment.get(
                            "assessment_date"
                        )
                        or "-"
                    ),
                }
            )

    average_understanding = (
        round(
            sum(understanding_scores)
            / len(understanding_scores),
            2,
        )
        if understanding_scores
        else 0
    )

    feedback_response_rate = (
        round(
            len(understanding_scores)
            / len(assessments)
            * 100,
            1,
        )
        if assessments
        else 0
    )

    risk_behavior_gap_rate = (
        round(
            defensive_high_risk_users
            / high_risk_users
            * 100,
            1,
        )
        if high_risk_users
        else 0
    )

    return {
        "total_latest_users": len(latest_by_user),
        "total_assessments": len(assessments),
        "feedback_count": len(understanding_scores),
        "average_understanding": average_understanding,
        "feedback_response_rate": feedback_response_rate,
        "style_counts": style_counts,
        "risk_counts": risk_counts,
        "behavior_counts": behavior_counts,
        "learning_counts": learning_counts,
        "accuracy_counts": accuracy_counts,
        "feedback_comments": feedback_comments,
        "high_risk_users": high_risk_users,
        "defensive_high_risk_users": defensive_high_risk_users,
        "risk_behavior_gap_rate": risk_behavior_gap_rate,
    }

def render_admin_bar_chart(
    title,
    counts,
    category_label,
):

    st.subheader(title)

    if not counts:

        st.info("ยังไม่มีข้อมูลเพียงพอ")
        return

    chart_data = pd.DataFrame(
        [
            {
                category_label: category,
                "จำนวน": count,
            }
            for category, count in counts.items()
        ]
    )

    chart_data = chart_data.sort_values(
        by="จำนวน",
        ascending=False,
    )

    st.bar_chart(
        chart_data,
        x=category_label,
        y="จำนวน",
    )

    with st.expander("🔢 ดูตัวเลขทั้งหมด"):

        for row in chart_data.to_dict(
            orient="records"
        ):

            st.write(
                f"**{row[category_label]}:** "
                f"{row['จำนวน']} คน"
            )


def render_admin_dashboard():

    if not st.session_state.admin_logged_in:

        go_to("admin_login")

    st.title("💚 HERBY ADMIN DASHBOARD")

    st.success("Welcome Founder 😁")

    stats = safe_admin_data(get_admin_stats)
    if not stats: return

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "👥 Users",
            stats["total_users"]
        )

        st.metric(
            "🔄 Returning",
            stats["returning_users"]
        )

    with col2:

        st.metric(
            "📝 Assessments",
            stats["total_assessments"]
        )

        st.metric(
            "🧠 Understanding",
            stats["average_understanding"]
        )
        st.divider()
        if st.button(
            "👥 เปิด User Explorer",
            type="primary",
            use_container_width=True,
        ):
            go_to("admin_users")
        if st.button(
            "🧠 เปิด Mindset Analytics",
            use_container_width=True,
        ):
            go_to("admin_analytics")
        
        st.divider()
        if st.button(
            "🚪 Logout Admin",use_container_width=True,):
            admin_logout()
   

def render_admin_users():

    if not st.session_state.admin_logged_in:
        go_to("admin_login")
        return

    st.title("👥 HERBY USER EXPLORER")

    if st.button("⬅️ กลับไป Admin Dashboard"):
        go_to("admin_dashboard")

    try:

        users = safe_admin_data(get_admin_users)
        if users is None: return

        search_text = st.text_input(
            "🔍 ค้นหาผู้ใช้ด้วย Nickname",
            placeholder="พิมพ์ Nickname ที่ต้องการค้นหา",
        )

        if search_text.strip():

            keyword = search_text.strip().casefold()

            users = [
                user
                for user in users
                if keyword in user["nickname"].casefold()
            ]

        st.caption(f"พบผู้ใช้ {len(users)} คน")

        if not users:

            st.info("ไม่พบผู้ใช้ตามเงื่อนไขที่ค้นหา")
            return

        for user in users:

            created_at = user.get("created_at")

            if created_at:
                created_display = (
                    created_at
                    .replace("T", " ")
                    [:16]
                )
            else:
                created_display = "-"

            latest_date = user.get(
                "latest_assessment_date"
            )

            if latest_date:
                latest_date_display = (
                    latest_date
                    .replace("T", " ")
                    [:16]
                )
            else:
                latest_date_display = "-"

            with st.container(border=True):

                st.subheader(
                    f"👤 {user['nickname']}"
                )

                st.write(
                    f"**📈 สไตล์ล่าสุด:** "
                    f"{user['latest_style']}"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "📝 จำนวนการประเมิน",
                        user["assessment_count"],
                    )

                with col2:

                    st.write(
                        f"**สร้างโปรไฟล์:**  \n"
                        f"{created_display}"
                    )

                    st.write(
                        f"**ประเมินล่าสุด:**  \n"
                        f"{latest_date_display}"
                    )

                    if st.button(
                        "🔎 ดูรายละเอียดผู้ใช้",
                        key=f"view_user_{user['id']}",
                        use_container_width=True,
                    ):
                        st.session_state.selected_admin_profile_id = user["id"]
                        st.session_state.selected_admin_nickname = user["nickname"]
                        go_to("admin_user_detail")

    
    except Exception as error:

        st.error(
            f"ไม่สามารถโหลดข้อมูลผู้ใช้ได้: {error}"
        )

def render_admin_user_detail():

    if not st.session_state.admin_logged_in:
        go_to("admin_login")
        return

    profile_id = st.session_state.get(
        "selected_admin_profile_id"
    )

    nickname = st.session_state.get(
        "selected_admin_nickname"
    )

    if not profile_id:
        st.warning("ยังไม่ได้เลือกผู้ใช้")
        if st.button("⬅️ กลับไป User Explorer"):
            go_to("admin_users")
        return

    st.title(f"👤 {nickname or 'User Detail'}")

    if st.button("⬅️ กลับไป User Explorer"):
        go_to("admin_users")

    try:

        assessments = safe_admin_data(
            lambda:get_admin_user_assessments(profile_id)
        )
        if assessments is None: return
                                      

        st.metric(
            "📝 จำนวนการประเมินทั้งหมด",
            len(assessments),
        )

        if not assessments:
            st.info(
                "ผู้ใช้คนนี้ยังไม่มีผลการประเมิน"
            )
            return

        latest_result = (
            assessments[0].get("result_json")
            or {}
        )

        latest_style = (
            assessments[0].get("style_name")
            or latest_result.get("style", {}).get("name")
            or "-"
        )

        latest_feedback = (
            latest_result.get("feedback")
            or {}
        )

        st.subheader("📌 ข้อมูลล่าสุด")

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                f"**สไตล์ล่าสุด:**  \n"
                f"{latest_style}"
            )

            st.write(
                f"**Learning Stage:**  \n"
                f"{assessments[0].get('learning_stage') or '-'}"
            )

        with col2:

            understanding = latest_feedback.get(
                "understanding"
            )

            accuracy = latest_feedback.get(
                "accuracy"
            )

            st.metric(
                "🧠 Understanding Score",
                (
                    f"{understanding} / 5"
                    if understanding is not None
                    else "ยังไม่มี Feedback"
                ),
            )

            st.write(
                f"**ความตรงของผลลัพธ์:**  \n"
                f"{accuracy or 'ยังไม่มี Feedback'}"
            )

        st.divider()
        st.subheader("📚 ประวัติการประเมิน")

        for number, assessment in enumerate(
            assessments,
            start=1,
        ):

            result = (
                assessment.get("result_json")
                or {}
            )

            assessment_date = (
                assessment.get("assessment_date")
                or "-"
            )

            if assessment_date != "-":
                assessment_date_display = (
                    assessment_date
                    .replace("T", " ")
                    [:16]
                )
            else:
                assessment_date_display = "-"

            style_name = (
                assessment.get("style_name")
                or result.get("style", {}).get("name")
                or "-"
            )

            assessment_number = (
                len(assessments) - number + 1
            )

            expander_title = (
                f"ครั้งที่ {assessment_number} • "
                f"{assessment_date_display} • "
                f"{style_name}"
            )

            with st.expander(
                expander_title,
                expanded=(number == 1),
            ):

                st.markdown("### 📈 ผลการวิเคราะห์")

                st.write(
                    f"**สไตล์:** {style_name}"
                )

                learning_stage = (
                    assessment.get("learning_stage")
                    or result.get("mindsets", {}).get(
                        "learning_stage"
                    )
                    or "-"
                )

                st.write(
                    f"**Learning Stage:** "
                    f"{learning_stage}"
                )

                insight = result.get("insight")

                if insight:
                    st.markdown(
                        "#### 🌟 สิ่งที่ Herby เรียนรู้"
                    )
                    st.info(insight)

                observations = (
                    result.get("observations")
                    or []
                )

                if observations:

                    st.markdown(
                        "#### 🔎 สิ่งที่ Herby สังเกตเห็น"
                    )

                    for observation in observations:
                        st.warning(observation)

                answers = (
                    result.get("answers")
                    or {}
                )

                if answers:

                    st.markdown(
                        "#### 📝 คำตอบของผู้ใช้"
                    )

                    st.write(
                        f"**ช่วงอายุ:** "
                        f"{answers.get('age', '-')}"
                    )

                    st.write(
                        f"**เป้าหมาย:** "
                        f"{answers.get('goal', '-')}"
                    )

                    st.write(
                        f"**ระยะเวลา:** "
                        f"{answers.get('timeline', '-')}"
                    )

                    st.write(
                        f"**ประสบการณ์:** "
                        f"{answers.get('experience', '-')}"
                    )

                    assets = (
                        answers.get("assets")
                        or []
                    )

                    st.write(
                        f"**สินทรัพย์ที่สนใจ:** "
                        f"{', '.join(assets) if assets else '-'}"
                    )

                    st.write(
                        f"**พฤติกรรมเมื่อขาดทุน:** "
                        f"{answers.get('feeling', '-')}"
                    )

                    st.write(
                        f"**ระดับความผันผวน:** "
                        f"{answers.get('volatility', '-')} / 10"
                    )

                feedback = (
                    result.get("feedback")
                    or {}
                )

                st.markdown(
                    "#### 💬 Feedback"
                )

                if feedback:

                    st.write(
                        f"**ความตรงของผลลัพธ์:** "
                        f"{feedback.get('accuracy', '-')}"
                    )

                    feedback_score = feedback.get(
                        "understanding"
                    )

                    st.write(
                        f"**Understanding Score:** "
                        f"{feedback_score if feedback_score is not None else '-'}"
                        f" / 5"
                    )

                    comment = (
                        feedback.get("comment")
                        or ""
                    ).strip()

                    if comment:
                        st.success(
                            f"ความคิดเห็น: {comment}"
                        )
                    else:
                        st.caption(
                            "ผู้ใช้ไม่ได้เขียนความคิดเห็นเพิ่มเติม"
                        )

                else:

                    st.caption(
                        "Assessment นี้สร้างก่อนเริ่มใช้ Feedback System"
                    )

    except Exception as error:

        st.error(
            f"ไม่สามารถโหลดรายละเอียดผู้ใช้ได้: {error}"
        )

def render_admin_analytics():

    if not st.session_state.admin_logged_in:
        go_to("admin_login")
        return

    st.title("🧠 HERBY MINDSET ANALYTICS")

    if st.button("⬅️ กลับไป Admin Dashboard"):
        go_to("admin_dashboard")

    try:

        analytics = safe_admin_data(get_admin_analytics)
        if not analytics: return

        st.caption(
            "Mindset ใช้ผลประเมินล่าสุดของผู้ใช้แต่ละคน "
            "ส่วน Feedback ใช้ข้อมูลจากทุก Assessment"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "👥 ผู้ใช้ที่มีผลประเมิน",
                analytics["total_latest_users"],
            )

            st.metric(
                "💬 Feedback ที่ได้รับ",
                analytics["feedback_count"],
            )

        with col2:

            st.metric(
                "🧠 Understanding เฉลี่ย",
                (
                    f"{analytics['average_understanding']} / 5"
                    if analytics["feedback_count"] > 0
                    else "ยังไม่มีข้อมูล"
                ),
            )

            st.metric(
                "📨 Feedback Response Rate",
                (
                    f"{analytics['feedback_response_rate']}%"
                ),
            )

        st.divider()

        render_admin_bar_chart(
            "📈 การกระจายของสไตล์การลงทุน",
            analytics["style_counts"],
            "สไตล์",
        )

        st.divider()

        render_admin_bar_chart(
            "🎯 ระดับการยอมรับความเสี่ยง",
            analytics["risk_counts"],
            "ระดับความเสี่ยง",
        )

        st.divider()

        render_admin_bar_chart(
            "⚡ พฤติกรรมเมื่อเผชิญความผันผวน",
            analytics["behavior_counts"],
            "พฤติกรรม",
        )

        st.divider()

        render_admin_bar_chart(
            "🌱 Learning Stage",
            analytics["learning_counts"],
            "Learning Stage",
        )

        st.divider()

        render_admin_bar_chart(
            "💚 ความตรงของผลลัพธ์จาก Feedback",
            analytics["accuracy_counts"],
            "ระดับความตรง",
        )

        st.divider()
        st.subheader("🔍 Risk–Behavior Insight")

        high_risk_users = analytics[
            "high_risk_users"
        ]

        defensive_users = analytics[
            "defensive_high_risk_users"
        ]

        gap_rate = analytics[
            "risk_behavior_gap_rate"
        ]

        if high_risk_users == 0:

            st.info(
                "ยังไม่มีผู้ใช้ที่ถูกจัดอยู่ในระดับ "
                "Risk Tolerance: High"
            )

        elif defensive_users == 0:

            st.success(
                "ยังไม่พบ Risk–Behavior Gap "
                "ในกลุ่มผู้ใช้ที่รับความเสี่ยงระดับสูง"
            )

            st.caption(
                f"วิเคราะห์จากผู้ใช้ Risk Tolerance: "
                f"High จำนวน {high_risk_users} คน"
            )

        else:

            st.warning(
                f"พบผู้ใช้ {defensive_users} จาก "
                f"{high_risk_users} คน ที่ระบุว่า "
                f"รับความเสี่ยงได้สูง แต่มีแนวโน้ม "
                f"ขายทั้งหมดหรือขายบางส่วนเมื่อขาดทุน"
            )

            st.metric(
                "⚠️ Risk–Behavior Gap",
                f"{gap_rate}%",
            )

        st.divider()
        st.subheader("💬 ความคิดเห็นล่าสุดจากผู้ใช้")

        comments = analytics[
            "feedback_comments"
        ]

        if not comments:

            st.info(
                "ยังไม่มีความคิดเห็นเพิ่มเติมจากผู้ใช้"
            )

        else:

            for feedback in comments[:10]:

                assessment_date = feedback.get(
                    "assessment_date",
                    "-",
                )

                if assessment_date != "-":

                    assessment_date_display = (
                        assessment_date
                        .replace("T", " ")
                        [:16]
                    )

                else:

                    assessment_date_display = "-"

                with st.container(border=True):

                    st.write(
                        f"💬 {feedback['comment']}"
                    )

                    st.caption(
                        f"{feedback['accuracy']} • "
                        f"Understanding: "
                        f"{feedback['understanding'] or '-'} / 5 • "
                        f"{assessment_date_display}"
                    )

    except Exception as error:

        st.error(
            f"ไม่สามารถโหลด Mindset Analytics ได้: "
            f"{error}"
        )


def main():
    initialize_session_state()
    apply_green_theme()
    url, key = get_supabase_config()
    if not url or not key:
        st.error("ยังไม่ได้ตั้งค่า Supabase กรุณาเพิ่ม SUPABASE_URL และ SUPABASE_KEY ใน Streamlit Secrets")
        st.stop()
    routes = {
        "home": render_home, "register": render_register, "login": render_login,
        "questionnaire": render_questionnaire, "about": render_about,
        "dashboard": render_dashboard, "review": render_review, "history": render_history,
        "admin_login": render_admin_login, "admin_dashboard": render_admin_dashboard,
        "admin_users": render_admin_users, "admin_user_detail": render_admin_user_detail,
        "admin_analytics": render_admin_analytics, "guide_me": render_guide_me,
        "asset_detail": render_asset_detail,
    }
    routes.get(st.session_state.page, render_home)()

if __name__ == "__main__":
    main()
