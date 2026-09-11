import joblib

# 加载已训练好的模型
model = joblib.load('lr_model.pkl')

# 加载标准化器
scaler = joblib.load('scaler.pkl')

# 加载训练时的特征集
feature_columns = joblib.load('feature_columns.pkl')

def predict_swap(x):
    """
    接收已经构建好的交换特征，返回成功概率
    """
    x = x.reindex(columns = feature_columns , fil_value = 0)

    # 使用训练好的 scaler
    x = scaler.transform(x)

    # 预测成功率
    probability = model.predict(x)

    return probability