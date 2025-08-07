import React, { useState } from 'react';

const LogoDisplay = ({ 
  name, 
  website, 
  size = 'md',
  className = '',
  showFallback = true 
}) => {
  const [logoError, setLogoError] = useState(false);
  const [logoLoading, setLogoLoading] = useState(true);

  // Size variants
  const sizeClasses = {
    sm: 'w-8 h-8',
    md: 'w-12 h-12',
    lg: 'w-16 h-16',
    xl: 'w-20 h-20'
  };

  const textSizeClasses = {
    sm: 'text-xs',
    md: 'text-sm',
    lg: 'text-base',
    xl: 'text-lg'
  };

  // Generate logo URL from website domain
  const getLogoUrl = (website, name) => {
    if (!website) return null;
    
    try {
      const domain = new URL(website).hostname.replace('www.', '');
      
      // Try multiple logo services
      const logoServices = [
        `https://logo.clearbit.com/${domain}`,
        `https://www.google.com/s2/favicons?domain=${domain}&sz=128`,
        `https://favicons.githubusercontent.com/${domain}`
      ];
      
      return logoServices[0]; // Start with Clearbit as it's highest quality
    } catch {
      return null;
    }
  };

  // Generate initials from name
  const getInitials = (name) => {
    if (!name) return '?';
    return name
      .split(' ')
      .map(word => word[0])
      .join('')
      .substring(0, 2)
      .toUpperCase();
  };

  // Generate a consistent color based on name
  const getColorFromName = (name) => {
    if (!name) return 'bg-gray-500';
    
    const colors = [
      'bg-blue-500',
      'bg-green-500', 
      'bg-purple-500',
      'bg-red-500',
      'bg-yellow-500',
      'bg-indigo-500',
      'bg-pink-500',
      'bg-teal-500',
      'bg-orange-500',
      'bg-cyan-500'
    ];
    
    const hash = name.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
    return colors[hash % colors.length];
  };

  const logoUrl = getLogoUrl(website, name);
  const initials = getInitials(name);
  const bgColor = getColorFromName(name);

  // Fallback component
  const FallbackLogo = () => (
    <div className={`${sizeClasses[size]} ${bgColor} rounded-lg flex items-center justify-center shadow-sm ${className}`}>
      <span className={`${textSizeClasses[size]} font-bold text-white`}>
        {initials}
      </span>
    </div>
  );

  // If no logo URL or showFallback is false, show fallback immediately
  if (!logoUrl || !showFallback) {
    return <FallbackLogo />;
  }

  return (
    <div className={`${sizeClasses[size]} relative ${className}`}>
      {logoLoading && (
        <div className={`${sizeClasses[size]} bg-gray-200 dark:bg-gray-700 rounded-lg animate-pulse absolute inset-0`} />
      )}
      
      <img
        src={logoUrl}
        alt={`${name} logo`}
        className={`${sizeClasses[size]} rounded-lg object-contain bg-white shadow-sm transition-opacity duration-200 ${
          logoLoading ? 'opacity-0' : 'opacity-100'
        }`}
        onLoad={() => {
          setLogoLoading(false);
          setLogoError(false);
        }}
        onError={() => {
          setLogoError(true);
          setLogoLoading(false);
        }}
        style={{ display: logoError ? 'none' : 'block' }}
      />
      
      {logoError && <FallbackLogo />}
    </div>
  );
};

export default LogoDisplay;