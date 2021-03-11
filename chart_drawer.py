import plotly.graph_objects as go
import plotly.express as px
import stock_analyze as s_a
from plotly.subplots import make_subplots
import pandas as pd
import sql_connector

fig = make_subplots()
df = []


def draw_chart(id):
    sql_connector.query_id(id)
    df = pd.read_csv("stock.csv")
    # trace_1 = go.Line(x=df["日期"], y=df["收盤價"])
    h_text = (
        "日期: "
        + df["日期"]
        + "<br>"
        + "開盤價: "
        + df["開盤價"]
        + "<br>"
        + "最高價: "
        + df["最高價"]
        + "<br>"
        + "最低價: "
        + df["最低價"]
        + "<br>"
        + "收盤價: "
        + df["收盤價"]
        + "<br>"
    )
    trace_2 = go.Candlestick(
        x=df["日期"],
        open=df["開盤價"],
        high=df["最高價"],
        low=df["最低價"],
        close=df["收盤價"],
        increasing_line_color="red",
        decreasing_line_color="green",
    )
    anay = s_a.Stock_Analyze()
    b_list = anay.set_breakpoint(df.loc[:, "收盤價"])
    trace_1 = go.Scatter(x=df["日期"], y=b_list, name="BreakPoint")

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.update_yaxes(tickvals=b_list)
    fig.add_trace(trace_2)
    fig.update_traces(hoverinfo="text", text=h_text, selector=dict(type="candlestick"))
    fig.show()


if __name__ == "__main__":
    draw_chart(1101)