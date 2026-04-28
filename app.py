import streamlit as st

st.title("🏥 威廉健康顧問AI小幫手")
st.write("（AI 小幫手會根據你輸入的身體資料 + 生活習慣來進行分析🧠💡）")

# =====================
# 👤 基本資料
# =====================

gender = st.selectbox("🚻 性別", ["男", "女"])
age = st.number_input("🎂 年齡", 10, 100, 35)
height = st.number_input("📏 身高 (cm)", 100, 230, 170)
weight = st.number_input("⚖️ 體重 (kg)", 30, 200, 55)

# =====================
# 🧠 AI 基礎計算
# =====================

# 💧 理想水量
def ideal_water(weight, gender):
    if gender == "男":
        return weight * 35 + 500
    else:
        return weight * 35

target_water = ideal_water(weight, gender)

# ⚖️ 理想體重
if gender == "男":
    ideal_weight = height - 100
else:
    ideal_weight = height - 110

weight_gap = weight - ideal_weight

# =====================
# 🧾 生活數據
# =====================

water = st.slider("💧 昨天喝水量 (cc)", 0, 5000, 1500, 100)
sleep = st.slider("😴 昨天睡眠時間 (小時)", 0.0, 12.0, 6.5, 0.5)

exercise = st.selectbox("🚶 昨天是否運動30分鐘（散步的強度）", ["有", "沒有"])
stress = st.selectbox("🧘 昨天壓力程度", ["低", "高"])
work = st.selectbox("💻 昨天工作是否忙碌", ["不忙", "忙"])
sleep_before_11 = st.selectbox("🌙 昨晚是否11PM前睡覺", ["是", "否"])

# =====================
# 🧠 AI Score + 教練分析
# =====================

def ai_score():
    score = 100
    reasons = []

    # 💧 水
    if water < target_water:
        score -= 20
        reasons.append(f"補足該有喝水量（差 {int(target_water - water)} cc）💦")

    # 😴 睡眠
    if sleep < 7:
        score -= 15
        reasons.append("睡眠不足（<7小時）💤")

    # ⚖️ 體重
    if weight > ideal_weight:
        score -= 10
        reasons.append(f"體重高於理想值 {weight - ideal_weight:.1f} kg")

    # 🧘 壓力
    if stress == "高":
        score -= 15
        reasons.append("壓力偏高")

    # 💻 忙碌
    if work == "忙":
        score -= 15
        reasons.append("辛苦了～工作過於忙碌")

    # 🚶 運動
    if exercise == "沒有":
        score -= 5
        reasons.append("可以適當稍微的活動一下")

    # 🌙 睡眠時間
    if sleep_before_11 == "否":
        score -= 20
        reasons.append("晚睡（在11PM前上床關燈睡覺/不滑手機📱）")

    # 🔒 防止負分
    if score < 0:
        score = 0

    return score, reasons

# =====================
# ▶️ 按鈕
# =====================

if st.button("🧠 生成今日AI健康報告"):
    score, reasons = ai_score()

    st.subheader("📊 健康分析結果")
    st.metric("今日分數", f"{score}/100")

    # =====================
    # 💧 水量分析
    # =====================
    st.write("---")
    st.subheader("💧 水量分析")
    st.write(f"建議水量：{int(target_water)} cc")
    st.write(f"實際喝水：{water} cc")

    if water < target_water:
        st.warning(f"還差 {int(target_water - water)} cc")

    # =====================
    # ⚖️ 體重分析
    # =====================
    st.subheader("⚖️ 體重分析")
    st.write(f"理想體重：{ideal_weight} kg")
    st.write(f"目前體重：{weight} kg")

    if weight_gap > 0:
        st.warning(f"超過理想體重 {weight_gap:.1f} kg")
    else:
        st.success("已在理想體重範圍內")

    # =====================
    # 🧠 教練語氣
    # =====================

    st.subheader("🔥 AI健康顧問小幫手建議報告")

    if score >= 80:
        st.success("很好，繼續維持 👍")
        st.write("😆你現在的生活習慣已經接近理想狀態。")
    elif score >= 60:
        st.warning("還可以，但要修正習慣")
        st.write("　👣你正在走對方向，但還沒穩定。")
    else:
        st.error("加油喔～需要立即調整生活模式💪")
        st.write("😵你的生活習慣正在拖累健康結果。")

    # =====================
    # ⚠️ 改善建議
    # =====================

    st.subheader("⚠️ 今日最重要改善項目⬇️⬇️（Priority AI Advice）")

    if len(reasons) == 0:
        st.write("🎉 完美！今天沒有主要問題")
    else:
        st.write("👉 最優先改善：")
        st.write("• " + reasons[0])

        st.write("\n📌 其他問題：")
        for r in reasons[1:]:
            st.write("• " + r)