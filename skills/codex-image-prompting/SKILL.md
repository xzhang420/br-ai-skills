---
name: codex-image-prompting
description: "Turn rough visual ideas into clear prompts for Codex Desktop ImageGen, then generate or edit images with the native image tool when available. Use when the user asks to create, generate, draw, render, edit, improve, or prepare an image prompt for posters, social cards, thumbnails, carousel slides, UI mockups, diagrams, infographics, data visualization concepts, README or article images, product renders, photo scenes, storyboards, or visual concepts. This skill is for prompt design and ImageGen iteration, not local API wrappers, CLI execution, key setup, deterministic layout tooling, or paid local generation paths."
---

# Codex image prompting

## Purpose

Use this skill to turn a rough visual intent into a strong prompt, then generate or edit the image with Codex Desktop's native image tool when the user asks for an image and the tool is available.

Keep the first public version simple: prompt design plus native ImageGen iteration. Do not install or call local image-generation CLIs, local image API scripts, environment files, key setup, paid local generation paths, canvas exporters, or deterministic typography tooling. Use the native Codex image tool instead of asking the user to copy prompts elsewhere.

## Operating loop

1. Classify the task: `new image`, `edit/reference image`, `prompt only`, `prompt repair`, or `carousel slides`.
2. Identify artifact type: poster, hero image, article cover, social card, thumbnail, UI mockup, infographic, research figure, technical diagram, product render, photo scene, storyboard, character sheet, data visualization, README image, article image, or carousel slide set.
3. Capture hard constraints: exact visible text, language, aspect ratio, audience, brand/product, output use, reference images, must-keep elements, and must-avoid elements.
4. Run the Brief Gate. If the request has a named event, quoted concept, emotional title, audience-specific context, or underspecified style/mood, pause before generation and gather the missing anchors.
5. Choose a format recipe when the output is a known use case: README hero, article cover, social square, portrait feed, story, carousel slide, UI mockup, diagram, infographic, product render, photo scene, or image edit.
6. Apply the OpenAI image prompting pass for quality: intent, composition, exact text, style, constraints, likely failure modes, and iteration plan.
7. Draft the image prompt in English by default, while preserving user-supplied display text exactly in its original language.
8. Put structure before style: canvas, layout, zones, subject, exact text, visual semantics, materials/light, quality constraints, avoid-line.
9. If the user asked for a prompt only, return the prompt in a fenced block plus one short note.
10. If the user asked for an image, briefly surface the polished prompt or prompt summary, then call native image generation with that prompt.
11. After generation, give a concise critique and next-iteration suggestion, especially for text readability, composition, style fit, constraint drift, and whether the prompt should be simplified.

## Core rules

- Put every required visible string in quotes.
- Treat quoted names and titles as meaning-bearing constraints, not decorative text. Ask what they should feel like before inventing objects or palette.
- Start with format and layout, not adjectives.
- Use fixed regions for infographics, educational boards, posters, and diagrams.
- Write UI prompts like product specs: device, screen, information architecture, components, labels, values, states.
- For data/research figures, specify chart family, axes, legends, labels, arrows, panels, color semantics, and readability.
- For photorealistic scenes, specify capture context: camera position, lens feel, lighting, realistic surfaces, and concrete objects.
- For multi-panel work, specify panel count, grid, roles, consistent palette/style, and identity continuity.
- For image edits, state what to preserve before what to change.
- For visible text, prefer short, large, high-contrast phrases. Long text, small labels, and many exact captions are likely to fail in ImageGen.
- For strong results, use positive concrete instructions first: subject, spatial arrangement, lighting/materials, camera or diagram grammar, mood, and exact exclusions.
- For ambiguous style words such as "clean", "modern", "editorial", or "flat vector", anchor the prompt with real visual references: medium, palette economy, line weight, density, whitespace, and things to avoid.
- Use negation sparingly for likely failure modes: garbled text, fake logos, unreadable microtext, distorted hands, incoherent UI, cropped labels.

## Brief Gate

Before generation, stop and ask for a short brief when any of these are true:

- the request includes a quoted event, stream, episode, product, or campaign name whose meaning is not visually obvious;
- the user asks for a cover/poster/social image but gives no style or anti-style;
- the prompt could drift into a generic cozy room, SaaS card, brown/purple AI default, stock photo, or unrelated genre;
- the exact visible text is unclear or not explicitly quoted.

Ask for up to three anchors, then generate:

1. Meaning: what the title should communicate, for example meditative presence, irony, urgency, intimacy, launch, proof, or celebration.
2. Text: exact visible strings in quotes.
3. Style and anti-style: desired visual world plus what to avoid.

If the user gave enough information to infer the anchors safely, state the inferred brief in one compact block and proceed. Do not silently invent a room, person, object, palette, or mood for a meaning-heavy title.

## Style Neutrality

Do not apply a house style by default. The skill should follow the user's requested style, brand, medium, genre, mood, and palette as closely as possible.

- If the user names a style, use that style and do not replace it with a generic tech/editorial look.
- If the user does not name a style, infer a lightweight style from the artifact and audience, then state it briefly before generation.
- Do not reuse palettes or aesthetics from examples unless the user asks for them.
- Do not default to any recurring aesthetic from prior examples, prior generations, or the assistant's own taste.
- When style is underspecified, offer or choose a neutral fit such as clean, readable, high-contrast, and topic-appropriate rather than a fixed palette.
- If a result drifts into an unintended style, repair the next prompt by naming both the desired style and the styles to avoid.

## Text Strategy

For the first version, do not route text through a separate overlay step. Try to get ImageGen to render text directly, but keep it simple.

- Good ImageGen text: one short headline, one short subtitle, large type, high contrast, clean background.
- Risky ImageGen text: paragraphs, dense labels, tables, small UI copy, many exact captions, long Cyrillic strings.
- If text fails, simplify the words and regenerate before proposing external design tools or manual layout.
- URLs, legal text, credits, handles, and exact footer lines are high-risk in ImageGen. First try a short, large, isolated version in the generated image. If exact small text is required, explicitly label that as a post-production/production-layout need instead of silently adding a manual overlay.
- If the user explicitly asks for a production layout, explain that this skill focuses on prompting and ImageGen, not deterministic design assembly.

## Carousel Guidance

Use `references/prompt-patterns.md` for full carousel templates.

Prefer `separate-slide carousel` for social publishing: generate 3-7 square slides with one idea and one short headline per slide, while keeping the same visual system across prompts.

Use `panoramic carousel concept` only to explore a wide visual direction. Do not promise pixel-perfect seamless slicing or production geometry. If the user wants a publishable carousel, make a clear slide plan and generate separate slides unless they explicitly ask for a production design workflow outside this skill.

## When to read references

Read `references/prompt-patterns.md` when:

- the user asks for a common publishing format and would benefit from a ready recipe;
- the prompt must be client-ready or publication-ready;
- the request involves UI, diagrams, data visualization, posters, dense text, product renders, image editing, or carousels;
- the first draft would otherwise be generic;
- the user asks to make a prompt better or more precise.

Read `references/openai-imagegen-guide-notes.md` when:

- the user wants an impressive, polished, or publication-grade result;
- the request includes exact text, image editing, UI, diagrams, infographics, product renders, photorealistic scenes, or character/story continuity;
- the request includes a quoted concept/title or sparse event brief that needs meaning before visual execution;
- a generated image drifts from the requested style, layout, text, or constraints.

## Output shapes

For prompt-only requests:

```text
Prompt:
<polished prompt>

Note:
<one sentence explaining the main prompt strategy>
```

For generation requests:

```text
Prompt used:
<polished prompt or compact prompt summary>

Generation:
<call native image generation with the full polished prompt>

Review:
<one or two concrete notes about what worked and what to refine next>
```

Do not ask the user to copy the prompt into another tool when native image generation is available.

For edit/reference-image requests:

```text
Edit prompt:
Preserve: <identity, layout, product, face, text, composition, colors>.
Change: <specific transformation>.
Output: <format, style, quality, avoid-line>.
```

For carousel requests:

```text
Carousel mode:
<separate-slide carousel | panoramic concept>

Slide plan:
<numbered list of slide messages and visuals>

Generation:
<generate the requested slide(s) with native ImageGen>
```

For carousel generation, start with either a full slide plan or the first 1-2 slides if the user wants to explore direction. Keep text large and short.

## Source pattern

This skill adapts prompt-craft ideas from `wuyoscar/GPT-Image2-Skill`, but intentionally replaces local API/CLI execution with native Codex image generation when available.
