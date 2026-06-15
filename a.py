import streamlit as st
import pandas as pd
import base64
import os

# --- 페이지 설정 ---
st.set_page_config(page_title="SKIN CHEMI - 성분 궁합 솔루션", layout="wide")

# --- 데이터 로드 함수 ---
@st.cache_data
def load_data():
    try:
        df_ingredients = pd.read_excel('화장품 성분 총합.xlsx')
        product_dict = df_ingredients.groupby('상품명')['성분'].apply(lambda x: [str(i).strip() for i in x]).to_dict()
        df_clash = pd.read_excel('성분 충돌 데이터 + 사용 팁.xlsx')
        return product_dict, df_clash
    except Exception as e:
        st.error(f"데이터 로드 중 오류가 발생했습니다. 파일 이름과 위치를 확인해주세요.\n{e}")
        return {}, pd.DataFrame()

# --- 배경 이미지 설정 함수 ---
def set_background(image_file):
    if os.path.exists(image_file):
        with open(image_file, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url(data:image/jpeg;base64,{encoded_string});
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            header {{background-color: transparent !important;}}
            </style>
            """,
            unsafe_allow_html=True
        )

# --- 이미지 HTML 생성 함수 ---
def get_image_html(prod_name):
    img_path = f"{prod_name}.jpg"
    if os.path.exists(img_path):
        with open(img_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return f'<img src="data:image/jpeg;base64,{b64}" class="product-image" alt="{prod_name}">'
    else:
        return '<div class="no-image">이미지 없음</div>'

# --- CSS 스타일 정의 ---
def local_css():
    st.markdown("""
        <style>
        .main-title {
            text-align: center;
            font-size: 3rem;
            font-weight: 900;
            color: #2e3d86;
            margin-bottom: 0px;
            letter-spacing: 2px;
        }
        .sub-title {
            text-align: center;
            font-size: 1.2rem;
            color: #2e3d86;
            margin-bottom: 40px;
        }

        /* 검색창(Selectbox) UI 커스텀 */
        div[data-baseweb="select"] > div {
            position: relative !important; 
            border-radius: 50px !important; 
            border: 2px solid #E5E7EB !important;
            background-color: white !important;
            padding: 8px 15px 8px 45px !important; 
            min-height: 52px !important; 
            height: auto !important; 
            box-shadow: 0 4px 10px rgba(0,0,0,0.04) !important;
            transition: all 0.2s ease !important;
            cursor: pointer !important;
        }
        
        div[data-baseweb="select"] > div::before {
            content: '';
            position: absolute;
            left: 16px;
            top: 50%;
            transform: translateY(-50%);
            width: 20px;
            height: 20px;
            background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="%239CA3AF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>');
            background-size: contain;
            background-repeat: no-repeat;
            pointer-events: none; 
            z-index: 10;
        }

        div[data-baseweb="select"] > div:hover,
        div[data-baseweb="select"] > div:focus-within {
            border-color: #9CA3AF !important; 
            box-shadow: 0 4px 12px rgba(0,0,0,0.08) !important;
        }
        div[data-baseweb="select"] span {
            font-size: 1.05rem !important;
            color: #4B5563 !important;
            font-weight: 500 !important;
            white-space: normal !important; 
            overflow: visible !important;
            text-overflow: clip !important;
            line-height: 1.4 !important;
        }
        ul[role="listbox"] li span {
            white-space: normal !important;
            word-break: keep-all !important;
            line-height: 1.4 !important;
        }
        
        .product-card {
            background-color: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            text-align: center;
            height: 100%;
        }
        
        .product-image {
            width: 140px;
            height: 140px;
            object-fit: contain;
            margin: 0 auto 15px auto;
            display: block;
            border-radius: 8px;
            background-color: #ffffff;
        }
        .no-image {
            width: 140px;
            height: 140px;
            background-color: #f3f4f6;
            color: #9ca3af;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 15px auto;
            border-radius: 8px;
            font-size: 0.9rem;
        }
        
        .product-name {
            font-size: 1.3rem;
            font-weight: 700;
            color: #1f2937;
            margin-bottom: 20px;
        }

        /* 성분 컨테이너 */
        .ingredient-container {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            justify-content: center;
            margin-bottom: 15px;
        }
        
        /* 성분 태그 기본 둥근 디자인 */
        .ingredient-tag {
            background-color: #F3F4F6; 
            border: 1px solid #E5E7EB; 
            border-radius: 50px; 
            padding: 6px 16px;
            font-size: 0.9rem;
            font-weight: 500;
            color: #4B5563; 
            box-shadow: 0 1px 2px rgba(0,0,0,0.03);
            display: inline-block;
            position: relative;
        }
        
        /* HTML5 아코디언 로직 */
        .ingredient-details {
            display: flex;
            flex-direction: column;
            width: 100%;
            margin-top: 5px;
        }
        
        .extra-ing-container {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            justify-content: center;
            order: 1; 
            margin-bottom: 8px;
        }
        
        .ingredient-details summary {
            order: 2; 
            list-style: none;
            display: inline-block;
            margin: 0 auto;
            background-color: #E0F2FE; 
            border: 1px solid #BAE6FD;
            color: #0369A1; 
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .ingredient-details summary::-webkit-details-marker { display: none; }
        .ingredient-details summary:focus { outline: none; }
        .ingredient-details summary:hover { background-color: #BAE6FD; transform: translateY(-1px); }
        
        /* 텍스트 동적 변경 */
        .summary-text::before { content: "자세히보기 ▼"; }
        details[open] .summary-text::before { content: "접기 ▲"; }

        /* 경고 타이틀 (박스 바깥쪽, 왼쪽 정렬) */
        .warning-title {
            color: #D32F2F;
            font-size: 1.3rem;
            font-weight: bold;
            text-align: left; 
            margin-top: 40px; 
            margin-bottom: 10px; 
            padding-left: 5px;
        }

        /* ✨ 경고 카드 디자인 (여러개 로드 시 간격 추가) ✨ */
        .warning-card {
            background-color: #EEEEEE;
            border: 1px solid #D32F2F;
            border-radius: 15px;
            padding: 25px;
            margin-top: 0px; 
            margin-bottom: 20px; /* 여러 박스가 겹치지 않도록 아래 여백 추가 */
            text-align: left; 
        }
        
        /* 충돌 궁합 성분명 (박스 안쪽, 왼쪽 정렬) */
        .warning-ingredients {
            text-align: left; 
            font-size: 1.6rem; 
            font-weight: 900;
            color: #111;
            margin-bottom: 15px;
            letter-spacing: -0.5px;
        }
        .warning-reason {
            color: #555;
            font-size: 1rem;
            margin-bottom: 10px;
        }
        .warning-tip {
            background-color: #FFEAEA;
            padding: 15px;
            border-radius: 8px;
            color: #D32F2F;
            font-weight: bold;
        }

        /* 찰떡 궁합 UI */
        .perfect-match-card {
            background-color: #F0FDF4; 
            border: 2px solid #BBF7D0;
            border-radius: 15px;
            padding: 30px;
            margin-top: 30px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            display: flex;
            flex-direction: column;
            gap: 12px;
            text-align: left;
        }
        .match-p1 { font-size: 1.4rem; font-weight: 900; color: rgba(22, 101, 52, 1.0); margin-bottom: 5px; letter-spacing: -0.5px; }
        .match-p2 { font-size: 1.15rem; font-weight: 600; color: rgba(31, 41, 55, 0.8); }
        .match-p3 { font-size: 1.05rem; font-weight: 400; color: rgba(55, 65, 81, 0.6); line-height: 1.5; margin-top: 5px; }

        /* 하단 면책 조항 */
        .disclaimer-text {
            color: #DC2626; 
            text-align: center;
            font-size: 0.95rem;
            font-weight: 600;
            margin-top: 30px;
            margin-bottom: 20px;
            letter-spacing: -0.3px;
        }
        </style>
    """, unsafe_allow_html=True)

# --- 메인 실행 로직 ---
def main():
    set_background('배경3.png')
    local_css()

    st.markdown('<div class="main-title">SKIN CHEMI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">AI가 분석하는 화장품 성분 궁합 솔루션</div>', unsafe_allow_html=True)

    product_dict, df_clash = load_data()
    if not product_dict:
        return

    default_option = "사용 중인 화장품을 검색하세요"
    product_list = [default_option] + list(product_dict.keys())

    st.markdown('<div style="margin-bottom: 20px;"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        prod1 = st.selectbox("상품1", product_list, key="search1", label_visibility="collapsed")
    
    with col2:
        prod2 = st.selectbox("상품2", product_list, key="search2", label_visibility="collapsed")

    st.write("---")

    if prod1 != default_option and prod2 != default_option:
        res_col1, res_col2 = st.columns(2)

        # --- 상품 1 영역 ---
        with res_col1:
            ing_list1 = product_dict[prod1]
            tags_html_1 = '<div class="ingredient-container">'
            
            # 1. 기본 성분 5개 렌더링
            for i, ing in enumerate(ing_list1):
                if i < 5:
                    tags_html_1 += f'<div class="ingredient-tag">{ing}</div>'
            
            # 2. 5개가 넘을 경우 HTML5 <details> 태그를 이용해 접기/펼치기 구현
            if len(ing_list1) > 5:
                tags_html_1 += '<details class="ingredient-details">'
                tags_html_1 += '<summary class="ingredient-tag more-tag-btn"><span class="summary-text"></span></summary>'
                tags_html_1 += '<div class="extra-ing-container">'
                for i, ing in enumerate(ing_list1):
                    if i >= 5:
                        tags_html_1 += f'<div class="ingredient-tag">{ing}</div>'
                tags_html_1 += '</div></details>'
            
            tags_html_1 += '</div>'

            card_html_1 = f'''
            <div class="product-card">
                {get_image_html(prod1)}
                <div class="product-name">{prod1}</div>
                {tags_html_1}
            </div>
            '''
            st.markdown(card_html_1, unsafe_allow_html=True)

        # --- 상품 2 영역 ---
        with res_col2:
            ing_list2 = product_dict[prod2]
            tags_html_2 = '<div class="ingredient-container">'
            
            for i, ing in enumerate(ing_list2):
                if i < 5:
                    tags_html_2 += f'<div class="ingredient-tag">{ing}</div>'
            
            if len(ing_list2) > 5:
                tags_html_2 += '<details class="ingredient-details">'
                tags_html_2 += '<summary class="ingredient-tag more-tag-btn"><span class="summary-text"></span></summary>'
                tags_html_2 += '<div class="extra-ing-container">'
                for i, ing in enumerate(ing_list2):
                    if i >= 5:
                        tags_html_2 += f'<div class="ingredient-tag">{ing}</div>'
                tags_html_2 += '</div></details>'
                
            tags_html_2 += '</div>'
            
            card_html_2 = f'''
            <div class="product-card">
                {get_image_html(prod2)}
                <div class="product-name">{prod2}</div>
                {tags_html_2}
            </div>
            '''
            st.markdown(card_html_2, unsafe_allow_html=True)

        # --- 성분 충돌 검사 로직 ---
        clashes_found = []
        col_ing1 = '성분1'
        col_ing2 = '성분 2' if '성분 2' in df_clash.columns else '성분2'
        col_reason = '이유'
        col_tip = '팁 (꼭 함께 쓰고 싶다면)' if '팁 (꼭 함께 쓰고 싶다면)' in df_clash.columns else '팁'

        for index, row in df_clash.iterrows():
            c_ing1 = str(row[col_ing1]).strip()
            c_ing2 = str(row[col_ing2]).strip()
            
            match_case1 = any(c_ing1 in item for item in ing_list1) and any(c_ing2 in item for item in ing_list2)
            match_case2 = any(c_ing2 in item for item in ing_list1) and any(c_ing1 in item for item in ing_list2)
            
            if match_case1 or match_case2:
                clashes_found.append({
                    'ing1': c_ing1,
                    'ing2': c_ing2,
                    'reason': row[col_reason],
                    'tip': row[col_tip]
                })

        # --- 분석 결과 UI 출력 ---
        if clashes_found:
            # ✨ 타이틀은 반복문 바깥에서 단 한 번만 출력되도록 수정 ✨
            st.markdown('<div class="warning-title">⚠️ 주의가 필요한 성분 조합</div>', unsafe_allow_html=True)
            
            for clash in clashes_found:
                st.markdown(f"""
                <div class="warning-card">
                    <div class="warning-ingredients">{clash['ing1']} ❌ {clash['ing2']}</div>
                    <div class="warning-reason">{clash['reason']}</div>
                    <div class="warning-tip">💡 <b>TIP:</b> {clash['tip']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="perfect-match-card">
                <div class="match-p1">✅ 함께 발라도 안전해요! (성분 충돌 없음)</div>
                <div class="match-p2">이 두 가지 화장품은 서로 부딪히는 성분이 없어요.</div>
                <div class="match-p3">💡 평소 스킨케어 하시던 대로 묽은 제형부터 차례대로 흡수시켜 주시면 됩니다.</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="disclaimer-text">
            본 분석 결과는 보편적인 성분 데이터를 기반으로 제공되는 참고용 정보이며, 개인의 피부 상태에 따라 차이가 있을 수 있습니다.
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
