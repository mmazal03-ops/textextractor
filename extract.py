import os
from PIL import Image
import pytesseract
from pdf2image import convert_from_path


def extract_and_save_text(file_path):
  try:
    ext = os.path.splitext(file_path)[1].lower()
    full_text = ''

    if ext == '.pdf':
      images = convert_from_path(file_path)
      full_text = ''.join(
          f'\n--- עמוד {i+1} ---\n'
          + pytesseract.image_to_string(img, lang='eng+heb')
          for i, img in enumerate(images)
      )
    elif ext in ['.png', '.jpg', '.jpeg', '.tiff']:
      full_text = pytesseract.image_to_string(
          Image.open(file_path), lang='eng+heb'
      )
    else:
      return False

    # שמירה אוטומטית לקובץ טקסט באותה התיקייה
    output_path = f'{os.path.splitext(file_path)[0]}_extracted.txt'
    with open(output_path, 'w', encoding='utf-8') as f:
      f.write(full_text)
    return True

  except Exception as e:
    print(f'שגיאה בעיבוד הקובץ {file_path}: {e}')
    return False


def process_entire_folder(folder_path):
  """סורק תיקייה שלמה ומחלץ טקסט מכל קבצי ה-PDF והתמונות שבה"""
  if not os.path.exists(folder_path):
    print('התיקייה שצוינה לא קיימת.')
    return

  supported_extensions = ['.pdf', '.png', '.jpg', '.jpeg', '.tiff']
  files = os.listdir(folder_path)

  success_count = 0
  for filename in files:
    ext = os.path.splitext(filename)[1].lower()
    if ext in supported_extensions:
      full_path = os.path.join(folder_path, filename)
      print(f'מעבד: {filename}...')
      if extract_and_save_text(full_path):
        success_count += 1

  print(f'\nסיום! עובדו ונשמרו בהצלחה {success_count} קבצים.')


if __name__ == '__main__':
  # דוגמה להפעלה מול תיקייה:
  # process_entire_folder("C:/path/to/your/folder")
  pass
