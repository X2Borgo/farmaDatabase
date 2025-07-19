"""Centralized styling configuration for the pharmacy inventory GUI."""

# Modern Medical/Pharmacy Color Palette
COLORS = {
    # Primary Colors - Medical Blues/Teals
    'primary': '#2E8B94',           # Medical teal
    'primary_light': '#4A90A4',     # Lighter teal
    'primary_dark': '#1E5A61',      # Darker teal
    
    # Background Colors
    'bg_primary': '#FFFFFF',        # Pure white
    'bg_secondary': '#F8F9FA',      # Light gray
    'bg_accent': '#E3F2FD',         # Very light blue
    'bg_table': '#FAFBFC',          # Table background
    'bg_table_alt': '#F1F3F4',      # Alternate row color
    
    # Text Colors
    'text_primary': '#212529',      # Dark gray (not pure black)
    'text_secondary': '#6C757D',    # Medium gray
    'text_light': '#FFFFFF',        # White text
    
    # Action Colors
    'success': '#28A745',           # Green for success/add actions
    'success_hover': '#218838',     # Darker green for hover
    'info': '#17A2B8',              # Blue for info actions
    'info_hover': '#138496',        # Darker blue for hover
    'warning': '#FD7E14',           # Orange for warning
    'warning_hover': '#E55D00',     # Darker orange for hover
    'danger': '#DC3545',            # Red for danger/cancel
    'danger_hover': '#C82333',      # Darker red for hover
    
    # Border and Shadow Colors
    'border': '#DEE2E6',            # Light border
    'border_focus': '#80BDFF',      # Focus border
    'shadow': '#00000020',          # Subtle shadow
}

# Typography Configuration
FONTS = {
    'heading_large': ('Segoe UI', 24, 'bold'),
    'heading_medium': ('Segoe UI', 20, 'bold'),
    'heading_small': ('Segoe UI', 16, 'bold'),
    'body_large': ('Segoe UI', 14),
    'body_medium': ('Segoe UI', 12),
    'body_small': ('Segoe UI', 10),
    'button': ('Segoe UI', 12, 'bold'),
    'table_header': ('Segoe UI', 14, 'bold'),
    'table_body': ('Segoe UI', 12),
}

# Layout Spacing
SPACING = {
    'xs': 4,
    'sm': 8,
    'md': 16,
    'lg': 24,
    'xl': 32,
    'xxl': 48,
}

# Button Styles
BUTTON_STYLES = {
    'primary': {
        'bg': COLORS['primary'],
        'fg': COLORS['text_light'],
        'activebackground': COLORS['primary_dark'],
        'relief': 'flat',
        'borderwidth': 0,
        'cursor': 'hand2',
        'font': FONTS['button'],
        'padx': SPACING['lg'],
        'pady': SPACING['sm'],
    },
    'success': {
        'bg': COLORS['success'],
        'fg': COLORS['text_light'],
        'activebackground': COLORS['success_hover'],
        'relief': 'flat',
        'borderwidth': 0,
        'cursor': 'hand2',
        'font': FONTS['button'],
        'padx': SPACING['lg'],
        'pady': SPACING['sm'],
    },
    'info': {
        'bg': COLORS['info'],
        'fg': COLORS['text_light'],
        'activebackground': COLORS['info_hover'],
        'relief': 'flat',
        'borderwidth': 0,
        'cursor': 'hand2',
        'font': FONTS['button'],
        'padx': SPACING['lg'],
        'pady': SPACING['sm'],
    },
    'danger': {
        'bg': COLORS['danger'],
        'fg': COLORS['text_light'],
        'activebackground': COLORS['danger_hover'],
        'relief': 'flat',
        'borderwidth': 0,
        'cursor': 'hand2',
        'font': FONTS['button'],
        'padx': SPACING['lg'],
        'pady': SPACING['sm'],
    },
}

# Input Styles
INPUT_STYLES = {
    'default': {
        'font': FONTS['body_large'],
        'bg': COLORS['bg_primary'],
        'fg': COLORS['text_primary'],
        'insertbackground': COLORS['primary'],
        'relief': 'solid',
        'borderwidth': 1,
        'bd': 1,
        'highlightthickness': 2,
        'highlightcolor': COLORS['border_focus'],
        'highlightbackground': COLORS['border'],
    }
}

# Table/Treeview Styles
TABLE_STYLE_CONFIG = {
    'Treeview': {
        'configure': {
            'background': COLORS['bg_table'],
            'foreground': COLORS['text_primary'],
            'rowheight': 45,
            'fieldbackground': COLORS['bg_table'],
            'font': FONTS['table_body'],
            'borderwidth': 0,
            'relief': 'flat',
        },
        'map': {
            'background': [('selected', COLORS['primary_light'])],
            'foreground': [('selected', COLORS['text_light'])],
        }
    },
    'Treeview.Heading': {
        'configure': {
            'background': COLORS['primary'],
            'foreground': COLORS['text_light'],
            'font': FONTS['table_header'],
            'relief': 'flat',
            'borderwidth': 0,
        },
        'map': {
            'background': [('active', COLORS['primary_dark'])],
        }
    }
}