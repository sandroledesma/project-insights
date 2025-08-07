import React from 'react';
import { useLocation } from 'react-router-dom';

const ComingSoonPage = () => {
  const location = useLocation();
  
  // Map paths to category info
  const categoryMap = {
    '/productivity': { title: 'Productivity Tools', description: 'Task management, note-taking, and workflow optimization tools', icon: '⚡' },
    '/creative': { title: 'Creative Tools', description: 'Design software, photo editors, and creative AI assistants', icon: '🎨' },
    '/kitchen': { title: 'Kitchen Appliances', description: 'Smart ovens, refrigerators, and cooking gadgets', icon: '🍳' },
    '/laundry': { title: 'Laundry Appliances', description: 'Washers, dryers, and laundry care innovations', icon: '👕' },
    '/small-appliances': { title: 'Small Appliances', description: 'Coffee makers, blenders, and countertop essentials', icon: '☕' },
    '/guitars': { title: 'Guitars', description: 'Electric, acoustic, and bass guitars with community reviews', icon: '🎸' },
    '/keyboards': { title: 'Keyboards', description: 'Digital pianos, synthesizers, and MIDI controllers', icon: '🎹' },
    '/turntables': { title: 'Turntables', description: 'DJ equipment and vinyl record players', icon: '🎧' },
    '/audio-gear': { title: 'Audio Gear', description: 'Speakers, headphones, and recording equipment', icon: '🔊' },
    '/scooters': { title: 'Electric Scooters', description: 'Urban mobility and commuter scooters', icon: '🛴' },
    '/skateboards': { title: 'Electric Skateboards', description: 'E-skates and longboards for thrills and commuting', icon: '🛹' },
    '/bikes': { title: 'E-Bikes', description: 'Electric bicycles and bike accessories', icon: '🚴' },
    '/cars': { title: 'Electric Cars', description: 'EVs, charging solutions, and automotive tech', icon: '🚗' },
    '/gaming-pc': { title: 'Gaming PCs', description: 'Custom builds, pre-builts, and gaming hardware', icon: '🖥️' },
    '/consoles': { title: 'Gaming Consoles', description: 'PlayStation, Xbox, Nintendo, and accessories', icon: '🎮' },
    '/peripherals': { title: 'Gaming Peripherals', description: 'Keyboards, mice, headsets, and controllers', icon: '⌨️' },
    '/mobile-gaming': { title: 'Mobile Gaming', description: 'Gaming phones, accessories, and mobile setups', icon: '📱' },
    '/home-gym': { title: 'Home Gym Equipment', description: 'Weights, cardio machines, and workout gear', icon: '🏋️' },
    '/wearables': { title: 'Fitness Wearables', description: 'Smartwatches, fitness trackers, and health monitors', icon: '⌚' },
    '/supplements': { title: 'Supplements', description: 'Protein, vitamins, and fitness nutrition', icon: '💊' },
    '/outdoor': { title: 'Outdoor Gear', description: 'Hiking, camping, and adventure equipment', icon: '🏕️' }
  };

  const currentCategory = categoryMap[location.pathname] || { 
    title: 'New Category', 
    description: 'Exciting new content coming soon', 
    icon: '🚀' 
  };

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-dark-bg">
      {/* Header */}
      <div className="bg-white dark:bg-dark-card border-b border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="py-8">
            <div className="text-center">
              <div className="text-6xl mb-4">{currentCategory.icon}</div>
              <h1 className="text-4xl font-bold text-gray-800 dark:text-white mb-2">
                {currentCategory.title}
              </h1>
              <p className="text-lg text-gray-500 dark:text-gray-400">
                {currentCategory.description}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center">
          <div className="max-w-2xl mx-auto">
            {/* Animated Icon */}
            <div className="w-24 h-24 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-8 animate-pulse">
              <svg className="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>

            <h2 className="text-3xl font-bold text-gray-800 dark:text-white mb-6">
              Coming Soon!
            </h2>
            
            <p className="text-gray-600 dark:text-gray-300 mb-8 text-lg leading-relaxed">
              We're working hard to bring you comprehensive reviews and insights for <strong>{currentCategory.title.toLowerCase()}</strong>. 
              Our team is analyzing thousands of Reddit discussions to provide you with the most authentic and helpful information.
            </p>

            <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-700 rounded-xl p-8 mb-8">
              <h3 className="font-semibold text-blue-800 dark:text-blue-200 mb-4 text-lg">
                What to Expect:
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-left">
                <div className="flex items-start space-x-3">
                  <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></div>
                  <span className="text-blue-700 dark:text-blue-300">Real user reviews from Reddit communities</span>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></div>
                  <span className="text-blue-700 dark:text-blue-300">AI-powered sentiment analysis</span>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></div>
                  <span className="text-blue-700 dark:text-blue-300">Product comparisons and rankings</span>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></div>
                  <span className="text-blue-700 dark:text-blue-300">Trend insights and recommendations</span>
                </div>
              </div>
            </div>

            <div className="text-center">
              <p className="text-gray-500 dark:text-gray-400 mb-6">
                Want to be notified when this section launches?
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4 justify-center items-center max-w-md mx-auto">
                <input
                  type="email"
                  placeholder="Enter your email"
                  className="flex-1 px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
                />
                <button className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-medium rounded-lg hover:shadow-lg transform hover:scale-105 transition-all duration-200 whitespace-nowrap">
                  Notify Me
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ComingSoonPage;