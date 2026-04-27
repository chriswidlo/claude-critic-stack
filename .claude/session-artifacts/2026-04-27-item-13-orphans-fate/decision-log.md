# decision-log.md — item 13 (orphans fate)

Step 10 verdict was architecture = rework, operations = rework, product = rework (3-of-3 minority-veto); rewrite; routed to step 9 with frame correction "implicit primitive vs. explicit primitive."

Triggers for the rewrite:
- Architecture: name the new primitive explicitly; audit the O3 rename's inbound link graph; justify the CLAUDE.md amendment on its own merits or drop it.
- Operations: sequence rename → observe → deletes (not atomic); CLAUDE.md amendment as separate commit with rollback criterion; replace 6-month memory-falsifier with a memory-independent trigger.
- Product: drop or session-isolate the CLAUDE.md amendment (no bait-and-switch); make empty `prompts/` self-explanatory (delete the dir or add a one-line README); name a concrete mechanism for the falsifier.

Loop counter: 1 of 2 permitted.

Step 10 verdict (loop 2) was architecture = approve, operations = approve, product = approve (3-of-3 minority-veto cleared); proceed to step 12 (synthesis). Loop counter: 2 of 2 permitted.
