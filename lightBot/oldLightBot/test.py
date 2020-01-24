from googletrans import Translator

def main():
  t = Translator()
  tr = t.translate("Hello world!", dest=de)
  print(tr.text)

