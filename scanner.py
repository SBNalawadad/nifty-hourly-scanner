import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import yfinance as yf
import pandas as pd

stocks = ["RELIANCE.NS", "TCS.NS", "INFY.NS"]

rows = []

for stock in stocks:
    df = yf.download(
        stock,
        interval="1h",
        period="7d",
        progress=False
    )

    if df.empty:
        continue

    # remove incomplete candle
    df = df[:-1]

    last5 = df.tail(5).reset_index()

    for _, r in last5.iterrows():
        rows.append([
            stock.replace(".NS", ""),
            r["Datetime"].strftime("%Y-%m-%d %H:%M"),
            round(r["Open"], 2),
            round(r["High"], 2),
            round(r["Low"], 2),
            round(r["Close"], 2),
            int(r["Volume"])
        ])

df_final = pd.DataFrame(
    rows,
    columns=["Symbol", "Time", "Open", "High", "Low", "Close", "Volume"]
)

html = f"""
<html>
<head>
<title>NIFTY 1H – Last 5 Candles</title>
<style>
body {{ font-family: Arial; padding: 20px; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid #ccc; padding: 8px; text-align: center; }}
th {{ background: #222; color: white; }}
tr:nth-child(even) {{ background: #f2f2f2; }}
</style>
</head>
<body>

<h2>NIFTY – Last 5 Hourly Candles</h2>
<p>Auto updated every hour</p>

{df_final.to_html(index=False)}

</body>
</html>
"""

with open("index.html", "w") as f:
    f.write(html)
