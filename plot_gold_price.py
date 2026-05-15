import sys
import subprocess
import os

# 필수 라이브러리 설치 학인 및 설치
def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        print(f"'{package}' 패키지가 필요합니다. 설치를 진행합니다...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_and_import('pandas')
install_and_import('matplotlib')
install_and_import('seaborn')

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

# 한글 폰트 설정 (Windows 전용)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False # 마이너스 기호 깨짐 방지

def generate_charts():
    # 1. 데이터 로드 및 전처리
    print("데이터를 불러오는 중...")
    try:
        df = pd.read_csv('gold_price_1y.csv')
    except Exception as e:
        print(f"데이터를 읽어오는 중 에러 발생: {e}")
        return
        
    df['date'] = pd.to_datetime(df['date'])
    # 날짜 기준으로 오름차순 정렬
    df = df.sort_values('date').reset_index(drop=True)
    df.set_index('date', inplace=True)
    
    # 일별 보간 (혹은 빈 데이터 채우기, 그래프를 부드럽게 그리기 위함)
    # df_daily = df.resample('D').mean().ffill()
    # 우리는 그냥 기존 데이터로 그림
    
    output_files = []

    # 2. 첫 번째 그래프: 1년치 살 때/팔 때 순금 가격 추이 (Line Chart)
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['s_pure'], label='내가 살 때 (순금 3.75g)', color='#e74c3c', linewidth=2)
    plt.plot(df.index, df['p_pure'], label='내가 팔 때 (순금 3.75g)', color='#3498db', linewidth=2)
    plt.title('최근 1년 한국금거래소 순금 가격 추이', fontsize=18, pad=15)
    plt.xlabel('날짜', fontsize=12)
    plt.ylabel('금액 (원)', fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
    plt.tight_layout()
    plt.savefig('gold_trend_1y.png', dpi=300)
    plt.close()
    output_files.append('gold_trend_1y.png')
    print("1. 금값 추세 그래프(gold_trend_1y.png) 생성 완료.")

    # 3. 두 번째 그래프: 월별 평균 금값 (Bar Chart)
    monthly_avg = df.resample('M').mean()
    monthly_avg.index = monthly_avg.index.strftime('%Y-%m')
    
    plt.figure(figsize=(14, 6))
    x_indexes = range(len(monthly_avg))
    width = 0.35
    
    plt.bar([x - width/2 for x in x_indexes], monthly_avg['s_pure'], width=width, label='살 때 평균', color='#ff7675')
    plt.bar([x + width/2 for x in x_indexes], monthly_avg['p_pure'], width=width, label='팔 때 평균', color='#74b9ff')
    
    plt.xticks(ticks=x_indexes, labels=monthly_avg.index, rotation=45)
    plt.title('월별 순금 평균 시세', fontsize=18, pad=15)
    plt.ylabel('금액 (원)', fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
    plt.tight_layout()
    plt.savefig('gold_monthly_avg.png', dpi=300)
    plt.close()
    output_files.append('gold_monthly_avg.png')
    print("2. 월별 평균 금값 그래프(gold_monthly_avg.png) 생성 완료.")

    # 4. 세 번째 그래프: 살 때 가격의 이동평균선 (30일, 60일) (Line Chart)
    daily_df = df.resample('D').mean().ffill()  # 일별 데이터로 리샘플링하여 이평선 계산
    daily_df['MA30'] = daily_df['s_pure'].rolling(window=30).mean()
    daily_df['MA60'] = daily_df['s_pure'].rolling(window=60).mean()

    plt.figure(figsize=(12, 6))
    plt.plot(daily_df.index, daily_df['s_pure'], label='일간 가격', color='lightgrey', alpha=0.8)
    plt.plot(daily_df.index, daily_df['MA30'], label='30일 이동평균', color='#e67e22', linewidth=2)
    plt.plot(daily_df.index, daily_df['MA60'], label='60일 이동평균', color='#2ecc71', linewidth=2)
    
    plt.title('살 때 기준 이동평균선 (30일/60일)', fontsize=18, pad=15)
    plt.xlabel('날짜', fontsize=12)
    plt.ylabel('금액 (원)', fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
    plt.tight_layout()
    plt.savefig('gold_moving_average.png', dpi=300)
    plt.close()
    output_files.append('gold_moving_average.png')
    print("3. 이동평균선 그래프(gold_moving_average.png) 생성 완료.")

    # 5. 네 번째 그래프: 가격 분포도 (Histogram + KDE)
    plt.figure(figsize=(10, 6))
    sns.histplot(df['s_pure'], kde=True, color="#e74c3c", bins=30, label='내가 살 때')
    sns.histplot(df['p_pure'], kde=True, color="#3498db", bins=30, label='내가 팔 때')
    plt.title('최근 1년 순금 가격 분포도', fontsize=18, pad=15)
    plt.xlabel('금액 (원)', fontsize=12)
    plt.ylabel('빈도 수', fontsize=12)
    plt.legend(fontsize=12)
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
    plt.tight_layout()
    plt.savefig('gold_price_distribution.png', dpi=300)
    plt.close()
    output_files.append('gold_price_distribution.png')
    print("4. 가격 분포도 그래프(gold_price_distribution.png) 생성 완료.")

if __name__ == "__main__":
    generate_charts()
    print("모든 시각화 작업이 완료되었습니다!")
