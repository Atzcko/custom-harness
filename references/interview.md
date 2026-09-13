# Interview question bank

Pick, do not recite. Three or four questions per batch. Record answers in
`harness/brief.md` with the date. Questions marked **must** are the ones the
architect cannot work without.

## Purpose and outcome

- In one paragraph, what is this project for and who is it for?
- What does success look like in three months? What would make you stop?
- **must** What is "done" for the project, and what is "done" for a typical
  task? (Tests pass? Reviewed? Flashed and verified on hardware? Published?)

## People

- Who else touches this? Who reviews, who approves, who is affected?
- How do you want to be talked to: short and direct, or with reasoning shown?
- How often do you want to be pulled in? Only for decisions, or for every
  milestone?

## Delegation

- Which kinds of work do you want to hand off entirely?
- Which do you want to keep doing yourself, or at least see before it lands?
- Is there work you have handed off before that came back wrong? What was
  wrong about it?

## Risk and approvals

- **must** What must never happen without you? Deploys, pushes, releases,
  payments, sending messages, deleting data, touching production, flashing
  hardware. Name each one.
- What is expensive to undo in this project?
- Are there secrets, credentials or private data an agent might stumble on?
  Where do they live so agents can be told to stay out?

## Constraints

- Technical constraints that look arbitrary but are not (pinned versions,
  banned libraries, hardware limits).
- Budget: is there a token or cost ceiling per day or per task?
- Time: deadlines, cadences, quiet hours.

## Knowledge

- Where does the truth live when documents disagree: code, a spec, a person?
- Which external sources should the wiki ingest (docs, papers, standards)?
- Which past decisions do you want every agent to know before they start?

## For an empty project

- What will exist in the repository first?
- Which domains do you already know it will have?
- Is there a reference project this should resemble?
