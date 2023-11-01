import openai
from django.conf import settings
from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.shared import Inches, Cm, Pt, RGBColor
from docx.oxml.ns import qn

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
    
    def get_reply(messages):
        try:
            response = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo",
                messages = messages,
            )
            reply = response["choices"][0]["message"]["content"]
        except openai.OpenAIError as err:
            reply = f"發生 {err.error.type} 錯誤\n{err.error.message}"
        return reply
    
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

    def export_resume():
        # 設定段落格式
        def set_run_font(run, ch_font_name, en_font_name, font_size, bold=False, italic=False, underline=False, font_color=None):
            run.font.name = en_font_name # 英文字型
            run.element.rPr.rFonts.set(qn('w:eastAsia'), ch_font_name)  # 中文字型
            run.font.size = Pt(font_size)
            run.font.bold = bold
            run.font.italic = italic
            run.font.underline = underline

            if font_color:
                run.font.color.rgb = font_color
                
        doc = Document()
        doc.add_heading("個人簡歷", 0).alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

        records = (
            ('amos', '12345678', 'teacher'),
            ('carol', '23456789', '學生'),
            ('frank', '34567890', ''),
        )

        
        table = doc.add_table(rows=1, cols=3, style='Table Grid')
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = '姓名'
        hdr_cells[1].text = '電話'
        hdr_cells[2].text = '職稱'

        for name, tel, title in records:
            row_cells = table.add_row().cells
            row_cells[0].text = name
            row_cells[1].text = tel
            row_cells[2].text = title
            for cell in row_cells:
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        set_run_font(run, '標楷體', 'Times New Roman', 12)
                        # Set vertical alignment for cell text
                        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        row_3_cells = table.rows[3].cells
        row_3_cells[1].merge(row_3_cells[2])

        doc.save('resume.docx')