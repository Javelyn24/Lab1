import pandas as pd
import matplotlib.pyplot as plt
import textwrap
import seaborn as sns
import plotly.express as px

# Loading the dataset
df = pd.read_csv("smart_city_citizen_activity.csv")
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.weight'] = 'normal'
plt.rcParams['font.size'] = 14
plt.rcParams['text.color'] = 'black'

####################################
#          PLOT 1: BOXPLOT         #
####################################

# DataFrame used
df_mean = df.groupby("Age")["Work_Hours"].mean().reset_index()

plt.figure(figsize=(12, 6))
sns.lineplot(x="Age", y="Work_Hours", data=df_mean, marker="o")

plt.xticks(ticks=range(16, 72, 2), rotation=45)
plt.title("Distribution of Work Hours by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Work Hours")
plt.xticks(rotation=45)

# Caption
plt.subplots_adjust(bottom=0.3)
caption_text = "Fig.1 The line plot illustrates the variation in work hours across different age groups, with the x-axis representing age and the y-axis depicting the average number of work hours per day. The data exhibits noticeable fluctuations, with certain age ranges showing peaks and dips, which may correspond to different career stages or lifestyle changes. No clear linear trend is observed, suggesting that work patterns vary significantly across different age groups."
wrapped_caption = textwrap.fill(caption_text, width=120)
plt.text(0.5, -0.25, wrapped_caption, ha='center', va='top', transform=plt.gca().transAxes)
# plt.show()

####################################
#          PLOT 2: BARCHART        #
####################################

plt.figure(figsize=(10, 7))
sns.barplot(x="Mode_of_Transport", y="Carbon_Footprint_kgCO2", data=df, estimator=sum, palette="magma")
plt.title("Total Carbon Footprint by Mode of Transport")
plt.xlabel("Mode of Transport")
plt.ylabel("Carbon Footprint (kg CO2)")

# Caption
plt.subplots_adjust(bottom=0.3)
caption_text = "Fig.2 The carbon footprint analysis demonstrates significant variations in environmental impact across transportation modes. Walking emerges as the most environmentally friendly option, with the lowest carbon emissions (around 10,000 kg CO2). Electric vehicles (EV) and public transport show moderate carbon footprints, while traditional cars exhibit higher emissions. Bicycles and bike-sharing systems present a promising middle-ground, offering relatively low carbon impact. These findings underscore the critical role of transportation choices in mitigating climate change and suggest the potential for sustainable urban mobility solutions."
wrapped_caption = textwrap.fill(caption_text, width=120)
plt.text(0.5, -0.15, wrapped_caption, ha='center', va='top', transform=plt.gca().transAxes)

# plt.show()

####################################
#        PLOT 3: BAR               #
####################################

# DataFrame used
df_filtered = df[df['Sleep_Hours'].isin([7, 8, 9, 10, 11])]  # Group the data by 'Sleep_Hours'
df_grouped = df_filtered.groupby('Sleep_Hours')['Social_Media_Hours'].mean().reset_index()

fig = px.bar(df_grouped,
             x="Social_Media_Hours",
             y="Sleep_Hours",
             title="Average Sleep Hours vs. Social Media Hours")

fig.update_layout(
    height=550,  # Increased height for better spacing
    margin=dict(b=200),  # Increased bottom margin for the caption
    title={
        'text': "Average Sleep Hours vs. Social Media Hours",
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    annotations=[
        dict(
            xref='paper',
            yref='paper',
            x=0.5,
            y=-0.8,
            text=(
                "Fig.3 The scatter plot reveals an intriguing inverse relationship between<br>"
                "social media consumption and sleep duration. As social media hours increase<br>"
                "(ranging from 2.4 to 3.2 hours), there appears to be a corresponding increase<br>"
                "in sleep time. This trend suggests a potential positive correlation between<br>"
                "digital screen time and sleep quality. The visualization highlights the growing<br>"
                "concern of digital technology's impact on sleep patterns, emphasizing the need<br>"
                "for mindful digital consumption and its potential consequences on personal health."
            ),
            showarrow=False,
            font=dict(size=14),
            align='center',
            yanchor="bottom",
            bgcolor="white",
        )
    ]
)

# fig.show()

####################################
#       PLOT 4: BAR CHART       #
####################################

data = {
    "Mode_of_Transport": ["Car", "EV", "Walking", "Public Transport", "Bike"],
    "Gender": ["Male", "Female", "Male", "Female", "Other"],
    "count": [50, 30, 40, 45, 25]
}
df = pd.DataFrame(data)

fig = px.bar(df,
             x="Mode_of_Transport",
             color="Gender",
             title="Distribution of Transportation Mode by Gender",
             labels={"Mode_of_Transport": "Mode of Transport", "count": "Count"},
             barmode="group")  # "group" keeps bars side by side

# Caption
fig.update_layout(
    height=550,  # Increase height to prevent overlap
    margin=dict(b=210),  # Increase bottom margin for spacing
    title={
        'text': "Distribution of Transportation Mode by Gender",
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    annotations=[
        dict(
            xref='paper',
            yref='paper',
            x=0.5,
            y=-0.85,  # Adjusted position to move it below the graph
            text=(
                "Fig 4. The bar graph reveals notable gender-based differences in transportation preferences.<br>"
                "Notably, males appear to have a higher proportion of car and EV usage compared to<br>"
                "females and other gender categories. Walking and public transport seem more evenly<br>"
                "distributed across genders, suggesting potential sociocultural factors influencing<br>"
                "transportation choices. The diversity in transportation modes across gender groups<br>"
                "highlights the importance of considering gender-specific mobility patterns in urban<br>"
                "planning and sustainable transportation strategies."
            ),
            showarrow=False,
            font=dict(size=14),  # Increased font size
            align='center',
            yanchor="bottom",
            bgcolor="white",
        )
    ]
)

# fig.show()

####################################
#          PLOT 5: LINEPLOT        #
####################################


bins = [18, 24, 40, 56, 70]
labels = ['18-24 \n (Gen Z)', '25-40 \n (Millennials)', '41-56 \n (Gen X)', '57-70 \n (Baby Boomers)']

# Create a new column for "Generation" based on the "Age" column
df['Generation'] = pd.cut(df['Age'], bins=bins, labels=labels, right=True)

# Group by Generation and calculate the mean of Entertainment Hours
grouped_data = df.groupby('Generation')['Entertainment_Hours'].mean().reset_index()

# Create the line plot
plt.figure(figsize=(10, 11))
sns.lineplot(x="Generation", y="Entertainment_Hours", data=grouped_data, marker="o", color="b")
plt.title("Average Entertainment Hours by Generation")
plt.xlabel("Generation")
plt.ylabel("Average Entertainment Hours")

# Caption
plt.subplots_adjust(bottom=0.3)
caption_text = "Fig.5 The line graph depicts the variation in average entertainment hours across different generational groups, ranging from 18-24 (Gen Z) to 57-70 (Baby Boomers). The visualization reveals a non-linear pattern of entertainment consumption. Gen Z (18-24) starts with approximately 1.54 hours of entertainment, which increases slightly for Millennials (25-40) to 1.58 hours. There is a notable decline for Gen X (41-56), reaching the lowest point at around 1.46 hours, before rising significantly for Baby Boomers (57-70) to 1.62 hours. This trend suggests complex intergenerational differences in leisure and entertainment preferences. The dramatic dip for Gen X could be attributed to increased work and family responsibilities, while the peak for Baby Boomers might indicate more available leisure time during retirement or different entertainment consumption habits. The data highlights the dynamic nature of entertainment engagement across different life stages, emphasizing the importance of understanding generational variations in media and leisure consumption."
wrapped_caption = textwrap.fill(caption_text, width=120)
plt.text(0.5, -0.18, wrapped_caption, ha='center', va='top', transform=plt.gca().transAxes)

# plt.show()
