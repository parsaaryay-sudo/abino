import streamlit as st
import json, hashlib, copy
from datetime import datetime

# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="آبینو | Abino",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;900&display=swap');

:root {
    --bg:      #020617;
    --surface: #0f172a;
    --card:    rgba(15,23,42,0.85);
    --primary: #0EA5E9;
    --accent:  #10B981;
    --accent2: #6366f1;
    --muted:   #94a3b8;
    --white:   #f1f5f9;
    --ice:     #cbd5e1;
    --danger:  #f43f5e;
    --warn:    #f59e0b;
    --success: #10B981;
    --border:  rgba(14,165,233,0.18);
    --glass:   rgba(255,255,255,0.03);
}

* { font-family: 'Vazirmatn', sans-serif !important; direction: rtl; box-sizing: border-box; }

html, body, .stApp {
    background: var(--bg) !important;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(14,165,233,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 100%, rgba(16,185,129,0.08) 0%, transparent 60%) !important;
    color: var(--white);
}
.block-container { padding: 0 1.5rem 4rem !important; max-width: 1280px !important; }
header, #MainMenu, footer { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }

/* ── TOPBAR ── */
.topbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 1rem 0 .8rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.5rem;
}
.logo { display: flex; align-items: center; gap: .7rem; }
.logo-icon { font-size: 2.2rem; }
.logo-text {
    font-size: 1.7rem; font-weight: 900; letter-spacing: -1px;
    background: linear-gradient(135deg, var(--white) 20%, var(--primary) 60%, var(--accent));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.logo-sub {
    font-size: .65rem; color: var(--muted); font-weight: 500;
    letter-spacing: 4px; text-transform: uppercase; display: block; margin-top: -5px;
}

/* ── HERO ── */
.hero { text-align: center; padding: 3rem 1rem 1.5rem; }
.hero-badge {
    display: inline-block;
    background: linear-gradient(90deg, rgba(14,165,233,.15), rgba(16,185,129,.15));
    border: 1px solid rgba(14,165,233,.35);
    color: var(--primary);
    font-size: .7rem; font-weight: 800; padding: .35rem 1.3rem;
    border-radius: 999px; letter-spacing: 3px;
    margin-bottom: 1rem; text-transform: uppercase;
}
.hero h1 {
    font-size: clamp(2.2rem, 5vw, 4rem); font-weight: 900; line-height: 1.15;
    background: linear-gradient(135deg, var(--white) 20%, var(--primary) 55%, var(--accent) 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 0 0 .7rem;
}
.hero p { font-size: 1rem; color: var(--ice); max-width: 520px; margin: 0 auto 1.5rem; line-height: 1.9; }

/* ── FEATURES STRIP ── */
.features-strip {
    display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;
    background: rgba(14,165,233,.04);
    border: 1px solid rgba(14,165,233,.1);
    border-radius: 16px; padding: 1.1rem 2rem; margin: 1rem 0 2rem;
}
.fi { text-align: center; }
.fi-icon { font-size: 1.6rem; }
.fi-label { font-size: .72rem; color: var(--muted); margin-top: .2rem; }

/* ── SECTION TITLE ── */
.sec-title {
    font-size: 1.35rem; font-weight: 700; color: var(--primary);
    margin: 2.2rem 0 1rem; padding-right: .7rem;
    border-right: 3px solid var(--accent);
}

/* ── PRODUCT CARD ── */
.pcard {
    background: var(--card);
    backdrop-filter: blur(20px);
    border: 1px solid var(--border);
    border-radius: 20px; padding: 1.5rem 1.3rem;
    text-align: center; position: relative; overflow: hidden; margin-bottom: .5rem;
    transition: transform .25s ease, box-shadow .25s ease, border-color .25s ease;
}
.pcard::before {
    content:''; position:absolute; top:0; left:0; right:0; height:2px;
    background: linear-gradient(90deg, var(--primary), var(--accent));
    border-radius: 20px 20px 0 0;
}
.pcard:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 50px rgba(14,165,233,.12);
    border-color: rgba(14,165,233,.3);
}
.pcard.out-of-stock { opacity: .45; filter: grayscale(.5); }
.pcard-icon { font-size: 2.8rem; margin-bottom: .4rem; }
.pcard-name { font-size: 1.05rem; font-weight: 700; color: var(--white); margin-bottom: .3rem; }
.pcard-desc { font-size: .82rem; color: var(--muted); line-height: 1.75; margin-bottom: .75rem; }
.pcard-price { font-size: 1.3rem; font-weight: 900; color: var(--primary); }
.pcard-price span { font-size: .75rem; font-weight: 400; color: var(--muted); }
.pcard-stock { font-size: .75rem; margin-top: .35rem; }
.stock-ok   { color: var(--success); }
.stock-low  { color: var(--warn); }
.stock-out  { color: var(--danger); }
.stock-inf  { color: var(--primary); }

/* ── BADGES ── */
.badge {
    display: inline-block; padding: .2rem .7rem; border-radius: 999px;
    font-size: .68rem; font-weight: 700; margin-bottom: .5rem;
}
.badge-new  { background: rgba(14,165,233,.12);  color: var(--primary); border: 1px solid rgba(14,165,233,.4); }
.badge-hot  { background: rgba(244,63,94,.12);   color: #fb7185;        border: 1px solid rgba(244,63,94,.4); }
.badge-sale { background: rgba(245,158,11,.12);  color: var(--warn);    border: 1px solid rgba(245,158,11,.4); }
.badge-out  { background: rgba(244,63,94,.1);    color: var(--danger);  border: 1px solid rgba(244,63,94,.4); }

/* ── CART ── */
.cart-box {
    background: var(--card); border: 1px solid var(--border);
    border-radius: 18px; padding: 1.4rem;
}
.cart-total { font-size: 1.15rem; font-weight: 700; color: var(--accent); text-align: left; margin-top: .8rem; }

/* ── ADMIN PANEL ── */
.admin-header {
    background: linear-gradient(135deg, rgba(99,102,241,.15), rgba(16,185,129,.08));
    border: 1px solid rgba(99,102,241,.25);
    border-radius: 20px; padding: 1.8rem; text-align: center; margin-bottom: 1.5rem;
}
.admin-header h2 { font-size: 1.6rem; font-weight: 800; color: var(--accent2); margin: 0 0 .3rem; }
.admin-header p { font-size: .85rem; color: var(--muted); margin: 0; }

.stat-card {
    background: linear-gradient(135deg, rgba(14,165,233,.06), rgba(16,185,129,.04));
    border: 1px solid var(--border); border-radius: 16px; padding: 1.3rem; text-align: center;
}
.stat-num { font-size: 1.8rem; font-weight: 900; color: var(--primary); }
.stat-lbl { font-size: .78rem; color: var(--muted); margin-top: .25rem; }

.edit-card {
    background: rgba(15,23,42,.95);
    border: 1px solid rgba(14,165,233,.15);
    border-radius: 16px; padding: 1.3rem; margin-bottom: 1rem;
}
.edit-card h4 {
    font-size: 1rem; font-weight: 700; color: var(--white); margin: 0 0 1rem;
    padding-bottom: .5rem; border-bottom: 1px solid rgba(255,255,255,.06);
}

/* ── USER PANEL ── */
.user-header {
    background: linear-gradient(135deg, rgba(14,165,233,.1), rgba(16,185,129,.06));
    border: 1px solid rgba(14,165,233,.2);
    border-radius: 20px; padding: 1.8rem; text-align: center; margin-bottom: 1.5rem;
}
.user-header h2 { font-size: 1.4rem; font-weight: 800; color: var(--primary); margin: 0 0 .25rem; }
.user-header p { font-size: .82rem; color: var(--muted); margin: 0; }

.order-row {
    background: var(--card); border: 1px solid var(--border);
    border-radius: 14px; padding: 1rem 1.2rem; margin-bottom: .7rem;
}
.order-row .or-top { display:flex; justify-content:space-between; align-items:center; margin-bottom:.4rem; }
.or-code { font-size: .85rem; font-weight: 700; color: var(--accent); }
.or-date { font-size: .75rem; color: var(--muted); }
.or-status { font-size: .72rem; font-weight: 600; padding: .15rem .65rem; border-radius: 999px; }
.s-pending { background: rgba(245,158,11,.12); color: var(--warn);    border: 1px solid rgba(245,158,11,.35); }
.s-sent    { background: rgba(14,165,233,.12); color: var(--primary); border: 1px solid rgba(14,165,233,.35); }
.s-done    { background: rgba(16,185,129,.12); color: var(--success); border: 1px solid rgba(16,185,129,.35); }

/* ── LOGIN ── */
.login-box {
    max-width: 400px; margin: 3rem auto;
    background: var(--card); border: 1px solid var(--border);
    border-radius: 20px; padding: 2.5rem; text-align: center;
}
.login-box h2 { font-size: 1.5rem; font-weight: 800; color: var(--primary); margin-bottom: .5rem; }
.login-box p  { font-size: .85rem; color: var(--muted); margin-bottom: 1.5rem; }

/* ── STREAMLIT OVERRIDES ── */
div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input,
div[data-testid="stSelectbox"] > div > div,
textarea {
    background: rgba(14,165,233,.05) !important;
    color: var(--white) !important;
    border: 1px solid rgba(14,165,233,.2) !important;
    border-radius: 10px !important;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stNumberInput"] input:focus,
textarea:focus {
    border-color: rgba(14,165,233,.5) !important;
    box-shadow: 0 0 0 3px rgba(14,165,233,.08) !important;
}
label { color: var(--muted) !important; font-size: .85rem !important; }

div[data-testid="stButton"] button {
    width: 100%;
    background: linear-gradient(135deg, var(--primary), var(--accent)) !important;
    color: #020617 !important;
    font-weight: 800 !important; font-size: .95rem !important;
    border: none !important; border-radius: 12px !important; padding: .65rem !important;
    transition: opacity .2s, transform .15s !important;
}
div[data-testid="stButton"] button:hover {
    opacity: .88 !important; transform: translateY(-1px) !important;
}

div[data-testid="stSuccess"] { background: rgba(16,185,129,.08) !important; border-radius: 12px !important; border-left: 3px solid var(--success) !important; }
div[data-testid="stWarning"] { background: rgba(245,158,11,.08) !important; border-radius: 12px !important; border-left: 3px solid var(--warn) !important; }
div[data-testid="stError"]   { background: rgba(244,63,94,.07)  !important; border-radius: 12px !important; border-left: 3px solid var(--danger) !important; }
div[data-testid="stInfo"]    { background: rgba(14,165,233,.07) !important; border-radius: 12px !important; border-left: 3px solid var(--primary) !important; }

div[data-testid="stTabs"] [role="tab"] { color: var(--muted) !important; font-weight: 600 !important; }
div[data-testid="stTabs"] [aria-selected="true"] {
    color: var(--primary) !important;
    border-bottom: 2px solid var(--primary) !important;
}
div[data-testid="stCheckbox"] label { color: var(--ice) !important; }
hr { border-color: rgba(255,255,255,.06) !important; }
div[data-testid="stExpander"] {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
}

/* ── ABOUT PAGE ── */
.about-hero {
    text-align: center; padding: 3rem 1rem 2rem;
}
.about-hero h1 {
    font-size: clamp(1.8rem, 4vw, 3rem); font-weight: 900;
    background: linear-gradient(135deg, var(--white) 20%, var(--primary) 60%, var(--accent));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 0 0 .7rem;
}
.about-hero p { font-size: 1rem; color: var(--muted); max-width: 580px; margin: 0 auto; line-height: 1.9; }

.contact-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 20px; padding: 2rem;
    position: relative; overflow: hidden;
}
.contact-card::before {
    content:''; position:absolute; top:0; left:0; right:0; height:2px;
    background: linear-gradient(90deg, var(--primary), var(--accent));
}
.contact-item {
    display: flex; align-items: flex-start; gap: 1rem;
    padding: 1.1rem 0; border-bottom: 1px solid rgba(255,255,255,.05);
}
.contact-item:last-child { border-bottom: none; padding-bottom: 0; }
.contact-icon {
    width: 46px; height: 46px; border-radius: 12px; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.4rem;
}
.ci-blue  { background: rgba(14,165,233,.12); border: 1px solid rgba(14,165,233,.25); }
.ci-green { background: rgba(16,185,129,.12); border: 1px solid rgba(16,185,129,.25); }
.ci-tg    { background: rgba(38,169,224,.12); border: 1px solid rgba(38,169,224,.25); }
.contact-info-label { font-size: .72rem; color: var(--muted); margin-bottom: .2rem; letter-spacing: 1px; text-transform: uppercase; }
.contact-info-value { font-size: 1rem; font-weight: 600; color: var(--white); line-height: 1.5; }
.contact-info-value a { color: var(--primary); text-decoration: none; }
.contact-info-value a:hover { color: var(--accent); }

.map-box {
    background: rgba(14,165,233,.04);
    border: 1px solid rgba(14,165,233,.15);
    border-radius: 16px; padding: 1.5rem; text-align: center;
    margin-top: 1.5rem;
}
.map-box iframe { border-radius: 12px; border: none; width: 100%; height: 280px; }

.value-card {
    background: var(--card); border: 1px solid var(--border);
    border-radius: 16px; padding: 1.5rem; text-align: center;
    margin-bottom: .5rem;
}
.value-icon { font-size: 2.2rem; margin-bottom: .6rem; }
.value-title { font-size: 1rem; font-weight: 700; color: var(--primary); margin-bottom: .4rem; }
.value-desc { font-size: .83rem; color: var(--muted); line-height: 1.75; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def fmt(n): return f"{n:,}"

def hashpw(pw): return hashlib.sha256(pw.encode()).hexdigest()

# ══════════════════════════════════════════════════════════════════════════════
# DEFAULT DATA
# ══════════════════════════════════════════════════════════════════════════════
DEFAULT_PRODUCTS = {
    "آب مقطر": [
        {"id":"d1","name":"آب مقطر ۱ لیتری","icon":"💧","price":18000,"desc":"مناسب آزمایشگاه و باتری؛ خلوص بالا","badge":"new","badge_label":"جدید","unit":"لیتر","stock":50,"unlimited":False},
        {"id":"d2","name":"آب مقطر ۵ لیتری","icon":"🫙","price":75000,"desc":"اقتصادی برای مصارف صنعتی و پزشکی","badge":"hot","badge_label":"پرفروش","unit":"گالن","stock":30,"unlimited":False},
        {"id":"d3","name":"آب مقطر ۲۰ لیتری","icon":"🛢️","price":260000,"desc":"گالن بزرگ، بهترین انتخاب برای کارگاه","badge":"sale","badge_label":"تخفیف","unit":"گالن","stock":15,"unlimited":False},
    ],
    "آب رادیاتور": [
        {"id":"r1","name":"آب رادیاتور ۱ لیتری","icon":"🔵","price":22000,"desc":"ضد‌انجماد و ضد‌زنگ؛ فرمول پیشرفته","badge":"new","badge_label":"جدید","unit":"لیتر","stock":80,"unlimited":False},
        {"id":"r2","name":"آب رادیاتور ۴ لیتری","icon":"🧴","price":78000,"desc":"محافظت کامل موتور در تمام فصول سال","badge":"hot","badge_label":"پرفروش","unit":"لیتر","stock":0,"unlimited":False},
        {"id":"r3","name":"آب رادیاتور ۲۰ لیتری","icon":"🛢️","price":350000,"desc":"مخصوص ناوگان و تعمیرگاه‌های بزرگ","badge":"sale","badge_label":"تخفیف","unit":"گالن","stock":5,"unlimited":True},
    ],
    "شیشه‌شور": [
        {"id":"w1","name":"شیشه‌شور تابستانه ۱L","icon":"🪟","price":15000,"desc":"پاک‌کننده قوی، بدون اثر، مناسب گرما","badge":"new","badge_label":"جدید","unit":"لیتر","stock":100,"unlimited":False},
        {"id":"w2","name":"شیشه‌شور زمستانه ۱L","icon":"❄️","price":17000,"desc":"ضد‌یخ تا ۲۵- درجه، شفافیت کامل","badge":"hot","badge_label":"پرفروش","unit":"لیتر","stock":60,"unlimited":False},
        {"id":"w3","name":"شیشه‌شور ۴ لیتری ویژه","icon":"🧼","price":55000,"desc":"بسته خانوادگی، صرفه‌جویی بیشتر","badge":"sale","badge_label":"تخفیف","unit":"لیتر","stock":25,"unlimited":False},
    ],
}

# Default users: admin + two customers
DEFAULT_USERS = {
    "admin": {"password": hashpw("admin123"), "role": "admin", "name": "مدیر سیستم"},
    "ali":   {"password": hashpw("ali123"),   "role": "customer", "name": "علی احمدی"},
    "sara":  {"password": hashpw("sara123"),  "role": "customer", "name": "سارا رضایی"},
}

# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE INIT
# ══════════════════════════════════════════════════════════════════════════════
def init_state():
    if "products"  not in st.session_state: st.session_state.products  = copy.deepcopy(DEFAULT_PRODUCTS)
    if "users"     not in st.session_state: st.session_state.users     = copy.deepcopy(DEFAULT_USERS)
    if "orders"    not in st.session_state: st.session_state.orders    = []
    if "cart"      not in st.session_state: st.session_state.cart      = {}
    if "logged_in" not in st.session_state: st.session_state.logged_in = False
    if "username"  not in st.session_state: st.session_state.username  = ""
    if "page"      not in st.session_state: st.session_state.page      = "shop"

init_state()

# ══════════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════
def get_product(pid):
    for cat_prods in st.session_state.products.values():
        for p in cat_prods:
            if p["id"] == pid:
                return p
    return None

def is_available(p):
    return p["unlimited"] or p["stock"] > 0

def stock_label(p):
    if p["unlimited"]:         return '<span class="stock-inf">∞ نامحدود</span>'
    if p["stock"] == 0:        return '<span class="stock-out">ناموجود</span>'
    if p["stock"] <= 5:        return f'<span class="stock-low">فقط {p["stock"]} عدد مانده</span>'
    return f'<span class="stock-ok">موجود: {p["stock"]} عدد</span>'

def add_to_cart(product, qty):
    pid = product["id"]
    if pid in st.session_state.cart:
        st.session_state.cart[pid]["qty"] += qty
    else:
        st.session_state.cart[pid] = {"name": product["name"], "price": product["price"], "qty": qty}

def cart_total():
    return sum(v["price"]*v["qty"] for v in st.session_state.cart.values())

def current_user():
    if st.session_state.logged_in:
        return st.session_state.users.get(st.session_state.username, {})
    return {}

def user_orders():
    return [o for o in st.session_state.orders if o["username"] == st.session_state.username]

BADGE_CLASS = {"new":"badge-new","hot":"badge-hot","sale":"badge-sale"}

# ══════════════════════════════════════════════════════════════════════════════
# TOPBAR
# ══════════════════════════════════════════════════════════════════════════════
cu = current_user()
role = cu.get("role","")

col_logo, col_nav = st.columns([3,5])
with col_logo:
    st.markdown("""
    <div class="topbar">
        <div class="logo">
            <span class="logo-icon">💧</span>
            <div>
                <span class="logo-text">آبینو</span>
                <span class="logo-sub">Abino Water Store</span>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

with col_nav:
    nav_items = ["🏪 فروشگاه", "🏢 درباره ما"]
    nav_keys  = ["shop", "about"]
    if st.session_state.logged_in:
        nav_items.append("👤 پنل کاربری")
        nav_keys.append("user_panel")
        if role == "admin":
            nav_items.append("⚙️ پنل مدیریت")
            nav_keys.append("admin_panel")
        nav_items.append("🛒 سبد خرید")
        nav_keys.append("cart")
        nav_items.append(f"خروج ({cu.get('name','')})")
        nav_keys.append("logout")
    else:
        nav_items.append("🔐 ورود / ثبت‌نام")
        nav_keys.append("login")

    st.markdown("<br>", unsafe_allow_html=True)
    btn_cols = st.columns(len(nav_items))
    for i, (label, key) in enumerate(zip(nav_items, nav_keys)):
        with btn_cols[i]:
            if st.button(label, key=f"nav_{key}"):
                if key == "logout":
                    st.session_state.logged_in = False
                    st.session_state.username  = ""
                    st.session_state.cart      = {}
                    st.session_state.page      = "shop"
                else:
                    st.session_state.page = key
                st.rerun()

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: SHOP
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "shop":
    st.markdown("""
    <div class="hero">
        <div class="hero-badge">فروشگاه آنلاین آبینو</div>
        <h1>کیفیت آب؛ اعتماد شما</h1>
        <p>بهترین محصولات آب مقطر، آب رادیاتور و شیشه‌شور با کیفیت تضمینی و ارسال سریع به سراسر ایران</p>
    </div>
    <div class="features-strip">
        <div class="fi"><div class="fi-icon">🚚</div><div class="fi-label">ارسال رایگان بالای ۲۰۰هزار</div></div>
        <div class="fi"><div class="fi-icon">✅</div><div class="fi-label">کیفیت تضمینی</div></div>
        <div class="fi"><div class="fi-icon">🔄</div><div class="fi-label">ضمانت بازگشت ۷ روزه</div></div>
        <div class="fi"><div class="fi-icon">📞</div><div class="fi-label">پشتیبانی ۲۴ ساعته</div></div>
    </div>
    """, unsafe_allow_html=True)

    for cat, prods in st.session_state.products.items():
        st.markdown(f'<div class="sec-title">{cat}</div>', unsafe_allow_html=True)
        cols = st.columns(3, gap="medium")
        for col, p in zip(cols, prods):
            with col:
                avail = is_available(p)
                oos   = "" if avail else " out-of-stock"
                bc    = BADGE_CLASS.get(p["badge"],"badge-new")
                bl    = p["badge_label"] if avail else "ناموجود"
                bc2   = bc if avail else "badge-out"
                st.markdown(f"""
                <div class="pcard{oos}">
                    <span class="badge {bc2}">{bl}</span>
                    <div class="pcard-icon">{p['icon']}</div>
                    <div class="pcard-name">{p['name']}</div>
                    <div class="pcard-desc">{p['desc']}</div>
                    <div class="pcard-price">{fmt(p['price'])} <span>تومان / {p['unit']}</span></div>
                    <div class="pcard-stock">{stock_label(p)}</div>
                </div>""", unsafe_allow_html=True)
                if avail:
                    qty = st.number_input("تعداد", 1, 99, 1, key=f"qty_{p['id']}", label_visibility="collapsed")
                    if st.button("افزودن به سبد 🛒", key=f"add_{p['id']}"):
                        if not st.session_state.logged_in:
                            st.warning("برای خرید ابتدا وارد شوید.")
                        else:
                            add_to_cart(p, qty)
                            st.success(f"✅ {p['name']} اضافه شد!")
                else:
                    st.markdown('<div style="text-align:center;color:#ff4d6d;font-size:.85rem;padding:.4rem">این محصول موجود نیست</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: LOGIN / REGISTER
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "login":
    st.markdown('<div style="max-width:420px;margin:0 auto">', unsafe_allow_html=True)
    tab_login, tab_reg = st.tabs(["🔐 ورود", "📝 ثبت‌نام"])

    with tab_login:
        st.markdown('<div style="padding:1rem 0">', unsafe_allow_html=True)
        st.markdown("**ورود به حساب کاربری**")
        uname = st.text_input("نام کاربری", key="li_u")
        upass = st.text_input("رمز عبور", type="password", key="li_p")
        if st.button("ورود", key="btn_login"):
            users = st.session_state.users
            if uname in users and users[uname]["password"] == hashpw(upass):
                st.session_state.logged_in = True
                st.session_state.username  = uname
                st.session_state.page      = "shop"
                st.rerun()
            else:
                st.error("نام کاربری یا رمز عبور اشتباه است.")
        st.markdown("---")
        st.markdown('<div style="font-size:.78rem;color:var(--ice);text-align:center">حساب آزمایشی مدیر: <b>admin / admin123</b><br>حساب آزمایشی مشتری: <b>ali / ali123</b></div>', unsafe_allow_html=True)

    with tab_reg:
        st.markdown('<div style="padding:1rem 0">', unsafe_allow_html=True)
        st.markdown("**ساخت حساب جدید**")
        rname  = st.text_input("نام و نام خانوادگی", key="r_name")
        runame = st.text_input("نام کاربری", key="r_u")
        rpass  = st.text_input("رمز عبور", type="password", key="r_p")
        rpass2 = st.text_input("تکرار رمز عبور", type="password", key="r_p2")
        if st.button("ثبت‌نام", key="btn_reg"):
            if not all([rname, runame, rpass, rpass2]):
                st.warning("همه فیلدها را پر کنید.")
            elif rpass != rpass2:
                st.error("رمز عبور و تکرار آن یکسان نیستند.")
            elif runame in st.session_state.users:
                st.error("این نام کاربری قبلاً ثبت شده است.")
            elif len(rpass) < 5:
                st.warning("رمز عبور باید حداقل ۵ کاراکتر باشد.")
            else:
                st.session_state.users[runame] = {"password": hashpw(rpass), "role": "customer", "name": rname}
                st.session_state.logged_in = True
                st.session_state.username  = runame
                st.session_state.page      = "shop"
                st.success("✅ ثبت‌نام موفق!")
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: CART
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "cart":
    st.markdown('<div class="sec-title">🛒 سبد خرید</div>', unsafe_allow_html=True)
    if not st.session_state.cart:
        st.info("سبد خرید شما خالی است.")
    else:
        for pid, item in list(st.session_state.cart.items()):
            c1, c2, c3, c4 = st.columns([4, 2, 2, 1])
            with c1: st.markdown(f"**{item['name']}**")
            with c2: st.markdown(f"×{item['qty']}")
            with c3: st.markdown(f"{fmt(item['price']*item['qty'])} تومان")
            with c4:
                if st.button("🗑️", key=f"rm_{pid}"):
                    del st.session_state.cart[pid]; st.rerun()
        st.markdown("---")
        total = cart_total()
        ship  = 0 if total >= 200000 else 30000
        st.markdown(f"هزینه ارسال: **{'رایگان 🎉' if ship==0 else fmt(ship)+' تومان'}**")
        st.markdown(f"### مجموع: {fmt(total+ship)} تومان")
        if total < 200000:
            st.warning(f"⚡ تا ارسال رایگان {fmt(200000-total)} تومان مانده!")
        st.markdown("---")
        st.markdown("**اطلاعات ارسال**")
        cc1, cc2 = st.columns(2)
        with cc1:
            o_name  = st.text_input("نام و نام خانوادگی *", key="o_name")
            o_phone = st.text_input("شماره موبایل *", key="o_phone")
            o_city  = st.text_input("شهر *", key="o_city")
        with cc2:
            o_addr = st.text_area("آدرس کامل *", key="o_addr", height=110)
            o_pay  = st.selectbox("روش پرداخت", ["درگاه آنلاین","کارت به کارت","پرداخت در محل"])

        if st.button("✅ ثبت سفارش"):
            if not all([o_name, o_phone, o_city, o_addr]):
                st.warning("همه فیلدهای ستاره‌دار را پر کنید.")
            elif len(o_phone) < 10:
                st.warning("شماره موبایل معتبر وارد کنید.")
            else:
                code = f"AB-{abs(hash(o_name+o_phone+str(datetime.now()))) % 100000:05d}"
                order = {
                    "code": code, "username": st.session_state.username,
                    "name": o_name, "phone": o_phone, "city": o_city,
                    "address": o_addr, "pay": o_pay,
                    "items": dict(st.session_state.cart),
                    "total": total + ship,
                    "date": datetime.now().strftime("%Y/%m/%d %H:%M"),
                    "status": "در انتظار تأیید"
                }
                # reduce stock
                for pid, itm in st.session_state.cart.items():
                    p = get_product(pid)
                    if p and not p["unlimited"]:
                        p["stock"] = max(0, p["stock"] - itm["qty"])
                st.session_state.orders.append(order)
                st.session_state.cart = {}
                st.success(f"🎉 سفارش ثبت شد! کد پیگیری: **{code}**")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: USER PANEL
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "user_panel":
    if not st.session_state.logged_in:
        st.warning("ابتدا وارد شوید."); st.stop()
    cu = current_user()
    st.markdown(f"""
    <div class="user-header">
        <h2>👤 پنل کاربری</h2>
        <p>خوش آمدید، <b>{cu.get('name','')}</b></p>
    </div>""", unsafe_allow_html=True)

    t1, t2, t3 = st.tabs(["📦 سفارشات من", "👤 اطلاعات حساب", "🔑 تغییر رمز"])

    with t1:
        my_orders = user_orders()
        if not my_orders:
            st.info("هنوز سفارشی ثبت نکرده‌اید.")
        else:
            for o in reversed(my_orders):
                sc = {"در انتظار تأیید":"s-pending","ارسال شده":"s-sent","تحویل داده شده":"s-done"}.get(o["status"],"s-pending")
                st.markdown(f"""
                <div class="order-row">
                    <div class="or-top">
                        <span class="or-code">{o['code']}</span>
                        <span class="or-date">{o['date']}</span>
                        <span class="or-status {sc}">{o['status']}</span>
                    </div>
                    <div style="font-size:.82rem;color:var(--ice)">
                        {' | '.join([f"{v['name']} ×{v['qty']}" for v in o['items'].values()])}
                    </div>
                    <div style="font-size:.9rem;font-weight:700;color:var(--accent);margin-top:.3rem">
                        {fmt(o['total'])} تومان
                    </div>
                </div>""", unsafe_allow_html=True)

    with t2:
        st.markdown(f"**نام:** {cu.get('name','')}")
        st.markdown(f"**نام کاربری:** {st.session_state.username}")
        st.markdown(f"**نقش:** {'مشتری' if cu.get('role')=='customer' else 'مدیر'}")
        new_name = st.text_input("ویرایش نام", value=cu.get("name",""), key="edit_name")
        if st.button("ذخیره نام", key="save_name"):
            st.session_state.users[st.session_state.username]["name"] = new_name
            st.success("نام به‌روزرسانی شد!")
            st.rerun()

    with t3:
        op = st.text_input("رمز فعلی", type="password", key="cp_old")
        np = st.text_input("رمز جدید", type="password", key="cp_new")
        np2= st.text_input("تکرار رمز جدید", type="password", key="cp_new2")
        if st.button("تغییر رمز", key="btn_cp"):
            if cu["password"] != hashpw(op):
                st.error("رمز فعلی اشتباه است.")
            elif np != np2:
                st.error("رمز جدید و تکرار آن یکسان نیستند.")
            elif len(np) < 5:
                st.warning("رمز جدید باید حداقل ۵ کاراکتر باشد.")
            else:
                st.session_state.users[st.session_state.username]["password"] = hashpw(np)
                st.success("✅ رمز عبور تغییر کرد!")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ADMIN PANEL
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "admin_panel":
    if not st.session_state.logged_in or current_user().get("role") != "admin":
        st.error("دسترسی محدود به مدیران."); st.stop()

    st.markdown("""
    <div class="admin-header">
        <h2>⚙️ پنل مدیریت آبینو</h2>
        <p>مدیریت محصولات، قیمت‌ها، موجودی و سفارشات</p>
    </div>""", unsafe_allow_html=True)

    # Stats
    all_orders = st.session_state.orders
    total_rev  = sum(o["total"] for o in all_orders)
    total_prods= sum(len(v) for v in st.session_state.products.values())
    total_users= len([u for u in st.session_state.users.values() if u["role"]=="customer"])

    sc1,sc2,sc3,sc4 = st.columns(4)
    for col, num, lbl in zip(
        [sc1,sc2,sc3,sc4],
        [len(all_orders), fmt(total_rev)+" ت", total_prods, total_users],
        ["سفارشات کل","درآمد کل","تعداد محصولات","مشتریان"]
    ):
        with col:
            st.markdown(f'<div class="stat-card"><div class="stat-num">{num}</div><div class="stat-lbl">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    admin_tab1, admin_tab2, admin_tab3, admin_tab4 = st.tabs(["📦 مدیریت محصولات", "🧾 سفارشات", "👥 کاربران", "➕ محصول جدید"])

    # ── TAB 1: PRODUCT MANAGEMENT ──
    with admin_tab1:
        st.markdown('<div class="sec-title">ویرایش محصولات</div>', unsafe_allow_html=True)
        for cat, prods in st.session_state.products.items():
            with st.expander(f"📂 {cat}  ({len(prods)} محصول)", expanded=False):
                for idx, p in enumerate(prods):
                    st.markdown(f'<div class="edit-card"><h4>{p["icon"]} {p["name"]}</h4>', unsafe_allow_html=True)
                    e1, e2, e3 = st.columns([3,2,2])
                    with e1:
                        new_name = st.text_input("نام محصول", value=p["name"], key=f"pn_{p['id']}")
                        new_desc = st.text_input("توضیحات", value=p["desc"], key=f"pd_{p['id']}")
                        new_unit = st.text_input("واحد", value=p["unit"], key=f"pu_{p['id']}")
                    with e2:
                        new_price = st.number_input("قیمت (تومان)", value=p["price"], step=1000, key=f"pp_{p['id']}")
                        new_badge = st.selectbox("برچسب", ["new","hot","sale"],
                            index=["new","hot","sale"].index(p["badge"]), key=f"pb_{p['id']}")
                        new_bl    = st.text_input("متن برچسب", value=p["badge_label"], key=f"pbl_{p['id']}")
                    with e3:
                        st.markdown("**موجودی انبار:**")
                        new_unlimited = st.checkbox("موجودی نامحدود ♾️", value=p["unlimited"], key=f"pinf_{p['id']}")
                        new_stock = p["stock"]
                        if not new_unlimited:
                            new_stock = st.number_input("تعداد موجودی", value=p["stock"], min_value=0, step=1, key=f"ps_{p['id']}")

                    if st.button(f"💾 ذخیره تغییرات", key=f"save_{p['id']}"):
                        p.update({
                            "name": new_name, "desc": new_desc, "unit": new_unit,
                            "price": new_price, "badge": new_badge, "badge_label": new_bl,
                            "unlimited": new_unlimited, "stock": new_stock,
                        })
                        st.success(f"✅ {new_name} به‌روزرسانی شد!")
                        st.rerun()

                    cola, colb = st.columns(2)
                    with cola:
                        if st.button("✅ موجود کردن", key=f"instock_{p['id']}"):
                            if p["stock"] == 0: p["stock"] = 10
                            st.rerun()
                    with colb:
                        if st.button("❌ ناموجود کردن", key=f"outstock_{p['id']}"):
                            p["stock"] = 0; p["unlimited"] = False
                            st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

    # ── TAB 2: ORDERS ──
    with admin_tab2:
        st.markdown('<div class="sec-title">مدیریت سفارشات</div>', unsafe_allow_html=True)
        if not all_orders:
            st.info("هنوز سفارشی ثبت نشده.")
        else:
            for i, o in enumerate(reversed(all_orders)):
                real_idx = len(all_orders) - 1 - i
                with st.expander(f"📦 {o['code']}  —  {o['name']}  —  {fmt(o['total'])} تومان  |  {o['status']}"):
                    d1,d2 = st.columns(2)
                    with d1:
                        st.markdown(f"**نام:** {o['name']}")
                        st.markdown(f"**موبایل:** {o['phone']}")
                        st.markdown(f"**شهر:** {o['city']}")
                        st.markdown(f"**آدرس:** {o['address']}")
                    with d2:
                        st.markdown(f"**تاریخ:** {o['date']}")
                        st.markdown(f"**پرداخت:** {o['pay']}")
                        st.markdown("**اقلام:**")
                        for v in o["items"].values():
                            st.markdown(f"• {v['name']} ×{v['qty']}  →  {fmt(v['price']*v['qty'])} تومان")
                        st.markdown(f"**مجموع:** {fmt(o['total'])} تومان")
                    new_status = st.selectbox("وضعیت سفارش", ["در انتظار تأیید","ارسال شده","تحویل داده شده"],
                        index=["در انتظار تأیید","ارسال شده","تحویل داده شده"].index(o["status"]),
                        key=f"st_{real_idx}")
                    if st.button("💾 ذخیره وضعیت", key=f"sv_st_{real_idx}"):
                        st.session_state.orders[real_idx]["status"] = new_status
                        st.success("وضعیت به‌روزرسانی شد!")
                        st.rerun()

    # ── TAB 3: USERS ──
    with admin_tab3:
        st.markdown('<div class="sec-title">مدیریت کاربران</div>', unsafe_allow_html=True)
        for uname, udata in st.session_state.users.items():
            role_badge = "🔴 مدیر" if udata["role"]=="admin" else "🟢 مشتری"
            u_orders = len([o for o in all_orders if o["username"]==uname])
            with st.expander(f"{role_badge}  {udata['name']}  (@{uname})  —  {u_orders} سفارش"):
                uc1,uc2 = st.columns(2)
                with uc1:
                    new_uname_display = st.text_input("نام نمایشی", value=udata["name"], key=f"un_{uname}")
                    new_role = st.selectbox("نقش", ["customer","admin"],
                        index=0 if udata["role"]=="customer" else 1, key=f"ur_{uname}")
                with uc2:
                    new_pw_admin = st.text_input("تنظیم رمز جدید (خالی = بدون تغییر)", type="password", key=f"upw_{uname}")
                if st.button("💾 ذخیره", key=f"usave_{uname}"):
                    st.session_state.users[uname]["name"] = new_uname_display
                    st.session_state.users[uname]["role"] = new_role
                    if new_pw_admin:
                        st.session_state.users[uname]["password"] = hashpw(new_pw_admin)
                    st.success("اطلاعات کاربر به‌روزرسانی شد!")
                    st.rerun()

    # ── TAB 4: ADD PRODUCT ──
    with admin_tab4:
        st.markdown('<div class="sec-title">افزودن محصول جدید</div>', unsafe_allow_html=True)
        ap1, ap2 = st.columns(2)
        with ap1:
            np_cat   = st.selectbox("دسته‌بندی", list(st.session_state.products.keys()), key="np_cat")
            np_name  = st.text_input("نام محصول", key="np_name")
            np_desc  = st.text_input("توضیحات", key="np_desc")
            np_icon  = st.text_input("آیکون (ایموجی)", value="💧", key="np_icon")
        with ap2:
            np_price = st.number_input("قیمت (تومان)", min_value=0, step=1000, key="np_price")
            np_unit  = st.text_input("واحد", value="لیتر", key="np_unit")
            np_badge = st.selectbox("برچسب", ["new","hot","sale"], key="np_badge")
            np_bl    = st.text_input("متن برچسب", value="جدید", key="np_bl")
            np_stock = st.number_input("موجودی اولیه", min_value=0, value=10, key="np_stock")
            np_inf   = st.checkbox("موجودی نامحدود", key="np_inf")

        if st.button("➕ افزودن محصول", key="btn_add_prod"):
            if not np_name:
                st.warning("نام محصول الزامی است.")
            else:
                new_id = f"custom_{len(st.session_state.products[np_cat])+1}_{np_name[:4]}"
                new_p  = {"id": new_id, "name": np_name, "icon": np_icon,
                           "price": np_price, "desc": np_desc, "badge": np_badge,
                           "badge_label": np_bl, "unit": np_unit,
                           "stock": np_stock, "unlimited": np_inf}
                st.session_state.products[np_cat].append(new_p)
                st.success(f"✅ محصول «{np_name}» به دسته {np_cat} اضافه شد!")
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ABOUT
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "about":
    st.markdown("""
    <div class="about-hero">
        <h1>💧 درباره آبینو</h1>
        <p>
            آبینو با هدف تأمین محصولات باکیفیت آب مقطر، آب رادیاتور و شیشه‌شور
            برای صنایع، کارگاه‌ها و مشتریان عزیز سراسر کشور فعالیت می‌کند.
            اعتماد شما، انگیزه ماست.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── ارزش‌ها ──
    st.markdown('<div class="sec-title">چرا آبینو؟</div>', unsafe_allow_html=True)
    v1, v2, v3, v4 = st.columns(4, gap="medium")
    values = [
        ("🏆", "کیفیت تضمینی", "تمام محصولات از تأمین‌کنندگان معتبر و با استانداردهای بالا انتخاب می‌شوند."),
        ("🚚", "ارسال سریع", "ارسال به سراسر ایران با بسته‌بندی مطمئن و در کوتاه‌ترین زمان ممکن."),
        ("💰", "قیمت مناسب", "بهترین قیمت بازار با حفظ کیفیت؛ صرفه‌جویی واقعی برای مشتریان."),
        ("🤝", "پشتیبانی ۲۴ ساعته", "تیم پشتیبانی ما در تمام ساعات آماده پاسخگویی به سوالات شماست."),
    ]
    for col, (icon, title, desc) in zip([v1,v2,v3,v4], values):
        with col:
            st.markdown(f"""
            <div class="value-card">
                <div class="value-icon">{icon}</div>
                <div class="value-title">{title}</div>
                <div class="value-desc">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── اطلاعات تماس ──
    c_left, c_right = st.columns([3, 2], gap="large")

    with c_left:
        st.markdown('<div class="sec-title">راه‌های ارتباطی</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="contact-card">

            <div class="contact-item">
                <div class="contact-icon ci-blue">📍</div>
                <div>
                    <div class="contact-info-label">آدرس کارخانه</div>
                    <div class="contact-info-value">
                        کرمانشاه، جاده بیستون، پلیس راه بیستون، پل چهره
                    </div>
                </div>
            </div>

            <div class="contact-item">
                <div class="contact-icon ci-green">📱</div>
                <div>
                    <div class="contact-info-label">واتساپ</div>
                    <div class="contact-info-value">
                        <a href="https://wa.me/989028313977" target="_blank">
                            ۰۹۰۲۸۳۱۳۹۷۷
                        </a>
                        &nbsp;— پیام دهید، پاسخ می‌دهیم
                    </div>
                </div>
            </div>

            <div class="contact-item">
                <div class="contact-icon ci-tg">✈️</div>
                <div>
                    <div class="contact-info-label">تلگرام</div>
                    <div class="contact-info-value">
                        <a href="https://t.me/+989028313977" target="_blank">
                            ۰۹۰۲۸۳۱۳۹۷۷
                        </a>
                        &nbsp;— ارتباط مستقیم با تیم فروش
                    </div>
                </div>
            </div>

            <div class="contact-item">
                <div class="contact-icon ci-blue">🕐</div>
                <div>
                    <div class="contact-info-label">ساعات پاسخگویی</div>
                    <div class="contact-info-value">شنبه تا پنجشنبه — ۸ صبح تا ۸ شب</div>
                </div>
            </div>

        </div>
        """, unsafe_allow_html=True)

    with c_right:
        st.markdown('<div class="sec-title">موقعیت روی نقشه</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="map-box">
            <iframe
                src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d6590.280600641756!2d47.42890114521986!3d34.321446192226745!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3ffaa06153ce09b5%3A0x1ea7f696db2ec63f!2sChehr%2C%20Kermanshah%20Province%2C%20Iran!5e0!3m2!1sen!2sus!4v1782924506501!5m2!1sen!2sus" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="strict-origin-when-cross-origin"></iframe>"
                allowfullscreen loading="lazy">
            </iframe>
            <div style="margin-top:.8rem; font-size:.8rem; color:var(--muted);">
                📍 کرمانشاه — جاده بیستون — پلیس راه بیستون — پل چهره
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background:rgba(16,185,129,.07);border:1px solid rgba(16,185,129,.2);
             border-radius:14px;padding:1.2rem;text-align:center;">
            <div style="font-size:1.5rem;margin-bottom:.4rem">💬</div>
            <div style="font-weight:700;color:var(--accent);margin-bottom:.3rem">سفارش عمده؟</div>
            <div style="font-size:.83rem;color:var(--muted);line-height:1.7">
                برای خرید عمده و قیمت ویژه کارخانه،<br>
                مستقیم با ما در واتساپ یا تلگرام در تماس باشید.
            </div>
        </div>
        """, unsafe_allow_html=True)

else:
    st.session_state.page = "shop"
    st.rerun()
