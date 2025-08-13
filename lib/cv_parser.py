# lib/cv_parser.py
from PIL import Image
import pytesseract
import fitz  

class CVParser:
    def __init__(self, uploaded_file):
        self.file = uploaded_file
        print(f"--- Yeni dosya işleniyor: {self.file.name} ---")
        self.raw_text = self._extract_text()

    def _extract_text(self):
        file_name = self.file.name
        try:
            if file_name.lower().endswith('.pdf'):
                return self._extract_text_from_pdf()
            elif file_name.lower().endswith(('png', 'jpg', 'jpeg')):
                print("Görüntü dosyası algılandı, OCR başlatılıyor...")
                return self._extract_text_from_image()
            else:
                return "Desteklenmeyen dosya formatı."
        except Exception as e:
            print(f"HATA: '{file_name}' dosyası işlenirken bir istisna oluştu: {e}")
            return f"HATA: '{file_name}' dosyası işlenemedi."

    def _extract_text_from_image(self, image_data=None):
        """Görüntüden veya görüntü verisinden metin çıkarır."""
        try:
            image = image_data if image_data else Image.open(self.file)
            text = pytesseract.image_to_string(image, lang='eng+tur')
            print(f"OCR işlemi tamamlandı. {len(text)} karakter bulundu.")
            return text
        except pytesseract.TesseractNotFoundError:
            print("\n!!! HATA: Tesseract OCR motoru bulunamadı. !!!")
            print("Lütfen Tesseract'in sisteminize kurulu ve PATH'e ekli olduğundan emin olun.")
            return "HATA: Tesseract OCR motoru bulunamadı."
        except Exception as e:
            print(f"Görüntüden metin çıkarırken hata: {e}")
            return "HATA: Görüntü işlenirken bir sorun oluştu."

    def _extract_text_from_pdf(self):
        """PDF'ten metin çıkarır. Metin yoksa OCR denemesi yapar."""
        print("PDF dosyası algılandı, metin katmanı okunuyor...")
        text = ""
        self.file.seek(0)
        
        with fitz.open(stream=self.file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        
            if not text.strip():
                print("PDF'te metin katmanı bulunamadı. Sayfalar için OCR denemesi yapılıyor...")
                for i, page in enumerate(doc):
                    print(f"Sayfa {i+1} OCR işleminde...")
                    pix = page.get_pixmap(dpi=300)  
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    text += self._extract_text_from_image(image_data=img)

        print(f"PDF işlemi tamamlandı. {len(text)} karakter bulundu.")
        return text

    def get_raw_text(self):
        """Çıkarılan ham metni döndürür."""
        print(f"Sonuç: {len(self.raw_text)} karakterlik ham metin AI modeline gönderilecek.")
        return self.raw_text