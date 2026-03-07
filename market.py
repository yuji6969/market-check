import yfinance as yf
import datetime

today = datetime.date.today()
lines = []
lines.append(f"=== 市場チェック {today} ===\n")

def check_stock(ticker, name, currency="$"):
    data = yf.download(ticker, period="1mo", interval="1d", progress=False)
    close = data["Close"].squeeze()
    volume = data["Volume"].squeeze()
    latest = close.iloc[-1]
    prev = close.iloc[-2]
    change = (latest - prev) / prev * 100
    high = close.max()
    low = close.min()
    ma25 = close.rolling(window=25).mean().iloc[-1]
    latest_volume = volume.iloc[-1]
    avg_volume = volume.mean()
    volume_ratio = latest_volume / avg_volume * 100
    if latest > ma25:
        trend = "↑ 上げ局面（25日平均を上回っている）"
    else:
        trend = "↓ 下げ局面（25日平均を下回っている）"
    if currency == "円":
        lines.append(f"【{name}】\n  現在値: {latest:.0f}円\n  前日比: {change:+.2f}%\n  1ヶ月高値: {high:.0f}円 / 安値: {low:.0f}円\n  トレンド: {trend}\n  出来高: 平均比 {volume_ratio:.0f}%\n")
    else:
        lines.append(f"【{name}】\n  現在値: ${latest:.2f}\n  前日比: {change:+.2f}%\n  1ヶ月高値: ${high:.2f} / 安値: ${low:.2f}\n  トレンド: {trend}\n  出来高: 平均比 {volume_ratio:.0f}%\n")

def check_vix():
    data = yf.download("^VIX", period="5d", interval="1d", progress=False)
    close = data["Close"].squeeze()
    latest = close.iloc[-1]
    if latest >= 30:
        comment = "高水準（市場が不安定・調整局面）"
    elif latest >= 20:
        comment = "やや高め（警戒・調整中の可能性）"
    else:
        comment = "落ち着いている（安定局面）"
    lines.append(f"【VIX指数（恐怖指数）】\n  現在値: {latest:.2f}\n  基準: 20以下=安定 / 20〜30=警戒 / 30以上=不安定\n  状態: {comment}\n")

check_stock("^N225", "日経平均", "円")
check_stock("^SOX", "SOX指数（半導体）")
check_stock("NVDA", "エヌビディア(NVDA)")
check_vix()
check_stock("8035.T", "東京エレクトロン(8035)", "円")
check_stock("6146.T", "ディスコ(6146)", "円")
check_stock("9501.T", "東京電力(9501)", "円")

lines.append("=== チェック完了 ===")
print("\n".join(lines))
