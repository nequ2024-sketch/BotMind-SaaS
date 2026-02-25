import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

export default function App() {
  const [token, setToken] = useState(localStorage.getItem('token') || '');
  const [userId, setUserId] = useState(localStorage.getItem('userId') || '');
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

  const fetchProducts = async () => {
    try {
      const res = await axios.get(`${API_URL}/products/list/${userId}`);
      setProducts(res.data);
    } catch (err) { console.log(err); }
  };

  useEffect(() => {
    if (token) {
      axios.get(`${API_URL}/agents/`).then(res => setAgents(res.data)).catch(err => console.log(err));
      axios.get(`${API_URL}/agents/status/${userId}`).then(res => {
         if(res.data.is_bot_active !== undefined) setIsBotActive(res.data.is_bot_active);
      }).catch(err => console.log(err));
      fetchProducts();
    }
  }, [token]);

  const handleAuth = async (e) => {
    e.preventDefault();
    try {
      const endpoint = isLoginMode ? '/auth/login' : '/auth/register';
      const res = await axios.post(`${API_URL}${endpoint}`, { email, password });
      setToken(res.data.access_token);
      localStorage.setItem('token', res.data.access_token);
      setUserId(1); 
    } catch (err) { alert("تأكد من البيانات ❌"); }
  };

  const toggleBot = async () => {
    try {
      const res = await axios.post(`${API_URL}/agents/toggle-bot/${userId}`);
      if(res.data.is_bot_active !== undefined) setIsBotActive(res.data.is_bot_active);
    } catch(err) { alert("خطأ في تغيير حالة البوت"); }
  };

  const saveAgent = async () => {
    if(!selectedAgent) return alert("اختر شخصية أولاً!");
    try {
      const res = await axios.post(`${API_URL}/agents/select/${userId}/${selectedAgent}`);
      alert(res.data.message);
    } catch(err) { alert("خطأ في حفظ البوت"); }
  };

  const addProduct = async () => {
    if(!newProductName || !newProductPrice) return alert("أدخل اسم وسعر المنتج!");
    try {
      await axios.post(`${API_URL}/products/add/${userId}`, { name: newProductName, price: parseFloat(newProductPrice) });
      setNewProductName(''); setNewProductPrice('');
      fetchProducts();
      alert("تمت إضافة المنتج!");
    } catch (err) { alert("خطأ في إضافة المنتج"); }
  };

  const AnimatedNetworkLogo = () => (
    <div className="logo-wrapper" style={{ display: 'flex', justifyContent: 'center' }}>
      <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="#00f2ff" strokeWidth="1.5">
        <style>
          {` @keyframes pulse { 0% { opacity: 0.4; filter: drop-shadow(0 0 5px #00f2ff); } 50% { opacity: 1; filter: drop-shadow(0 0 15px #00f2ff); } 100% { opacity: 0.4; filter: drop-shadow(0 0 5px #00f2ff); } } .node { animation: pulse 2s infinite ease-in-out; } .line-anim { stroke-dasharray: 10; animation: dash 1.5s linear infinite; } @keyframes dash { to { stroke-dashoffset: -20; } } `}
        </style>
        <circle className="node" cx="12" cy="12" r="2" fill="#00f2ff"/>
        <circle className="node" cx="12" cy="4" r="2"/><circle className="node" cx="12" cy="20" r="2"/>
        <circle className="node" cx="4" cy="12" r="2"/><circle className="node" cx="20" cy="12" r="2"/>
        <line className="line-anim" x1="12" y1="6" x2="12" y2="10"/><line className="line-anim" x1="12" y1="14" x2="12" y2="18"/>
        <line className="line-anim" x1="6" y1="12" x2="10" y2="12"/><line className="line-anim" x1="14" y1="12" x2="18" y2="12"/>
      </svg>
    </div>
  );

  if (token) {
    return (
      <div style={styles.dashWrapper}>
        <aside style={styles.sidebar}>
          <AnimatedNetworkLogo />
          <h2 style={{color: '#fff', marginTop: '10px', textAlign: 'center'}}>BotMind AI</h2>
          <div style={activeTab === 'home' ? styles.navItemActive : styles.navItem} onClick={() => setActiveTab('home')}>🏠 الرئيسية</div>
          <div style={activeTab === 'products' ? styles.navItemActive : styles.navItem} onClick={() => setActiveTab('products')}>🛍️ المنتجات الذكية</div>
          <div style={styles.navItem} onClick={() => {localStorage.clear(); setToken('');}}>🚪 خروج</div>
        </aside>

        <main style={styles.main}>
          <h1 style={{color: '#fff', fontSize: '26px', marginBottom: '20px'}}>لوحة التحكم</h1>
          
          {activeTab === 'home' ? (
            <>
              {/* زر التحكم بالبوت */}
              <div style={{...styles.agentsCard, display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
                <div style={{textAlign: 'right'}}>
                  <h3 style={{color: '#fff', margin: 0}}>⚙️ محرك الذكاء الاصطناعي</h3>
                  <p style={{color: '#8b949e', margin: '5px 0 0'}}>أوقف البوت مؤقتاً إذا أردت الرد بنفسك.</p>
                </div>
                <button onClick={toggleBot} style={isBotActive ? styles.btnActive : styles.btnInactive}>
                  {isBotActive ? '🟢 البوت يعمل' : '🔴 البوت متوقف'}
                </button>
              </div>

              {/* اختيار الشخصية */}
              <div style={styles.agentsCard}>
                <h3 style={{color: '#00f2ff', margin: 0}}>🤖 تخصيص الوكيل الذكي (AI Agent)</h3>
                <p style={{color: '#8b949e', margin: '5px 0 15px'}}>اختر شخصية المشهور الذي سيرد على زبائنك:</p>
                <div style={{display: 'flex', gap: '10px', justifyContent: 'center'}}>
                   <select style={styles.selectBox} onChange={(e) => setSelectedAgent(e.target.value)} value={selectedAgent}>
                      <option value="">-- اختر المشهور --</option>
                      {agents.map(a => <option key={a.id} value={a.id}>{a.name} ({a.persona})</option>)}
                   </select>
                   <button onClick={saveAgent} style={styles.secondaryBtn}>حفظ الشخصية</button>
                </div>
              </div>

              {/* الاشتراكات */}
              <div style={styles.actionGrid}>
                 <div style={styles.cardPro}>
                   <h3 style={{color: '#fff'}}>الاشتراك الاحترافي 🌟</h3>
                   <p style={{color: '#8b949e'}}>ردود ذكية على 10 بوستات شهرياً.</p>
                   <h2 style={{color: '#a855f7'}}>50$ <span style={{fontSize: '14px', color: '#8b949e'}}>/شهر</span></h2>
                   <button onClick={() => window.open(`${API_URL}/payment/subscribe/${userId}`)} style={styles.payBtn}>دفع بالبطاقة 💳</button>
                 </div>
                 <div style={styles.card}>
                   <h3 style={{color: '#fff'}}>بوست إضافي ⚡</h3>
                   <h2 style={{color: '#00f2ff'}}>5$ <span style={{fontSize: '14px', color: '#8b949e'}}>/بوست</span></h2>
                   <button onClick={() => window.open(`${API_URL}/payment/pay-extra-post/${userId}`)} style={styles.secondaryBtn}>شراء بوست</button>
                 </div>
              </div>
            </>
          ) : (
            // قسم إدارة المنتجات
            <div>
              <div style={{...styles.card, display: 'flex', gap: '10px', marginBottom: '20px'}}>
                <input style={styles.loginInput} placeholder="اسم المنتج" value={newProductName} onChange={e => setNewProductName(e.target.value)} />
                <input style={styles.loginInput} type="number" placeholder="السعر ($)" value={newProductPrice} onChange={e => setNewProductPrice(e.target.value)} />
                <button onClick={addProduct} style={styles.payBtn}>إضافة للمتجر ➕</button>
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

  // شاشة الدخول
  return (
    <div style={styles.loginPage}>
      <div style={styles.glowCircle}></div>
      <div style={styles.loginContent}>
        <div style={styles.logoSection}>
          <AnimatedNetworkLogo />
          <h1 style={styles.brandTitle}>BotMind AI</h1>
        </div>
        <form onSubmit={handleAuth} style={styles.form}>
          <input type="email" placeholder="App/page inbox" style={styles.loginInput} onChange={e => setEmail(e.target.value)} required />
          <input type="password" placeholder="Password / Secret" style={styles.loginInput} onChange={e => setPassword(e.target.value)} required />
          <button type="submit" style={styles.loginSubmit}>Login</button>
          <div style={styles.divider}><span>أو</span></div>
          <button type="button" style={styles.igLogin}>Login with Instagram</button>
        </form>
        <p style={{color: '#888', cursor: 'pointer', marginTop: '20px'}} onClick={() => setIsLoginMode(!isLoginMode)}>
          {isLoginMode ? 'أنشئ حساباً جديداً' : 'لديك حساب؟ سجل دخولك'}
        </p>
      </div>
    </div>
  );
}

const styles = {
  loginPage: { height: '100vh', backgroundColor: '#02060f', display: 'flex', justifyContent: 'center', alignItems: 'center', position: 'relative', overflow: 'hidden', direction: 'rtl', fontFamily: 'sans-serif' },
  glowCircle: { position: 'absolute', width: '600px', height: '600px', background: 'radial-gradient(circle, rgba(0,242,255,0.1) 0%, rgba(168,85,247,0.05) 40%, transparent 70%)', zIndex: 0 },
  loginContent: { display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', zIndex: 1, width: '100%', maxWidth: '380px' },
  logoSection: { display: 'flex', flexDirection: 'column', alignItems: 'center', marginBottom: '35px' },
  brandTitle: { color: '#fff', fontSize: '46px', fontWeight: 'bold', margin: '15px 0 0 0', textShadow: '0 0 20px rgba(0,242,255,0.4)', textAlign: 'center' },
  form: { width: '100%', display: 'flex', flexDirection: 'column', gap: '15px' },
  loginInput: { backgroundColor: 'rgba(30, 30, 45, 0.6)', border: '1px solid rgba(255,255,255,0.05)', color: '#fff', padding: '16px', borderRadius: '8px', outline: 'none', textAlign: 'center' },
  loginSubmit: { backgroundColor: '#2c2c3a', color: '#fff', border: 'none', padding: '16px', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' },
  divider: { textAlign: 'center', borderBottom: '1px solid #1f2937', lineHeight: '0.1em', margin: '20px 0', color: '#555' },
  igLogin: { background: 'rgba(0, 130, 255, 0.1)', color: '#0082ff', border: '1px solid rgba(0, 130, 255, 0.2)', padding: '14px', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' },
  dashWrapper: { display: 'flex', height: '100vh', backgroundColor: '#050a10', direction: 'rtl', fontFamily: 'sans-serif' },
  sidebar: { width: '260px', backgroundColor: '#0b0f17', borderLeft: '1px solid #1f2937', padding: '30px', display: 'flex', flexDirection: 'column', alignItems: 'center' },
  navItemActive: { width: '100%', padding: '14px', color: '#a855f7', background: 'rgba(168,85,247,0.1)', borderRadius: '8px', fontWeight: 'bold', marginTop: '20px', textAlign: 'center', cursor: 'pointer' },
  navItem: { width: '100%', padding: '14px', color: '#8b949e', cursor: 'pointer', marginTop: '10px', textAlign: 'center' },
  main: { flex: 1, padding: '40px', overflowY: 'auto' },
  agentsCard: { background: 'rgba(0,242,255,0.05)', border: '1px solid rgba(0,242,255,0.2)', padding: '30px', borderRadius: '12px', marginBottom: '30px', textAlign: 'center' },
  selectBox: { padding: '12px', backgroundColor: '#111827', border: '1px solid #374151', color: '#fff', borderRadius: '8px', width: '60%', outline: 'none' },
  actionGrid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px' },
  card: { background: '#0b0f17', padding: '25px', borderRadius: '15px', border: '1px solid #1f2937' },
  cardPro: { background: '#111827', padding: '25px', borderRadius: '15px', border: '1px solid #a855f7', boxShadow: '0 0 20px rgba(168,85,247,0.1)' },
  payBtn: { width: '100%', background: 'linear-gradient(90deg, #a855f7, #6b21a8)', color: '#fff', border: 'none', padding: '14px', borderRadius: '8px', fontWeight: 'bold', cursor: 'pointer', marginTop: '10px' },
  secondaryBtn: { background: '#1f2937', color: '#00f2ff', border: '1px solid #00f2ff', padding: '12px 20px', borderRadius: '8px', fontWeight: 'bold', cursor: 'pointer' },
  btnActive: { background: 'rgba(16, 185, 129, 0.2)', color: '#10b981', border: '1px solid #10b981', padding: '12px 25px', borderRadius: '8px', fontWeight: 'bold', cursor: 'pointer', transition: '0.3s' },
  btnInactive: { background: 'rgba(239, 68, 68, 0.2)', color: '#ef4444', border: '1px solid #ef4444', padding: '12px 25px', borderRadius: '8px', fontWeight: 'bold', cursor: 'pointer', transition: '0.3s' },
};