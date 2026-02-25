import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from sklearn.linear_model import LinearRegression
import ssl

#0.Anti-ssl error
ssl._create_default_https_context = ssl._create_unverified_context

#1. Call data
url = "your google sheets' url here" # Put your google sheets' .csv url of mood
df = pd.read_csv(url, names = ['Date', 'Time', 'Raw_Emotion'], header = None, sep = ',')

#2. Check sample data
print("---Check Raw Data---")
print(df.head())

#3. Data Frames
df['Emotion'] = df['Raw_Emotion'].str.strip().str.split(' ').str[0]
df['Emoji'] = df['Raw_Emotion'].str.strip().str.split(' ').str[1]
emoji_text = " ".join(df['Emoji'].dropna())   #Protecting Emoji characters
df['Timestamp'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
mapping = {'Excited':3, 'Happy': 2, 'Peace':1, 'Tired':0, 'Anxious':-1, 'Angry':-2}  # You can score mood as you want (The larger scale is, the more dramatic graph becomes)
df['Score'] = df['Emotion'].map(mapping)
df['Diff'] = df['Score'].diff() 
df['Abs_Diff'] = df['Diff'].abs()

#4. Draw bar chart & Array by frequency
sns.countplot(data=df, x='Emotion', hue = 'Emotion', palette='pastel', order=df['Emotion'].value_counts().index, legend = False)
plt.title('Mood I felt most', fontsize=15)
plt.xlabel('Mood', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.show()

#5. Draw Time Series graph
plt.figure(figsize=(12, 5))
plt.plot(df['Timestamp'], df['Score'], marker='o', linestyle='-', color='skyblue')
plt.axhline(0, color='gray', linestyle='--', alpha=0.5)  #line score 0 : baseline
plt.title('Mood over Time', fontsize=15)
plt.ylabel('Mood Score', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout
plt.show()

#6. Preparing axises & Fitting model
df = df.reset_index()
X = df[['index']]
Y = df['Score']
model = LinearRegression()
model.fit(X, Y)
Y_pred = model.predict(X)

#7. Interpretation
if model.coef_[0] > 0 :
    print(f"Regression analysis shows a steady upward trend in your mood by {model.coef_[0]:.4f} over time. Good job!")
else:
    print(f"Regression analysis shows a steady downward trend in your mood over time. Let's hang in there!")

#8. Draw Linear Regression line
plt.figure(figsize=(10, 5))
plt.scatter(X, Y, color = 'gray', label = 'Real Mood')  # Dots of data
plt.plot(X, Y_pred, color = 'red', linewidth=2, label='Regression Line of Mood')  # Regression line
plt.title(f'Mood Trends (slope: {model.coef_[0]:.4f})', fontsize=15)
plt.xlabel('Flow of Time(Order of Records)', fontsize=12)
plt.ylabel('Score of Mood', fontsize=12)
plt.legend()
plt.show()

#9. Set WordCloud
wc_emoji = WordCloud(width=800, height=400, background_color='black', regexp=r"\S+",
min_font_size=10, max_font_size=300, relative_scaling=1, margin=1).generate(emoji_text)

#10. Draw WordCloud
plt.figure(figsize=(10, 5))
plt.imshow(wc_emoji, interpolation='bilinear')
plt.axis('off')
plt.tight_layout(pad=0)
plt.title('Clouds of My Moods', fontsize=15, color='white')
plt.show()

#13. Volatility Analysis
sd_score = df['Score'].std()
avg_swing = df['Abs_Diff'].mean()

print(f"--- Volatility Analysis ---")
print(f"1. Standard Deviation (SD): {sd_score:.2f}")
print(f"2. Average Mood Swing: {avg_swing:.2f}")

#14. Draw Volatility chart (VIX)
plt.figure(figsize=(12, 5))
plt.plot(df.index, df['Diff'], marker='x', linestyle='--', color='orange', label='Mood Swing (diff)')
plt.axhline(0, color='gray', linestyle='-')
plt.fill_between(df.index, df['Diff'], color='orange', alpha=0.2)
plt.title('Daily Mood Swings (Volatility)', fontsize=15)
plt.ylabel('Score Change', fontsize=12)
plt.legend()
plt.show()
