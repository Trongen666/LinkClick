// src/App.tsx
import './App.css';

import React from 'react';
import { motion } from 'framer-motion'; // animation library
import { LockClosedIcon } from '@heroicons/react/20/solid'; // SVG icon

export default function App() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-tr from-gray-900 to-blue-900">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white/10 backdrop-blur-md rounded-2xl p-8 shadow-xl max-w-sm w-full"
      >
        <h2 className="text-3xl font-semibold text-white mb-6 text-center">
          Welcome Back
        </h2>
        <form className="space-y-4">
          <div>
            <label className="block text-white mb-1">Email</label>
            <input
              type="email"
              className="w-full px-4 py-2 rounded-lg bg-gray-800 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="you@example.com"
            />
          </div>
          <div>
            <label className="block text-white mb-1">Password</label>
            <div className="relative">
              <input
                type="password"
                className="w-full px-4 py-2 rounded-lg bg-gray-800 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="••••••••"
              />
              <LockClosedIcon className="w-5 h-5 text-gray-400 absolute right-3 top-3" />
            </div>
          </div>
          <button
            type="submit"
            className="w-full flex justify-center py-2 px-4 bg-blue-600 hover:bg-blue-700 rounded-lg text-white font-medium transition"
          >
            Sign In
          </button>
        </form>
      </motion.div>
    </div>
  );
}
