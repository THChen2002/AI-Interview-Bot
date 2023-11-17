import openai
from django.conf import settings
from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.shared import Inches, Cm, Pt, RGBColor
from docx.oxml.ns import qn
import os

class ContentsService:
    def __init__():
        openai.api_key = settings.OPENAI_API_KEY
    
    # 取得OPEN AI API對話訊息
    def get_messages(user_prompt):
        messages=[
            {
                "role": "system",
                "content": "#zh-tw You are an excellent interviewee and want to apply for work or school."
            },
            user_prompt
        ]
        return messages
    
    # 取得OPEN AI API回覆訊息
    def get_reply(messages):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=1024, 
            )
            reply = response["choices"][0]["message"]["content"]
        except openai.OpenAIError as err:
            reply = f"發生 {err.error.type} 錯誤\n{err.error.message}"
        return reply
    
    # 取得OPEN AI API回覆訊息(Streaming)
    def get_reply_s(messages):
        try:
            response = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo",
                messages = messages,
                stream = True
            )
            for chunk in response:
                if 'content' in chunk['choices'][0]['delta']:
                    yield chunk["choices"][0]["delta"]["content"]
        except openai.OpenAIError as err:
            reply = f"發生 {err.error.type} 錯誤\n{err.error.message}"

    # 匯出簡歷
    def export_resume(resume):
        # 設定段落格式
        def set_run_font(run, ch_font_name, en_font_name, font_size, bold=False, italic=False, underline=False, font_color=None):
            run.font.name = en_font_name
            run.element.rPr.rFonts.set(qn('w:eastAsia'), ch_font_name)
            run.font.size = Pt(font_size)
            run.font.bold = bold
            run.font.italic = italic
            run.font.underline = underline
            if font_color:
                run.font.color.rgb = font_color

        # 設定路徑      
        template_path = os.path.join(settings.STATICFILES_DIRS[0], 'template.docx')
        output_path = os.path.join(settings.STATICFILES_DIRS[0], 'resume.docx')
        # 載入現有的Word文件
        doc = Document(template_path)
        # 文件的第一個表格
        table = doc.tables[0]
        # 填入數據
        table.cell(1, 2).text = resume['name']
        table.cell(2, 2).text = resume['gender']
        table.cell(1, 4).text = resume['birth_date']
        table.cell(2, 4).text = resume['education']
        table.cell(4, 2).text = resume['email']
        table.cell(5, 2).text = resume['personal_experience']
        table.cell(6, 2).text = resume['skill']
        table.cell(7, 2).text = resume['interest']
        table.cell(9, 0).text = resume['self_introduction']

        # 遍歷表格設定樣式
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        set_run_font(run, '標楷體', 'Times New Roman', 12)
                        # Set vertical alignment for cell text
                        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER

        # 保存文件
        doc.save(output_path)

        return output_path