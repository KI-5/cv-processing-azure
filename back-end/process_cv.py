# import pdfplumber
# import docx
# import spacy
# import re

# nlp=spacy.load("en_core_web_sm")

# def extract_text_from_pdf(pdf_path):
#     text=""
#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             text+=page.extract_text()+"\n" if page.extract_text() else ""
#     return text.strip()

# def extract_text_from_docx(docx_path):
#     doc=docx.Document(docx_path)
#     return "\n".join([para.text for para in doc.paragraphs]).strip()
# def extract_personal_info(text):
#     doc=nlp(text)
    
#     name=None
#     email=None
#     phone=None

#     for ent in doc.ents:
#         if ent.label_=="PERSON" and not name:
#             name=ent.text
#         if ent.label_=="EMAIL" and not email:
#             email=ent.text

#     phone_match=re.search(r"\+?\d[\d\s\-\(\)]{8,}\d", text)
#     phone=phone_match.group(0) if phone_match else "Unknown"

#     return {
#         "name":name if name else "Unknown",
#         "email":email if email else "Unknown",
#         "phone":phone
#     }

# def extract_sections(text):
#     sections={"Education":[],"Certifications":[],"Projects":[]}
#     current_section=None

#     for line in text.split("\n"):
#         line=line.strip()

#         if re.match(r"(?i)^(Education|Certifications|Projects|Experience|Skills)$",line):
#             current_section=line.lower()

#         elif current_section:
#             if "education" in current_section:
#                 sections["Education"].append(line)
#             elif "certifications" in current_section:
#                 sections["Certifications"].append(line)
#             elif "projects" in current_section:
#                 sections["Projects"].append(line)

#     return {key:[entry for entry in val if entry] for key, val in sections.items()}

# def extract_cv_data(file_path):
#     text=extract_text_from_pdf(file_path) if file_path.endswith(".pdf") else extract_text_from_docx(file_path)
    
#     personal_info=extract_personal_info(text)
#     sections=extract_sections(text)

#     return {
#         "personal_info":personal_info,
#         **sections
#     }
