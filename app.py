import streamlit as st
import PyPDF2
from docx import Document

# دالة البحث داخل PDF
def search_in_pdf(file_obj, search_text):
    results = []
    try:
        # في ستريم ليت نتعامل مع الملف مباشرة كـ Bytes
        reader = PyPDF2.PdfReader(file_obj)
        for page_num, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                lines = text.split('\n')
                for line in lines:
                    if search_text.strip() and search_text.lower() in line.lower():
                        results.append(f"صفحة {page_num + 1}: {line.strip()}")
    except Exception as e:
        return [f"خطأ: {e}"]
    return results

# دالة البحث داخل Word
def search_in_docx(file_obj, search_text):
    results = []
    try:
        doc = Document(file_obj)
        for para in doc.paragraphs:
            if search_text.strip() and search_text.lower() in para.text.lower():
                results.append(para.text.strip())
    except Exception as e:
        return [f"خطأ: {e}"]
    return results

# --- واجهة التطبيق باستخدام Streamlit ---
st.title("بحث القيود (PDF & Word)")
st.write("أدخل الاسم أو جزء منه ليظهر لك السطر كاملاً.")

# 1. رفع الملف
uploaded_file = st.file_uploader("حمل الملف (PDF أو Word)", type=['pdf', 'docx'])

# 2. مربع البحث
search_text = st.text_input("اكتب الاسم للبحث")

# 3. زر البحث والنتائج
if st.button("بحث"):
    if uploaded_file is not None and search_text:
        results = []
        
        # تحديد نوع الملف بناءً على الاسم
        if uploaded_file.name.endswith('.pdf'):
            results = search_in_pdf(uploaded_file, search_text)
        elif uploaded_file.name.endswith('.docx'):
            results = search_in_docx(uploaded_file, search_text)
        
        # عرض النتائج
        if results:
            st.success(f"تم العثور على {len(results)} نتيجة:")
            for res in results:
                st.text(res) # عرض النتيجة كـ نص
                st.markdown("---") # خط فاصل
        else:
            st.warning("لم يتم العثور على الاسم.")
            
    elif not uploaded_file:
        st.error("الرجاء تحميل ملف أولاً.")
    elif not search_text:
        st.error("الرجاء كتابة نص للبحث.")