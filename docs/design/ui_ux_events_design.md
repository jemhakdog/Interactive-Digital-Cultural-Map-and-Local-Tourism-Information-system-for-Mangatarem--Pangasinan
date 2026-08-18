## Design System: Events Page

### Pattern
- **Name:** Storytelling-Driven + Hero
- **CTA Placement:** Above fold
- **Sections:** Hero > Features > CTA

### Style
- **Name:** Aurora UI
- **Keywords:** Vibrant gradients, smooth blend, Northern Lights effect, mesh gradient, luminous, atmospheric, abstract
- **Best For:** Modern SaaS, creative agencies, branding, music platforms, lifestyle, premium products, hero sections
- **Performance:** ⚠ Good | **Accessibility:** ⚠ Text contrast

### Colors
| Role | Hex |
|------|-----|
| Primary | #EC4899 |
| Secondary | #F472B6 |
| CTA | #06B6D4 |
| Background | #FDF2F8 |
| Text | #831843 |

*Notes: Vibrant destination colors + Sky Blue + Warm accents*

### Typography
- **Heading:** Noto Serif TC
- **Body:** Noto Sans TC
- **Mood:** chinese, traditional, elegant, cultural, multilingual, readable
- **Best For:** Traditional Chinese sites, cultural content, Taiwan/Hong Kong markets
- **Google Fonts:** https://fonts.google.com/share?selection.family=Noto+Sans+TC:wght@300;400;500;700|Noto+Serif+TC:wght@400;500;600;700
- **CSS Import:**
```css
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700&family=Noto+Serif+TC:wght@400;500;600;700&display=swap');
```

### Key Effects
Large flowing CSS/SVG gradients, subtle 8-12s animations, depth via color layering, smooth morph

### Avoid (Anti-patterns)
- Generic photos
- Complex booking

### Pre-Delivery Checklist
- [ ] No emojis as icons (use SVG: Heroicons/Lucide)
- [ ] cursor-pointer on all clickable elements
- [ ] Hover states with smooth transitions (150-300ms)
- [ ] Light mode: text contrast 4.5:1 minimum
- [ ] Focus states visible for keyboard nav
- [ ] prefers-reduced-motion respected
- [ ] Responsive: 375px, 768px, 1024px, 1440px

