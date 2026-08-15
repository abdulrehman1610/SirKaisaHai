---
name: SirKaisaHai Core
colors:
  surface: '#f8f9fb'
  surface-dim: '#d9dadc'
  surface-bright: '#f8f9fb'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f4f6'
  surface-container: '#edeef0'
  surface-container-high: '#e7e8ea'
  surface-container-highest: '#e1e2e4'
  on-surface: '#191c1e'
  on-surface-variant: '#50434b'
  inverse-surface: '#2e3132'
  inverse-on-surface: '#f0f1f3'
  outline: '#82737b'
  outline-variant: '#d4c1cb'
  surface-tint: '#8b4678'
  primary: '#501243'
  on-primary: '#ffffff'
  primary-container: '#6b2a5b'
  on-primary-container: '#e795cd'
  inverse-primary: '#ffade4'
  secondary: '#7c41b1'
  on-secondary: '#ffffff'
  secondary-container: '#c588fd'
  on-secondary-container: '#541289'
  tertiary: '#002b60'
  on-tertiary: '#ffffff'
  tertiary-container: '#004089'
  on-tertiary-container: '#85afff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffd7ee'
  primary-fixed-dim: '#ffade4'
  on-primary-fixed: '#3a0030'
  on-primary-fixed-variant: '#702e5f'
  secondary-fixed: '#f1dbff'
  secondary-fixed-dim: '#deb7ff'
  on-secondary-fixed: '#2d0050'
  on-secondary-fixed-variant: '#632598'
  tertiary-fixed: '#d7e2ff'
  tertiary-fixed-dim: '#acc7ff'
  on-tertiary-fixed: '#001a40'
  on-tertiary-fixed-variant: '#004492'
  background: '#f8f9fb'
  on-background: '#191c1e'
  surface-variant: '#e1e2e4'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '800'
    lineHeight: '1.1'
    letterSpacing: -0.04em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '700'
    lineHeight: '1.2'
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
  stat-display:
    fontFamily: JetBrains Mono
    fontSize: 28px
    fontWeight: '700'
    lineHeight: '1'
    letterSpacing: -0.02em
  label-sm:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: '1'
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  container-max: 1280px
  gutter: 24px
  margin-mobile: 16px
  stack-sm: 12px
  stack-md: 24px
  stack-lg: 48px
---

## Brand & Style
The design system for this platform is built on a "Premium Academic Tech" aesthetic. It targets a student demographic that values transparency, speed, and high-end digital experiences. The visual narrative combines the reliability of academic institutions with the sleek, high-motion feel of modern developer tools.

The style is a hybrid of **Modern Minimalism** and **Glassmorphism**. It utilizes expansive white space, ultra-refined typography, and floating interface layers. High-end visual cues—such as backdrop blurs, soft multi-layered shadows, and vibrant accent gradients—are used to differentiate "SirKaisaHai" from traditional, utilitarian review sites. The goal is to make academic feedback feel like a premium, safe, and modern social interaction.

## Colors
The palette is dominated by "Deep Plum" and "Purple" to establish an authoritative yet creative brand presence. 

- **Primary & Secondary:** Used for high-level branding, navigation headers, and primary calls to action. Use subtle linear gradients between these two for interactive states.
- **Surface Strategy:** The page background is a cool `#F4F5F7` to allow white `#FFFFFF` surface cards to pop with depth.
- **Accents:** `#EFE5FA` (Pale Purple) is reserved exclusively for the backgrounds of stat boxes and informational chips to group data without the harshness of high-contrast borders.
- **Feedback:** Semantic colors for success and warning follow a high-chroma profile to ensure ratings are instantly scannable.

## Typography
The system uses a dual-type approach. **Inter** provides a clean, neutral, and highly legible foundation for the majority of the UI, ensuring that long-form student reviews are comfortable to read.

**JetBrains Mono** is introduced as a high-contrast functional element. It is used specifically for quantitative data—professor ratings, course codes, and date-stamps. This creates a "data-rich" feel that mimics a grade report or a technical dashboard. For headlines, use tight letter-spacing to achieve the "Dribbble-esque" editorial look.

## Layout & Spacing
This design system utilizes a **12-column fluid grid** for desktop, collapsing to a single column for mobile. 

- **The Floating Grid:** Layouts should feel "airy." Use large vertical stack spacing (`48px+`) between major sections (e.g., Course Header vs. Review List).
- **Safe Margins:** Content containers are capped at `1280px` to maintain line-length readability on ultrawide monitors.
- **Internal Padding:** Cards should use generous internal padding (minimum `32px` on desktop) to support the "Premium" feel. Avoid crowding elements; if a card feels full, increase its size rather than decreasing the padding.

## Elevation & Depth
Elevation is the primary driver of hierarchy in this system. It is achieved through two distinct methods:

1.  **2XL Ambient Shadows:** Main surface cards use an ultra-diffused shadow (`y: 20px, blur: 50px, color: rgba(107, 42, 91, 0.08)`). The slight plum tint in the shadow prevents it from looking "dirty" on the light gray background.
2.  **Glassmorphism Layers:** Floating action buttons (FABs), dropdown menus, and modal backgrounds use a `backdrop-filter: blur(12px)` combined with a semi-transparent white fill (`rgba(255, 255, 255, 0.7)`). These elements should have a 1px solid white border at 20% opacity to define their edges against complex backgrounds.

## Shapes
The shape language is consistently "Rounded" to evoke friendliness and modern tech sensibilities.

- **Primary Cards:** Use `rounded-lg` (16px) for all main content containers.
- **Input Fields & Buttons:** Use `rounded-md` (8px) to maintain a slightly more structured look for interactive elements.
- **Badges & Tags:** Use `Pill-shaped` (full radius) for status indicators like "Verified Student" or "Top Rated."
- **Progress Bars:** Should always have fully rounded end-caps.

## Components

### Buttons
- **Primary:** Solid Deep Plum (#6B2A5B) with white text. Apply a subtle gradient transition to Secondary Purple (#6B2FA0) on hover.
- **Ghost:** Transparent background with a 1.5px border in Primary Plum. High-end "clicky" feel with a slight scale-down (0.98) on active state.

### Stat Boxes
- **Visuals:** Background color `#EFE5FA`. The number is displayed in **JetBrains Mono** at `stat-display` size. A small "up/down" trend indicator or badge should float in the top-right corner.

### Review Cards
- **Structure:** White background, 2XL shadow. Use a progress bar for specific metrics (Difficulty, Clarity). 
- **Floating Badges:** Use vibrant semantic colors (Green/Orange) for "Overall Rating" badges, floating them slightly over the card's top-left edge using negative margins.

### Input Fields
- **Style:** Subtle light gray fill (#F4F5F7) that transitions to a white background with a Blue (#2D6FD1) 2px border on focus. No harsh shadows.

### Progress Bars
- **Style:** Height of 8px. The track is `#F4F5F7`. The fill is a linear gradient from Secondary Purple (#6B2FA0) to Action Blue (#2D6FD1).