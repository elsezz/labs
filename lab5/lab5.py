import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

# налаштовуємо сторінку
st.set_page_config(page_title="Лабораторна 5", layout="wide")

# завантаження даних з лаби 2
@st.cache_data
def load_data():
    DATA_DIR = "vhi_data"
    
# перевірка наявності папки з даними
    if not os.path.exists(DATA_DIR):
        st.error(f"Папку '{DATA_DIR}' не знайдено! Будь ласка, переконайтеся, що файли з Лабораторної 2 знаходяться у цій папці поруч зі скриптом.")
        return pd.DataFrame()

    NOAA_TO_UA = {
        1: "Черкаська", 2: "Чернігівська", 3: "Чернівецька", 4: "Кримська",
        5: "Дніпропетровська", 6: "Донецька", 7: "Івано-Франківська", 8: "Харківська",
        9: "Херсонська", 10: "Хмельницька", 11: "Київська", 12: "Київ (місто)",
        13: "Кіровоградська", 14: "Луганська", 15: "Львівська", 16: "Миколаївська",
        17: "Одеська", 18: "Полтавська", 19: "Рівненська", 20: "Севастополь",
        21: "Сумська", 22: "Тернопільська", 23: "Закарпатська", 24: "Вінницька",
        25: "Волинська", 26: "Запорізька", 27: "Житомирська",
    }

    frames = []
    for fname in sorted(os.listdir(DATA_DIR)):
        if not fname.endswith(".csv"):
            continue

        noaa_id = int(fname.split("_")[1])
        fpath = os.path.join(DATA_DIR, fname)

        try:
            df = pd.read_csv(fpath, header=1, index_col=False)
        except Exception:
            continue

# очищення даних
        df.columns = df.columns.str.replace(r'<[^>]+>', '', regex=True).str.strip().str.upper()

        if "YEAR" not in df.columns:
            continue

        needed = ["YEAR", "WEEK", "VCI", "TCI", "VHI"]
        df = df[[c for c in needed if c in df.columns]]

        for col in needed:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df.dropna(subset=["YEAR", "WEEK", "VHI"])
        df = df[df["VHI"] != -1]

        df["noaa_id"] = noaa_id
        df["region"] = NOAA_TO_UA.get(noaa_id, "Невідома")

        frames.append(df)

    if not frames:
        return pd.DataFrame()

    final_df = pd.concat(frames, ignore_index=True)
    final_df['YEAR'] = final_df['YEAR'].astype(int)
    final_df['WEEK'] = final_df['WEEK'].astype(int)
    
# фільтруємо помилкові тижні 
    final_df = final_df[final_df['WEEK'] <= 52]
    
    return final_df

df = load_data()

# якщо дані не завантажились, зупиняємо виконання
if df.empty:
    st.stop()

# ініціалізація стану для роботи кнопки ресет
defaults = {
    'selected_index': 'VHI',
    'selected_region': sorted(df['region'].unique())[0],
    'week_range': (1, 52),
    'year_range': (int(df['YEAR'].min()), int(df['YEAR'].max())),
    'sort_asc': False,
    'sort_desc': False
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

def reset_filters():
    """Скидання всіх фільтрів до початкових значень"""
    for key, value in defaults.items():
        st.session_state[key] = value

# інтерфейс: 2 колонки
col_filters, col_main = st.columns([1, 3])

with col_filters:
    st.header("Налаштування")
    
    st.selectbox("Оберіть індекс:", ['VCI', 'TCI', 'VHI'], key='selected_index')
    st.selectbox("Оберіть область:", sorted(df['region'].unique()), key='selected_region')
    
    st.slider("Інтервал тижнів:", 1, 52, key='week_range')
    st.slider("Інтервал років:", int(df['YEAR'].min()), int(df['YEAR'].max()), key='year_range')
    
    st.write("Сортування даних:")
    st.checkbox("За зростанням", key='sort_asc')
    st.checkbox("За спаданням", key='sort_desc')
    
    st.button("Скинути фільтри", on_click=reset_filters, type="primary", use_container_width=True)

with col_main:
    st.header("Результати аналізу")
    
# логіка фільтрації
    filtered_df = df[
        (df['region'] == st.session_state.selected_region) &
        (df['YEAR'] >= st.session_state.year_range[0]) &
        (df['YEAR'] <= st.session_state.year_range[1]) &
        (df['WEEK'] >= st.session_state.week_range[0]) &
        (df['WEEK'] <= st.session_state.week_range[1])
    ]
    
# логіка сортування
    if st.session_state.sort_asc and st.session_state.sort_desc:
        st.warning("Обрано обидва типи сортування. Таблиця залишається у хронологічному порядку.")
    elif st.session_state.sort_asc:
        filtered_df = filtered_df.sort_values(by=st.session_state.selected_index, ascending=True)
    elif st.session_state.sort_desc:
        filtered_df = filtered_df.sort_values(by=st.session_state.selected_index, ascending=False)
        
# вкладки табс
    tab1, tab2, tab3 = st.tabs(["Відфільтровані дані", "Графік часового ряду", "Порівняння областей"])
    
    with tab1:
        st.dataframe(filtered_df[['YEAR', 'WEEK', 'region', 'VCI', 'TCI', 'VHI']], 
                     use_container_width=True, hide_index=True)
        
    with tab2:
        plot_df = filtered_df.copy()
        plot_df['Час'] = plot_df['YEAR'].astype(str) + " - Тиждень " + plot_df['WEEK'].astype(str)
# для графіка завжди сортуємо хронологічно, незалежно від налаштувань таблиці
        plot_df = plot_df.sort_values(['YEAR', 'WEEK'])
        
        if not plot_df.empty:
            fig_line = px.line(
                plot_df, x='Час', y=st.session_state.selected_index, 
                title=f"Динаміка {st.session_state.selected_index} ({st.session_state.selected_region} область)",
                markers=True
            )
# оновлюю вісь х, щоб вона не була занадто перевантажена
            fig_line.update_xaxes(nticks=10)
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.info("Немає даних для побудови графіка за обраний період.")
            
    with tab3:
# для порівняння беремо дані всіх областей за обраний проміжок часу
        comp_df = df[
            (df['YEAR'] >= st.session_state.year_range[0]) &
            (df['YEAR'] <= st.session_state.year_range[1]) &
            (df['WEEK'] >= st.session_state.week_range[0]) &
            (df['WEEK'] <= st.session_state.week_range[1])
        ]
        
        if not comp_df.empty:
# рахуємо середнє значення для кожної області
            mean_df = comp_df.groupby('region')[st.session_state.selected_index].mean().reset_index()
            
# підсвічуємо область, яка обрана у фільтрах
            mean_df['Виділення'] = np.where(mean_df['region'] == st.session_state.selected_region, 
                                            'Обрана область', 'Інші області')
            mean_df = mean_df.sort_values(by=st.session_state.selected_index, ascending=False)
            
            fig_bar = px.bar(
                mean_df, x='region', y=st.session_state.selected_index, color='Виділення',
                color_discrete_map={'Обрана область': 'crimson', 'Інші області': '#1f77b4'},
                title=f"Середнє значення {st.session_state.selected_index} по областях за вказаний період",
                labels={'region': 'Область'}
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Немає даних для порівняння.")