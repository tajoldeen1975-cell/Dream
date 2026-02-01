import streamlit as stimport gradio as gr
import PyPDF2
from docx import Document
import os

def search_in_pdf(file_obj, search_text):
    results = []
    try:
        with open(file_obj.name, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    lines = text.split('\n')
                    for line in lines:
                        if search_text.strip() and search_text.lower() in line.lower():
                            results.append(line.strip())
    except Exception as e:
        return [f"خطأ: {e}"]
    return results

def search_in_docx(file_obj, search_text):
    results = []
    try:
        doc = Document(file_obj.name)
        for para in doc.paragraphs:
            if search_text.strip() and search_text.lower() in para.text.lower():
                results.append(para.text.strip())
    except Exception as e:
        return [f"خطأ: {e}"]
    return results

def gradio_search_files(file, search_text):
    if not file or not search_text:
        return "الرجاء اختيار ملف وكتابة نص للبحث"

    file_path = file.name
    ext = os.path.splitext(file_path)[1].lower()
    results = []

    if ext == '.pdf':
        results = search_in_pdf(file, search_text)
    elif ext == '.docx':
        results = search_in_docx(file, search_text)
    else:
        return "خطأ: صيغة الملف غير مدعومة."

    if results:
        return "\n".join(results)
    else:
        return "لم يتم العثور على الاسم."

# واجهة التطبيق
iface = gr.Interface(
    fn=gradio_search_files,
    inputs=[
        gr.File(label="حمل الملف (PDF أو Word)"),
        gr.Textbox(label="اكتب الاسم للبحث")
    ],
    outputs=gr.Textbox(label="النتيجة", lines=5, show_copy_button=True),
    title="بحث القيود",
    description="أدخل الاسم أو جزء منه ليظهر لك السطر كاملاً."
)

iface.launch()