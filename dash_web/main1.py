import dash
import dash_html_components as html

# 创建 Dash 应用
app = dash.Dash(__name__)

# 示例数据
r2 = 0.85
mse = 0.23
accuracy = 0.92

# 格式化结果
evaluation_result = f"顯示評估結果:\nR^2: {r2:.3f}\nMSE: {mse:.3f}\n容忍度: {accuracy:.3f}\n"

# Dash 布局
app.layout = html.Div([
    html.Pre(evaluation_result, style={'white-space': 'pre-line'})
])

# 运行 Dash 应用
if __name__ == '__main__':
    app.run_server("localhost", 8040,debug=True)