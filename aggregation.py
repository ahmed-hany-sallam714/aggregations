# -------------------------------------------------------
# 💼 مشروع تحليل بيانات Titanic + استخدامات GroupBy في Pandas 💼
#
# الهدف من المشروع:
# - استخدام بيانات Titanic الجاهزة من مكتبة seaborn.
# - تطبيق تحليل إحصائي باستخدام pivot_table.
# - استعراض وشرح استخدام groupby مع apply، aggregate، filter، و transform.
# - تنفيذ بعض الحسابات الإحصائية ومعالجة البيانات بطريقة احترافية.
# -------------------------------------------------------

import numpy as np
import pandas as pd
import seaborn as sns

# -------------------------------------------------------
# 🛳️ تحميل وعرض أول 5 صفوف من بيانات Titanic
# -------------------------------------------------------
titanic = sns.load_dataset("titanic")
print(titanic.head())

# -------------------------------------------------------
# 🔍 إنشاء Pivot Table لمتوسط الأعمار ومتوسط الأجرة (fare)
# حسب الجنس والشخص (who) ومقارنة الطبقات (class) والبقاء على قيد الحياة (alive)
# -------------------------------------------------------
pivot = titanic.pivot_table(
    index=["sex", "who"],                 # الصفوف: الجنس ومن هو الشخص (طفل، رجل، امرأة)
    values=["age", "fare"],               # القيم التي نريد حسابها
    aggfunc={"age": "mean", "fare": "median"},  # نوع الإجراء الإحصائي
    columns=["class", "alive"],           # الأعمدة: الطبقة والبقاء على قيد الحياة
    margins=True                          # يعرض الإجماليات في النهاية
)
print(pivot)

# -------------------------------------------------------
# 📊 إنشاء DataFrame بسيط لتجربة GroupBy
# -------------------------------------------------------
df = pd.DataFrame({
    "key": ["A", "B", "D", "A", "B", "D"],
    "data1": [1, 2, 3, 4, 5, 12],
    "data2": [6, 7, 8, 9, 10, 15]
})

# -------------------------------------------------------
# 🔄 apply_func: لحساب normalized_data1 داخل كل مجموعة
# -------------------------------------------------------
def apply_func(dataframe):
    dataframe = dataframe.copy()  # لحماية الداتا الأصلية من التعديل المباشر
    dataframe["normalized_data1"] = dataframe["data1"] / dataframe["data1"].mean()
    return dataframe

# تطبيق apply_func باستخدام groupby
print(df.groupby("key").apply(apply_func).reset_index(drop=True))

# -------------------------------------------------------
# 📈 aggregate: حساب المتوسط (mean) لكل عمود باستخدام طريقتين
# -------------------------------------------------------
# الطريقة 1: aggregate بدون تحديد الأعمدة
print(df.groupby("key").aggregate([np.mean]))

# الطريقة 2: aggregate مع تحديد دوال مختلفة لكل عمود
print(df.groupby("key").aggregate({
    "data1": np.mean,
    "data2": np.max
}))

# -------------------------------------------------------
# 🚫 filter_func: فلترة المجموعات التي متوسط data1 فيها أقل من 5
# -------------------------------------------------------
def filter_func(dataframe):
    return dataframe["data1"].mean() < 5

# تطبيق filter
print(df.groupby("key").filter(filter_func))

# -------------------------------------------------------
# 🔁 transform_func: تطبيع البيانات داخل كل مجموعة بطرح المتوسط
# -------------------------------------------------------
def transform_func(dataframe):
    return dataframe - dataframe.mean()

# تطبيق transform داخل كل مجموعة
print(df.groupby("key").transform(transform_func))
