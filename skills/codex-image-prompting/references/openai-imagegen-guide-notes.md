# OpenAI image prompting guide notes

These notes adapt the OpenAI image generation prompting guide for Codex Desktop native ImageGen. They are prompt-writing rules, not API instructions. Do not add local API wrappers, API keys, CLI generation, or model parameter setup.

Source: https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide

## Table of contents

- Prompt quality pass
- Text inside images
- Style and visual specificity
- Edits and reference images
- UI and product surfaces
- Diagrams and educational visuals
- Photorealistic scenes
- Multi-image consistency
- Iteration rubric

## Prompt quality pass

Before generating, make the prompt answer:

- What is the artifact and where will it be used?
- What is the exact canvas or aspect ratio?
- What is the main subject?
- Where are the main elements placed?
- What exact visible text must appear?
- What visual style, medium, palette, lighting, camera, or diagram grammar should guide the image?
- What must not happen?

Prefer concrete nouns and spatial instructions over vague adjectives. "Three large zones connected by arrows" is stronger than "clear workflow". "White background, deep navy line art, one accent color" is stronger than "clean tech style".

## Brief-first cases

Some requests look complete but are visually underspecified. Named events, streams, episodes, performances, campaigns, and quoted concepts often carry meaning that cannot be guessed from the words alone.

Do not jump straight from a sparse event request to generation if it would require inventing the tone, symbolism, room, palette, or genre.

Use this three-anchor brief:

```text
Brief:
1. Meaning: "[what the title should feel like]"
2. Exact visible text: "[title]" / "[date or platform if needed]"
3. Style / anti-style: "[desired style]" / avoid "[unwanted default]"
```

Example:

```text
User request:
Create a cover for a stream called "Just Sitting" on July 11 at 11:11.

Do not assume:
A cozy room, armchair, muddy dark palette, or generic streaming poster.

Ask or infer:
"Just Sitting" = meditative presence, not household sitting.
Visible text = "Just Sitting", "July 11 · 11:11".
Anti-style = no dark-brown cozy room, no generic AI purple/brown default.
```

If the user is not available and the request must continue, explicitly state the inferred brief before the prompt.

## Text inside images

ImageGen can render short text, but it needs discipline.

- Put every required string in quotes.
- Ask for one appearance of the text unless repetition is intended.
- Keep text short, large, high-contrast, and isolated from visual clutter.
- Say where text belongs: title band, top-left, centered headline, caption under image, label beside object.
- Use "no other readable text" when random extra text would hurt the result.
- If text fails, shorten it, increase its size, reduce the number of text elements, and regenerate.
- Long URLs, exact handles, legal lines, credits, and tiny footers are fragile. For prompt-only/ImageGen-first work, prefer short visible strings such as a domain or repo owner/name. If exact footer typography is mandatory, call it a production-layout/post-production step rather than hiding it inside the normal ImageGen loop.

Template:

```text
Visible text:
Render exactly one large headline: "[headline]".
Render one smaller subtitle: "[subtitle]".
Place both in the top third with high contrast and clear margins.
No other readable text.
```

For a URL or credit test, make it large and isolated:

```text
Visible footer text:
Render exactly one short footer line: "[short domain or repo path]".
Place it as large readable text in the lower-left whitespace. No logo, no UI pill, no extra footer text.
```

## Style and visual specificity

Do not rely on broad style labels alone. Add visual constraints that make the style operational:

- medium: editorial illustration, technical diagram, photorealistic scene, product render, ink line art, museum field guide;
- palette: exact colors, palette size, background color, contrast level;
- density: sparse, dense dashboard, single hero object, 3-panel board;
- geometry: grid, bands, zones, central object, left-to-right flow;
- material and lighting: paper, glass, metal, softbox, natural window light, harsh noon sun;
- camera when relevant: eye level, overhead, close-up, wide shot, 35mm feel.

When a result drifts into generic colorful SaaS illustration, repair with palette economy and object limits:

```text
Use only [color 1], [color 2], and white negative space. No other colors.
Use three large objects only. No stickers, sticky notes, confetti, multicolor cards, tiny icons, or dense dashboard UI.
```

## Edits and reference images

For edits, separate what must stay from what changes. This reduces accidental identity, composition, or product drift.

Template:

```text
Preserve:
[identity, pose, product shape, layout, camera angle, lighting direction, important text].

Change:
[specific edit].

Output:
[format, style, final use].

Avoid:
[identity drift, added objects, changed text, changed angle, extra logos].
```

If the edit is style transfer, explicitly say which content should remain unchanged and which style elements should change.

## UI and product surfaces

Treat UI prompts as product specs, not decorative screenshots.

- Name the user, job-to-be-done, screen type, and device/canvas.
- Specify information architecture: header, navigation, primary work area, secondary panel, states.
- Provide realistic labels and values.
- Ask for coherent spacing, alignment, density, and component hierarchy.
- Avoid marketing landing-page composition when the request is a real app surface.

## Diagrams and educational visuals

For diagrams, make the visual grammar explicit:

- zones: input, process, output, evidence, risk, legend;
- relationships: arrows, dashed lines, grouping boxes, numbered callouts;
- labels: short exact labels only;
- hierarchy: title, panels, labels, legend;
- accessibility: readable contrast, consistent line weights, generous spacing.

Avoid random math, fake infrastructure logos, unreadable labels, and sci-fi dashboards unless requested.

## Photorealistic scenes

For realistic images, describe the capture:

- camera position and distance;
- lens feel or shot type;
- lighting and time of day;
- physical environment;
- concrete objects and surfaces;
- imperfections that make the scene lived-in.

Avoid over-polished AI advertising unless the user wants an ad.

## Multi-image consistency

For carousels, storyboards, character sheets, and visual sets:

- define the shared visual system before slide-specific prompts;
- reuse palette, lighting, line style, background grammar, and recurring objects;
- keep one idea per image;
- use the same character/object identity markers when continuity matters;
- after the first generated image, describe what to preserve in the next prompt.

## Iteration rubric

After generation, review:

- Text: exact, readable, no random extra words?
- Composition: correct format, hierarchy, margins, no cropped essentials?
- Subject: did the requested objects/people/system appear?
- Style: did it follow the requested style rather than a generic model default?
- Constraints: any forbidden colors, logos, UI clutter, extra labels, distorted details?
- Use readiness: concept-only or good enough for the intended surface?

For the next prompt, change only the highest-impact failure first. Avoid stacking many unrelated corrections in one regeneration.
