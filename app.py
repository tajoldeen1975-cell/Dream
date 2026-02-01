import streamlit as st
import g4f
import nest_asyncio
import requests

# تطبيق إصلاح مشاكل التزامن
nest_asyncio.apply()

# إعدادات الصفحة
st.set_page_config(
    page_title="مفسر الأحلام الشامل",
    page_icon="🕌",
    layout="centered"
)

# --- تنسيق CSS مخصص للمظهر العربي ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri&family=Tajawal:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    .main-title {
        color: #1abc9c;
        text-align: center;
        font-family: 'Amiri', serif;
        font-size: 3rem;
        margin-bottom: 0px;
    }
    
    .subtitle {
        text-align: center;
        color: #7f8c8d;
        font-size: 1.2rem;
        margin-bottom: 30px;
    }

    .stTextArea textarea {
        direction: rtl;
        text-align: right;
        font-size: 1.1rem;
        border: 2px solid #1abc9c !important;
    }
    
    .interpretation-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        border-right: 8px solid #1abc9c;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        line-height: 1.8;
        font-size: 1.2rem;
        color: #2c3e50;
    }
    </style>
    """, unsafe_allow_html=True)

# --- دالة التفسير ---
def interpret_dream(scholar_choice, dream_text):
    base_instruction = "أنت خبير تفسير أحلام، لغتك عربية فصحى رصينة، تبدأ ببسم الله وتختم بـ 'والله تعالى أعلم'."

    if scholar_choice == "الإمام الصادق (ع)":
        specific_instruction = "تعتمد حصراً على تراث الإمام جعفر الصادق (عليه السلام). ركز على 'الوجوه' والروايات المعتبرة."
    elif scholar_choice == "ابن سيرين":
        specific_instruction = "تعتمد حصراً على منهج ابن سيرين (القياس والدلالات القرآنية)."
    elif scholar_choice == "النابلسي":
        specific_instruction = "تعتمد حصراً على منهج النابلسي (الحالة الاجتماعية والرموز الدقيقة)."
    elif scholar_choice == "ابن شاهين":
        specific_instruction = "تعتمد حصراً على منهج ابن شاهين (تصنيف الرؤيا حسب نوع الرائي)."
    else:
        specific_instruction = "أنت 'المفسر الجامع'. قارن بين المدارس وأعطِ الخلاصة الجامعة."

    prompt = f"{base_instruction}\n{specific_instruction}\nالحلم: '{dream_text}'\nالمطلوب: تفسير دقيق وشامل."

    try:
        # المحاولة الأولى: Blackbox
        response = g4f.ChatCompletion.create(
            model="gpt-4o",
            provider=g4f.Provider.Blackbox,
            messages=[{"role": "user", "content": prompt}],
        )
        if response: return response
    except:
        pass

    try:
        # المحاولة الثانية: PollinationsAI
        response = g4f.ChatCompletion.create(
            model="gpt-4o",
            provider=g4f.Provider.PollinationsAI,
            messages=[{"role": "user", "content": prompt}],
        )
        if response: return response
    except:
        pass

    try:
        # الوضع التلقائي
        response = g4f.ChatCompletion.create(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt}],
        )
        return response
    except Exception as e:
        return f"⚠️ عذراً، الخوادم مشغولة حالياً. يرجى المحاولة بعد لحظات.\n(الخطأ: {str(e)})"

# --- واجهة التطبيق ---
st.markdown('<h1 class="main-title">🕌 موسوعة تفسير الأحلام</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">تفسير بالذكاء الاصطناعي مستند إلى أمهات الكتب</p>', unsafe_allow_html=True)

# تقسيم الشاشة لمدخلات منظمة
col1, col2 = st.columns([1, 1])

with col1:
    scholar = st.selectbox(
        "اختر منهج التفسير:",
        ["التفسير الشامل (الأمثل)", "الإمام الصادق (ع)", "ابن سيرين", "النابلسي", "ابن شاهين"]
    )

input_dream = st.text_area("صف حلمك بالتفصيل:", placeholder="مثلاً: رأيت أنني أمشي في بستان أخضر...", height=150)

if st.button("تفسير الرؤيا ✨", use_container_width=True):
    if not input_dream.strip():
        st.error("الرجاء كتابة الحلم أولاً")
    else:
        with st.spinner('جاري تحليل الرموز والبحث في المصادر...'):
            result = interpret_dream(scholar, input_dream)
            st.markdown("### نتيجة التفسير:")
            st.markdown(f'<div class="interpretation-box">{result}</div>', unsafe_allow_html=True)

# تذييل الصفحة
st.markdown("---")
st.markdown("<p style='text-align: center; color: #95a5a6;'>تم التطوير باستخدام الذاء الاصطناعي - 2024</p>", unsafe_allow_html=True)
