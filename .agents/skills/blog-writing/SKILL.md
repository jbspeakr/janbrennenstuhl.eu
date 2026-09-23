---
name: blog-writing
description: Write, review, tune, and optimize blog articles for janbrennenstuhl.eu. Use when drafting new articles from ideas, reviewing existing drafts, or refining published posts. Requires the shared prose voice and blog structure references. Trigger with /blog-write, /blog-review, or whenever the user asks to create, edit, or improve a blog article.
---

# Blog Writing

Help the author write a personal technical blog as an experienced, helpful peer. Produce evidence-backed opinions and practical explanations that readers can follow without insider context. Never invent the author's experience or imitate another writer's signature personality, jokes, or verbal tics.

## Required Reading and Ownership

Before outlining, drafting, reviewing, or editing an article, read both files in full:

1. [Shared prose voice](references/voice.md): person, sentence shape, density, word choice, banned language, and calibration examples.
2. [Blog structure and Hugo presentation](references/structure.md): article shape, headings, evidence, links, formatting, front matter, and rendering checks.

These are required parts of this skill, not optional resources to load only when a draft looks wrong. Keep 1 entry point so a structure-only task cannot accidentally skip voice. If a reference cannot be read, report the missing prerequisite instead of silently substituting generic writing advice.

The voice reference owns sentence-level register and all banned lists. The structure reference owns blog organization and mechanics and cannot relax voice. This file owns the procedure and completion checks; do not duplicate rule lists here. Requirements take precedence over calibration examples. Evidence and privacy requirements always apply: an instruction to make prose personal never authorizes invented first-person claims.

Apply the prose rules to the requested article and its authored metadata. The rules do not prescribe the formatting of these instruction files, which use numbered procedures and examples of prohibited language for teaching. Do not rewrite untouched archive articles, create newsletter infrastructure, or add a prose linter unless asked.

## Workflow: Idea to Article

1. Establish the contribution and reader need. Identify the artifact, method, result, or supplied observation that makes the article useful. State privately what the reader should understand or be able to do afterward. Use the user's notes and available public artifacts; ask only for essential personal context that cannot be recovered from them.
2. Map the evidence before drafting. Distinguish facts, observations, inferences, and recommendations. Find the strongest available source for material claims, verify quantitative scope, and identify unsupported claims to remove or qualify. Do not fill gaps with invented experience.
3. Choose a structure from the structure reference. Give each proposed H2 a distinct, 1-sentence purpose and order the sections around the reader's reasoning. Plan a concrete opening. Do not force every article into a fixed number of sections or a mandatory conclusion.
4. Draft with the voice reference open. Make actors visible, introduce necessary terms, and develop each point with its evidence. Use the author's supplied attitude and observations where appropriate. Do not add colloquialisms, anecdotes, questions, or analogies as a personality checklist.
5. Compress without losing reasoning. Make each point once, remove reaction-only paragraphs and repeated benefits, and keep the material limitations. Prefer 1 useful example to several interchangeable ones. Preserve distinct evidence and explanatory motives.
6. Run the complete review below, then verify the article's Hugo mechanics when files changed. Deliver the requested article or edits with a brief, accurate account of verification and any remaining source uncertainty.

## Workflow: Review and Optimize

For a review-only request, report prioritized findings with locations and concrete suggested rewrites. Do not modify the article unless editing is requested. For an editing request, make the revisions and summarize the meaningful changes. In either case, complete these passes in order:

1. Contribution and provenance: identify what the reader gains. Check first-person claims against supplied context or inspectable support. Remove implied employer details and invented experience. Flag missing evidence without manufacturing a replacement fact.
2. Reasoning and evidence: verify material claims, sources, quantitative scope, and quoted statistics. Keep facts, observations, inferences, and recommendations distinguishable. Preserve uncertainty that affects the conclusion.
3. Structure: check the chosen article route, opening, section purposes, and information order. Merge duplicate points across sections. Remove endings that only recap or advertise what comes next. Make the article understandable without following every link.
4. Voice: apply every section of the voice reference, including both banned lists, to titles, headings, body, captions, and metadata. Search can help locate words and punctuation; inspect each match for legitimate source quotations or literal technical text. Do not treat a clean search as a completed voice review.
5. Read aloud for flow: inspect paragraphs in sequence. Repair chopped thoughts, nested clauses, vague pronouns, repeated rhetorical openers, and decorative wording. Keep natural contractions and useful colloquial qualification. Check who does what without inserting unsupported `I` or `we`.
6. Mechanics: for article file edits, follow the structure reference's front matter, bundle, link, shortcode, and build checks. Report only checks actually run. For review-only work or changes to this skill, check the relevant documents and references instead of claiming a site build validates prose.

## Completion Gate

Before delivering an article or review, confirm:

- [ ] Both required references were read and applied in full.
- [ ] The reader can identify the contribution, and the chosen structure makes it easy to follow.
- [ ] Every section has a distinct purpose; the opening and ending suit the article type.
- [ ] First-person claims are honest, professional claims have inspectable support, and no employer or internal context is disclosed.
- [ ] Material claims and quantities are sourced, scoped, and attributed; uncertainty is preserved.
- [ ] The voice review covers every rule, not just searchable banned words.
- [ ] Each sentence contributes information or necessary reasoning; no section repeats a point for emphasis.
- [ ] A read-aloud pass confirms clear actors, readable clauses, resolved pronouns, and varied paragraph openings.
- [ ] Authored headings, captions, and metadata pass the same voice review as the body.
- [ ] Applicable Hugo checks were run for article edits, and any blocked verification is reported accurately.

For changes to this skill itself, check reference resolution and rule consistency, then exercise the instructions on a small disposable prose sample. Do not edit published articles to demonstrate the skill.
