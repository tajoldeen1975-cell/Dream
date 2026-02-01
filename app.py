import streamlit as st
import os
import gradio as gr
import g4f
import nest_asyncio
import requests

# تطبيق إصلاح مشاكل التزامن
nest_asyncio.apply()

# --- إعداد الأيقونة ---
def get_icon_path():
    try:
        icon_url = "https://cdn-icons-png.flaticon.com/512/4358/4358767.png"
        response = requests.get(icon_url, timeout=2)
        if response.status_code == 200:
            with open("icon.png", "wb") as f:
                f.write(response.content)
            return "icon.png"
    except:
        pass
    return None

app_icon = get_icon_path()

# --- دالة التفسير السريعة ---
def interpret_dream(scholar_choice, dream_text):
    if not dream_text.strip():
        return "يرجى كتابة تفاصيل الحلم أولاً."
    
    if not scholar_choice:
        return "يرجى اختيار المنهج أولاً."

    # إعداد الموجه (Prompt)
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

    # --- محاولة الاتصال السريع (Fast Providers) ---
    # هنا التغيير الجذري: نحدد مزودين سريعين بدلاً من البحث العشوائي
    
    try:
        # المحاولة الأولى: استخدام Blackbox (سريع جداً ومجاني)
        response = g4f.ChatCompletion.create(
            model="gpt-4o",
            provider=g4f.Provider.Blackbox,
            messages=[{"role": "user", "content": prompt}],
        )
        if response: return response
    except:
        pass

    try:
        # المحاولة الثانية: استخدام PollinationsAI (سريع جداً)
        response = g4f.ChatCompletion.create(
            model="gpt-4o",
            provider=g4f.Provider.PollinationsAI,
            messages=[{"role": "user", "content": prompt}],
        )
        if response: return response
    except:
        pass

    try:
        # المحاولة الثالثة: الوضع التلقائي (أبطأ قليلاً لكنه مضمون)
        response = g4f.ChatCompletion.create(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt}],
        )
        return response
    except Exception as e:
        return f"⚠️ عذراً، حدث ضغط على الخوادم المجانية. يرجى المحاولة مرة أخرى.\n(الخطأ: {str(e)})"

# --- التصميم والواجهة ---
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');

body { font-family: 'Amiri', serif !important; background-color: #f4f6f7; }
.gradio-container { font-family: 'Amiri', serif !important; }
h1 { text-align: center; color: #1abc9c; font-family: 'Tajawal', sans-serif; font-size: 2.5em; }
.subtitle { text-align: center; color: #7f8c8d; margin-bottom: 20px; }
.scholar-radio { background: white; padding: 15px; border-radius: 10px; }
#dream_input textarea { direction: rtl; text-align: right; font-size: 18px; border: 2px solid #1abc9c; }
#output_box { direction: rtl; text-align: right; font-size: 18px; background-color: white; padding: 25px; border-radius: 12px; border-right: 5px solid #16a085; line-height: 1.8; }
"""

with gr.Blocks(css=custom_css, theme=gr.themes.Soft(primary_hue="teal"), title="مفسر الأحلام الشامل") as demo:
    
    gr.Markdown("# 🕌 موسوعة تفسير الأحلام الكبرى")
    gr.Markdown("<div class='subtitle'>تفسير دقيق بالذكاء الاصطناعي استناداً لأمهات الكتب</div>")
    
    with gr.Row():
        with gr.Column(scale=4):
            scholar_radio = gr.Radio(
                choices=["التفسير الشامل (الأمثل)", "الإمام الصادق (ع)", "ابن سيرين", "النابلسي", "ابن شاهين"], 
                value="التفسير الشامل (الأمثل)", 
                label="اختر منهج التفسير",
                elem_classes="scholar-radio"
            )
            input_text = gr.Textbox(lines=5, label="تفاصيل الرؤيا", placeholder="اكتب حلمك هنا...", elem_id="dream_input")
            submit_btn = gr.Button("تفسير الرؤيا ✨", variant="primary", size="lg")
        
        with gr.Column(scale=5):
            output_text = gr.Markdown(label="التفسير والتحليل", elem_id="output_box")

    submit_btn.click(fn=interpret_dream, inputs=[scholar_radio, input_text], outputs=output_text)

if app_icon:
    demo.launch(favicon_path=app_icon)
else:
    demo.launch()
