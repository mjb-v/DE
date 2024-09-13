import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests

# FastAPI URL
API_URL = "http://127.0.0.1:8000/docs#/default/"

# GET
def get_production_data():
    response = requests.get(f"{API_URL}/get_plans_plans__get")
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        st.error("백엔드에서 데이터를 가져오는 데 실패했습니다.")
        return pd.DataFrame()

# POST
def create_production_plan(data):
    response = requests.post(f"{API_URL}/create_plan_plans__post", json=data)
    if response.status_code == 200:
        st.success("데이터가 성공적으로 저장되었습니다!")
    else:
        st.error("데이터 저장에 실패했습니다.")

def page1_view():
    st.title("생산계획관리")
    tab = st.sidebar.selectbox("생산계획관리", ["생산계획관리조회", "생산계획등록/수정"])

    # 1. 생산계획 관리 페이지
    if tab == "생산계획관리조회":
        df = get_production_data()

        if not df.empty:
            columns_to_display = [
                "사업계획", "월간계획", "실적", "사업달성율", 
                "생산계획", "월간생산계획", "생산실적", "생산달성율"
            ]

            # 데이터 정렬 및 가공
            st.subheader("월별 생산 계획 및 실적")
            df_display = df[columns_to_display]
            df_display = df_display.T
            df_display.columns = list(df["월"])
            for col in df_display.columns:
                df_display[col] = df_display[col].apply(lambda x: f"{x:.1f}" if col in ['사업달성율', '생산달성율'] else f"{int(x)}")

            st.table(df_display)

            # 그래프
            st.subheader("월별 달성률 그래프")
            fig, ax = plt.subplots()
            ax.plot(df["월"], df["사업달성율"], label="사업달성율 (%)", marker='o')
            ax.plot(df["월"], df["생산달성율"], label="생산달성율 (%)", marker='o')
            ax.set_xlabel("월")
            ax.set_ylabel("달성률 (%)")
            ax.set_title("월별 달성률")
            ax.legend()
            st.pyplot(fig)

    # 2. 생산계획 등록 페이지
    elif tab == "생산계획등록/수정":
        st.subheader("검색 및 조회")
        col1, col2 = st.columns([1, 1])

        with col1:
            search_year = st.selectbox("년도 선택", options=list(range(2014, 2100)), index=10)
        with col2:
            search_month = st.selectbox("월 선택", options=list(range(1, 13)))
        search_item_code = st.text_input("품번 입력")
        search_category = st.selectbox("종류 선택", options=["가전", "건조기", "세탁기"])

        if st.button("검색"):
            params = {
                "year": search_year,
                "month": search_month,
                "item_code": search_item_code,
                "category": search_category
            }
            response = requests.get(f"{API_URL}/search_production_plan", params=params)
            if response.status_code == 200:
                search_results = pd.DataFrame(response.json())
                st.table(search_results)
            else:
                st.error("검색에 실패했습니다.")

        st.subheader("생산계획 등록/수정")
        new_item_code = st.text_input("품번 입력 (등록)")
        new_item_name = st.text_input("품명 입력 (등록)")
        col3, col4 = st.columns([1, 1])
        with col3:
            new_year = st.selectbox("년도 선택 (등록)", options=list(range(2014, 2100)), index=10)
        with col4:
            new_month = st.selectbox("월 선택 (등록)", options=list(range(1, 13)))
        new_category = st.selectbox("종류 선택 (등록)", options=["가전", "건조기", "세탁기"])

        if st.button("저장"):
            new_data = {
                "item_code": new_item_code,
                "item_name": new_item_name,
                "year": new_year,
                "month": new_month,
                "category": new_category
            }
            create_production_plan(new_data)
