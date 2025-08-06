import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';

const CategorySlider = () => {
  const location = useLocation();
  const [hoveredCategory, setHoveredCategory] = useState(null);

  const categories = [
    {
      id: 'tech',
      title: 'Technology',
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
        </svg>
      ),
      gradient: 'from-blue-500 to-purple-600',
      subcategories: [
        { path: '/', title: 'AI Tools', active: true },
        { path: '/productivity', title: 'Productivity' },
        { path: '/creative', title: 'Creative' }
      ]
    },
    {
      id: 'appliances',
      title: 'Appliances',
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
        </svg>
      ),
      gradient: 'from-green-500 to-teal-600',
      subcategories: [
        { path: '/kitchen', title: 'Kitchen' },
        { path: '/laundry', title: 'Laundry' },
        { path: '/small-appliances', title: 'Small Appliances' },
        { path: '/luxe', title: 'Luxury Appliances', active: true }
      ]
    },
    {
      id: 'music',
      title: 'Music',
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3" />
        </svg>
      ),
      gradient: 'from-pink-500 to-rose-600',
      subcategories: [
        { path: '/guitars', title: 'Guitars' },
        { path: '/keyboards', title: 'Keyboards' },
        { path: '/turntables', title: 'Turntables' },
        { path: '/audio-gear', title: 'Audio Gear' }
      ]
    },
    {
      id: 'transport',
      title: 'Transport',
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
      ),
      gradient: 'from-orange-500 to-red-600',
      subcategories: [
        { path: '/scooters', title: 'Scooters' },
        { path: '/skateboards', title: 'Electric Skateboards' },
        { path: '/bikes', title: 'E-Bikes' },
        { path: '/cars', title: 'Electric Cars' }
      ]
    },
    {
      id: 'gaming',
      title: 'Gaming',
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
        </svg>
      ),
      gradient: 'from-indigo-500 to-purple-600',
      subcategories: [
        { path: '/gaming-pc', title: 'Gaming PCs' },
        { path: '/consoles', title: 'Consoles' },
        { path: '/peripherals', title: 'Peripherals' },
        { path: '/mobile-gaming', title: 'Mobile Gaming' }
      ]
    },
    {
      id: 'tech-products',
      title: 'Tech Products',
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
        </svg>
      ),
      gradient: 'from-cyan-500 to-blue-600',
      subcategories: [
        { path: '/pocket-tech', title: 'Pocket Tech' },
        { path: '/desk-tech', title: 'Desk Tech' },
        { path: '/tech-toys', title: 'Tech Toys' },
        { path: '/gadgets', title: 'Cool Gadgets' }
      ]
    },
    {
      id: 'fitness',
      title: 'Fitness',
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
        </svg>
      ),
      gradient: 'from-emerald-500 to-green-600',
      subcategories: [
        { path: '/home-gym', title: 'Home Gym' },
        { path: '/wearables', title: 'Wearables' },
        { path: '/supplements', title: 'Supplements' },
        { path: '/outdoor', title: 'Outdoor Gear' }
      ]
    }
  ];

  const isActive = (path) => location.pathname === path;
  
  const isCategoryActive = (category) => {
    return category.subcategories.some(sub => isActive(sub.path));
  };

  return (
    <div className="bg-white dark:bg-dark-card border-b border-gray-200 dark:border-gray-700 sticky top-16 z-40 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Desktop View - macOS style menu */}
        <div 
          className="hidden md:block"
          onMouseEnter={() => {/* Keep hover active when in menu area */}}
          onMouseLeave={() => setHoveredCategory(null)}
        >
          {/* Main Categories Row - Clean fixed height */}
          <div className="flex justify-center space-x-12 py-6">
            {categories.map((category, index) => {
              const active = isCategoryActive(category);
              return (
                <div
                  key={category.id}
                  className="relative text-center"
                  onMouseEnter={() => setHoveredCategory(category.id)}
                >
                  {/* Icon Container */}
                  <div className={`inline-flex items-center justify-center w-12 h-12 rounded-xl bg-gradient-to-br ${category.gradient} text-white shadow-md transition-all duration-300 ease-out mb-3 ${
                    active ? 'ring-2 ring-blue-500 dark:ring-blue-400 shadow-lg' : ''
                  } ${hoveredCategory && hoveredCategory !== category.id ? 'opacity-30 scale-95' : 'opacity-100 scale-100'}`}>
                    {React.cloneElement(category.icon, { className: 'w-6 h-6' })}
                  </div>
                  
                  {/* Title */}
                  <h3 className={`text-sm font-semibold transition-all duration-300 ease-out ${
                    active 
                      ? 'text-blue-600 dark:text-blue-400' 
                      : hoveredCategory && hoveredCategory !== category.id
                        ? 'text-gray-400 dark:text-gray-600 opacity-60'
                        : 'text-gray-700 dark:text-gray-300'
                  }`}>
                    {category.title}
                  </h3>
                  
                  {/* Active Indicator - Properly positioned */}
                  {active && (
                    <div className="absolute top-full mt-2 left-1/2 transform -translate-x-1/2 w-6 h-0.5 bg-blue-500 rounded-full"></div>
                  )}
                </div>
              );
            })}
          </div>

          {/* Subcategories Area - Optimized spacing and styling */}
          <div className="pt-1 pb-3 h-11 flex items-center justify-center">
            {hoveredCategory ? (
              <div className="flex items-center gap-3 transition-all duration-300 ease-out">
                {categories
                  .find(cat => cat.id === hoveredCategory)
                  ?.subcategories.map((subcat, subIndex) => (
                    <Link
                      key={subcat.path}
                      to={subcat.path}
                      className={`inline-flex items-center px-3 py-1.5 rounded-lg text-sm font-medium transition-all duration-200 ease-out ${
                        isActive(subcat.path)
                          ? 'bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 shadow-sm'
                          : 'text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800 hover:text-gray-900 dark:hover:text-white hover:shadow-sm hover:scale-105'
                      }`}
                      style={{
                        animationDelay: `${subIndex * 50}ms`
                      }}
                    >
                      <span>{subcat.title}</span>
                      {!subcat.active && (
                        <span className="ml-2 text-xs text-gray-400 dark:text-gray-500 bg-gray-100 dark:bg-gray-700 px-2 py-0.5 rounded-full">
                          Soon
                        </span>
                      )}
                    </Link>
                  ))}
              </div>
            ) : (
              <div className="text-sm text-gray-400 dark:text-gray-500 transition-opacity duration-300">
                Hover over a category to see options
              </div>
            )}
          </div>
        </div>

        {/* Mobile View - Simple navigation */}
        <div className="md:hidden">
          <div className="flex justify-center space-x-8">
            {categories.slice(0, 4).map((category, index) => {
              const active = isCategoryActive(category);
              return (
                <div
                  key={category.id}
                  className="relative flex-shrink-0 text-center"
                >
                  {/* Icon Container */}
                  <div className={`inline-flex items-center justify-center w-12 h-12 rounded-xl mb-3 bg-gradient-to-br ${category.gradient} text-white shadow-md transform transition-all duration-200 ${
                    active ? 'scale-110 shadow-lg ring-2 ring-blue-500 dark:ring-blue-400' : 'hover:scale-105 hover:shadow-lg'
                  }`}>
                    {React.cloneElement(category.icon, { className: 'w-6 h-6' })}
                  </div>
                  
                  {/* Title */}
                  <h3 className={`text-sm font-semibold transition-colors ${
                    active 
                      ? 'text-blue-600 dark:text-blue-400' 
                      : 'text-gray-700 dark:text-gray-300'
                  }`}>
                    {category.title}
                  </h3>
                  
                  {/* Active Indicator */}
                  {active && (
                    <div className="absolute -bottom-1 left-1/2 transform -translate-x-1/2 w-6 h-0.5 bg-blue-500 rounded-full"></div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};

export default CategorySlider;