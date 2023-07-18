from datetime import datetime, timedelta, timezone
 
 
def get_date_string(timestamp_file: str) -> str:
    with open(timestamp_file, 'r', encoding='utf-8') as f:
        timestamp = int(f.readline())
    diferenca = timedelta(hours=-3)
    fuso_horario = timezone(diferenca)
    dt = datetime.fromtimestamp(timestamp).astimezone(fuso_horario).strftime("%Y-%m-%d %H:%M:00.000 -0300")
    return dt
