import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

st.write(
    """
    # Rental Bike APP
    By Adnan Cindyana
    """
)

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe
#day
all_data = pd.read_csv("all_data.csv")
hour = pd.read_csv("hour.csv")
day = pd.read_csv("day.csv")

def create_data_grouped_cnt(df):
    data_grouped = df.groupby(by=["mnth_x"]).agg({
        "casual_x": "sum",
        "registered_x": "sum",
        "cnt_x": "sum"
    })
    cnt_x_data = data_grouped["cnt_x"]
    return data_grouped, cnt_x_data
# Assuming you have a DataFrame named 'all_rental'
data_grouped_result, cnt_x_data_result = create_data_grouped_cnt(all_data)
print(data_grouped_result)
print(cnt_x_data_result)

def create_data_permonth(df):
    data_permonth = df.groupby(by=["mnth_x"]).agg({
        "cnt_x": "sum"
    }).reset_index()
    data_permonth = data_permonth.sort_values(by="mnth_x")
    return data_permonth

# Assuming you have a DataFrame named 'all_rental'
data_permonth_result = create_data_permonth(all_data)
print(data_permonth_result)


def create_data_tipeday(df):
    day['day_type'] = 'weekday'
    day.loc[day['holiday'] == 1, 'day_type'] = 'holiday'
    day.loc[(day['holiday'] == 0) & (day['workingday'] == 0), 'day_type'] = 'weekend'

    # Membuat group tipe day
    data_grouped = day.groupby(by=["day_type", "mnth"]).agg({
    "cnt": "sum"
    }).reset_index()


    return create_data_tipeday
# Assuming you have a DataFrame named 'all_rental'
data_tipeday_result = create_data_tipeday(all_data)
print(data_tipeday_result)


#HOUR
def create_rental_hour(df):
    data_rental_hour = df.groupby(by=["hr"]).agg({
        "cnt_y": "sum"
    }).reset_index()
    data_rental_hour = data_rental_hour.sort_values(by="hr")
    return data_rental_hour
# Assuming you have a DataFrame named 'all_rental'
data_rental_hour_result = create_rental_hour(all_data)
print(data_rental_hour_result)


def create_rental_2month(df):
    data_rental_2month = df.groupby(by=["mnth_y"]).agg({
        "cnt_y": "sum"
    }).reset_index()
    data_rental_2month = data_rental_2month.sort_values(by="mnth_y")
    return data_rental_2month
# Assuming you have a DataFrame named 'all_rental'
data_rental_2month_result = create_rental_2month(all_data)
print(data_rental_2month_result)



def create_hour_tipe_day(df):
    df['day_type'] = 'weekday'
    df.loc[df['holiday'] == 1, 'day_type'] = 'holiday'
    df.loc[(df['holiday'] == 0) & (df['workingday'] == 0), 'day_type'] = 'weekend'

    # Membuat group tipe day
    data_grouped = df.groupby(by=["day_type", "hr"]).agg({
        "cnt": "sum"
    }).reset_index()

    return data_grouped
# Assuming you have a DataFrame named 'hour'
data_grouped_result = create_hour_tipe_day(hour)
print(data_grouped_result)


# # Menyiapkan berbagai dataframe
#create_data_grouped_cnt = create_data_grouped_cnt(main_df)
#create_data_permonth = create_data_permonth(main_df)
#create_data_tipeday = create_data_tipeday(main_df)
#create_rental_hour = create_rental_hour(main_df)
#create_rental_2month = create_rental_2month(main_df)
#create_hour_tipe_day = create_hour_tipe_day(main_df)

# plot Frequency Vs Count Total Rental Bike
st.header('Graph Frequency Vs Count Total Rental Bike')
fig, ax = plt.subplots(figsize=(12, 5))

# Menggabungkan data
data_grouped = all_data.groupby(by=["mnth_x"]).agg({
    "casual_x": "sum",
    "registered_x": "sum",
    "cnt_x": "sum"
})
# menggabungkan keseluruhan cnt_x
cnt_x_data = data_grouped["cnt_x"]
ax = plt.hist(cnt_x_data, bins=20, edgecolor='black')
plt.title('Graph Frequency Vs Count Total Rental Bike')
plt.xlabel('Total Rental Bike Including')
plt.ylabel('Frequency')
plt.show()
st.pyplot(fig)


# Plot grafik hubungan bulan dan total rental
st.subheader("Plot grafik hubungan bulan dan total rental")
fig, ax = plt.subplots(figsize=(12, 5))
all_rental_month = all_data.groupby(by=["mnth_x"]).agg({
    "cnt_x": "sum"
}).reset_index()

# Merubah bulan menjadi bulan 1-12
all_rental_month = all_rental_month.sort_values(by="mnth_x")

ax = plt.plot(all_rental_month["mnth_x"], all_rental_month["cnt_x"], marker='o')
plt.title('Total Rental Bike Including per Month')
plt.xlabel('Month')
plt.ylabel('Total Rental Bike Including')
plt.show()
st.pyplot(fig)

# Rental Bike Including based on Day Type and Hour of the Day
st.subheader("Rental Bike Including based on Day Type and Hour of the Day")
# Mmembuat kolom baru untuk tipe day (holiday, weekday, weekend)
day['day_type'] = 'weekday'
day.loc[day['holiday'] == 1, 'day_type'] = 'holiday'
day.loc[(day['holiday'] == 0) & (day['workingday'] == 0), 'day_type'] = 'weekend'

# Membuat group tipe day
data_grouped = day.groupby(by=["day_type", "mnth"]).agg({
    "cnt": "sum"
}).reset_index()

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x="mnth", y="cnt", hue="day_type", data=data_grouped, palette="viridis")
plt.title('Rental Bike Including based on Day Type and Hour of the Day')
plt.xlabel('Month')
plt.ylabel('Total Rental Bike Including')
plt.legend(title="Day Type", loc="upper right")
plt.show()
st.pyplot(fig)

# Total Rental Bike Including per Hour
st.subheader("Total Rental Bike Including per Hour")
# Membuat Group Data
all_rental_month = all_data.groupby(by=["hr"]).agg({
    "cnt_y": "sum"
}).reset_index()

# Merubah bulan menjadi bulan 1-12
all_rental_month = all_rental_month.sort_values(by="hr")
fig, ax = plt.subplots(figsize=(12, 5))
ax = plt.plot(all_rental_month["hr"], all_rental_month["cnt_y"], marker='o')
plt.title('Total Rental Bike Including per Hour')
plt.xlabel('Hour')
plt.ylabel('Total Rental Bike Including')
plt.show()
st.pyplot(fig)


# Total Rental Bike Including for 2 Month
st.subheader("Total Rental Bike Including for 2 Month")
# Membuat Group Data
all_rental_month = all_data.groupby(by=["mnth_y"]).agg({
    "cnt_y": "sum"
}).reset_index()

# gorup data bulan
all_rental_month = all_rental_month.sort_values(by="mnth_y")
fig, ax = plt.subplots(figsize=(12, 5))
ax = plt.plot(all_rental_month["mnth_y"], all_rental_month["cnt_y"], marker='o')
plt.title('Total Rental Bike Including for 2 Month')
plt.xlabel('Month')
plt.ylabel('Total Rental Bike Including')
plt.show()
st.pyplot(fig)


# Rental Bike Including based on Day Type and Hour of the Day
st.subheader("Rental Bike Including based on Day Type and Hour of the Day")
# Mmembuat kolom baru untuk tipe day (holiday, weekday, weekend)
hour['day_type'] = 'weekday'
hour.loc[hour['holiday'] == 1, 'day_type'] = 'holiday'
hour.loc[(hour['holiday'] == 0) & (hour['workingday'] == 0), 'day_type'] = 'weekend'

# Membuat group tipe day
data_grouped = hour.groupby(by=["day_type", "hr"]).agg({
    "cnt": "sum"
}).reset_index()
fig, ax = plt.subplots(figsize=(35, 15))
ax = sns.lineplot(x="hr", y="cnt", hue="day_type", data=data_grouped, palette="viridis")
plt.title('Rental Bike Including based on Day Type and Hour of the Day')
plt.xlabel('Hour')
plt.ylabel('Total Rental Bike Including')
plt.legend(title="Day Type", loc="upper right")
plt.show()
st.pyplot(fig)

st.caption('Copyright © Adnan Cindyana 2023')
