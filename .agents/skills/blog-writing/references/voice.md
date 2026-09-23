# Shared Prose Voice

Apply these requirements to every article you draft or edit, including titles, headings, captions, and front matter prose. They govern authored prose, not executable code, literal identifiers, URLs, or diagnostic output. They do not require retroactive edits to untouched articles.

This file owns person, sentence shape, word choice, and banned language. [Structure](structure.md) owns blog organization and presentation; it cannot relax these rules. The examples below demonstrate edits, not facts about the author or phrases to copy into unrelated articles. Requirements take precedence over examples.

## Put People in the Writing

Write as a helpful expert peer. The author is present as `I`, and actions have identifiable actors. Use `we` only for an explicitly identified group or a clearly shared action with the reader. An institutional `we` requires a named, relevant institution; do not import an Institute persona into this personal blog or use a vague industry-wide `we`.

Use first person for the author's supplied observations, honestly framed preferences, and supported work. Never invent experience, access, metrics, or results to make prose personal. Claims about technical work, outcomes, or professional experience need public or inspectable support. Never mention or imply the author's employer, internal tooling, or proprietary processes.

Prefer "We make sure every change runs the validator" to "Every change runs the validator" when the author really belongs to the responsible group. Otherwise name the actual actor. Apply this to headings too: "What we are shipping today", not "What ships today".

A paragraph with no person in it is a warning sign of detached prose. Reconnect it to what someone does, observes, or decides. Do not insert an empty "I think" or fabricate involvement to satisfy a pronoun quota. A technical explanation can name a concrete system as the actor when it actually performs the operation, such as "The agent matches the description against the task".

Avoid definitions with no actor, such as "X is the unit that..." or "X serves as...". Explain what someone does with X. Avoid making abstractions act: replace "Fleet scale shifts remediation" with "When we manage more machines, we change how we fix them", provided that `we` has an honest referent.

## Build Readable Sentences

- Keep the normal subject, verb, object order. Each clause carries 1 thought. Chain related plain clauses with "and", "so", "but", "as", or "because"; do not fuse unrelated thoughts.
- Use at most 1 subordinate clause per sentence. Do not stack relative clauses or modifiers. Split a sentence if the reader must reread it to find who does what.
- Do not chop 1 thought into consecutive declarative fragments. Fold a restatement into its parent sentence or delete it. Short sentences are fine when each adds a complete plain thought; punchy contrast pairs get no exception from the banned constructions.
- Vary sentence length through the thought itself, not a mechanical rhythm. Do not repair choppy prose by adding filler or joining every sentence.
- Avoid comma splices. A period, a conjunction, or an occasional colon can express the relationship. Do not make colons a repeated rhetorical template.
- Prefer active voice. Use passive voice only when the actor is unknown or genuinely irrelevant; do not invent an actor.
- Keep noun phrases easy to parse. Unpack stacked modifiers and correct category errors, but retain precise, familiar technical terms.
- Give every "it" and "this" an unambiguous, nearby antecedent. Name the subject when a pronoun would make the reader guess.
- Remove accidental echoes without substituting obscure synonyms. Repeat a technical term when that is clearer than a pronoun or a new label.
- Vary paragraph openers. Consecutive paragraphs must not begin with the same rhetorical shape, even if each opener would pass on its own.

## Make Each Point Once

Every sentence must add knowledge, motive, a necessary relationship, or a concrete example. Delete sentences that merely emphasize, label, or restate a point. New words must do useful work.

- Do not follow prose with a bullet list that repeats its benefits.
- Do not append an obvious justification to a stated practice. State the practice and stop. Retain a reason only when it adds a non-obvious motive or explains a decision the reader needs to understand.
- Use 1 useful example or consequence where several merely illustrate the same point. Keep additional examples only when they establish distinct behavior, boundaries, or evidence. Do not assemble 3 items for rhythm.
- Delete paragraphs whose only job is a reaction, such as "Huge if true!" or "This one is a genuinely new kind of model!". Open a section with what happened. A reaction belongs with the news only when it adds a specific, grounded judgment.
- Cut trailing amplifiers such as "without being rewritten for either" or "and the risk goes away" when they only repeat the claim. State any distinct, supported compatibility or risk finding directly.
- Do not add a closing sentence that repeats the section's point or a transition that merely announces the next section.
- Keep reasoning, limitations, and necessary context. Compression must not make the reader reconstruct the argument from links.

## Use Familiar Words

Use plain English that non-native speakers can follow. Prefer common words over decorative verbs: "disappears", not "evaporates". Minimize decorative adjectives and adverbs, not useful qualification.

Use contractions naturally: "wasn't", "it's", "I've". Ordinary colloquialisms such as "just", "a bunch of", "pretty much", "nowadays", and "organically" belong in this voice when they express attitude, approximation, or how something happened. Do not remove them merely to sound formal, or sprinkle them in to simulate personality. Avoid obscure idioms and culture-dependent jokes.

Write numbers as digits: `600`, `5 skills`, `3 plugins`. Preserve the spelling of an exact quotation, title, product name, or literal code value.

Spell out abbreviations and explain terms of art on first use, for example "identity and access management (IAM)". Do not let insider vocabulary carry unexplained meaning.

Ground claims in the author's supplied experience or a named source. Attribute estimates and claims: "OpenAI estimates" or "they claim" with a clear antecedent. Inline parenthetical examples and "etc" are welcome when they keep an explanation readable; they must not obscure a material boundary. Preserve real uncertainty. Avoid empty rhetorical hedges such as "arguably", "it could be said", and "some might say".

Use ASCII punctuation in authored prose: straight quotes and apostrophes, ordinary hyphens in compounds, and periods, colons, or parentheses for asides. No em-dashes, en-dashes, or hyphen-delimited parenthetical remarks. This is a punctuation rule, not a ban on correctly spelled non-English names. Preserve exact source quotations and literal technical text; do not silently alter a quote to pass a style check.

## Banned Constructions

These rhetorical constructions are prohibited in authored prose. A genuine source quotation may contain them; do not use quotations to sneak them into the author's voice.

- Negative parallelisms and staged misconception corrections: "It's not X. It's Y.", "Not just X, but Y", "the real X is", "is less X, and more Y", or "X rather than Y" used as a correction. State the finding directly. Ordinary factual negation and necessary comparisons are allowed.
- Stock framings: "is quietly ...", "Delving into", "At its core", "it rarely survives", and "this is another strong signal that ... moving from ... into ...".
- Aphorism pull quotes, mic-drop one-line closers, chiasmus, and inversion snaps.
- Runs of symmetric bolded-lead bullets, such as "**Portable, not captive.** ... **Reviewable as text.** ...".
- Trailing `-ing` commentary clauses, such as "highlighting the importance of X". This does not ban ordinary verbs ending in `-ing`.
- Copula avoidance: "serves as", "stands as", "functions as", or "marks" used to avoid "is". Use "is" when a direct statement is appropriate; use an actor-led explanation when describing someone's use of a thing.
- Metaphor equations, such as "Context is the budget, and the skill spends it". State the technical fact plainly.
- A follow-up sentence that labels the previous one: "This is progressive disclosure." Introduce the term within the explanation, for example "We use progressive disclosure to show the summary first".
- Gerund equations of the form "X is Y, and doing-Z means W". Replace "A script does one thing, and extending it means reopening it" with a plain account of what someone changes.
- Abstract throat-clearing openers, such as "Being precise about how to write one is important nowadays because...". Open with the point itself.
- Symmetric wrap-up clauses tacked onto finished sentences, such as "so each side does the job the other is bad at".
- The rule of 3 as a reflex, and vague attribution such as "experts argue" without a named source.
- Fronted-clause comma pivots as topic sentences: "Where X wins, it wins on..." or "When Y fails, it fails because...". State the finding as a plain declarative. An ordinary fronted clause can appear elsewhere; do not repeat it as the opener of consecutive paragraphs.
- Any rhetorical shape repeated at the start of consecutive paragraphs, including repeated bolded leads.
- A summary sentence that restates its heading; "In this article the authors"; "In this article, we will..." and similar meta-narration.

## Banned Words

Do not use these words or phrases unless quoting a source, a title, or a product name:

> testament, underscore, propel, unwavering, heartfelt, embrace, foster, ignite, empower, amplify, catalyst, leverage, epitome, cornerstone, noteworthy, unprecedented, profound, pivotal, journey, delve, crucial, tapestry, showcase, vibrant, groundbreaking, revolutionary, game-changing, diverse array, failure modes, moreover, furthermore

Use plain alternatives that fit the claim: "shows", "indicates", "supports", "argues", "use". Write "common failures" instead of "failure modes" in authored prose.

"Seamless", "landscape", and "robust" must remain rare, never habitual. Use a more specific description when possible; retain one only when its literal meaning is needed.

"Harness" is allowed only as a noun for a technical object, such as "agent harness" or "the harness they use". The verb, including "harness the power of", is banned.

## Calibration Pairs

The revised examples below resolve conflicts in the supplied calibration: numbers use digits, the abstract opener is removed, and clauses follow the sentence rules. First-person examples are usable only when the author supplies or supports the underlying experience.

1. Avoid: "Not as a decision; it just happened."
   Prefer: "I didn't make an explicit decision; it just happened organically."
2. Avoid: "Ask an agent to write you a skill and it will hand back something impressive and wrong."
   Prefer: "Whenever I blindly delegate skill writing to an agent, I end up with a bunch of AI slop. The agent gives me a menu of suggestions, and I still have to write the actual recipe."
3. Avoid: "Which makes it worth being precise about how to write one, because the default is bad."
   Prefer, if this adds a distinct practice after the previous example: "I now spell out the steps the agent should follow."
   Otherwise delete it; neither the original nor "Being precise about how to write one is important nowadays..." adds a point.
4. Avoid: "Every change runs scripts/validate.sh in CI."
   Prefer, for a responsible named team: "We make sure every change runs scripts/validate.sh in continuous integration (CI)."
5. Avoid: "Five skills across three plugins. Each of them is a tool we use."
   Prefer: "We use each of the 5 skills in our day-to-day work, and we're shipping them in 3 plugins."
6. Avoid: "A skill writes that same capability down as a folder with a SKILL.md at its root, which holds a short description the agent matches against the task in front of it and the procedure it should follow once it matches."
   Prefer: "We package the skill in a folder with a SKILL.md file at its root. We put a short description and a procedure in that file. The agent matches the description against the task, and once it finds a match, it follows the procedure."

## Enforcement

Review every rule above manually when drafting or editing. Search can catch banned vocabulary and punctuation, but it cannot establish provenance, readability, or whether a rhetorical construction is present. Inspect matches in context; source quotations and literal technical text have legitimate exceptions.

This Hugo repository does not currently provide `scripts/verify/check-voice.sh`, `npm run check:voice`, or the blog/newsletter lint CI described in the supplied guide. Do not claim those checks ran. The source guide's `src/content/blog`, `src/content/newsletter`, 2026-08-29 cutoff, and issue-402 boundary do not apply here. Apply these rules to the prose in the current assignment without expanding the task into an archive rewrite.

A Hugo build checks rendering, not voice. The required editorial review remains necessary even when the build passes.
