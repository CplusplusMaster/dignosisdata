import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# 파일 경로 설정
input_pdf_path = "data/진단서 양식.pdf"
output_pdf_path = "완성된_진단서_한글5.pdf"
temp_pdf_path = "temp_overlay.pdf"
data_file_path = "data_list.json"  # JSON 데이터 파일 경로

# 한글 폰트 등록 (맑은 고딕 사용)
pdfmetrics.registerFont(TTFont('malgun', 'malgun.ttf'))

# JSON 파일에서 데이터 불러오기
with open(data_file_path, 'r', encoding='utf-8') as file:
    data_list = json.load(file)

# 각 데이터를 PDF로 출력하는 부분
for i, data in enumerate(data_list[:100]): 
    output_pdf_path = f"완성된_진단서_한글_{i+1}.pdf"
    temp_pdf_path = f"temp_overlay_{i+1}.pdf"
    
    # 오버레이 PDF 생성
    c = canvas.Canvas(temp_pdf_path, pagesize=A4)

    # 한글 폰트 설정
    c.setFont("malgun", 9)

    # 데이터 입력
    c.drawString(220, 710, f"{data['동물 소유자']}")
    c.drawString(220, 690, f"{data['주소']}")
    c.drawString(220, 670, f"{data['사육장소']}")
    c.drawString(220, 650, f"{data['종류']}")
    c.drawString(420, 650, f"{data['품종']}")
    c.drawString(290, 630, f"{data['동물명']}")
    c.drawString(420, 630, f"{data['성별']}")
    c.drawString(220, 615, f"{data['연령']}")
    c.drawString(420, 615, f"{data['모색']}")
    c.drawString(220, 600, f"{data['특징']}")
    c.drawString(220, 550, f"{data['병명']}")
    c.drawString(220, 530, f"{data['발병 연월일']}")
    c.drawString(220, 490, f"{data['진단 연월일']}")
    c.drawString(220, 450, f"{data['주요 증상']}")
    c.drawString(220, 420, f"{data['치료명칭']}")
    c.drawString(220, 390, f"{data['입원*퇴원일']}")
    c.drawString(220, 370, f"{data['예후 소견']}")
    c.drawString(220, 340, f"{data['그 밖의 사항']}")
    c.drawString(330, 195, f"{data['년']}")
    c.drawString(420, 195, f"{data['월']}")
    c.drawString(500, 195, f"{data['일']}")
    c.drawString(200, 175, f"{data['동물병원 명칭']}")
    c.drawString(200, 155, f"{data['동물병원 주소']}")
    c.drawString(370, 155, f"{data['전화번호']}")
    c.drawString(220, 130, f"{data['면허번호']}")
    c.drawString(370, 130, f"{data['수의사 성명']}")

    # 오버레이 PDF 저장
    c.save()

    # 기존 PDF에 오버레이 병합
    pdf_reader = PdfReader(input_pdf_path)
    overlay_pdf_reader = PdfReader(temp_pdf_path)
    pdf_writer = PdfWriter()

    # 각 페이지 병합
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        overlay_page = overlay_pdf_reader.pages[0]  # 오버레이는 첫 번째 페이지에만 존재
        page.merge_page(overlay_page)
        pdf_writer.add_page(page)

    # 최종 PDF 생성
    with open(output_pdf_path, "wb") as output_pdf_file:
        pdf_writer.write(output_pdf_file)

    print(f"PDF 파일이 성공적으로 생성되었습니다: {output_pdf_path}")
