from re import sub


def regex_replacer(value: str) -> str:
  return sub(r"[^a-zA-Zà-úÀ-Ú0-9_\s\.>\(\)\[\]\+\*\-\%\$\#\@\/\:\\]", "", value)
