import streamlit as st
import pandas as pd
import random
import datetime

# --- ページ設定 ---
st.set_page_config(page_title="プロ野球GMシミュレーター", layout="wide")

# --- セッション状態の初期化（ブラウザを更新してもデータを保持する仕組み） ---
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.date = datetime.date(2026, 2, 1)
    st.session_state.budget = 500000 # 50億円
    st.session_state.wins = 0
    st.session_state.losses = 0
    st.session_state.logs = ["2026年シーズン、キャンプインしました！"]
    
    # 初期選手データの生成（少し能力低め）
    initial_players = []
    names = ["佐藤", "鈴木", "高橋", "田中", "伊藤", "渡辺", "山本", "中村", "小林", "加藤"]
    for i, name in enumerate(names):
        initial_players.append({
            "ID": i,
            "名前": name,
            "年齢": random.randint(18, 35),
            "誕生月": random.randint(1, 12),
            "誕生日": random.randint(1, 28),
            "ミート": random.randint(20, 50),
            "パワー": random.randint(20, 50),
            "ポテンシャル": random.randint(50, 90),
            "年俸": 1000,
            "状態": "1軍"
        })
    st.session_state.roster = pd.DataFrame(initial_players)

# --- 共通ロジック：日付を進める ---
def advance_day():
    st.session_state.date += datetime.timedelta(days=1)
    curr_date = st.session_state.date
    
    # 1. 誕生日チェック
    for idx, row in st.session_state.roster.iterrows():
        if row['誕生月'] == curr_date.month and row['誕生日'] == curr_date.day:
            st.session_state.roster.at[idx, '年齢'] += 1
            st.session_state.logs.append(f"🎂 {curr_date}: {row['名前']}選手が誕生日を迎え、{st.session_state.roster.at[idx, '年齢']}歳になりました！")

    # 2. 試合（適度な確率で発生）
    if 3 <= curr_date.month <= 9 and random.random() < 0.2:
        if random.random() > 0.5:
            st.session_state.wins += 1
            st.session_state.logs.append(f"⚾️ {curr_date}: 試合に勝利しました！")
        else:
            st.session_state.losses += 1
            st.session_state.logs.append(f"⚾️ {curr_date}: 敗戦しました。")

# --- サイドバー：球団情報 ---
st.sidebar.title("🏢 球団フロント室")
st.sidebar.write(f"📅 **日付**: {st.session_state.date}")
st.sidebar.metric("予算", f"{st.session_state.budget}万円")
st.sidebar.write(f"📊 **成績**: {st.session_state.wins}勝 {st.session_state.losses}敗")

if st.sidebar.button("📅 1日進める"):
    advance_day()
    st.rerun()

# --- メイン画面 ---
st.title("⚾️ 本格派GMシミュレーター")

tab1, tab2, tab3 = st.tabs(["📋 選手名鑑", "🤝 補強・ドラフト", "📜 運営ログ"])

with tab1:
    st.subheader("所属選手一覧")
    # 年齢や能力でソートできるように表示
    st.dataframe(st.session_state.roster, use_container_width=True)

with tab2:
    st.subheader("新外国人獲得（ガチャ）")
    st.write("スカウトがアメリカの独立リーグから候補を探してきます。")
    if st.button("新外国人を調査（2000万）"):
        if st.session_state.budget >= 2000:
            st.session_state.budget -= 2000
            new_id = len(st.session_state.roster)
            # 初期能力は少し下げつつ、パワーだけ高い設定
            new_f = {
                "ID": new_id,
                "名前": random.choice(["ゴンザレス", "スミス", "ロドリゲス"]),
                "年齢": random.randint(24, 32),
                "誕生月": random.randint(1, 12),
                "誕生日": random.randint(1, 28),
                "ミート": random.randint(10, 35),
                "パワー": random.randint(70, 95),
                "ポテンシャル": random.randint(40, 70),
                "年俸": 15000,
                "状態": "1軍"
            }
            st.session_state.roster = pd.concat([st.session_state.roster, pd.DataFrame([new_f])], ignore_index=True)
            st.success(f"新外国人 {new_f['名前']} 選手を獲得しました！")
            st.session_state.logs.append(f"🌎 {st.session_state.date}: 新外国人 {new_f['名前']} を獲得。")
        else:
            st.error("予算が足りません。")

with tab3:
    st.subheader("球団運営ログ")
    for log in reversed(st.session_state.logs):
        st.write(log)
