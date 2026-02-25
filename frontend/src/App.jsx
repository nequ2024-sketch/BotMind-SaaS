import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'https://botmind-saas.onrender.com';

export default function App() {
  // الحالات الأساسية (State)
  const [token, setToken] = useState(localStorage.getItem('token') || '');
  const [userId, setUserId] = useState(localStorage.getItem('userId') || '1');
  const [isLoginMode, setIsLoginMode] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [activeTab, setActiveTab] = useState('home');
  const [isBotActive, setIsBotActive] = useState(true);
  const [agents, setAgents] = useState([]);
  const [selectedAgent, setSelectedAgent] = useState('');
  const [products, setProducts] = useState([]);
  const [newProductName, setNewProductName] = useState('');
  const [newProductPrice, setNewProductPrice] = useState('');

  // دالة جلب المنتجات من السيرفر
  const fetchProducts = async (currentId) => {
    try {
      const id = currentId || userId;
      const res = await axios.get(`${API_URL}/products/list/${id}`);
      setProducts(res.data);
    } catch (err) { console.log("Products fetch error:", err); }
  };

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    
    // 🔴 مستشعر النجاح التلقائي بعد العودة من فيسبوك
    if (urlParams.get('login') === 'success') {
      const activeToken = "authorized_ig_session";
      setToken(activeToken);
      localStorage.setItem('token', activeToken);
      localStorage.setItem('userId', "1");
      setUserId("1");
      window.history.replaceState({}, document.title, "/");
    }

    if (token) {
      axios.get(`${API_URL}/agents/`).then(res => setAgents(res.data)).catch(err => console.log(err));
      axios.get(`${API_URL}/agents/status/${userId}`).then(res => {
         if(res.data.is_bot_active !== undefined) setIsBotActive(res.data.is_bot_active);
      }).catch(err => console.log(err));
      fetchProducts();
    }
  }, [token, userId]);

  // دالة المصادقة (دخول / تسجيل)
  const handleAuth = async (e) => {
    e.preventDefault();
    const endpoint = isLoginMode ? '/auth/login' : '/auth/register';
    try {
      const res = await axios.post(`${API_URL}${endpoint}`, { email, password });
      const newToken = res.data.access_token;
      setToken(newToken);
      localStorage.setItem('token', newToken);
      setUserId("1"); // أو UserId القادم من السيرفر
      localStorage.setItem('userId', "1");
    } catch (err) { alert("تأكد من البيانات أو أنشئ حساباً جديداً ❌"); }
  };

  const handleInstagramLogin = () => {
    window.location.href = `${API_URL}/auth/instagram/login`;
  };

  const toggleBot = async () => {
    try {
      const res = await axios.post(`${API_URL}/agents/toggle-bot/${userId}`);
      setIsBotActive(res.data.is_bot_active);
    } catch(err) { alert("خطأ في تغيير حالة البوت"); }
  };

  const saveAgent = async () => {
    if(!selectedAgent) return alert("اختر شخصية أولاً!");
    try {
      const res = await axios.post(`${API_URL}/agents/select/${userId}/${selectedAgent}`);
      alert("تم حفظ الوكيل الذكي بنجاح! ✅");
    } catch(err) { alert("خطأ في الحفظ"); }
  };

  const addProduct = async () => {
    if(!newProductName || !newProductPrice) return alert("أدخل بيانات المنتج");
    try {
      await axios.post(`${API_URL}/products/add/${userId}`, { name: newProductName, price: parseFloat(newProductPrice) });
      setNewProductName(''); setNewProductPrice('');
      fetchProducts();
      alert("تمت إضافة المنتج للمتجر! 🛍️");
    } catch (err) { alert("خطأ في الإضافة"); }
  };

  // شعار الشبكة المتحرك (SVG)
  const AnimatedLogo = () => (
    <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '15px' }}>
      <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="#00f2ff" strokeWidth="1.5">
        <style>{`
          @keyframes glow { 0%, 100% { opacity: 0.3; } 50% { opacity: 1; } }
          .node { animation: glow 2s infinite ease-in-out; }
        `}</style>
        <circle className="node" cx="12" cy="12" r="3" fill="#00f2ff"/>
        <circle cx="12" cy="4" r="2" stroke="#a855f7"/><circle cx="12" cy="20" r="2" stroke="#a855f7"/>
        <circle cx="4" cy="12" r="2" stroke="#a855f7"/><circle cx="20" cy="12" r="2" stroke="#a855f7"/>
        <path d="M12 7v3m0 4v3M7 12h3m4 0h3" stroke="#00f2ff" strokeLinecap="round"/>
      </svg>
    </div>
  );

  // واجهة لوحة التحكم (Dashboard)
  if (token) {
    return (
      <div style={styles.dashWrapper}>
        <aside style={styles.sidebar}>
          <AnimatedLogo />
          <h2 style={{color: '#fff', textAlign: 'center', fontSize: '20px'}}>BotMind AI</h2>
          <div style={activeTab === 'home' ? styles.navItemActive : styles.navItem} onClick={() => setActiveTab('home')}>🏠 الرئيسية</div>
          <div style={activeTab === 'products' ? styles.navItemActive : styles.navItem} onClick={() => setActiveTab('products')}>🛍️ المنتجات</div>
          <div style={styles.navItem} onClick={() => {localStorage.clear(); setToken('');}}>🚪 خروج</div>
        </aside>

        <main style={styles.main}>
          <h1 style={{color: '#fff', fontSize: '28px', marginBottom: '30px'}}>لوحة التحكم</h1>
          
          {activeTab === 'home' ? (
            <>
              <div style={styles.cardPro}>
                <div style={{textAlign: 'right'}}>
                  <h3 style={{color: '#fff', margin: 0}}>حالة جيش الـ 1000 روبوت 🤖</h3>
                  <p style={{color: '#8b949e'}}>الذكاء الاصطناعي جاهز للرد على زبائنك فوراً.</p>
                </div>
                <button onClick={toggleBot} style={isBotActive ? styles.btnActive : styles.btnInactive}>
                  {isBotActive ? '🟢 البوت يعمل' : '🔴 البوت متوقف'}
                </button>
              </div>

              <div style={styles.card}>
                <h3 style={{color: '#00f2ff'}}>تخصيص شخصية الوكيل</h3>
                <div style={{display: 'flex', gap: '10px', marginTop: '15px'}}>
                  <select style={styles.selectBox} onChange={(e) => setSelectedAgent(e.target.value)} value={selectedAgent}>
                    <option value="">-- اختر الشخصية --</option>
                    {agents.map(a => <option key={a.id} value={a.id}>{a.name}</option>)}
                  </select>
                  <button onClick={saveAgent} style={styles.secondaryBtn}>حفظ الشخصية</button>
                </div>
              </div>

              <div style={styles.actionGrid}>
                <div style={styles.cardProBorder}>
                  <h3 style={{color: '#fff'}}>الاشتراك الاحترافي 🌟</h3>
                  <h2 style={{color: '#a855f7', fontSize: '32px'}}>50$ <span style={{fontSize: '14px', color: '#555'}}>/شهر</span></h2>
                  <button onClick={() => window.open(`${API_URL}/payment/subscribe/${userId}`)} style={styles.payBtn}>تفعيل الدفع 💳</button>
                </div>
                <div style={styles.card}>
                   <h3 style={{color: '#fff'}}>ربط الحساب الاجتماعي 🔗</h3>
                   <button onClick={handleInstagramLogin} style={styles.igLogin}>ربط إنستغرام 🔄</button>
                </div>
              </div>
            </>
          ) : (
            <div>
              <div style={{...styles.card, display: 'flex', gap: '10px', marginBottom: '30px'}}>
                <input style={styles.loginInput} placeholder="اسم المنتج" value={newProductName} onChange={e => setNewProductName(e.target.value)} />
                <input style={styles.loginInput} type="number" placeholder="السعر $" value={newProductPrice} onChange={e => setNewProductPrice(e.target.value)} />
                <button onClick={addProduct} style={styles.payBtnSmall}>إضافة ➕</button>
              </div>
              <div style={styles.actionGrid}>
                {products.map(p => (
                  <div key={p.id} style={styles.card}>
                    <h3 style={{color: '#00f2ff'}}>{p.name}</h3>
                    <h2 style={{color: '#fff'}}>{p.price} $</h2>
                  </div>
                ))}
              </div>
            </div>
          )}
        </main>
      </div>
    );
  }

  // واجهة تسجيل الدخول (Login / Register)
  return (
    <div style={styles.loginPage}>
      <div style={styles.glowCircle}></div>
      <div style={styles.loginContent}>
        <AnimatedLogo />
        <h1 style={styles.brandTitle}>BotMind AI</h1>
        <form onSubmit={handleAuth} style={styles.form}>
          <input type="email" placeholder="Email" style={styles.loginInput} onChange={e => setEmail(e.target.value)} required />
          <input type="password" placeholder="Password" style={styles.loginInput} onChange={e => setPassword(e.target.value)} required />
          <button type="submit" style={styles.loginSubmit}>{isLoginMode ? 'Login' : 'Register'}</button>
          <div style={styles.divider}><span>أو</span></div>
          <button type="button" onClick={handleInstagramLogin} style={styles.igLogin}>Login with Instagram</button>
        </form>
        <p style={{color: '#8b949e', cursor: 'pointer', marginTop: '25px', fontSize: '14px'}} onClick={() => setIsLoginMode(!isLoginMode)}>
          {isLoginMode ? 'ليس لديك حساب؟ أنشئ واحداً الآن' : 'لديك حساب بالفعل؟ سجل دخولك'}
        </p>
      </div>
    </div>
  );
}

// الستايلات الكاملة (CSS-in-JS) لضمان الشكل المثالي
const styles = {
  loginPage: { height: '100vh', backgroundColor: '#02060f', display: 'flex', justifyContent: 'center', alignItems: 'center', position: 'relative', overflow: 'hidden', direction: 'rtl', fontFamily: 'sans-serif' },
  glowCircle: { position: 'absolute', width: '600px', height: '600px', background: 'radial-gradient(circle, rgba(0,242,255,0.08) 0%, transparent 70%)', zIndex: 0 },
  loginContent: { width: '100%', maxWidth: '400px', textAlign: 'center', zIndex: 1, padding: '20px' },
  brandTitle: { color: '#fff', fontSize: '42px', fontWeight: 'bold', marginBottom: '30px', textShadow: '0 0 15px rgba(0,242,255,0.3)' },
  form: { display: 'flex', flexDirection: 'column', gap: '15px' },
  loginInput: { padding: '16px', borderRadius: '12px', border: '1px solid #1f2937', backgroundColor: '#0b0f17', color: '#fff', textAlign: 'center', outline: 'none' },
  loginSubmit: { padding: '16px', borderRadius: '12px', border: 'none', backgroundColor: '#00f2ff', fontWeight: 'bold', cursor: 'pointer', color: '#000' },
  igLogin: { padding: '16px', borderRadius: '12px', border: '1px solid #0082ff', color: '#0082ff', backgroundColor: 'transparent', cursor: 'pointer', fontWeight: 'bold' },
  divider: { margin: '20px 0', borderBottom: '1px solid #1f2937', lineHeight: '0.1em', color: '#444' },
  dashWrapper: { display: 'flex', height: '100vh', backgroundColor: '#050a10', direction: 'rtl' },
  sidebar: { width: '260px', backgroundColor: '#0b0f17', padding: '30px', borderLeft: '1px solid #1f2937' },
  navItem: { padding: '15px', color: '#8b949e', cursor: 'pointer', textAlign: 'center', marginTop: '10px', borderRadius: '10px' },
  navItemActive: { padding: '15px', color: '#00f2ff', backgroundColor: 'rgba(0,242,255,0.05)', borderRadius: '10px', fontWeight: 'bold', textAlign: 'center', marginTop: '10px' },
  main: { flex: 1, padding: '40px', overflowY: 'auto' },
  card: { backgroundColor: '#0b0f17', padding: '25px', borderRadius: '18px', border: '1px solid #1f2937' },
  cardPro: { backgroundColor: '#0b0f17', padding: '25px', borderRadius: '18px', border: '1px solid #1f2937', display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '25px' },
  cardProBorder: { backgroundColor: '#111827', padding: '30px', borderRadius: '18px', border: '1px solid #a855f7' },
  payBtn: { padding: '14px 30px', borderRadius: '10px', border: 'none', backgroundColor: '#a855f7', color: '#fff', fontWeight: 'bold', cursor: 'pointer', marginTop: '15px' },
  payBtnSmall: { padding: '12px 25px', borderRadius: '10px', border: 'none', backgroundColor: '#00f2ff', fontWeight: 'bold', cursor: 'pointer' },
  secondaryBtn: { padding: '12px 20px', borderRadius: '10px', border: '1px solid #00f2ff', color: '#00f2ff', backgroundColor: 'transparent', cursor: 'pointer' },
  selectBox: { flex: 1, padding: '12px', borderRadius: '10px', backgroundColor: '#050a10', color: '#fff', border: '1px solid #1f2937' },
  actionGrid: { display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginTop: '25px' },
  btnActive: { padding: '12px 25px', borderRadius: '10px', border: 'none', backgroundColor: '#10b981', color: '#fff', fontWeight: 'bold', cursor: 'pointer' },
  btnInactive: { padding: '12px 25px', borderRadius: '10px', border: 'none', backgroundColor: '#ef4444', color: '#fff', fontWeight: 'bold', cursor: 'pointer' }
};