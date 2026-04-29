import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import numpy as np
import os

# ---------- 页面设置 ----------
st.set_page_config(
    page_title="赵州桥 vs 加尔桥 · 跨时空对话",
    page_icon="🌉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- 中文字体与样式 ----------
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'WenQuanYi Micro Hei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

st.markdown("""
<style>
    .big-title { font-size: 2.4rem; font-weight: 700; color: #3A5F40; text-align: center; }
    .sub-title { font-size: 1.2rem; color: #5A4A3A; text-align: center; margin-bottom: 2rem; }
    .card { background: #F7F3EC; border-left: 6px solid #8B6F47; padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; }
    .caption { color: #6B5744; font-size: 0.9rem; }
    .footer { background: #EAE3D5; padding: 1rem; border-radius: 8px; font-size: 0.8rem; color: #4D3B2C; margin-top: 2rem; }
</style>
""", unsafe_allow_html=True)

# ---------- 定义图片路径 ----------
IMG_COMPARE = "zj_qdb.jpg"  # 两桥全景对比
IMG_GARD_STRUCT = "jeq_gsjg.jpg"  # 加尔桥三层结构标注
IMG_ARCH_COMPARE = "zj_gdb.jpg"  # 敞肩拱与叠层拱示意图
IMG_JEQ_QM="jeq_sang.jpg" #加尔桥今貌
IMG_ZZQ_QJ="zzq_qj.jpg" #赵州桥今貌
# ---------- 数据准备（摘自文档） ----------
# 模块一：工程定位对比
info_data = {
    '对比项': ['地理位置', '建造年代', '建造者', '功能定位', '服务对象'],
    '赵州桥': [
        '河北赵县洨河（隋，约595-605年）',
        '约1420年历史',
        '匠师李春',
        '陆路交通桥',
        '百姓出行、皇家官宦'
    ],
    '加尔桥': [
        '法国加尔省加尔东河（公元1世纪）',
        '输水功能约500年',
        '古罗马工程师（阿格里帕督造）',
        '高架输水渠',
        '尼姆城淡水供给'
    ]
}
df_info = pd.DataFrame(info_data)

# 模块二：结构尺寸
size_data = pd.DataFrame({
    '指标': ['全长 (m)', '主跨/最大拱 (m)', '高度 (m)', '小拱/拱门数'],
    '赵州桥': [64.4, 37.02, 7.23, 4],
    '加尔桥': [269, 24.5, 49, 52]  # 52为全部拱门数（6+11+35）
})

# 模块三：力学特性比较（文字为主）
# 模块四：耐久性考验次数
disaster_data = pd.DataFrame({
    '考验类型': ['大洪水', '战乱', '大地震'],
    '赵州桥': [10, 8, 8],
    '加尔桥': [3, 0, 0]  # 加尔桥无战乱地震记录，洪水记录已知多次
})

# 文物保护级别
heritage_zhao = ["全国重点文物保护单位 (1961)", "ASCE国际土木工程历史古迹 (1991)"]
heritage_gard = ["法国第一批历史古迹 (1840)", "UNESCO世界遗产 (1985)"]

# 模块五：文化影响力雷达图指标
radar_labels = ['民间传说', '教材/票面传播', '民族自豪感', '国际遗产认可', '艺术价值']
zhao_vals = [5, 5, 5, 4, 5]  # 1-5主观相对强度
gard_vals = [3, 4, 3, 5, 4]

# ---------- 侧边栏导航 ----------
with st.sidebar:
    st.markdown("## 🌉 赵州桥 vs 加尔桥")
    st.markdown("**东方匠心与罗马工程的跨时空对话**")
    st.markdown("---")
    nav = st.radio(
        "选择模块",
        ["一、工程定位与背景", "二、核心结构创新", "三、力学智慧",
         "四、耐久性与保护", "五、文化内涵", "六、结语"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    if os.path.exists(IMG_COMPARE):
        st.image(IMG_COMPARE, caption="两桥全景对比", use_container_width=True)

# ---------- 主内容区 ----------
st.markdown('<div class="big-title">赵州桥 vs 加尔桥 · 跨时空对话</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">敞肩坦弧 vs 叠拱输水 —— 两种文明，一种伟大</div>', unsafe_allow_html=True)

# ========== 模块一 ==========
if nav.startswith("一"):
    st.header("一、工程定位与建造背景")
    st.table(df_info.set_index('对比项'))
    st.caption("建造年代跨度对比：赵州桥距今约1420年，加尔桥输水功能约500年，之后废弃。")
    # 甘特图风格时间轴（使用Altair条形图模拟）
    time_data = pd.DataFrame({
        '桥梁': ['赵州桥', '加尔桥(输水期)'],
        '开始(公元)': [595, 40],
        '结束(公元)': [2026, 540]  # 当前年份作为赵州桥延续至今
    })
    time_data['持续年数'] = time_data['结束(公元)'] - time_data['开始(公元)']
    chart = alt.Chart(time_data).mark_bar().encode(
        x='开始(公元)',
        x2='结束(公元)',
        y=alt.Y('桥梁', title=None),
        color=alt.Color('桥梁', legend=None)
    ).properties(title="存世/使用时间对比（公元年份）")
    st.altair_chart(chart, use_container_width=True)

# ========== 模块二 ==========
elif nav.startswith("二"):
    st.header("二、核心结构创新：敞肩拱 vs 叠层拱")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("赵州桥 · 世界首座敞肩圆弧石拱桥")
        st.markdown("""
        - **4个小拱**：减重、泄洪、节约石材
        - **坦拱设计**：矢跨比≈1:5.25，坡度极缓
        - **净跨37.02米**，隋代世界之最
        """)
        if os.path.exists(IMG_ARCH_COMPARE):
            st.image(IMG_ARCH_COMPARE, caption="敞肩拱 vs 叠层拱示意图", use_container_width=True)
    with col2:
        st.subheader("加尔桥 · 三层叠拱输水渠")
        st.markdown("""
        - **三层拱门**：下层6拱、中层11拱、上层35拱
        - **总高约49米**，总长约269米
        - **坡度1/3000**，精密水利工程
        """)
        if os.path.exists(IMG_GARD_STRUCT):
            st.image(IMG_GARD_STRUCT, caption="加尔桥三层结构标注", use_container_width=True)

    st.markdown("---")
    st.subheader("尺寸对比")
    size_melt = size_data.melt(id_vars='指标', var_name='桥梁', value_name='数值')
    bar_chart = alt.Chart(size_melt).mark_bar().encode(
        x=alt.X('指标', title=None),
        y='数值',
        color='桥梁',
        column=alt.Column('指标', title=None, header=alt.Header(labelFontSize=0)),
        tooltip=['桥梁', '数值']
    ).properties(width=100, title="主要尺寸对比").configure_facet(spacing=15)
    st.altair_chart(bar_chart, use_container_width=True)
    st.info("**领先性**：赵州桥的敞肩拱领先西方约1200年，直到19世纪欧洲才出现类似结构。")

# ========== 模块三 ==========
elif nav.startswith("三"):
    st.header("三、力学智慧与持久之谜")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🌊 赵州桥 “顺势而为”")
        st.markdown("""
        - **28道独立并列拱券**，单券损坏不垮塌，可局部更换
        - **腰铁横向锁固**，铁水浇灌严丝合缝
        - **浅基础天然地基**，1400年下沉仅约5厘米
        - 坦拱使拱内主要为压力，完美利用石材抗压特性
        """)
    with col2:
        st.subheader("📐 加尔桥 “精密计算”")
        st.markdown("""
        - **三层叠拱**分担输水与通行功能
        - **水渠坡度1/3000**，全程落差仅17米
        - 桥墩建在河床岩石上，带有水角抵御洪水
        - 损坏后维修难度较高，冗余度相对较低
        """)
    st.markdown("---")
    st.markdown(
        "**核心差异**：赵州桥通过 **结构冗余+自然地基适应** 实现超长待机；加尔桥依靠 **精准选址+刚性结构** 保障输水功能。")

# ========== 模块四 ==========
elif nav.startswith("四"):
    st.header("四、耐久性与文物保护")
    st.subheader("自然灾害考验对比")
    disaster_melt = disaster_data.melt(id_vars='考验类型', var_name='桥梁', value_name='次数')
    dis_chart = alt.Chart(disaster_melt).mark_bar().encode(
        x=alt.X('桥梁', title=None),
        y='次数',
        color='桥梁',
        column='考验类型',
        tooltip=['桥梁', '次数']
    ).properties(width=80, title="历史重大考验次数 (据公开报道)")
    st.altair_chart(dis_chart, use_container_width=True)

    st.subheader("文物保护级别")
    col_z, col_g = st.columns(2)
    with col_z:
        st.markdown("**赵州桥**")
        for h in heritage_zhao:
            st.success(h)
    with col_g:
        st.markdown("**加尔桥**")
        for h in heritage_gard:
            st.info(h)

    st.markdown("**修缮与加固**：赵州桥1950年代大修，用新材料替换旧石；加尔桥19世纪大规模修复，20世纪列为遗产后持续维护。")

# ========== 模块五 ==========
# ========== 模块五 ==========
elif nav.startswith("五"):
    st.header("五、文化内涵与象征意义")
    st.subheader("文化影响力雷达图")

    # ------------- 修复中文显示的雷达图代码 -------------
    import matplotlib.pyplot as plt
    import numpy as np

    # 强制加载中文字体（彻底解决方框乱码）
    plt.rcParams['font.family'] = ['WenQuanYi Micro Hei', 'SimHei', 'Microsoft YaHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

    radar_labels = ['民间传说', '教材/票面传播', '民族自豪感', '国际遗产认可', '艺术价值']
    zhao_vals = [5, 5, 5, 4, 5]
    gard_vals = [3, 4, 3, 5, 4]

    labels = np.array(radar_labels)
    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    zhao_vals_plot = zhao_vals + zhao_vals[:1]
    gard_vals_plot = gard_vals + gard_vals[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    # 正常显示中文标签
    plt.xticks(angles[:-1], labels, color='grey', size=10)
    ax.set_rlabel_position(30)
    ax.plot(angles, zhao_vals_plot, 'o-', linewidth=2, label='赵州桥', color='#8B4513')
    ax.fill(angles, zhao_vals_plot, alpha=0.25, color='#8B4513')
    ax.plot(angles, gard_vals_plot, 'o-', linewidth=2, label='加尔桥', color='#2F4F4F')
    ax.fill(angles, gard_vals_plot, alpha=0.25, color='#2F4F4F')
    ax.set_ylim(0, 5)
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

    st.pyplot(fig)
    # ---------------------------------------------------

    st.caption("评分基于民间传说、教材/欧元纸币传播、民族自豪感、国际遗产认定等维度综合估算，仅作相对示意。")
    st.markdown("**赵州桥**：鲁班传说、小学课文、民族骄傲；**加尔桥**：欧元纸币、UNESCO杰作、欧洲文旅地标。")
# ========== 模块六 ==========
else:
    st.header("六、结语：两种智慧，一种伟大")
    st.markdown("""
    <div class="card">
    <p style="font-size:1.2rem;">
    <strong>加尔桥</strong>以宏大规模、三层叠拱的组织美学与精准坡度控制，彰显罗马帝国的工程组织力与计算力；<br><br>
    <strong>赵州桥</strong>以领先世界千年的敞肩拱革命，展现东方匠人“四两拨千斤”的力学智慧——小材料、浅地基、长寿命。<br><br>
    二者分别代表了古代中国与古罗马在工程领域的最高成就，用不同的路径书写了世界建筑史的辉煌篇章。
    </p>
    </div>
    """, unsafe_allow_html=True)
    if os.path.exists(IMG_ZZQ_QJ):
        st.image(IMG_ZZQ_QJ, use_container_width=True, caption="赵州桥今貌")
    else:
        st.warning(f"图片 `{IMG_ZZQ_QJ}` 未找到，请将图片置于当前目录。此处展示占位图。")
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Zhaozhou_Bridge.jpg/640px-Zhaozhou_Bridge.jpg",
             caption="赵州桥今貌", width=400)
    if os.path.exists(IMG_JEQ_QM):
        st.image(IMG_JEQ_QM, use_container_width=True, caption="加尔桥今貌")
    else:
        st.warning(f"图片 `{IMG_JEQ_QM}` 未找到，请将图片置于当前目录。此处展示占位图。")
        st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Pont_du_Gard_Oct_2007.jpg/640px-Pont_du_Gard_Oct_2007.jpg",
        caption="加尔桥今貌", width=400)

# ---------- 底部统一标注 ----------
st.markdown("---")
st.markdown("""
<div class="footer">
<strong>📖 数据来源：</strong> 中国新闻网、澎湃新闻、百度百科、UNESCO、科普中国等网络公开资料综合整理。所有历史考验次数与文化评分均基于文档提供数据，仅供参考。<br>
<strong>🖱️ 交互说明：</strong> 页面基于Streamlit构建，图表支持悬停查看数值，各模块通过侧边栏自由切换。请确保三张指定图片置于同目录下以保证显示。
</div>
""", unsafe_allow_html=True)