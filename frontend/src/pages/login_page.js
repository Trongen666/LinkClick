import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { IoPersonOutline, IoKeyOutline, IoEyeOutline, IoEyeOffOutline, IoFaceOutline } from 'react-icons/io5';
import { useAuth } from '../../contexts/AuthContext';
import FaceLoginComponent from '../../components/auth/FaceLoginComponent';
import OTPLoginComponent from '../../components/auth/OTPLoginComponent';

const LoginPage = () => {
  const { login } = useAuth();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [authMethod, setAuthMethod] = useState('face'); // 'face', 'password', 'otp'
  const [failedAttempts, setFailedAttempts] = useState(0);

  const handleFaceLoginSuccess = (token) => {
    login(token);
  };

  const handleFaceLoginFailure = () => {
    setFailedAttempts(prev => prev + 1);
    if (failedAttempts + 1 >= 2) {
      setAuthMethod('otp');
    }
  };

  const handlePasswordLogin = async (e) => {
    e.preventDefault();
    
    if (!username || !password) {
      setError('Please enter your username and password');
      return;
    }
    
    try {
      setIsLoading(true);
      setError('');
      const response = await login(username, password);
      // Success will be handled by auth context
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed. Please check your credentials.');
      setFailedAttempts(prev => prev + 1);
      if (failedAttempts + 1 >= 2) {
        setAuthMethod('otp');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleOtpLoginSuccess = (token) => {
    login(token);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 to-black p-4">
      {/* Background decorative elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 left-0 w-2/3 h-1/3 bg-blue-500/5 rounded-full filter blur-3xl"></div>
        <div className="absolute bottom-0 right-0 w-1/2 h-1/2 bg-purple-500/10 rounded-full filter blur-3xl"></div>
        
        {/* Grid pattern */}
        <div className="absolute inset-0" style={{ 
          backgroundImage: 'radial-gradient(circle at 1px 1px, rgba(255,255,255,0.05) 1px, transparent 0)',
          backgroundSize: '40px 40px'
        }}></div>
      </div>
      
      <div className="w-full max-w-md z-10">
        {/* App title */}
        <motion.div 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl font-bold text-white mb-2">
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500">
              HORIZON
            </span>
          </h1>
          <p className="text-gray-400 font-light">The future of authentication</p>
        </motion.div>
        
        <AnimatePresence mode="wait">
          {authMethod === 'face' && (
            <FaceLoginComponent 
              key="face-login"
              username={username}
              onSuccess={handleFaceLoginSuccess}
              onFailure={handleFaceLoginFailure}
              onSwitchMethod={() => setAuthMethod('password')}
            />
          )}
          
          {authMethod === 'password' && (
            <motion.div
              key="password-login"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="w-full max-w-md p-8 rounded-2xl bg-gray-900/50 backdrop-blur-lg border border-gray-800"
            >
              <h2 className="text-2xl font-bold text-white mb-6">Sign In</h2>
              
              <form onSubmit={handlePasswordLogin}>
                <div className="mb-6">
                  <label htmlFor="username" className="block text-sm font-medium text-gray-400 mb-2">
                    Username
                  </label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <IoPersonOutline className="text-gray-500" />
                    </div>
                    <input
                      id="username"
                      type="text"
                      value={username}
                      onChange={(e) => setUsername(e.target.value)}
                      className="w-full py-3 pl-10 pr-3 border border-gray-700 rounded-lg bg-gray-800 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-white"
                      placeholder="Enter your username"
                    />
                  </div>
                </div>
                
                <div className="mb-6">
                  <div className="flex justify-between items-center mb-2">
                    <label htmlFor="password" className="block text-sm font-medium text-gray-400">
                      Password
                    </label>
                    <button
                      type="button"
                      onClick={() => setAuthMethod('otp')}
                      className="text-sm text-blue-400 hover:text-blue-300"
                    >
                      Use OTP instead
                    </button>
                  </div>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <IoKeyOutline className="text-gray-500" />
                    </div>
                    <input
                      id="password"
                      type={showPassword ? "text" : "password"}
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      className="w-full py-3 pl-10 pr-10 border border-gray-700 rounded-lg bg-gray-800 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-white"
                      placeholder="Enter your password"
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute inset-y-0 right-0 pr-3 flex items-center"
                    >
                      {showPassword ? (
                        <IoEyeOffOutline className="text-gray-500 hover:text-gray-400" />
                      ) : (
                        <IoEyeOutline className="text-gray-500 hover:text-gray-400" />
                      )}
                    </button>
                  </div>
                </div>
                
                {error && (
                  <p className="text-red-500 mb-4 text-sm">{error}</p>
                )}
                
                <div className="flex items-center justify-between mb-6">
                  <button
                    type="button"
                    onClick={() => setAuthMethod('face')}
                    className="flex items-center text-blue-400 hover:text-blue-300 text-sm"
                  >
                    <IoFaceOutline className="mr-1" />
                    Use Face ID
                  </button>
                  <a href="#" className="text-sm text-blue-400 hover:text-blue-300">
                    Forgot password?
                  </a>
                </div>
                
                <button
                  type="submit"
                  disabled={isLoading}
                  className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white font-medium py-3 px-4 rounded-lg transition-colors flex items-center justify-center"
                >
                  {isLoading ? (
                    <span className="inline-block w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></span>
                  ) : null}
                  Sign In
                </button>
              </form>
              
              <div className="mt-6 text-center">
                <p className="text-gray-400">
                  Don't have an account?{' '}
                  <a href="/register" className="text-blue-400 hover:text-blue-300">
                    Sign up
                  </a>
                </p>
              </div>
            </motion.div>
          )}
          
          {authMethod === 'otp' && (
            <OTPLoginComponent
              key="otp-login"
              username={username}
              onBack={() => setAuthMethod('password')}
              onSuccess={handleOtpLoginSuccess}
            />
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default LoginPage;