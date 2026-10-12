# Prompt patterns for Codex Desktop imagegen

Use these patterns as prompt skeletons. Replace bracketed fields with concrete details. Keep user-provided display text exact.

For polished or failure-sensitive work, also apply `openai-imagegen-guide-notes.md` before generating.

## Table of contents

- Universal prompt skeleton
- Posters, covers, social cards
- Format recipes
- Social carousel slides
- UI mockups
- Research, technical, and system diagrams
- Data visualization concepts
- Infographics and field guides
- Product and food renders
- Photorealistic scenes
- Multi-panel boards and storyboards
- Image editing with references
- Quick repair checklist

## Universal prompt skeleton

```text
[Format/aspect/canvas]. Create [artifact type] for [audience/use].

Layout:
- [Region 1]: [role, visual weight, exact text if any]
- [Region 2]: [role, visual weight, exact text if any]
- [Region 3]: [role, visual weight, exact text if any]

Subject:
[Concrete subject, setting, objects, people, product, or system].

Text:
Accurately render the exact visible text: "[text 1]" / "[text 2]" / "[text 3]".

Style:
[Specific visual direction, medium, palette, material, lighting, camera or diagram grammar].

Quality constraints:
Crisp typography, clear hierarchy, readable labels, coherent spacing, no garbled text, no fake logos, no random extra text.
```

## Common format menu

Use this quick mapping when the user describes the goal in plain language:

| User intent | Default format | Prompt focus |
|---|---|---|
| "picture for a post" | 16:9 social cover or 1:1 social card | one strong visual metaphor, one large headline |
| "carousel" | 3-7 separate 1:1 slides | one idea per slide, consistent style |
| "README / article image" | 16:9 article image | workflow, concept, or product idea without logos |
| "app idea / screen" | UI mockup | product context, screen structure, realistic labels |
| "explain how it works" | diagram or infographic | zones, arrows, labels, visual hierarchy |
| "product / object" | product render | materials, lighting, camera, environment |
| "realistic scene" | photorealistic scene | capture context, objects, people, lighting |

For visible text, start with one large headline. Add a subtitle only when it is short and necessary.

## Brief-first pattern

Use before generation when a quoted title or event name carries meaning and the visual direction is not obvious.

```text
Before generating, confirm three anchors:
1. Meaning: Does "[quoted title]" mean [literal interpretation] or [intended emotional/conceptual interpretation]?
2. Exact visible text: Should the image include "[title]", "[date/time]", "[platform]", or only the title?
3. Style / anti-style: What should it feel like, and what should it avoid?
```

If proceeding with inferred anchors:

```text
Inferred brief:
- Meaning: [inference].
- Visible text: "[exact title]" / "[exact date/time/platform if needed]".
- Style / anti-style: [style], avoid [likely wrong default].
```

## Format recipes

Use these recipes when the user names a common publishing surface. The recipe sets the canvas and main layout discipline; the user's requested subject, text, and style still win.

### README hero / GitHub social preview

Use for repository previews, README headers, package announcements, and open-source project pages.

```text
Create a 2:1 GitHub social preview / README hero image for [project/package].

Visible text:
Main title: "[exact title]"
Subtitle: "[exact subtitle]"

Layout:
- Left or top zone: large readable title and subtitle.
- Main zone: one simple visual metaphor for [what the project does].
- Flow zone if relevant: 2-4 simple stages connected by arrows.

Style:
[User-requested style]. Keep it readable at small preview size, with strong whitespace and no dense UI.

Avoid:
Tiny text, fake GitHub UI, fake logos, cluttered badges, random code snippets.
```

### Article cover / share image

Use for blog posts, Telegram/Facebook/LinkedIn sharing, newsletters, and article thumbnails.

```text
Create a 16:9 article cover image for [article topic].

Visible text:
Title: "[exact title]"
Subtitle if needed: "[exact subtitle]"

Layout:
- Title block with large readable typography.
- One central image or metaphor that explains the article.
- Optional small supporting objects, but no dense labels.

Style:
[User-requested editorial style], clear contrast, calm hierarchy.

Avoid:
Poster clutter, tiny captions, fake publication logos, generic stock business scene.
```

If the user asks to include a URL, credit, or repository address, keep it short and readable. Do not ask for a tiny exact footer unless the user accepts post-production layout.

```text
Optional footer:
Render exactly one short footer line: "[domain or short repo path]".
Place it in the lower-left whitespace, large enough to read, without logo marks or UI chrome.
```

### Square social card

Use for Instagram, Threads, LinkedIn square feed, Telegram posts, and compact social previews.

```text
Create a square 1:1 social card for [platform/audience] about [topic].

Visible text:
Large headline: "[exact headline]"
Short subtitle if needed: "[exact subtitle]"

Layout:
- Top or center: headline.
- Center: one strong symbol, product object, scene, or diagram.
- Bottom: optional small cue or visual continuation, not extra text.

Style:
[User-requested style], high contrast, simple composition readable on a phone.

Avoid:
Many competing objects, multiple text blocks, decorative stickers unless requested.
```

### Portrait feed image

Use for Instagram/LinkedIn portrait posts where vertical space helps the message breathe.

```text
Create a 4:5 portrait feed image for [platform/audience] about [topic].

Visible text:
Large headline: "[exact headline]"
Short subtitle if needed: "[exact subtitle]"

Layout:
- Top: headline and subtitle.
- Middle: main visual idea.
- Bottom: secondary symbol, process step, or quiet visual closure.

Style:
[User-requested style], generous margins, phone-readable text.

Avoid:
Cropping important text near the edges, overly tall story-like composition, tiny labels.
```

### Story / vertical short-form cover

Use for Instagram Stories, Telegram Stories, Reels covers, Shorts covers, and vertical announcements.

```text
Create a 9:16 vertical story image for [platform/audience] about [topic].

Visible text:
Large title: "[exact title]"
Short subtitle if needed: "[exact subtitle]"

Layout:
- Top safe area: title, large and readable.
- Middle: main image or process.
- Bottom safe area: optional visual anchor, no long text.

Style:
[User-requested style], strong margins, mobile-first readability.

Avoid:
Small text, important content at extreme top/bottom edges, crowded poster composition.
```

### Thumbnail

Use for video thumbnails, preview cards, and highly compressed feeds.

```text
Create a [16:9 or 1:1] thumbnail for [platform] about [topic].

Visible text:
Render only this large text: "[2-5 word hook]"

Layout:
One dominant subject, one readable hook, high contrast, strong silhouette.

Style:
[User-requested style]. Optimize for readability at tiny sizes.

Avoid:
Subtitles, paragraphs, multiple small objects, subtle low-contrast details.
```

### UI concept mockup

Use for product concepts, SaaS screens, admin panels, dashboards, and mobile app ideas.

```text
Create a [desktop/mobile/tablet] UI concept mockup for [product/use case].

Visible UI labels:
"[product name]", "[screen title]", "[button]", "[tab 1]", "[tab 2]".

Layout:
- Header/navigation.
- Primary work area.
- Secondary panel or details area.
- Realistic empty/loading/status states if relevant.

Style:
[User-requested product UI style], realistic density, precise alignment.

Avoid:
Lorem ipsum, fake charts with unreadable labels, decorative marketing layout instead of real UI.
```

### Technical diagram / workflow

Use for explaining processes, systems, agent workflows, architecture, or method diagrams.

```text
Create a [16:9 or square] technical diagram explaining [process/system].

Visible labels:
"[input]", "[step 1]", "[step 2]", "[output]".

Layout:
- Left/top: input.
- Center: 2-4 processing stages.
- Right/bottom: output or decision.
- Arrows show flow; dashed lines show optional or risky paths.

Style:
[User-requested diagram style], large labels, consistent line weights.

Avoid:
Sci-fi dashboard, random equations, dense microtext, fake infrastructure logos.
```

### Infographic / educational explainer

Use for teaching a concept, comparing options, field guides, checklists, or visual summaries.

```text
Create a [aspect ratio] educational infographic about [subject].

Visible text:
Title: "[exact title]"
Use only these short labels: "[label 1]", "[label 2]", "[label 3]".

Layout:
- Title band.
- Main illustration or comparison area.
- 3-5 numbered callouts or sections.
- Optional legend.

Style:
[User-requested infographic style], clear hierarchy, readable labels.

Avoid:
Too many facts, tiny tables, random extra labels, cartoon chaos unless requested.
```

### Product render / object hero

Use for fictional products, packaging concepts, physical objects, devices, food, or materials.

```text
Create a [aspect ratio] product hero image of [object/product].

Composition:
Hero object at [angle/scale], placed on [surface/environment].

Material and lighting:
[materials], [texture], [lighting], [background].

Text:
Only render exact text if essential: "[label text]".

Style:
[User-requested render/photo/illustration style].

Avoid:
Fake brand marks, unreadable label text, cheap e-commerce look, plastic CGI unless requested.
```

### Photorealistic scene

Use when the user wants a real-life moment rather than a designed graphic.

```text
Create a photorealistic [aspect ratio] scene showing [situation].

Capture:
[camera position], [lens feel], [lighting], [time/place].

Scene:
Include concrete objects and lived-in details: [objects/surfaces/people/weather].

Style:
Natural color, plausible shadows, realistic imperfections, not an ad unless requested.

Avoid:
Glossy AI-ad look, impossible lighting, fake text, distorted hands, over-staged composition.
```

### Image edit / transformation

Use when the user attaches or references an existing image and wants a specific change.

```text
Edit the provided image.

Preserve:
[identity, composition, pose, product shape, important text, lighting direction].

Change:
[specific edit].

Output:
[aspect ratio/use/style].

Avoid:
Changing identity, inventing new logos/text, moving important objects unless requested.
```

## Posters, covers, social cards

Use when making article covers, webinar cards, ads, posters, thumbnails, or event visuals.

```text
Design a [aspect ratio] [poster/article cover/social card] for [topic/event/product].

Promotional hierarchy:
1. Main title largest: "[exact title]"
2. Supporting line: "[exact subtitle]"
3. Metadata/CTA: "[date/author/action if needed]"

Composition:
[Hero object/person/scene] occupies [top/center/left] with [background/environment].
Leave clean negative space for the title. Make the title readable at thumbnail size.

Style:
[User-requested style or a topic-appropriate visual style] with [palette], [lighting], [texture/material if relevant].

Avoid:
Unreadable microtext, garbled letters, fake sponsor logos, stock-photo blandness, cluttered hierarchy.
```

## Social carousel slides

Use for Instagram, Threads, LinkedIn, or similar carousels. For the first public version of this skill, prefer separate square slides in one consistent style. This is simpler, more reliable, and easier to iterate than a seamless panorama.

### Separate-slide carousel

Use this mode for practical social publishing.

```text
Create square 1:1 carousel slide [K] of [N] for [platform/audience].

Theme:
"[central idea]"

Visible text:
Render the exact large headline: "[short headline]"
Render the exact short subtitle if needed: "[short subtitle]"

Scene:
[What this slide shows: hook/problem/process/proof/punchline].

Continuity:
Keep the same visual system across all slides: [palette], [lighting], [character/object continuity], [icon style], [background grammar].

Output constraints:
Large readable text, one clear idea per slide, no random extra text, no tiny labels, no fake logos.
```

Recommended slide plan:

```text
1. Hook: "[short headline]"
2. Setup/problem: "[short headline]"
3. Method/process: "[short headline]"
4. Insight/proof: "[short headline]"
5. Punchline/CTA: "[short headline]"
```

### Panoramic concept

Use this mode only to explore a wide visual direction. Do not treat it as a guaranteed slice-ready master.

```text
Create one ultra-wide panoramic concept artwork for a social media carousel, designed to suggest [N] connected slides.

Theme:
"[central idea]"

Continuity:
A single visual element travels across the panorama: [glowing line / road / ribbon / knowledge graph / timeline / river / cable].

Output constraints:
Continuous world, no hard panel borders, no random text, no dense microtext. This is concept art for direction, not a production slicing workflow.
```

## UI mockups

Use when making app screens, dashboard previews, SaaS concepts, admin panels, or mobile UI.

```text
Create a production-quality UI mockup on a [device/canvas], for a fictional product named "[product name]".

Product context:
[Who uses it and what job the screen performs].

Screen structure:
- Header: include "[exact header text]", [controls].
- Primary panel: [main metric/table/chart/form].
- Secondary panel: [supporting cards, filters, status].
- Navigation: [tabs/sidebar/bottom nav labels].

Data and copy:
Use realistic values and labels: "[label 1]", "[value 1]", "[button text]", "[status]".

Visual system:
[Palette], [density], [typography feel], [icon style], [component spacing].

Quality constraints:
Crisp typography, precise alignment, real product density, no lorem ipsum, no broken icons, no incoherent chart labels.
```

## Research, technical, and system diagrams

Use when making architecture diagrams, AI agent workflows, security diagrams, research figures, or explainer graphics.

```text
Landscape 16:9 publication-grade technical diagram explaining [system/process].

Diagram grammar:
- Left zone: [input/source actors]
- Center zone: [processing modules/components]
- Right zone: [outputs/decisions]
- Bottom strip: [timeline/legend/evidence/status]

Relationships:
Use arrows for [flow], dashed lines for [risk/optional path], color [A] for [meaning], color [B] for [meaning].

Exact labels:
"[module 1]", "[module 2]", "[data type]", "[risk label]", "[output label]".

Style:
[User-requested diagram style or a simple readable diagram style], large readable labels, clear lines, consistent spacing, accessible contrast.

Avoid:
Decorative sci-fi dashboard, tiny illegible labels, random math, fake company logos.
```

## Data visualization concepts

Use when the image is a visual concept of a chart, not a real computed chart. For analytical reports, prefer real data tooling.

```text
Create a [chart family] visualization concept about [metric/topic].

Structure:
[Small multiples / network graph / treemap / Sankey / timeline / choropleth] with [number of panels/groups].

Encodings:
- X axis: [field and units]
- Y axis: [field and units]
- Color: [meaning]
- Size/thickness: [meaning]

Labels:
Use exact labels: "[title]", "[axis label]", "[legend item]", "[annotation]".

Style:
[User-requested visualization style or a simple readable chart style], generous margins, consistent scales, accessible contrast.

Avoid:
Fake precision, unreadable axes, inconsistent legends, random numbers unless supplied.
```

## Infographics and field guides

Use when the image should teach, compare, classify, or explain an object/process.

```text
Create a [aspect ratio] [field guide / museum catalog board / educational infographic] about [subject].

Fixed layout:
- Top title band: "[exact title]"
- Main illustration zone: [central object/process/cross-section]
- Annotation zone: [numbered labels and lead lines]
- Side panel: [summary, comparison, checklist]
- Bottom legend: [scale, materials, notes]

Annotation behavior:
Use thin lead lines, numbered callouts, readable labels, and consistent spacing.

Style:
[Scientific poster / museum board / classroom wall chart / editorial explainer] with [palette].

Avoid:
Cartoon chaos, unlabeled parts, garbled labels, excessive realism where clarity matters.
```

## Product and food renders

Use when multiple visual systems must be controlled: product, material, environment, particles, lighting.

```text
/* PRODUCT_RENDER_CONFIG: [short name]
   AESTHETIC: [user-requested product/render aesthetic] */
{
  "canvas": "[aspect ratio]",
  "subject": "[product/food object]",
  "composition": "[hero angle, placement, scale]",
  "materials": ["[material 1]", "[surface detail]", "[texture]"],
  "environment": "[studio/table/location/background]",
  "lighting": "[softbox/natural/window/backlight/highlights]",
  "motion_or_details": ["[splash/steam/crumbs/particles/condensation]"],
  "palette": "[colors]",
  "output_mood": "[user-requested mood or topic-appropriate mood]",
  "avoid": ["cheap e-commerce look", "plastic CGI", "fake brand marks", "unreadable label text"]
}
```

## Photorealistic scenes

Use when the desired result should feel captured, not designed.

```text
Create a photorealistic [scene] as if captured by [camera/capture context].

Capture:
[Eye level / crowd distance / handheld phone photo / 28 mm lens feel / natural morning side light].

Scene density:
Include [5-12 concrete nouns: objects, surfaces, signs, weather, reflections, tools, furniture].

Human/context details:
[People, gestures, scale, imperfections, lived-in traces].

Style constraints:
RAW, unpolished realism, natural color, plausible shadows, no glossy AI-ad look unless requested.
```

## Multi-panel boards and storyboards

Use for character sheets, proof sheets, storyboard grids, visual explorations, and concept boards.

```text
Create a [grid size] [storyboard / character sheet / exploration board] with [number] panels.

Global consistency:
Same [character/product/world], same palette, same identity markers, coherent lighting and style.

Panel roles:
1. [Panel role/shot]
2. [Panel role/shot]
3. [Panel role/shot]

For storyboards:
Add camera language in each panel: WIDE, OTS, CU, low angle, aerial, static, pan, match cut.

Quality constraints:
Clearly separated panels, readable captions if used, no identity drift, no random extra panels.
```

## Image editing with references

Use when a source image is attached or the user wants to preserve an existing image.

```text
Preserve:
[Identity, pose, product shape, logo/text if allowed, composition, color relationships, lighting direction, background elements].

Change:
[Specific requested edit: replace background, adjust outfit, add object, change style, remove distraction, extend canvas].

Output:
[Aspect ratio, style, final use, quality constraints].

Avoid:
Changing face/product identity, altering exact text, adding extra objects, changing camera angle unless requested.
```

## Quick repair checklist

- Does it say the artifact type and aspect ratio first?
- Does it explain the intended use: article cover, README, social post, UI, edit, diagram, or concept?
- Are all required visible words quoted exactly?
- If the request includes a quoted title or named event, was its intended meaning clarified or explicitly inferred?
- Is text short, large, high-contrast, and placed in a clear region?
- Are URLs, credits, handles, or footer lines short enough for ImageGen, or should this be treated as production/post-production layout?
- Is the layout explicit enough to prevent improvisation?
- Does the style name a real visual context, not only "beautiful"?
- Does the style specify medium, palette, density, line/camera/lighting, and what to avoid?
- Are labels, axes, panels, legends, and UI values specified where needed?
- For UI, does the prompt describe a real product surface rather than a decorative marketing image?
- For edits, are preserve/change/output instructions separated?
- For photorealistic scenes, does the prompt describe capture context and concrete physical details?
- Does the avoid-line target likely failures rather than generic negativity?
- For carousels, is it clear whether this is a separate-slide set or only a panoramic concept?
- After generation, is the next prompt focused on the single biggest failure?
