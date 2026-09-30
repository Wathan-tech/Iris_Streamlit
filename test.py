import streamlit as st

# หัวข้อหน้าเว็บ
st.title("แอปเครื่องคิดเลขอย่างง่าย")

# ช่องกรอกตัวเลข
num1 = st.number_input("กรอกตัวเลขตัวแรก", value=100.00, format="%.2f")
num2 = st.number_input("กรอกตัวเลขตัวที่สอง", value=50.00, format="%.2f")

# ตัวเลือกการคำนวณ
operation = st.selectbox(
    "เลือกการดำเนินการ",
    ("บวก (+)", "ลบ (-)", "คูณ (×)", "หาร (÷)")
)

# ปุ่มกดคำนวณผลลัพธ์
if st.button("คำนวณ"):
    if operation == "บวก (+)":
        result = num1 + num2
        symbol = "+"
    elif operation == "ลบ (-)":
        result = num1 - num2
        symbol = "-"
    elif operation == "คูณ (×)":
        result = num1 * num2
        symbol = "×"
    elif operation == "หาร (÷)":
        if num2 != 0:
            result = num1 / num2
            symbol = "÷"
        else:
            st.error("ข้อผิดพลาด: ไม่สามารถหารด้วยศูนย์ได้")
            result = None

    if result is not None:
        st.success(f"ผลลัพธ์: {num1} {symbol} {num2} = {result}")