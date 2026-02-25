import React, { useState, useEffect } from 'react';
import bgImage from './assets/bg.jpg'; // استدعاء الصورة

export default function Dashboard() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isRegistering, setIsRegistering] = useState(false);
  
  const [accounts, setAccounts] = useState([]);
  const [subscription, setSubscription] = useState({ isSubscribed: false, plan: 'free' });

  useEffect(() => {
    if (token) {
      fetch('http://localhost:8000/api/dashboard/accounts', {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      .then(res => {
        if (!res.ok) throw new Error("Token expired");
        return res.json();
      })
      .then(data => setAccounts(data))
      .catch(() => handleLogout());
    }
  }, [token]);

  const handleAuth = async (e) => {
    e.preventDefault();
    const endpoint = isRegistering ? '/api/auth/register' : '/api/auth/login';
    
    let options = {};
    if (isRegistering) {
      options = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      };
    } else {
      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', password);
      options = {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formData
      };
    }

    try {
      const res = await fetch(`http://localhost:8000${endpoint}`, options);
      if (res.ok) {
        const data = await res.json();
        localStorage.setItem('token', data.access_token);
        setToken(data.access_token);
      } else {
        alert("تأكد من صحة البيانات أو أن الحساب غير مسجل مسبقاً.");
      }
    } catch (error) {
      alert("خطأ في الاتصال بالسيرفر. هل تأكدت من تشغيل Backend البايثون؟");
    }
  };

  const handleMetaConnect = async () => {
    const res = await fetch('http://localhost:8000/api/oauth/login', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (res.ok) {
      const data = await res.json();
      window.location.href = data.url;
    }
  };

  const saveAccountSettings = async (platform_name, persona_prompt, is_bot_active) => {
    const res = await fetch('http://localhost:8000/api/dashboard/accounts/update', {
      method: 'PUT',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}` 
      },
      body: JSON.stringify({ platform_name, persona_prompt, is_bot_active })
    });
    if (res.ok) alert("تم الحفظ بنجاح! 🚀");
  };

  const upgradePlan = async () => {
    const res = await fetch('http://localhost:8000/api/payments/verify-local-payment?receipt_number=TEST1234', {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (res.ok) {
      setSubscription({ isSubscribed: true, plan: 'pro' });
      alert("تمت الترقية للباقة الاحترافية! 🎉");
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setAccounts([]);
  };

  // ----------------------------------------------------------------
  // شاشة تسجيل الدخول (مع الخلفية والتأثير الزجاجي)
  // ----------------------------------------------------------------
  if (!token) {
    return (
      <div 
        className="min-h-screen flex items-center justify-center p-4 text-white bg-cover bg-center bg-fixed"
        style={{ backgroundImage: `linear-gradient(rgba(15, 23, 42, 0.8), rgba(15, 23, 42, 0.95)), url(${bgImage})` }}
      >
        <div className="bg-gray-800/50 backdrop-blur-md p-8 rounded-xl shadow-2xl border border-gray-600/30 w-full max-w-md">
          <h2 className="text-3xl font-bold mb-6 text-center text-blue-400">BotMind AI</h2>
          <form onSubmit={handleAuth} className="space-y-4">
            <input type="email" placeholder="البريد الإلكتروني" required value={email} onChange={e => setEmail(e.target.value)} className="w-full p-3 bg-gray-900/80 border border-gray-600 rounded-lg focus:outline-none focus:border-blue-500" />
            <input type="password" placeholder="كلمة المرور" required value={password} onChange={e => setPassword(e.target.value)} className="w-full p-3 bg-gray-900/80 border border-gray-600 rounded-lg focus:outline-none focus:border-blue-500" />
            <button type="submit" className="w-full bg-blue-600 hover:bg-blue-700 font-bold py-3 rounded-lg transition">{isRegistering ? 'إنشاء حساب جديد' : 'تسجيل الدخول'}</button>
          </form>
          <button onClick={() => setIsRegistering(!isRegistering)} className="w-full mt-4 text-sm text-gray-400 hover:text-white transition">
            {isRegistering ? 'لديك حساب؟ سجل دخولك' : 'ليس لديك حساب؟ أنشئ حساباً'}
          </button>
        </div>
      </div>
    );
  }

  // ----------------------------------------------------------------
  // شاشة لوحة التحكم (مع الخلفية والتأثير الزجاجي)
  // ----------------------------------------------------------------
  return (
    <div 
      className="min-h-screen text-white p-4 md:p-8 bg-cover bg-center bg-fixed"
      style={{ backgroundImage: `linear-gradient(rgba(15, 23, 42, 0.85), rgba(15, 23, 42, 0.95)), url(${bgImage})` }}
    >
      <div className="max-w-4xl mx-auto bg-gray-800/50 backdrop-blur-md p-6 rounded-xl shadow-2xl border border-gray-600/30">
        <div className="flex justify-between items-center mb-8 pb-6 border-b border-gray-700/50">
          <div>
            <h1 className="text-2xl md:text-3xl font-bold text-blue-400">لوحة تحكم BotMind</h1>
            <p className="text-sm text-gray-400 mt-1">{email}</p>
          </div>
          <div className="flex items-center gap-3">
            <span className={`hidden md:inline-block px-3 py-1 rounded-lg text-sm font-bold ${subscription.plan === 'pro' ? 'bg-green-600' : 'bg-yellow-600'}`}>
              {subscription.plan === 'pro' ? 'Pro 🚀' : 'مجانية'}
            </span>
            {subscription.plan !== 'pro' && <button onClick={upgradePlan} className="bg-purple-600 hover:bg-purple-700 px-3 py-1 rounded-lg text-sm font-bold">ترقية</button>}
            <button onClick={handleLogout} className="bg-red-500 hover:bg-red-600 px-3 py-1 rounded-lg text-sm font-bold">خروج</button>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div className="bg-gray-700/60 p-6 rounded-xl text-center border border-gray-600/30">
            <h2 className="text-lg font-bold mb-2">إنستغرام / فيسبوك</h2>
            <p className="text-sm text-gray-300 mb-4">اربط حسابات Meta لتفعيل الرد الآلي.</p>
            <button onClick={handleMetaConnect} className="w-full bg-blue-600 hover:bg-blue-700 py-2 rounded-lg font-bold shadow-lg">+ ربط حساب Meta</button>
          </div>
        </div>

        <h2 className="text-xl font-bold mb-4 border-l-4 border-blue-500 pl-2">حساباتك النشطة</h2>
        {accounts.length === 0 ? (
          <div className="text-center p-8 border-2 border-dashed border-gray-500/50 rounded-xl text-gray-400">لا يوجد حسابات مربوطة بعد.</div>
        ) : (
          accounts.map(acc => (
            <div key={acc.id} className="bg-gray-800/60 border border-gray-600/30 p-5 rounded-xl mb-4">
              <div className="flex justify-between items-center mb-4">
                <p className="font-bold text-lg text-blue-300 capitalize">{acc.platform_name}</p>
                <div className="flex items-center gap-2">
                  <span className="text-sm text-gray-300">تفعيل:</span>
                  <input type="checkbox" className="w-5 h-5 cursor-pointer accent-blue-500" checked={acc.is_bot_active} onChange={(e) => {
                    setAccounts(accounts.map(a => a.id === acc.id ? { ...a, is_bot_active: e.target.checked } : a));
                  }}/>
                </div>
              </div>
              <textarea 
                className="w-full p-3 bg-gray-900/80 border border-gray-600/50 rounded-lg text-sm mb-3 focus:outline-none focus:border-blue-500" 
                rows="2" 
                value={acc.persona_prompt} 
                onChange={(e) => {
                  setAccounts(accounts.map(a => a.id === acc.id ? { ...a, persona_prompt: e.target.value } : a));
                }} 
                placeholder="تعليمات البوت..."
              />
              <button onClick={() => saveAccountSettings(acc.platform_name, acc.persona_prompt, acc.is_bot_active)} className="w-full bg-green-600 hover:bg-green-700 py-2 rounded-lg font-bold text-sm shadow-lg">حفظ التعديلات</button>
            </div>
          ))
        )}
      </div>
    </div>
  );
}