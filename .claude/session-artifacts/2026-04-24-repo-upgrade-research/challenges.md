## Frame as given
The current frame is "understand this repo, then say how to upgrade it." Read literally, that invites a shopping list of capabilities. Because the repo is an adversarial-review stack rather than a product runtime, that frame risks equating "more advanced" with "more orchestrated."

## Alternative frame
Treat this as a calibration problem: what is the minimum additional machinery that would make this stack more right, more current, and more repeatable? On this frame, sophistication is a cost center that must justify itself with measured gains in review quality, source quality, or regression detection.

## Condition under which the current frame is wrong
The current frame is wrong if the user actually wants this repo to become a multi-user production service; in that case durability, tenancy, auth, and execution guarantees dominate prompt quality.

## Challenges to scope-map preservations (one per preserved primitive, if any)
- `.claude/agents/*.md`: preservation reason was auditability. That reason is weak if the prompts remain markdown-only and unscored, because text that cannot be diffed against behavior becomes ceremonial. The preservation biases the downstream answer toward artisanal prompt craft over measurable control.
- `canon/corpus/` and ingestion scripts: preservation reason was curated evidence. That reason is weak unless coverage, freshness, and contradiction are observable. The preservation biases the downstream answer toward corpus accumulation rather than corpus quality.
- `.claude/session-artifacts/*`: preservation reason was audit surface. That reason is weak if artifacts stay prose-only; prose is readable but hard to compare. The preservation biases the downstream answer toward human inspection over fast regression detection.

## Challenge to the classifier label (if the alternative classification is substantive)
If the user wants changes made in this repo immediately, `extend` becomes the honest primary label. Under that classification the right question is not "what does the research say?" but "which small set of changes gives the highest measured lift per added maintenance surface?" That would make evaluation and instrumentation even more central.

## Frame-level objection the orchestrator should carry forward
Do not mistake "another level" for "more agents"; any recommended complexity must beat better evals, better corpus controls, and better context management on measured outcomes.
