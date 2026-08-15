# SirKaisaHai — Design System
### Inspired by Superior University's ERP portal color language

**Note before you build:** I pulled the palette and component patterns from your ERP screenshot, but I'd swap the *exact* maroon for a close cousin rather than the literal same hex — using Superior's identical brand color could make SirKaisaHai look like an official university tool, which works against you (it's an independent, anonymous, unofficial platform — you don't want a confused student assuming their reviews reach the administration). The palette below keeps the same *family* and feel, shifted just enough to be clearly its own brand.

---

## 1. Color Palette

### Primary (maroon/plum — from the ERP header)
```
--primary-900: #4A1F42   /* deep maroon, hover/active states */
--primary-700: #6B2A5B   /* main brand color — header, primary buttons, logo */
--primary-500: #8B3A76   /* lighter accent, links, active nav */
--primary-100: #F3E5F0   /* pale tint — stat box backgrounds, hover fills */
```

### Secondary accent (purple — from the CGPA/SGPA numbers)
```
--accent-700: #6B2FA0    /* stat numbers, key metrics */
--accent-100: #EFE5FA    /* stat card backgrounds */
```

### Semantic colors (from Quick Access buttons + attendance bars)
```
--success: #2E9E4F       /* green — good rating, high attendance, "helpful" votes */
--success-bg: #E7F6EC

--warning: #E08A1F        /* orange — pending moderation, in-progress, mid rating */
--warning-bg: #FDF1E2

--danger: #D63B3B         /* red — low rating, F grade equivalent, rejected review */
--danger-bg: #FBEAEA

--info: #2D6FD1            /* blue — links, secondary actions, LMS-style button */
--info-bg: #E8F0FC
```

### Neutrals
```
--bg-page: #F4F5F7        /* page background, matches ERP's light gray */
--bg-card: #FFFFFF        /* card surfaces */
--border: #E4E6EA
--text-primary: #1F2430
--text-secondary: #6B7280
--text-muted: #9CA3AF
```

### Where each color is used in SirKaisaHai (mapped from the ERP patterns you shared)

| ERP element | ERP color | SirKaisaHai equivalent |
|---|---|---|
| Header bar | Maroon | App header/nav bar |
| Quick Access buttons (Website/LMS/Support/SIRC) | Red/Blue/Orange/Green blocks | Landing page quick links (Browse Professors / Browse Courses / Write a Review / How Anonymity Works) |
| CGPA/SGPA stat boxes | Purple number on pale purple bg | Professor rating stat boxes (Avg. Teaching / Avg. Grading Fairness / Avg. Workload) |
| Pass Credits (green number) | Green | High-rating badge, "helpful" vote count |
| F Grades (red number, 0) | Red | Low-rating flag, flagged-review count |
| Term-wise CGPA line chart | Red line, green dots | Rating trend over semesters (Phase 2/3 feature) |
| Attendance progress bars (green, one orange) | Green/orange horizontal bars | Rating breakdown bars per category (teaching, grading, workload) |
| Academic Progress circular ring | Green ring, % in center | Overall professor rating shown as a ring (e.g., "82% would recommend") |
| Academic Warnings pill (green checkmark badge) | Green pill | "Verified reviews" or "No flags" trust badge on a professor page |
| White cards on gray background, soft borders, rounded corners | — | Same card pattern for professor/course/review cards throughout |

---

## 2. Typography

```
--font-heading: 'Inter', sans-serif    /* matches the clean sans-serif in the ERP */
--font-body: 'Inter', sans-serif
--font-mono: 'JetBrains Mono', monospace  /* for rating numbers — gives them a "data" feel like CGPA/SGPA */

--text-3xl: 2rem      /* page titles */
--text-2xl: 1.5rem    /* card headers, stat numbers (like the "3.59" CGPA) */
--text-lg: 1.125rem   /* section headers */
--text-base: 1rem     /* body text */
--text-sm: 0.875rem   /* secondary text, labels */
--text-xs: 0.75rem    /* muted metadata */
```

Stat numbers (ratings) should be bold and large, same visual weight as the "3.59 CGPA" — that's the ERP pattern worth directly copying: **big number, small label underneath, centered, pale tinted background box.**

---

## 3. Core Components (mapped from your ERP's patterns)

### Stat Box (from CGPA/SGPA/Pass Credits/F Grades boxes)
```
Background: --accent-100 (or semantic color's -bg variant)
Border-radius: 12px
Padding: 20px
Number: --text-2xl, bold, --accent-700 (or semantic color)
Label: --text-sm, --text-secondary, centered below number
```
Use for: professor's average teaching rating, average grading fairness, average workload, total review count.

### Card (from the white profile card and widget cards)
```
Background: --bg-card
Border: 1px solid --border
Border-radius: 12px
Padding: 24px
Shadow: 0 1px 3px rgba(0,0,0,0.06)
```
Use for: professor cards, course cards, individual review cards.

### Progress Bar (from Attendance list)
```
Track: --border, height 8px, rounded
Fill: --success (or --warning if rating is mid, --danger if low)
Label: course/category name left-aligned, percentage right-aligned
```
Use for: rating breakdown per category (teaching, grading fairness, workload, attendance strictness) on a professor page — directly reuses the ERP's attendance-bar pattern.

### Circular Progress Ring (from Academic Progress widget)
```
Stroke: --success (green) for good aggregate rating
Track: --border
Center text: large bold percentage/score, small label below
```
Use for: an at-a-glance "overall recommend score" on professor pages.

### Pill Badge (from Academic Warnings "✅ 0")
```
Background: --success-bg or --warning-bg
Border-radius: full (999px)
Padding: 4px 12px
Icon + count, small bold text
```
Use for: "0 flags," "Verified badge" (Phase 2), review status indicators.

### Button Row (from Quick Access Links)
```
Border-radius: 10px
Padding: 14px 20px
Icon + label + arrow, left-aligned icon, right-aligned arrow
Solid color background matching semantic meaning, white text
```
Use for: landing page primary actions.

### Header Bar
```
Background: --primary-700
Height: 64px
Logo left, search center (optional at MVP), profile/menu right
Text/icons: white
```

---

## 4. Layout Patterns (from the ERP dashboard)

- **Top summary card first** — ERP puts identity + key stats in one card right under quick links. SirKaisaHai equivalent: professor page puts name + department + the 4 key stat boxes in one card right at the top, before reviews.
- **Two-column widget grid below the fold** — ERP does Term-wise CGPA (wide, left) + Upcoming Fee/Warnings (narrow, right) side by side. SirKaisaHai equivalent: Reviews list (wide, left) + Quick Facts/Tags panel (narrow, right) on desktop; stacks vertically on mobile.
- **Section cards separated by clear whitespace**, not tabs — matches the ERP's single-scroll dashboard feel rather than a tabbed interface. Keep SirKaisaHai's professor page as one scrollable page too.
- **Numbers-first, then bars, then lists** — the ERP leads with big stat numbers, then progress bars, then a list at the bottom (Notifications). Mirror this order on a professor page: rating stat boxes → rating breakdown bars → review list.

---

## 5. Dark Mode Note

The ERP screenshot is light-mode only. Your earlier "Terminal Amber" dark-mode-first direction and this maroon/purple light palette can coexist as a **light theme option**: keep dark mode as default (matches student mobile-usage habits per the original PRD §17), but offer this maroon/purple scheme as the light-mode palette instead of a generic light theme — gives light mode a distinct, intentional identity rather than being an inverted afterthought.

```
Light mode (this doc):     primary-700 maroon on white/gray
Dark mode (Terminal Amber): amber accent on near-black
```

Both can share the same component shapes (cards, stat boxes, progress bars) — only the color tokens swap.

---

## 6. What NOT to Copy Directly

- Don't reuse Superior's exact logo mark, wordmark, or the literal maroon hex (#6B2A5B territory but not identical) — keeps you clear of any brand-confusion issue given the platform is unofficial and anonymous.
- Don't mimic the ERP's dense, form-heavy admin aesthetic elsewhere in the app — that style fits a data-dashboard, not a browsing/review-reading experience. Use it specifically for stat-heavy views (professor page header), not for the review-reading list itself, which should feel lighter and more like a feed.
