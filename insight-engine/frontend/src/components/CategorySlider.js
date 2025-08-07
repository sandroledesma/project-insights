import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import apiService from '../services/api';

const CategorySlider = () => {
  const location = useLocation();
  const [hoveredCategory, setHoveredCategory] = useState(null);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [scrollY, setScrollY] = useState(0);
  const [isScrolled, setIsScrolled] = useState(false);

  // Fallback categories (original static data)
  const fallbackCategories = [
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
        { path: '/', title: 'AI Tools', active: true, status: 'New', product_count: 4 },
        { path: '/productivity', title: 'Productivity', status: 'Coming Soon' },
        { path: '/creative', title: 'Creative', status: 'Coming Soon' }
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
        { path: '/kitchen', title: 'Kitchen', status: 'Coming Soon' },
        { path: '/laundry', title: 'Laundry', status: 'Coming Soon' },
        { path: '/small-appliances', title: 'Small Appliances', status: 'Coming Soon' },
        { path: '/luxe', title: 'Luxury Appliances', active: true, status: 'New', product_count: 4 }
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
        { path: '/guitars', title: 'Guitars', status: 'Coming Soon' },
        { path: '/keyboards', title: 'Keyboards', status: 'Coming Soon' },
        { path: '/turntables', title: 'Turntables', status: 'Coming Soon' },
        { path: '/audio-gear', title: 'Audio Gear', status: 'Coming Soon' }
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
        { path: '/scooters', title: 'Scooters', status: 'Coming Soon' },
        { path: '/skateboards', title: 'Electric Skateboards', status: 'Coming Soon' },
        { path: '/bikes', title: 'E-Bikes', status: 'Coming Soon' },
        { path: '/cars', title: 'Electric Cars', status: 'Coming Soon' }
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
        { path: '/gaming-pc', title: 'Gaming PCs', status: 'Coming Soon' },
        { path: '/consoles', title: 'Consoles', status: 'Coming Soon' },
        { path: '/peripherals', title: 'Peripherals', status: 'Coming Soon' },
        { path: '/mobile-gaming', title: 'Mobile Gaming', status: 'Coming Soon' }
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
        { path: '/pocket-tech', title: 'Pocket Tech', status: 'Coming Soon' },
        { path: '/desk-tech', title: 'Desk Tech', status: 'Coming Soon' },
        { path: '/tech-toys', title: 'Tech Toys', status: 'Coming Soon' },
        { path: '/gadgets', title: 'Cool Gadgets', status: 'Coming Soon' }
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
        { path: '/home-gym', title: 'Home Gym', status: 'New' },
        { path: '/wearables', title: 'Wearables', status: 'New' },
        { path: '/supplements', title: 'Supplements', status: 'New' },
        { path: '/outdoor', title: 'Outdoor Gear', status: 'New' }
      ]
    }
  ];

  // Fetch categories from backend
  useEffect(() => {
    const fetchCategories = async () => {
      try {
        setLoading(true);
        const response = await apiService.getCategories();
        
        // Transform backend data to match original CategorySlider format
        const transformedCategories = response.categories.map(category => {
          // Get gradient color based on category name
          const gradients = {
            'Technology': 'from-blue-500 to-purple-600',
            'Appliances': 'from-green-500 to-teal-600',
            'Music': 'from-pink-500 to-rose-600',
            'Transport': 'from-orange-500 to-red-600',
            'Gaming': 'from-indigo-500 to-purple-600',
            'Tech Products': 'from-cyan-500 to-blue-600',
            'Fitness': 'from-emerald-500 to-green-600'
          };

          // Parse SVG icon or use fallback
          let icon;
          if (category.icon_svg) {
            try {
              // Create a React element from the SVG string
              icon = <div dangerouslySetInnerHTML={{ __html: category.icon_svg }} />;
            } catch (e) {
              // Fallback to default icon
              icon = (
                <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
              );
            }
          } else {
            // Default icon
            icon = (
              <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>
            );
          }

          // Map subcategories
          const subcategories = category.subcategories.map(subcat => {
            // Map subcategory names to paths
            const pathMappings = {
              'AI Tools': '/',
              'Productivity': '/productivity',
              'Creative': '/creative',
              'Kitchen': '/kitchen',
              'Laundry': '/laundry',
              'Small Appliances': '/small-appliances',
              'Luxury Appliances': '/luxe',
              'Guitars': '/guitars',
              'Keyboards': '/keyboards',
              'Turntables': '/turntables',
              'Audio Gear': '/audio-gear',
              'Scooters': '/scooters',
              'Electric Skateboards': '/skateboards',
              'E-Bikes': '/bikes',
              'Electric Cars': '/cars',
              'Gaming PCs': '/gaming-pc',
              'Consoles': '/consoles',
              'Peripherals': '/peripherals',
              'Mobile Gaming': '/mobile-gaming',
              'Pocket Tech': '/pocket-tech',
              'Desk Tech': '/desk-tech',
              'Tech Toys': '/tech-toys',
              'Cool Gadgets': '/gadgets',
              'Home Gym': '/home-gym',
              'Wearables': '/wearables',
              'Supplements': '/supplements',
              'Outdoor Gear': '/outdoor'
            };

            // Override status for AI Tools and Luxury Appliances to be "New"
            let displayStatus = subcat.status;
            if (subcat.name === 'AI Tools' || subcat.name === 'Luxury Appliances') {
              displayStatus = 'New';
            }

            return {
              path: pathMappings[subcat.name] || `/${subcat.name.toLowerCase().replace(/\s+/g, '-')}`,
              title: subcat.name,
              active: subcat.status === 'Live' && subcat.product_count > 0,
              status: displayStatus,
              product_count: subcat.product_count
            };
          });

          return {
            id: category.name.toLowerCase().replace(/\s+/g, '-'),
            title: category.name,
            description: category.description,
            status: category.status,
            icon: icon,
            gradient: gradients[category.name] || 'from-gray-500 to-gray-600',
            subcategories: subcategories
          };
        });

        setCategories(transformedCategories);
      } catch (error) {
        console.error('Error fetching categories:', error);
        // Use fallback categories on error
        setCategories(fallbackCategories);
      } finally {
        setLoading(false);
      }
    };

    fetchCategories();
  }, []);

  // Handle scroll events for responsive behavior
  useEffect(() => {
    const handleScroll = () => {
      const currentScrollY = window.scrollY;
      setScrollY(currentScrollY);
      setIsScrolled(currentScrollY > 50);
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const isActive = (path) => location.pathname === path;
  
  const isCategoryActive = (category) => {
    return category.subcategories.some(sub => isActive(sub.path));
  };

  // Show loading state
  if (loading) {
    return (
      <div className="bg-white dark:bg-dark-card border-b border-gray-200 dark:border-gray-700 sticky top-16 z-40 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <span className="ml-3 text-gray-600 dark:text-gray-400">Loading categories...</span>
          </div>
        </div>
      </div>
    );
  }

  // Calculate dynamic values based on scroll - tighter spacing
  const iconScale = Math.max(0.7, 1 - scrollY / 500);
  const titleOpacity = Math.max(0, 1 - scrollY / 200);
  const containerPadding = Math.max(6, 16 - scrollY / 10); // Reduced from 8-24 to 6-16
  const hoverAreaHeight = Math.max(24, 36 - scrollY / 20); // Reduced from 32-44 to 24-36

  return (
    <div 
      className={`bg-white dark:bg-dark-card border-b border-gray-200 dark:border-gray-700 sticky top-16 z-40 shadow-sm transition-all duration-300 ${
        isScrolled ? 'backdrop-blur-md bg-white/95 dark:bg-dark-card/95' : ''
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Desktop View - macOS style menu */}
        <div 
          className="hidden md:block"
          onMouseEnter={() => {/* Keep hover active when in menu area */}}
          onMouseLeave={() => setHoveredCategory(null)}
        >
          {/* Main Categories Row - Dynamic height based on scroll */}
          <div 
            className="flex justify-center space-x-8 transition-all duration-300" // Reduced from space-x-12 to space-x-8
            style={{ 
              paddingTop: `${containerPadding}px`, 
              paddingBottom: `${containerPadding}px` 
            }}
          >
            {categories.map((category, index) => {
              const active = isCategoryActive(category);
              return (
                <div
                  key={category.id}
                  className="relative text-center"
                  onMouseEnter={() => setHoveredCategory(category.id)}
                >
                  {/* Icon Container with dynamic scaling */}
                  <div 
                    className={`inline-flex items-center justify-center w-12 h-12 rounded-xl bg-gradient-to-br ${category.gradient} text-white shadow-md transition-all duration-300 ease-out mb-3 ${
                      active ? 'ring-2 ring-blue-500 dark:ring-blue-400 shadow-lg' : ''
                    } ${hoveredCategory && hoveredCategory !== category.id ? 'opacity-30 scale-95' : 'opacity-100'}`}
                    style={{ 
                      transform: `scale(${iconScale})`,
                      marginBottom: `${Math.max(3, 8 * iconScale)}px` // Reduced from 4-12 to 3-8
                    }}
                  >
                    {React.cloneElement(category.icon, { 
                      className: 'w-6 h-6',
                      style: { transform: `scale(${Math.max(0.8, iconScale)})` }
                    })}
                  </div>
                  
                  {/* Title with dynamic opacity */}
                  <h3 
                    className={`text-sm font-semibold transition-all duration-300 ease-out ${
                      active 
                        ? 'text-blue-600 dark:text-blue-400' 
                        : hoveredCategory && hoveredCategory !== category.id
                          ? 'text-gray-400 dark:text-gray-600 opacity-60'
                          : 'text-gray-700 dark:text-gray-300'
                    }`}
                    style={{ 
                      opacity: titleOpacity,
                      fontSize: `${Math.max(10, 14 * Math.max(0.7, titleOpacity))}px`,
                      transform: `translateY(${(1 - titleOpacity) * -5}px)`
                    }}
                  >
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

          {/* Subcategories Area - Dynamic height based on scroll */}
          <div 
            className="pt-1 pb-3 flex items-center justify-center transition-all duration-300"
            style={{ 
              height: `${hoverAreaHeight}px`,
              opacity: scrollY > 300 ? 0 : 1,
              pointerEvents: scrollY > 300 ? 'none' : 'auto'
            }}
          >
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
                          : subcat.status === 'New'
                            ? 'text-green-700 dark:text-green-400 hover:bg-green-50 dark:hover:bg-green-900/20 hover:text-green-800 dark:hover:text-green-300 hover:shadow-sm hover:scale-105 font-semibold'
                            : subcat.status === 'Live'
                              ? 'text-blue-700 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 hover:text-blue-800 dark:hover:text-blue-300 hover:shadow-sm hover:scale-105 font-semibold'
                              : subcat.status === 'Coming Soon'
                                ? 'text-amber-700 dark:text-amber-400 hover:bg-amber-50 dark:hover:bg-amber-900/20 hover:text-amber-800 dark:hover:text-amber-300 hover:shadow-sm hover:scale-105'
                                : 'text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800 hover:text-gray-900 dark:hover:text-white hover:shadow-sm hover:scale-105'
                      }`}
                      style={{
                        animationDelay: `${subIndex * 50}ms`
                      }}

                    >
                      <span>{subcat.title}</span>
                      
                      {/* Product Count */}
                      {subcat.product_count > 0 && (
                        <span className="ml-2 text-xs text-gray-500 dark:text-gray-400">
                          ({subcat.product_count})
                        </span>
                      )}
                      
                      {/* Status Badge */}
                      {subcat.status === 'Coming Soon' && (
                        <span className="ml-2 text-xs text-amber-600 dark:text-amber-400 bg-amber-100 dark:bg-amber-900/30 px-2 py-0.5 rounded-full font-medium">
                          Soon
                        </span>
                      )}
                      {subcat.status === 'New' && (
                        <span className="ml-2 text-xs text-green-600 dark:text-green-400 bg-green-100 dark:bg-green-900/30 px-2 py-0.5 rounded-full font-medium">
                          New
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