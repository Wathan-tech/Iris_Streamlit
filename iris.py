import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

# --- ตั้งค่าหน้าเว็บ ---
st.set_page_config(
    page_title="ระบบจำแนกสายพันธุ์ดอกไอริส (Iris Classification)",
    page_icon="🌸",
    layout="wide"
)

# --- โหลดข้อมูลและฝึกโมเดล (Cache ไว้เพื่อความเร็ว) ---
@st.cache_data
def load_data():
    iris = load_iris()
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    df['target'] = iris.target
    df['species'] = df['target'].map({0: 'setosa', 1: 'versicolor', 2: 'virginica'})
    return iris, df

@st.cache_resource
def train_model(X, y):
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

iris, df = load_data()
model = train_model(df[iris.feature_names], df['target'])

# --- ส่วนหัวของหน้าเว็บ ---
st.title("🌸 การจำแนกสายพันธุ์ดอกไอริส (Iris Flower Prediction)")
st.markdown("เว็บแอปพลิเคชันพยากรณ์สายพันธุ์ดอกไอริสด้วย **Machine Learning (Random Forest)**")

# --- แถบด้านข้าง (Sidebar): รับค่าจากผู้ใช้ ---
st.sidebar.header("⚙️ กำหนดค่าคุณลักษณะ (Features)")

def user_input_features():
    sepal_length = st.sidebar.slider(
        "Sepal Length (ซม.)",
        min_value=float(df['sepal length (cm)'].min()),
        max_value=float(df['sepal length (cm)'].max()),
        value=5.4,
        step=0.1
    )
    sepal_width = st.sidebar.slider(
        "Sepal Width (ซม.)",
        min_value=float(df['sepal width (cm)'].min()),
        max_value=float(df['sepal width (cm)'].max()),
        value=3.4,
        step=0.1
    )
    petal_length = st.sidebar.slider(
        "Petal Length (ซม.)",
        min_value=float(df['petal length (cm)'].min()),
        max_value=float(df['petal length (cm)'].max()),
        value=1.5,
        step=0.1
    )
    petal_width = st.sidebar.slider(
        "Petal Width (ซม.)",
        min_value=float(df['petal width (cm)'].min()),
        max_value=float(df['petal width (cm)'].max()),
        value=0.2,
        step=0.1
    )
    
    data = {
        'sepal length (cm)': sepal_length,
        'sepal width (cm)': sepal_width,
        'petal length (cm)': petal_length,
        'petal width (cm)': petal_width
    }
    return pd.DataFrame(data, index=[0])

input_df = user_input_features()

# --- ส่วนแสดงผลหลัก ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📋 ค่าที่คุณป้อนเข้ามา")
    st.dataframe(input_df, use_container_width=True)

    # พยากรณ์
    prediction = model.predict(input_df)[0]
    prediction_proba = model.predict_proba(input_df)[0]
    predicted_species = iris.target_names[prediction]

    # แสดงผลลัพธ์
    st.subheader("🎯 ผลการทำนาย")
    st.success(f"สายพันธุ์ที่ทำนายได้คือ: **Iris-{predicted_species.capitalize()}**")

    # แสดงความน่าจะเป็น
    proba_df = pd.DataFrame(
        prediction_proba,
        index=[name.capitalize() for name in iris.target_names],
        columns=["ความน่าจะเป็น (Probability)"]
    )
    st.bar_chart(proba_df)

with col2:
    st.subheader("📊 ตำแหน่งของข้อมูลเทียบกับชุดข้อมูลเดิม")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.scatterplot(
        data=df,
        x='petal length (cm)',
        y='petal width (cm)',
        hue='species',
        palette='Set2',
        ax=ax
    )
    # แสดงจุดที่ผู้ใช้เลือก
    ax.scatter(
        input_df['petal length (cm)'][0],
        input_df['petal width (cm)'][0],
        color='red',
        s=150,
        marker='X',
        label='ข้อมูลของคุณ'
    )
    ax.set_title("Petal Length vs Petal Width")
    ax.legend()
    st.pyplot(fig)

# --- ส่วนแสดงชุดข้อมูลดิบ ---
with st.expander("🔍 ดูชุดข้อมูล Iris Dataset"):
    st.dataframe(df, use_container_width=True)
    st.write(f"จำนวนข้อมูลทั้งหมด: {len(df)} แถว แบ่งเป็นคลาสละ {len(df)//3} ตัวอย่าง")