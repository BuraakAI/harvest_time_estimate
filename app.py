"""HasadHaber — Hasat Zamanı Karar Destek Sistemi (MVP demo).

Streamlit V1 arayüzü. Ekran hiyerarşisi: 06_URUN_VE_TICARILESTIRME.md §2.
"Tarlamı seç → 7/14 günlük hasat penceremi söyle."

Çalıştırma:  streamlit run app.py
"""
from __future__ import annotations

from datetime import date

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from core.datasource import DemoDataSource, GEEDataSource, load_parcels
from core.models import Parcel, Prediction
from core.phenology import compute_metrics, smooth_series
from core.rules import predict
from ml.evaluate import TARGETS, backtest, load_labels

st.set_page_config(page_title="HasadHaber — Hasat Zamanı", page_icon="🌾", layout="wide")

DEFAULT_TODAY = date(2026, 6, 26)


# --- Renk kodu (06_URUN §2: yeşil/sarı/kırmızı) --------------------------------
def status_color(remaining: int) -> str:
    if remaining <= 7:
        return "#d62728"   # kırmızı — hasat çok yakın
    if remaining <= 21:
        return "#ff7f0e"   # sarı — yaklaşıyor
    return "#2ca02c"       # yeşil — zaman var


def confidence_pill(conf: float) -> str:
    filled = round(conf * 5)
    return "●" * filled + "○" * (5 - filled) + f"  (%{round(conf * 100)})"


@st.cache_data(show_spinner=False)
def _load() -> list[Parcel]:
    return load_parcels()


def run_prediction(parcel: Parcel, source, season: int, today: date) -> tuple[Prediction, pd.DataFrame]:
    ts = source.get_timeseries(parcel, season, today)
    metrics = compute_metrics(ts.frame, pd.Timestamp(today))
    pred = predict(metrics, today, parcel.region_code)
    pred.parcel_id = parcel.id
    return pred, ts.frame


def reason_text(pred: Prediction) -> str:
    """reason_signals → doğal dil özeti (04_TEKNIK_MIMARI §8.1)."""
    r = pred.reason_signals
    parts = []
    if r.get("days_since_peak") is not None:
        parts.append(f"Tepe noktasından (POS) {r['days_since_peak']} gün geçti")
    if r.get("slope_ndvi_last_14d", 0) < -0.003:
        parts.append("NDVI son 14 günde belirgin düşüşte (senesens)")
    if r.get("ndmi_drop_last_14d", 0) > 0.10:
        parts.append(f"NDMI son 14 günde {r['ndmi_drop_last_14d']:.2f} düştü (kuruma sinyali)")
    if r.get("cloud_gap_days", 0) >= 10:
        parts.append(f"⚠ son gözlemden {r['cloud_gap_days']} gün geçti (bulutluluk/veri eskime)")
    rule = {
        "ndvi_decline": "NDVI düşüş kuralı",
        "ndmi_drying": "NDMI kuruma kuralı",
        "ndvi_decline+ndmi_drying": "NDVI düşüşü + NDMI kuruma kuralları birlikte",
        "calendar_prior": "henüz net senesens sinyali yok → bölgesel takvim önseli",
    }.get(r.get("rule_fired", ""), r.get("rule_fired", ""))
    parts.append(f"Tetiklenen mantık: **{rule}**")
    return ". ".join(parts) + "."


# === Sidebar ===================================================================
st.sidebar.title("🌾 HasadHaber")
st.sidebar.caption("Hasat zamanı karar destek sistemi — MVP demo")

mode = st.sidebar.radio("Veri kaynağı", ["Demo (sentetik)", "Canlı (GEE)"], index=0)
if mode.startswith("Demo"):
    source = DemoDataSource()
else:
    gee = GEEDataSource()
    ready, why = gee.check_ready()
    if ready:
        source = gee
    else:
        # Zarif düşüş: GEE hazır değilse çökme, Demo ile devam et + net uyarı.
        source = DemoDataSource()
        mode = "Demo (sentetik)"
        st.sidebar.error(f"Canlı (GEE) kullanılamıyor, Demo moduna dönüldü.\n\n{why}")

season = st.sidebar.number_input("Sezon yılı", min_value=2020, max_value=2030,
                                 value=DEFAULT_TODAY.year, step=1)
today = st.sidebar.date_input("Bugün (tahmin tarihi)", value=DEFAULT_TODAY)

st.sidebar.divider()
st.sidebar.markdown(
    "**Hakkında**\n\n"
    "Sentinel-2 zaman serisinden parsel bazında *hasada kalan gün* tahmini. "
    "V1 kural tabanlı, etiketsiz çalışır (Sedano 2025). "
    "Belirsizlik güven skorunda görünür."
)

parcels = _load()

# Tüm parseller için tahmin (harita renkleri + kooperatif tablosu)
try:
    with st.spinner("Veri çekiliyor / tahmin üretiliyor…"):
        results = {p.id: run_prediction(p, source, int(season), today) for p in parcels}
except Exception as e:  # GEE init/çekim hatası dahil
    st.error(f"Veri kaynağı hatası: {e}")
    if mode.startswith("Canlı"):
        st.info("GEE kurulumu için README → 'Canlı moda geçiş'. "
                "`earthengine authenticate` çalıştırıldı mı, `EE_PROJECT` ayarlı mı?")
    st.stop()

# === Başlık ====================================================================
st.title("Hasat Zamanı Karar Destek Sistemi")
st.markdown("**Tarlanız size hasada kaç gün kaldığını söyler.** "
            "Pilot: kışlık buğday · Konya / Çumra")

if mode.startswith("Demo"):
    st.warning(
        "🧪 **DEMO modu — veriler sentetiktir.** Tahmin sayıları (ör. kalan gün) ve "
        "parsel farkları gerçek uydudan ölçülmedi; veri hattını ve arayüzü göstermek için "
        "üretildi. **Doğruluk iddiası taşımaz.** Gerçek tahmin için sol panelden *Canlı (GEE)* "
        "modunu bağlayın.",
        icon="⚠️",
    )

tab_map, tab_coop, tab_eval = st.tabs(
    ["🗺️ Harita & Parsel", "👥 Kooperatif görünümü", "📊 Doğruluk (backtest)"])

# === Sekme 1: Harita & Parsel ==================================================
with tab_map:
    col_map, col_detail = st.columns([1.1, 1])

    with col_map:
        st.subheader("Parseller")
        try:
            import folium
            from streamlit_folium import st_folium

            center = (sum(p.centroid[0] for p in parcels) / len(parcels),
                      sum(p.centroid[1] for p in parcels) / len(parcels))
            fmap = folium.Map(location=center, zoom_start=13, tiles="OpenStreetMap")
            for p in parcels:
                pred, _ = results[p.id]
                color = status_color(pred.remaining_days)
                folium.Polygon(
                    locations=[[lat, lon] for lon, lat in p.polygon],
                    color=color, fill=True, fill_color=color, fill_opacity=0.55, weight=2,
                    tooltip=(f"{p.name} · {p.area_ha} ha<br>"
                             f"Kalan: {pred.remaining_days} gün · {pred.pheno_phase}"),
                ).add_to(fmap)
            st_folium(fmap, height=380, use_container_width=True, returned_objects=[])
        except ModuleNotFoundError:
            st.info("Harita için `folium` + `streamlit-folium` kurun. "
                    "Aşağıdaki listeden parsel seçebilirsiniz.")

        st.caption("🟢 zaman var · 🟠 yaklaşıyor (≤21 gün) · 🔴 hasat çok yakın (≤7 gün)")

    with col_detail:
        names = {p.id: p.name for p in parcels}
        sel_id = st.selectbox("Parsel seç", options=[p.id for p in parcels],
                              format_func=lambda i: names[i])
        parcel = next(p for p in parcels if p.id == sel_id)
        pred, frame = results[sel_id]

        st.markdown(f"#### {parcel.name} · {parcel.area_ha} ha · kışlık buğday")
        c1, c2 = st.columns(2)
        c1.metric("Tahmini hasat", pred.est_harvest.strftime("%d %b %Y"),
                  f"±{(pred.ci_upper - pred.ci_lower)//2} gün belirsizlik",
                  delta_color="off")
        c2.metric("Kalan gün", f"{pred.remaining_days}",
                  f"{pred.ci_lower}–{pred.ci_upper} gün aralığı", delta_color="off")
        c3, c4 = st.columns(2)
        c3.metric("Fenolojik evre", pred.pheno_phase)
        c4.metric(
            "Veri güveni", confidence_pill(pred.confidence),
            help="Bu skor GİRDİNİN kalitesini ölçer (gözlem yoğunluğu + veri tazeliği + "
                 "sinyal netliği). Tahminin DOĞRULUĞU değildir. Gerçek doğruluk (±gün isabet) "
                 "ancak saha hasat tarihiyle ölçülür — henüz etiket yok.",
        )
        st.caption("ℹ️ *Veri güveni ≠ doğruluk.* Yüksek skor 'girdi temiz' demek; "
                   "'tahmin %X doğru' demek değil. Tahmin tavsiyedir, karar değil.")

        if pred.confidence <= 0.4:
            st.warning("Düşük veri güveni: veri eski / bulutluluk yüksek / sinyal zayıf olabilir. "
                       "Aşağıdaki 'Neden bu tahmin?' panelini açın.")

        with st.expander("🔍 Neden bu tahmin?"):
            st.markdown(reason_text(pred))
            st.markdown(
                "**Kalan gün neye göre?** Tahmin üç bileşeni birleştirir: (1) NDVI tepe-sonrası "
                "düşüş hızı, (2) NDMI kuruma sinyali, (3) bölgesel hasat takvimi önseli "
                "(`05_VERI §7.1`). Yan parselden farklıysa, o tarlanın **kendi** indeks eğrisi "
                "farklı (ekim tarihi/çeşit/sulama). Demo modunda bu eğri sentetiktir."
            )
            st.json(pred.reason_signals, expanded=False)

# === Eğri grafiği (sekme 1 altında tam genişlik) ===============================
with tab_map:
    st.subheader(f"İndeks zaman serisi — {parcel.name}")
    obs = frame[frame["date"] <= pd.Timestamp(today)]
    ndvi_s = smooth_series(obs, "ndvi")
    ndmi_s = smooth_series(obs, "ndmi")

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=obs["date"], y=obs["ndvi"], mode="markers",
                             name="NDVI (gözlem)", marker=dict(color="#2ca02c", size=6)))
    fig.add_trace(go.Scatter(x=ndvi_s.index, y=ndvi_s.values, mode="lines",
                             name="NDVI (yumuşatılmış)", line=dict(color="#2ca02c")))
    fig.add_trace(go.Scatter(x=ndmi_s.index, y=ndmi_s.values, mode="lines",
                             name="NDMI (yumuşatılmış)", line=dict(color="#1f77b4", dash="dot")))
    has_vh = obs["vh"].notna().any()
    if has_vh:
        fig.add_trace(go.Scatter(x=obs["date"], y=obs["vh"], mode="lines",
                                 name="VH (radar, dB)", line=dict(color="#999", width=1)),
                      secondary_y=True)
    else:
        st.caption("ℹ️ Bu parsel-sezon için Sentinel-1 VH (radar) verisi yok — "
                   "grafik yalnız optik indekslerle çizildi (S1 zorunlu değil, Faz 4).")

    # İşaretler: POS, bugün, tahmini hasat ± güven aralığı
    r = pred.reason_signals
    fig.add_vline(x=pd.Timestamp(today), line=dict(color="#444", dash="dash"),
                  annotation_text="bugün")
    fig.add_vline(x=pd.Timestamp(pred.est_harvest), line=dict(color="#d62728"),
                  annotation_text="tahmini hasat")
    fig.add_vrect(x0=pd.Timestamp(today) + pd.Timedelta(days=pred.ci_lower),
                  x1=pd.Timestamp(today) + pd.Timedelta(days=pred.ci_upper),
                  fillcolor="#d62728", opacity=0.10, line_width=0)
    fig.update_yaxes(title_text="NDVI / NDMI", range=[0, 1], secondary_y=False)
    fig.update_yaxes(title_text="VH (dB)", secondary_y=True)
    fig.update_layout(height=380, margin=dict(l=10, r=10, t=30, b=10),
                      legend=dict(orientation="h", y=1.12))
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Bu tahmin NDVI düşüşü, NDMI kuruma sinyali ve bölgesel takvim önseline göre üretilmiştir. "
               "Tahmin tavsiyedir, karar değil (06_URUN §7.2).")

# === Sekme 2: Kooperatif görünümü ==============================================
with tab_coop:
    st.subheader("Hasat sırası — hangi tarla önce?")
    st.caption("Kooperatif/agronomist için: biçerdöver ve kantar planlamasında darboğazı önler "
               "(01_VIZYON §5.3).")
    rows = []
    for p in parcels:
        pr, _ = results[p.id]
        rows.append({
            "Parsel": p.name, "Alan (ha)": p.area_ha,
            "Tahmini hasat": pr.est_harvest.strftime("%d %b"),
            "Kalan gün": pr.remaining_days, "Evre": pr.pheno_phase,
            "Veri güveni %": round(pr.confidence * 100),
            "Durum": ("🔴" if pr.remaining_days <= 7 else "🟠" if pr.remaining_days <= 21 else "🟢"),
        })
    df = pd.DataFrame(rows).sort_values("Kalan gün").reset_index(drop=True)
    st.dataframe(df, use_container_width=True, hide_index=True)

    wave = df.groupby(pd.cut(df["Kalan gün"], [-1, 7, 14, 21, 999],
                             labels=["0–7 gün", "8–14 gün", "15–21 gün", "22+ gün"]),
                      observed=False)["Parsel"].count()
    st.bar_chart(wave, height=220)
    st.caption("Hafta hafta hasat dalgası — alım firması/kooperatif tedarik planlaması için.")

# === Sekme 3: Doğruluk (backtest) ==============================================
with tab_eval:
    st.subheader("Doğruluk ölçümü — lead-time backtest")
    st.error(
        "🧪 **Bu sonuçlar SENTETİK etiketle üretildi.** Ölçüm KODUNUN doğru çalıştığını "
        "ve motorun davranışını gösterir — **gerçek tarım doğruluğunu DEĞİL.** Gerçek MAE "
        "ancak saha hasat tarihleri (`data/harvest_labels.csv` → gerçek kayıtlar) + Canlı "
        "Sentinel-2 ile elde edilir. Çatı hazır; veri gelince aynı kodla çalışır.",
        icon="⚠️",
    )
    st.caption("Yöntem: her parselin gerçek hasat tarihinden 40/30/20/10/5 gün önce tahmin "
               "üretilir, hata = (tahmin − gerçek) gün. Validasyon yaklaşımı 05_VERI §8.")

    labels = load_labels()
    if mode.startswith("Demo"):
        res = backtest(parcels, labels, source)
    else:
        st.info("Canlı GEE modunda backtest çok sayıda gerçek uydu çağrısı yapar (yavaş). "
                "Çalıştırmak için butona basın.")
        if st.button("▶︎ Backtest çalıştır (gerçek GEE)"):
            with st.spinner("Backtest çalışıyor — gerçek uydu verisi çekiliyor…"):
                res = backtest(parcels, labels, source)
        else:
            st.stop()

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("MAE (gün)", f"{res.mae}",
              f"hedef ≤ {TARGETS['mae']:.0f}",
              delta_color="normal" if res.mae <= TARGETS["mae"] else "inverse")
    m2.metric("±7 gün isabet", f"%{res.hit7*100:.0f}",
              f"hedef ≥ %{TARGETS['hit7']*100:.0f}",
              delta_color="normal" if res.hit7 >= TARGETS["hit7"] else "inverse")
    m3.metric("±14 gün isabet", f"%{res.hit14*100:.0f}",
              f"hedef ≥ %{TARGETS['hit14']*100:.0f}",
              delta_color="normal" if res.hit14 >= TARGETS["hit14"] else "inverse")
    m4.metric("Bias (gün)", f"{res.bias:+.1f}",
              "− erken / + geç tahmin", delta_color="off")

    st.markdown(f"**RMSE:** {res.rmse} gün · **±3 gün isabet:** %{res.hit3*100:.0f} · "
                f"**kapsama:** %{res.coverage*100:.0f} · "
                f"**güven aralığı kapsaması:** %{res.ci_coverage*100:.0f} "
                f"(ideal ~%80; düşükse aralık dar → kalibrasyon gerekir, `05_VERI §8` ECE).")

    cL, cR = st.columns([1, 1])
    with cL:
        st.markdown("**Hasada yaklaşınca doğruluk artar mı?**")
        lead_df = pd.DataFrame({"lead (gün önce)": list(res.per_lead_mae.keys()),
                                "MAE (gün)": list(res.per_lead_mae.values())}
                               ).set_index("lead (gün önce)")
        st.bar_chart(lead_df, height=240)
        st.caption("Beklenen bilimsel davranış: lead küçüldükçe (hasat yaklaştıkça) MAE düşer.")
    with cR:
        st.markdown("**Parsel-bazlı kayıtlar**")
        show = res.rows[res.rows["producible"] == True].drop(columns=["producible"])  # noqa: E712
        st.dataframe(show, use_container_width=True, hide_index=True, height=240)
