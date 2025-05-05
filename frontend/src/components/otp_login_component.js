import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { IoLockClosedOutline, IoCheckmarkCircleOutline, IoArrowBackOutline } from 'react-icons/io5';
import { authApi } from '../../services/api';

const OTPLoginComponent = ({ username, onBack, onSuccess }) => {
  const [otp, setOtp] = useState(['', '', '', '', '', '']);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [isSuccess, setIsSuccess] = useState(false);
  const [timeLeft, setTimeLeft] = useState(0);
  const inputRefs = Array(6).fill(0).map(() => useRef(null));

  useEffect(() => {
    if (timeLeft > 0) {
      const timerId = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
      return () => clearTimeout(timerId);
    }
  }, [timeLeft]);

  const focusInput = (index) => {
    inputRefs[index]?.current?.focus();
  };

  const handleInputChange = (index, value) => {
    if (/^[0-9]$/.test(value) || value === '') {
      const newOtp = [...otp];
      newOtp[index] = value;
      setOtp(newOtp);
      
      // Auto focus next input
      if (value !== '' && index < 5) {
        focusInput(index + 1);
      }
    }
  };

  const handleKeyDown = (index, e) => {
    // Handle backspace
    if (e.key === 'Backspace') {
      if (otp[index] === '' && index > 0) {
        focusInput(index - 1);
      }
    }

    // Handle arrow keys
    if (e.key === 'ArrowLeft' && index > 0) {
      focusInput(index - 1);
    }
    if (e.key === 'ArrowRight' && index < 5) {
      focusInput(index + 1);
    }
  };

  const handlePaste = (e) => {
    e.preventDefault();
    const pastedData = e.clipboardData.getData('text');
    if (/^[0-9]{6}$/.test(pastedData)) {
      const newOtp = pastedData.split('').slice(0, 6);
      setOtp(newOtp);
      focusInput(5);
    }
  };

  const requestNewOTP = async () => {
    try {
      setIsLoading(true);
      setError('');
      await authApi.requestOtp(username);
      setTimeLeft(60);
    } catch (err) {
      setError('Failed to request new OTP. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const verifyOTP = async () => {
    try {
      setIsLoading(true);
      setError('');
      
      const otpCode = otp.join('');
      if (otpCode.length !== 6) {
        setError('Please enter the complete 6-digit OTP.');
        setIsLoading(false);
        return;
      }
      
      const response = await authApi.verifyOtp(username, otpCode);
      
      // Success animation
      setIsSuccess(true);
      
      // Pass token back to parent component
      setTimeout(() => {
        onSuccess(response.data.access_token);
      }, 1500);
      
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to verify OTP. Please try again.');
      setIsLoading(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="w-full max-w-md p-8 rounded-2xl bg-gray-900/50 backdrop-blur-lg border border-gray-800"
    >
      {isSuccess ? (
        <div className="flex flex-col items-center justify-center py-8">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: "spring", stiffness: 200, damping: 10 }}
            className="text-green-400 text-6xl mb-4"
          >
            <IoCheckmarkCircleOutline />
          </motion.div>
          <h3 className="text-2xl font-medium text-white mb-2">Authentication Successful</h3>
          <p className="text-gray-400">Redirecting you to the dashboard...</p>
        </div>
      ) : (
        <>
          <div className="flex items-center mb-6">
            <button 
              onClick={onBack}
              className="mr-4 p-2 rounded-full hover:bg-gray-800 transition-colors"
            >
              <IoArrowBackOutline className="text-gray-400 text-xl" />
            </button>
            <h2 className="text-2xl font-bold text-white">Enter OTP Code</h2>
          </div>
          
          <div className="mb-6">
            <p className="text-gray-300 mb-4">
              A verification code has been sent to your registered email or phone number.
            </p>
            
            <div className="flex justify-between mb-8">
              {otp.map((digit, index) => (
                <input
                  key={index}
                  ref={inputRefs[index]}
                  type="text"
                  maxLength={1}
                  value={digit}
                  onChange={(e) => handleInputChange(index, e.target.value)}
                  onKeyDown={(e) => handleKeyDown(index, e)}
                  onPaste={index === 0 ? handlePaste : undefined}
                  className="w-12 h-14 text-center text-xl font-bold rounded-lg bg-gray-800 border border-gray-700 focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:outline-none text-white"
                />
              ))}
            </div>
            
            {error && (
              <p className="text-red-500 mb-4 text-sm">{error}</p>
            )}
            
            <div className="flex items-center justify-between">
              <button
                disabled={timeLeft > 0 || isLoading}
                onClick={requestNewOTP}
                className="text-blue-400 hover:text-blue-300 text-sm font-medium transition-colors disabled:text-gray-500"
              >
                {timeLeft > 0 ? `Resend code (${timeLeft}s)` : 'Resend code'}
              </button>
              
              <button
                onClick={verifyOTP}
                disabled={isLoading || otp.some(d => d === '')}
                className="px-6 py-2 bg-blue-600 hover:bg-blue-500 disabled:bg-gray-700 disabled:text-gray-400 rounded-lg text-white font-medium transition-colors flex items-center"
              >
                {isLoading ? (
                  <span className="inline-block w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></span>
                ) : (
                  <IoLockClosedOutline className="mr-2" />
                )}
                Verify
              </button>
            </div>
          </div>
        </>
      )}
    </motion.div>
  );
};

export default OTPLoginComponent;