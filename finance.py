#Verificação que tudo esta importado
import yfinance as yf
acao_d=yf.Ticker("BTC-USD")
ultimo_historico= acao_d.history(period="1mo")
print(acao_d.info)
