import streamlit as st
import pandas as pd
from openai import OpenAI

# 1️⃣ OpenAI API 키 입력 (네 API 키로 바꿔야 함)
client = OpenAI(api_key="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")

# 2️⃣ CSV 파일 불러오기
data = pd.read_csv("gyeongsangpookdo_edu_problem.csv")

# 3️⃣ 웹사이트 제목
st.title("📊 지역별 교육 취약점 AI 컨설팅 서비스")

# 4️⃣ 사용자 입력 (질문)
user_question = st.text_input("질문을 입력해보세요 (예: 경산시는 어떤 점이 취약해?)")

# 5️⃣ 질문에서 지역 이름 찾기 (데이터 안에 있는 지역명 중 포함된 것 찾기)
if user_question:
    found_region = None
    for region in data["지역"]:
        if region in user_question:
            found_region = region
            break

    if not found_region:
        st.warning("질문에 지역 이름이 포함되어 있지 않아요. 예: '경산시는?' 처럼 지역명을 넣어주세요.")
    else:
        # 6️⃣ 해당 지역 데이터 가져오기
        row = data[data["지역"] == found_region].iloc[0]

        # 7️⃣ 데이터 요약 텍스트 만들기
        summary = (
            f"{found_region}의 교육 지표는 다음과 같습니다:\n"
            f"- 학교당학생수: {row['학교당학생수']}\n"
            f"- 교원1인당학생수: {row['교원1인당학생수']}\n"
            f"- 학급당학생수: {row['학급당학생수']}\n"
            f"- 청소년비율(%): {row['청소년비율(%)']}%\n"
        )

        st.write("🔍 데이터 요약:")
        st.text(summary)

        # 8️⃣ AI에게 요약 기반으로 답변 요청
        prompt = f"""
        너는 교육 전문가야. 다음 데이터를 기반으로 {found_region}의 교육 취약점을 간단하게 분석해줘.
        {summary}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        ai_answer = response.choices[0].message.content

        # 9️⃣ 결과 출력
        st.subheader("🤖 AI 분석 결과:")
        st.write(ai_answer)