import streamlit as st
import numpy as np
import pandas as pd
from scipy import stats
import plotly.express as px
from statsmodels.stats.multicomp import pairwise_tukeyhsd # 追加: 多重比較用

# ページ設定
st.set_page_config(page_title="農業データ統計解析入門", layout="wide")

st.title("🌱 新人研修用：農業データ統計解析シミュレーター")
st.markdown("""
このアプリでは、架空の試験データを作成し、**t検定**と**分散分析（F検定）**の仕組みを直感的に学びます。
左のサイドバーから、シミュレーションのパラメータを変更してみましょう。
※スライダーを動かすたびに、データはランダムに再生成されます。
""")

# タブの作成
tab1, tab2, tab3 = st.tabs(["1. t検定（2群の比較）", "2. 分散分析（3群以上の比較）", "3. 統計の基本用語"])

# ==========================================
# タブ1: t検定
# ==========================================
with tab1:
    st.header("🥔 t検定：新系統と標準品種の収量を比較する")
    st.markdown("**帰無仮説（$H_0$）**：「新系統と標準品種の収量に差はない」と仮定します。")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("データ設定")
        n_samples_t = st.slider("サンプルサイズ（株数）", min_value=3, max_value=50, value=10, key="n_t")
        mean_a = st.slider("標準品種の平均収量 (g/株)", 500, 1500, 1000, step=50)
        mean_b = st.slider("新系統の平均収量 (g/株)", 500, 1500, 1100, step=50)
        std_dev = st.slider("データのバラツキ（標準偏差）", 50, 300, 100, step=10, key="std_t")
        
    with col2:
        # データ生成
        data_a = np.random.normal(mean_a, std_dev, n_samples_t)
        data_b = np.random.normal(mean_b, std_dev, n_samples_t)
        
        df_t = pd.DataFrame({
            "品種": ["標準品種"] * n_samples_t + ["新系統"] * n_samples_t,
            "収量 (g)": np.concatenate([data_a, data_b])
        })
        
        # 可視化 (Plotly)
        fig_t = px.box(df_t, x="品種", y="収量 (g)", color="品種", points="all", title="収量データの分布（箱ひげ図）")
        fig_t.update_yaxes(range=[0, 2000]) # Y軸を固定し、バラツキの変化を視覚的に分かりやすく
        st.plotly_chart(fig_t, use_container_width=True)
        
        # t検定の実行（現代の主流である「ウェルチのt検定 (equal_var=False)」）
        t_stat, p_value_t = stats.ttest_ind(data_a, data_b, equal_var=False)
        
        st.subheader("📊 検定結果 (ウェルチのt検定)")
        st.write(f"**t値:** {t_stat:.3f}")
        st.write(f"**p値:** {p_value_t:.4f}")
        
        if p_value_t < 0.05:
            st.success("🎉 **有意差あり (p < 0.05)**：帰無仮説は棄却されました。「新系統と標準品種の収量には有意な差がある」と言えます。")
        else:
            st.warning("🤔 **有意差なし (p >= 0.05)**：帰無仮説は棄却されません。「収量に差があるとは言えない（たまたまのバラツキの範囲内）」という結論になります。")

# ==========================================
# タブ2: 分散分析 (ANOVA)
# ==========================================
with tab2:
    st.header("🌾 分散分析（F検定）：3つの施肥区の収量を比較する")
    st.markdown("**帰無仮説（$H_0$）**：「無施肥区、標準区、多肥区の3つのグループ間で、平均収量に差はない」と仮定します。")
    
    col3, col4 = st.columns([1, 2])
    
    with col3:
        st.subheader("データ設定")
        n_samples_f = st.slider("サンプルサイズ（株数）", min_value=3, max_value=50, value=10, key="n_f")
        mean_c = st.slider("無施肥区の平均収量", 500, 1500, 800, step=50)
        mean_d = st.slider("標準区の平均収量", 500, 1500, 1000, step=50)
        mean_e = st.slider("多肥区の平均収量", 500, 1500, 1050, step=50)
        std_dev_f = st.slider("データのバラツキ（標準偏差）", 50, 300, 150, step=10, key="std_f")

    with col4:
        # データ生成
        data_c = np.random.normal(mean_c, std_dev_f, n_samples_f)
        data_d = np.random.normal(mean_d, std_dev_f, n_samples_f)
        data_e = np.random.normal(mean_e, std_dev_f, n_samples_f)
        
        df_f = pd.DataFrame({
            "処理区": ["無施肥区"] * n_samples_f + ["標準区"] * n_samples_f + ["多肥区"] * n_samples_f,
            "収量 (g)": np.concatenate([data_c, data_d, data_e])
        })
        
        # 可視化 (Plotly)
        fig_f = px.box(df_f, x="処理区", y="収量 (g)", color="処理区", points="all", title="施肥区ごとの収量分布（箱ひげ図）")
        fig_f.update_yaxes(range=[0, 2000]) # Y軸を固定
        st.plotly_chart(fig_f, use_container_width=True)
        
        # 一元配置分散分析の実行
        f_stat, p_value_f = stats.f_oneway(data_c, data_d, data_e)
        
        st.subheader("📊 検定結果 (分散分析)")
        st.write(f"**F値:** {f_stat:.3f}")
        st.write(f"**p値:** {p_value_f:.4f}")
        
        if p_value_f < 0.05:
            st.success("🎉 **有意差あり (p < 0.05)**：少なくとも1つの処理区に有意な差があります！")
            
            # 分散分析で有意差が出た場合のみ、Tukeyの多重比較を自動で実行して表示
            st.markdown("#### 🔍 続けて多重比較 (Tukey法) を実行：具体的にどの区に差があるのか？")
            tukey = pairwise_tukeyhsd(endog=df_f['収量 (g)'], groups=df_f['処理区'], alpha=0.05)
            
            # 結果をデータフレーム化して見やすく表示
            tukey_df = pd.DataFrame(data=tukey._results_table.data[1:], columns=tukey._results_table.data[0])
            tukey_df['reject'] = tukey_df['reject'].map({True: '有意差あり', False: '差なし'})
            tukey_df = tukey_df.rename(columns={'group1': '比較A', 'group2': '比較B', 'meandiff': '平均値の差', 'p-adj': '調整済p値', 'reject': '判定'})
            
            st.dataframe(tukey_df[['比較A', '比較B', '平均値の差', '調整済p値', '判定']], use_container_width=True)
            
        else:
            st.warning("🤔 **有意差なし (p >= 0.05)**：処理区の間に有意な差があるとは言えません。")

# ==========================================
# タブ3: 統計用語の解説
# ==========================================
with tab3:
    st.header("📖 押さえておきたい基礎知識")
    
    st.markdown("### 帰無仮説とは？")
    st.info("「証明したいこと（例：新しい肥料は効果がある）」の逆、「効果がない（差がない）」という仮説のこと。この仮説が**「確率的にあり得ない（珍しい）」**ことを示すことで、間接的に証明したいことを主張する背理法のアプローチです。")
    
    st.markdown("### p値（p-value）とは？")
    st.info("帰無仮説が正しい（本当に差がない）と仮定したとき、今回得られたデータ、あるいはそれ以上に極端なデータが「たまたま偶然」発生する確率のこと。農業分野では一般的に **5%（0.05）** を基準（有意水準）とし、これより小さければ「偶然とは考えにくい＝有意差あり」と判定します。")

    st.markdown("---")
    st.markdown("### 📊 箱ひげ図（Box plot）の見方")
    st.info("""
    本アプリのグラフでも使用されている「箱ひげ図」は、データの**ばらつき（分布）**を視覚的に把握するのに便利なグラフです。
    
    * **箱の真ん中の線**：**中央値（メジアン）**。データを小さい順に並べたときに、ちょうど真ん中にくる値です。（※平均値とは異なる場合があります）
    * **箱の上下の端**：データの**真ん中50%**がこの箱の中に収まっています。箱が縦に長いほど、データのばらつきが大きいことを意味します。
    * **上下に伸びる線（ひげ）**：通常データの範囲を示します。
    * **点（ドット）**：本アプリでは、横に並ぶ点は**実際のデータ1つ1つ（各株の収量など）**を表しています。ひげの外側にある点は「外れ値（極端な値）」とされることもあります。
    
    「平均値」だけでは見えない、現場の「ばらつき具合」や「極端な生育不良・異常発育」がないかを確認するために、農業データの解析では必須のグラフです。
    """)

    st.markdown("---")
    st.markdown("### 💡 2つの「t検定」の違い（スチューデント vs ウェルチ）")
    st.info("""
    統計の教科書やソフトには「t検定」が2種類存在します。本アプリでは実務の標準である**「ウェルチのt検定」**を採用しています。

    **1. スチューデントのt検定（Student's t-test）**
    * **特徴**: 昔から教科書で一番最初に教えられてきた伝統的なt検定です。
    * **弱点**: 比較するA群とB群の**「データのばらつき（分散）が等しい」という厳しい前提条件（等分散性の仮定）**があります。
    * **農業現場での問題点**: 品種が違ったり、施肥量が違ったりすれば、平均値だけでなく「ばらつき方」も変わるのが自然です。前提が崩れた状態でこの検定を使うと、p値を正しく計算できず、間違った結論を出してしまうリスクがあります。

    **2. ウェルチのt検定（Welch's t-test）**
    * **特徴**: スチューデントのt検定を改良したもので、**「データのばらつきが等しくても、異なっていても、どちらでも使える」**万能型のt検定です。
    * **現在の常識**: 事前にばらつきが等しいかどうかを調べる（F検定など）のは手間であり、さらにその事前検定自体にもエラーのリスクがあるため、**「最初から無条件でウェルチのt検定を使う」のが現在の統計学のグローバルスタンダード**です。
    * **実務でのポイント**: 今回のアプリの実装や、R言語の `t.test()` 関数も、デフォルト（初期設定）でこのウェルチのt検定が選ばれるようになっています。
    """)
    
    st.markdown("---")
    st.markdown("### なぜ3群以上の比較でt検定を繰り返してはいけないのか？（検定の多重性）")
    st.error("A, B, Cの3品種があるとき、t検定を「A-B」「B-C」「A-C」と3回繰り返すと、「1回の検定で5%の確率で間違った結論を出すリスク」が雪だるま式に増え、**全体のミスの確率が約15%まで上昇**してしまいます。これを防ぐために、まずは全体を評価する**分散分析（F検定）**を使用します。")

    st.markdown("### 🔍 Tukey（テューキー）検定：全当たりの比較")
    st.success("""
    分散分析で「有意差あり」となった後、**具体的にどのグループ間に差があるか**をすべての組み合わせで調べる手法です。
    農業試験では「標準品種、新系統A、新系統B」の3つを比較して、新系統Aだけが本当に優れているのかを確認する際によく使われます。
    
    **なぜテューキー検定は「安全」なのか？**  
    最大のメリットは、比較する数が増えても**全体のミス（第一種の過誤）の確率を5%以内にピタリと抑えてくれる**点です。
    t検定を繰り返すより、Tukey検定のほうが得られた結果を「科学的な根拠」として安心して報告できます。
    """)

    st.markdown("---")
    st.markdown("### 💻 【参考】R言語での実行スクリプト")
    st.info("""
    実際の研究データ解析で広く使われる「R」でのコード例です。
    アプリで学んだ理論を、実際のデータ解析に当てはめる際のリファレンスとして活用してください。
    """)
    
    st.code("""
# ==========================================
# 1. t検定 (ウェルチのt検定: var.equal = FALSE)
# ==========================================
# data_t: 収量(Yield)と品種(Variety)の列を持つデータフレームと想定
t_result <- t.test(Yield ~ Variety, data = data_t, var.equal = FALSE)

# 結果の表示
print(t_result)


# ==========================================
# 2. 分散分析 (F検定) (3つ以上の処理区の比較)
# ==========================================
# data_f: 収量(Yield)と処理区(Treatment)の列を持つデータフレームと想定
# 処理区はあらかじめ因子型(factor)にしておく必要があります
data_f$Treatment <- as.factor(data_f$Treatment)

anova_model <- aov(Yield ~ Treatment, data = data_f)

# F値とp値の確認
summary(anova_model)


# ==========================================
# 3. Tukey（テューキー）検定 (多重比較)
# ==========================================
# 分散分析のモデル(anova_model)をそのまま使います
tukey_result <- TukeyHSD(anova_model, conf.level = 0.95)

# どのグループ間に差があるかを確認
print(tukey_result)

# 結果をグラフ化して視覚的に安全性を確認
plot(tukey_result)
    """, language="r")
