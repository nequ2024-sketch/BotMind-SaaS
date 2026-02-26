import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'https://botmind-saas.onrender.com';

export default function App() {
  // الحالات الأساسية (State Management)
  const [token, setToken] = useState(localStorage.getItem('token') || '');
  const [userId, setUserId] = useState(localStorage.getItem('userId') || 'user_1');
  const [isLoginMode, setIsLoginMode] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // مستشعرات النظام عند تحميل الصفحة
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    
    if (urlParams.get('login') === 'success') {
      const activeSession = "active_meta_session_2026";
      setToken(activeSession); 
      localStorage.setItem('token', activeSession);
      window.history.replaceState({}, document.title, "/");
    }
    
    if (urlParams.get('payment') === 'success') {
      alert("🎉 مبروك! تمت عملية الدفع بنجاح. تم تفعيل اشتراك الـ 10 بوستات الخاصة بك.");
      window.history.replaceState({}, document.title, "/");
    }
    
    if (urlParams.get('payment') === 'extra_success') {
      alert("⚡ تمت إضافة البوست الإضافي إلى رصيدك بنجاح! يمكنك تشغيل البوت الآن.");
      window.history.replaceState({}, document.title, "/");
    }
  }, []);

  // دالة تسجيل الدخول (محاكاة متقدمة للواجهة)
  const handleAuth = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    
    // تأخير وهمي لمحاكاة الاتصال بالسيرفر
    setTimeout(() => {
      setToken("session_active_mock_token_jwt"); 
      localStorage.setItem('token', "session_active_mock_token_jwt");
      setIsLoading(false);
    }, 1500);
  };

  // دالة طلب دفع USDT من السيرفر
  const handleUsdtPayment = async (type) => {
    try {
      setIsLoading(true);
      const res = await axios.get(`${API_URL}/payment/pay/usdt/${userId}?type=${type}`);
      setIsLoading(false);
      
      const details = `💰 طلب دفع عبر العملات الرقمية:\n\n` +
                      `الشبكة: ${res.data.payment_method}\n` +
                      `المبلغ المطلوب: ${res.data.amount_required}\n\n` +
                      `قم بالتحويل إلى هذه المحفظة:\n${res.data.wallet_address}\n\n` +
                      `${res.data.instructions}`;
      alert(details);
    } catch (err) {
      setIsLoading(false);
      alert("❌ حدث خطأ في الاتصال بالخادم لجلب تفاصيل الـ USDT. تأكد من تشغيل السيرفر.");
    }
  };

  // دالة تسجيل الخروج الآمنة
  const handleLogout = () => {
    if(window.confirm("هل أنت متأكد من رغبتك في تسجيل الخروج؟")) {
      localStorage.clear(); 
      setToken('');
    }
  };

  // ==========================================
  // شاشة لوحة التحكم (للمستخدمين المسجلين)
  // ==========================================
  if (token) {
    return (
      <div style={styles.dashWrapper}>
        <main style={styles.mainContainer}>
          
          {/* الترويسة العلوية */}
          <header style={styles.header}>
            <h1 style={styles.pageTitle}>BotMind AI <span style={{fontSize:'16px', color:'#00f2ff'}}>v2.0</span></h1>
            <p style={styles.subtitle}>الذكاء الاصطناعي الأقوى لإدارة حسابات إنستغرام</p>
          </header>
          
          {/* بطاقة الإحصائيات وحالة الحساب */}
          <section style={styles.statsSection}>
            <div style={styles.statsCard}>
               <div style={styles.statsIcon}>📊</div>
               <div>
                 <h3 style={styles.statsTitle}>رصيد البوستات المجانية</h3>
                 <p style={styles.statsValue}>3 / 3 <span style={{fontSize:'14px', color:'#8b949e'}}>(متبقي)</span></p>
               </div>
            </div>
            <div style={styles.statsCardPro}>
               <div style={styles.statsIcon}>🤖</div>
               <div>
                 <h3 style={styles.statsTitle}>حالة البوت</h3>
                 <p style={{color: '#10b981', fontWeight: 'bold', fontSize: '20px'}}>جاهز للعمل ✅</p>
               </div>
            </div>
          </section>

          {/* قسم خطط الاشتراك والباقات */}
          <h2 style={{color: '#fff', textAlign: 'right', marginBottom: '20px', borderBottom: '1px solid #1f2937', paddingBottom: '10px'}}>ترقية الحساب والباقات 💎</h2>
          <div style={styles.plansGrid}>
             
             {/* بطاقة الاشتراك الشهري (50$) */}
             <div style={styles.planCardPremium}>
               <div style={styles.badge}>الأكثر مبيعاً</div>
               <h3 style={styles.planName}>الاشتراك الاحترافي 🌟</h3>
               <p style={styles.planDesc}>تشغيل الذكاء الاصطناعي على 10 بوستات كاملة شهرياً.</p>
               <h2 style={styles.planPrice}>50$ <span style={styles.priceMonth}>/ شهر</span></h2>
               
               <button 
                  onClick={() => window.location.href=`${API_URL}/payment/subscribe/card/${userId}`} 
                  style={styles.btnStripePrimary}
                  disabled={isLoading}
               >
                 دفع آمن بالبطاقة 💳
               </button>
               <button 
                  onClick={() => handleUsdtPayment('monthly')} 
                  style={styles.btnCryptoPrimary}
                  disabled={isLoading}
               >
                 دفع عبر USDT (كريبتو) 🪙
               </button>
             </div>

             {/* بطاقة البوست الإضافي (5$) */}
             <div style={styles.planCardStandard}>
               <h3 style={styles.planName}>بوست إضافي ⚡</h3>
               <p style={styles.planDesc}>استنفذت الباقات؟ شغل البوت على بوست واحد إضافي.</p>
               <h2 style={styles.planPriceStandard}>5$ <span style={styles.priceMonth}>/ للبوست</span></h2>
               
               <button 
                  onClick={() => window.location.href=`${API_URL}/payment/extra-post/card/${userId}`} 
                  style={styles.btnStripeSecondary}
                  disabled={isLoading}
               >
                 دفع آمن بالبطاقة 💳
               </button>
               <button 
                  onClick={() => handleUsdtPayment('extra')} 
                  style={styles.btnCryptoSecondary}
                  disabled={isLoading}
               >
                 دفع عبر USDT 🪙
               </button>
             </div>
          </div>
          
          {/* قسم الإعدادات السريعة (ربط إنستغرام) */}
          <section style={styles.actionSection}>
             <button onClick={() => window.location.href=`${API_URL}/auth/instagram/login`} style={styles.btnInstagram}>
               🔗 ربط أو تحديث حساب إنستغرام الخاص بك
             </button>
             <button onClick={handleLogout} style={styles.btnLogout}>
               تسجيل خروج آمن 🚪
             </button>
          </section>

        </main>
      </div>
    );
  }

  // ==========================================
  // شاشة تسجيل الدخول والترحيب
  // ==========================================
  return (
    <div style={styles.loginPage}>
      <div style={styles.glowEffect}></div>
      <div style={styles.loginBox}>
        <div style={styles.logoCircle}>🤖</div>
        <h1 style={styles.loginTitle}>BotMind AI</h1>
        <p style={styles.loginSubtitle}>نظام الرد الذكي المتقدم</p>
        
        <form onSubmit={handleAuth} style={styles.loginForm}>
          <input 
            type="email" 
            placeholder="البريد الإلكتروني" 
            style={styles.inputField} 
            onChange={e => setEmail(e.target.value)} 
            required 
          />
          <input 
            type="password" 
            placeholder="كلمة المرور" 
            style={styles.inputField} 
            onChange={e => setPassword(e.target.value)} 
            required 
          />
          
          <button type="submit" style={styles.btnSubmit} disabled={isLoading}>
            {isLoading ? 'جاري التحميل...' : (isLoginMode ? 'تسجيل الدخول' : 'إنشاء حساب جديد')}
          </button>
          
          <div style={styles.dividerContainer}>
             <div style={styles.dividerLine}></div>
             <span style={styles.dividerText}>أو</span>
             <div style={styles.dividerLine}></div>
          </div>
          
          <button type="button" onClick={() => window.location.href=`${API_URL}/auth/instagram/login`} style={styles.btnInstagramLogin}>
            Login with Instagram 📸
          </button>
        </form>
        
        <p style={styles.toggleText} onClick={() => setIsLoginMode(!isLoginMode)}>
          {isLoginMode ? 'ليس لديك حساب؟ اضغط هنا للإنشاء' : 'لديك حساب بالفعل؟ قم بتسجيل الدخول'}
        </p>
      </div>
    </div>
  );
}

// ==========================================
// ملف الأنماط الكامل (CSS-in-JS Architecture)
// ==========================================
const styles = {
  // أنماط صفحة تسجيل الدخول
  loginPage: { minHeight: '100vh', backgroundColor: '#02060f', display: 'flex', justifyContent: 'center', alignItems: 'center', direction: 'rtl', fontFamily: 'system-ui, -apple-system, sans-serif', position: 'relative', overflow: 'hidden' },
  glowEffect: { position: 'absolute', width: '600px', height: '600px', background: 'radial-gradient(circle, rgba(0,242,255,0.05) 0%, transparent 70%)', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', zIndex: 0 },
  loginBox: { width: '100%', maxWidth: '420px', padding: '40px', backgroundColor: 'rgba(11, 15, 23, 0.8)', borderRadius: '24px', border: '1px solid #1f2937', backdropFilter: 'blur(10px)', zIndex: 1, textAlign: 'center', boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5)' },
  logoCircle: { fontSize: '48px', marginBottom: '10px' },
  loginTitle: { color: '#fff', fontSize: '36px', fontWeight: '800', margin: '0 0 5px 0', letterSpacing: '1px' },
  loginSubtitle: { color: '#8b949e', fontSize: '15px', margin: '0 0 30px 0' },
  loginForm: { display: 'flex', flexDirection: 'column', gap: '16px' },
  inputField: { padding: '16px', borderRadius: '12px', backgroundColor: '#161b22', color: '#fff', border: '1px solid #30363d', textAlign: 'center', fontSize: '16px', outline: 'none', transition: '0.2s' },
  btnSubmit: { padding: '16px', borderRadius: '12px', backgroundColor: '#00f2ff', color: '#000', fontWeight: 'bold', fontSize: '16px', border: 'none', cursor: 'pointer', transition: '0.2s', boxShadow: '0 0 15px rgba(0,242,255,0.3)' },
  dividerContainer: { display: 'flex', alignItems: 'center', margin: '15px 0' },
  dividerLine: { flex: 1, height: '1px', backgroundColor: '#30363d' },
  dividerText: { margin: '0 15px', color: '#8b949e', fontSize: '14px' },
  btnInstagramLogin: { padding: '16px', borderRadius: '12px', backgroundColor: 'transparent', color: '#38bdf8', border: '1px solid #0284c7', fontWeight: 'bold', fontSize: '16px', cursor: 'pointer', transition: '0.2s' },
  toggleText: { color: '#8b949e', fontSize: '14px', marginTop: '25px', cursor: 'pointer', textDecoration: 'underline' },

  // أنماط لوحة التحكم (Dashboard)
  dashWrapper: { minHeight: '100vh', backgroundColor: '#050a10', display: 'flex', justifyContent: 'center', direction: 'rtl', fontFamily: 'system-ui, -apple-system, sans-serif', padding: '40px 20px' },
  mainContainer: { width: '100%', maxWidth: '900px' },
  header: { textAlign: 'right', marginBottom: '40px' },
  pageTitle: { color: '#fff', fontSize: '38px', margin: '0 0 10px 0', fontWeight: '800' },
  subtitle: { color: '#8b949e', fontSize: '16px', margin: 0 },
  
  statsSection: { display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px', marginBottom: '40px' },
  statsCard: { display: 'flex', alignItems: 'center', gap: '20px', backgroundColor: '#111827', padding: '25px', borderRadius: '20px', border: '1px solid #1f2937' },
  statsCardPro: { display: 'flex', alignItems: 'center', gap: '20px', background: 'linear-gradient(145deg, #0b0f17, #111827)', padding: '25px', borderRadius: '20px', border: '1px solid #10b981', boxShadow: '0 0 20px rgba(16, 185, 129, 0.05)' },
  statsIcon: { fontSize: '40px', background: '#1f2937', width: '70px', height: '70px', display: 'flex', justifyContent: 'center', alignItems: 'center', borderRadius: '15px' },
  statsTitle: { color: '#8b949e', fontSize: '15px', margin: '0 0 5px 0' },
  statsValue: { color: '#fff', fontSize: '24px', fontWeight: 'bold', margin: 0 },

  plansGrid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', gap: '25px', marginBottom: '40px' },
  planCardPremium: { position: 'relative', background: 'linear-gradient(135deg, #111827 0%, #1f2937 100%)', padding: '40px', borderRadius: '24px', border: '1px solid #a855f7', boxShadow: '0 10px 30px -10px rgba(168,85,247,0.3)', textAlign: 'right' },
  badge: { position: 'absolute', top: '-15px', right: '30px', background: '#a855f7', color: '#fff', padding: '5px 15px', borderRadius: '20px', fontSize: '12px', fontWeight: 'bold' },
  planCardStandard: { backgroundColor: '#0b0f17', padding: '40px', borderRadius: '24px', border: '1px solid #1f2937', textAlign: 'right' },
  planName: { color: '#fff', fontSize: '24px', margin: '0 0 10px 0' },
  planDesc: { color: '#8b949e', fontSize: '15px', margin: '0 0 25px 0', lineHeight: '1.6' },
  planPrice: { color: '#a855f7', fontSize: '42px', fontWeight: '900', margin: '0 0 30px 0' },
  planPriceStandard: { color: '#00f2ff', fontSize: '42px', fontWeight: '900', margin: '0 0 30px 0' },
  priceMonth: { fontSize: '16px', color: '#555', fontWeight: 'normal' },
  
  btnStripePrimary: { width: '100%', padding: '16px', borderRadius: '14px', backgroundColor: '#a855f7', color: '#fff', fontSize: '16px', fontWeight: 'bold', border: 'none', cursor: 'pointer', marginBottom: '15px' },
  btnCryptoPrimary: { width: '100%', padding: '16px', borderRadius: '14px', backgroundColor: '#f59e0b', color: '#fff', fontSize: '16px', fontWeight: 'bold', border: 'none', cursor: 'pointer' },
  btnStripeSecondary: { width: '100%', padding: '16px', borderRadius: '14px', backgroundColor: '#00f2ff', color: '#000', fontSize: '16px', fontWeight: 'bold', border: 'none', cursor: 'pointer', marginBottom: '15px' },
  btnCryptoSecondary: { width: '100%', padding: '16px', borderRadius: '14px', backgroundColor: 'transparent', color: '#f59e0b', fontSize: '16px', fontWeight: 'bold', border: '1px solid #f59e0b', cursor: 'pointer' },

  actionSection: { display: 'flex', flexDirection: 'column', gap: '15px', alignItems: 'center', marginTop: '40px', paddingTop: '30px', borderTop: '1px solid #1f2937' },
  btnInstagram: { width: '100%', maxWidth: '400px', padding: '18px', borderRadius: '14px', background: 'linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%)', color: '#fff', fontSize: '16px', fontWeight: 'bold', border: 'none', cursor: 'pointer', boxShadow: '0 10px 20px -10px rgba(220, 39, 67, 0.5)' },
  btnLogout: { width: '100%', maxWidth: '400px', padding: '16px', borderRadius: '14px', backgroundColor: 'transparent', color: '#ef4444', fontSize: '15px', fontWeight: 'bold', border: '1px solid #ef4444', cursor: 'pointer' }
};