import os
import sys
import requests
import tushare as ts
from datetime import datetime



# 配置参数
TUSHARE_TOKEN = os.getenv('f4c0087186a55b886bdb5357f2ecbed49645621807accbe75b1e99b8')
FEISHU_APP_ID = os.getenv('cli_a819f9a899bed00d')
FEISHU_APP_SECRET = os.getenv('tQCP2GE4BXw0RlQctRS7peUQiAqe1PXG')
FEISHU_APP_TOKEN = os.getenv('JsWqbseLxaktydsnElVcIGCCnLf')
FEISHU_TABLE_ID = os.getenv('tbljZZCk6C97kLkW')

print("===== 环境变量检查 =====")
print(f"TUSHARE_TOKEN: {os.getenv('TUSHARE_TOKEN') is not None}")
print(f"FEISHU_APP_ID: {os.getenv('FEISHU_APP_ID') is not None}")
print(f"FEISHU_APP_SECRET: {os.getenv('FEISHU_APP_SECRET') is not None}")
print(f"FEISHU_APP_TOKEN: {os.getenv('FEISHU_APP_TOKEN')}")
print(f"FEISHU_TABLE_ID: {os.getenv('FEISHU_TABLE_ID')}")

# 在 main() 函数开始处添加
def main():
    print("===== 脚本开始执行 =====")
    # 原有代码...
    
    # 在 try/except 块中执行核心逻辑
    try:
        # 原有代码...
    except Exception as e:
        import traceback
        print(f"!!! 发生错误: {str(e)}")
        traceback.print_exc()
        sys.exit(1)  # 确保返回错误代码

def get_feishu_token():
    """获取飞书 tenant_access_token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {"Content-Type": "application/json"}
    payload = {
        "app_id": FEISHU_APP_ID,
        "app_secret": FEISHU_APP_SECRET
    }
    resp = requests.post(url, headers=headers, json=payload).json()
    return resp.get('tenant_access_token')

def add_to_feishu_table(data):
    """添加数据到飞书多维表格"""
    token = get_feishu_token()
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{FEISHU_APP_TOKEN}/tables/{FEISHU_TABLE_ID}/records"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    records = [{"fields": item} for item in data]
    resp = requests.post(url, headers=headers, json={"records": records})
    return resp.json()

def main():
    # 设置 Tushare
    ts.set_token(TUSHARE_TOKEN)
    pro = ts.pro_api()

    # 获取当日涨停股票
    today = datetime.now().strftime("%Y%m%d")
    df = pro.limit_list(trade_date=today, limit_type='U')  # U=涨停
    
    # 格式化数据
    records = []
    for _, row in df.iterrows():
        records.append({
            "股票代码": row['ts_code'],
            "股票名称": row['name'],
            "涨停价": row['close'],
            "涨停日期": today,
            "涨停原因": row['reason']
        })
    
    # 写入飞书
    if records:
        result = add_to_feishu_table(records)
        print(f"Added {len(records)} records: {result}")
    else:
        print("No limit-up stocks today")

if __name__ == "__main__":
    main()
