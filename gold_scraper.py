import urllib.request
import json
from datetime import datetime, timedelta
import csv

def get_gold_prices_1y():
    url = "https://www.koreagoldx.co.kr/api/price/chart/list"
    
    # Calculate today and exactly 1 year ago for the payload
    today = datetime.now()
    one_year_ago = today - timedelta(days=365)
    
    dataDateStart = one_year_ago.strftime('%Y.%m.%d')
    dataDateEnd = today.strftime('%Y.%m.%d')
    
    payload = {
        "srchDt": "1Y",
        "type": "Au",
        "dataDateStart": dataDateStart,
        "dataDateEnd": dataDateEnd
    }
    
    data = json.dumps(payload).encode('utf-8')
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    req = urllib.request.Request(url, data=data, headers=headers)
    
    try:
        print(f"[{dataDateStart} ~ {dataDateEnd}] 한국금거래소 1년치 금 시세 데이터를 수집합니다...")
        with urllib.request.urlopen(req) as response:
            response_text = response.read().decode('utf-8')
            json_data = json.loads(response_text)
            
            records = json_data.get('list', [])
            print(f"총 {len(records)}개의 데이터를 가져왔습니다.")
            return records
            
    except Exception as e:
        print(f"데이터를 가져오는 중 오류가 발생했습니다: {e}")
        return []

def save_to_csv(data, filename="gold_price_1y.csv"):
    if not data:
        print("저장할 데이터가 없습니다.")
        return
    
    # Determine columns from the first row
    keys = data[0].keys()
    
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
        
    print(f"데이터가 성공적으로 '{filename}'에 저장되었습니다.")

if __name__ == "__main__":
    gold_data = get_gold_prices_1y()
    
    if gold_data:
        # Example of printing first 5 records
        print("\n최근 5건 데이터 미리보기:")
        for record in gold_data[:5]:
            print(f"날짜: {record.get('date')} | 살때 순금: {record.get('s_pure')} | 팔때 순금: {record.get('p_pure')}")
        
        save_to_csv(gold_data)
