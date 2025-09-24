const theme = {
  colors: {
    // CashLab Primary Colors - Modern Green & Blue
    primaryGreen: '#10B981',      // Main brand color - growth/prosperity
    primaryBlue: '#1E40AF',       // Professional blue
    secondaryGreen: '#059669',    // Darker green for accents
    secondaryBlue: '#3B82F6',     // Lighter blue for secondary elements
    lightGreen: '#6EE7B7',        // Light green for backgrounds
    lightBlue: '#60A5FA',         // Light blue for backgrounds
    paleGreen: '#D1FAE5',         // Very light green
    paleBlue: '#DBEAFE',          // Very light blue

    // Accent Colors
    accentOrange: '#F59E0B',      // Warning/attention
    accentPurple: '#8B5CF6',      // Premium features

    // Neutral Colors
    input: '#374151',
    mediumGrey: '#6B7280',
    paleGrey: '#F9FAFB',
    white: '#FFFFFF', 
    black: '#000000',
    offWhite: '#F9FAFB',
    ghostWhite: '#F3F4F6',
    platinum: '#E5E7EB',

    // Status Colors
    success: '#10B981',           // Green for success
    error: '#EF4444',             // Red for errors
    warning: '#F59E0B',           // Orange for warnings
    info: '#3B82F6',              // Blue for info

    // Legacy support (keeping for compatibility)
    crimsonRed: '#DC2626',
    forestGreen: '#259800',

    darkIcon: '#1F2937',
    
    darkText: '#1F2937',
    lightText: '#F9FAFB',
    background: '#FFFFFF',
    backgroundSecondary: '#F8FAFC',
    backgroundTertiary: '#F1F5F9',
    
    // Text colors
    textPrimary: '#1F2937',
    textSecondary: '#6B7280',
    
    // Border colors
    border: '#E5E7EB',
  },
  
  spacing: {
    xs: '0.25rem',  // 4px
    sm: '0.5rem',   // 8px
    md: '1rem',     // 16px
    lg: '1.5rem',   // 24px
    xl: '2rem',     // 32px
    xxl: '3rem',    // 48px
  },
  
  shadows: {
    sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    md: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
    lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
  },
  
  borderRadius: {
    sm: '0.125rem', // 2px
    md: '0.25rem',  // 4px
    lg: '0.5rem',   // 8px
    xl: '1rem',     // 16px
    full: '9999px', // Circular
  },
  
  fontSizes: {
    xs: '0.75rem',  // 12px
    sm: '0.875rem', // 14px
    md: '1rem',     // 16px
    lg: '1.125rem', // 18px
    xl: '1.25rem',  // 20px
    xxl: '1.5rem',  // 24px
  }
} as const;

export default theme;
  