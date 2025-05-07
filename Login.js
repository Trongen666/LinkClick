import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import './Login.css';

function Login() {
  const [username, setUsername] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [otp, setOtp] = useState('');
  const { t, i18n } = useTranslation();
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    navigate('/home');
  };

  const handleLanguageChange = (langCode) => {
    i18n.changeLanguage(langCode);
  };

  return (
    <div className="container">
      <div className="logo">LinkClick</div>
      <p className="instruction">{t('enterDetails')}</p>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder={t('username')}
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type="tel"
          placeholder={t('phoneNumber')}
          value={phoneNumber}
          onChange={(e) => setPhoneNumber(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder={t('otp')}
          value={otp}
          onChange={(e) => setOtp(e.target.value)}
          required
        />
        <button type="submit">{t('login')}</button>
      </form>

      <div className="language-select">
        <span onClick={() => handleLanguageChange('te')}>తెలుగు</span>
        <span onClick={() => handleLanguageChange('hi')}>हिन्दी</span>
        <span onClick={() => handleLanguageChange('en')}>English</span>
      </div>

      <p className="no-account">
        {t('noAccount')} <Link to="/signup">signup</Link>
      </p>
    </div>
  );
}

export default Login;

