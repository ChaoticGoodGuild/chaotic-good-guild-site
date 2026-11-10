# Alignment test statements (Version 1, draft)

Drafted by Claude for Ryan to review and rewrite in his own words. Edit them in `src/alignment.json`.

Scale: Strongly disagree (-2) / Disagree (-1) / Not sure (+0) / Agree (+1) / Strongly agree (+2)

**Direction** says which way *agreeing* pushes the score.

## Law and chaos

| ID | Statement | Direction |
|---|---|---|
| O01 | I feel calmer when there's a clear plan to follow. | Lawful |
| O02 | I often make it up as I go, and it usually works out. | Chaotic |
| O03 | Rules usually exist for good reasons, even when I can't see them right away. | Lawful |
| O04 | A rule that makes no sense to me isn't one I feel bound to follow. | Chaotic |
| O05 | Traditions are worth keeping, even when they feel old-fashioned. | Lawful |
| O06 | I get restless when every day looks the same. | Chaotic |
| O07 | People in charge usually got there for a reason. | Lawful |
| O08 | Titles and uniforms don't earn my respect on their own. | Chaotic |
| O09 | I'd rather follow a proven method than experiment with a new one. | Lawful |
| O10 | When a plan falls apart, part of me gets a little excited. | Chaotic |
| O11 | Things run best when everyone knows their role. | Lawful |
| O12 | The best ideas come from breaking with how things have always been done. | Chaotic |
| O13 | When a rule is broken, there should be consequences, no exceptions. | Lawful |
| O14 | I'd rather ask forgiveness than permission. | Chaotic |
| O15 | Once I commit to a routine, I stick to it. | Lawful |
| O16 | Schedules are more like suggestions to me. | Chaotic |

## Good and evil

| ID | Statement | Direction |
|---|---|---|
| H01 | It bothers me when someone is treated unfairly, even if it doesn't affect me. | Good |
| H02 | If a deal works out in my favor, it isn't my job to make it fair. | Evil |
| H03 | I help people even when no one will ever know I did. | Good |
| H04 | Looking out for myself comes before looking out for others. | Evil |
| H05 | Everyone deserves kindness, no matter their status. | Good |
| H06 | Some people just aren't worth the trouble of helping. | Evil |
| H07 | I'd rather lose a deal than win it by taking advantage of someone. | Good |
| H08 | Bending the truth is fine if it gets me what I want. | Evil |
| H09 | The well-being of people I'll never meet matters to me. | Good |
| H10 | If someone is careless with their things, it's their own fault if they lose them. | Evil |
| H11 | I go out of my way to make newcomers feel welcome. | Good |
| H12 | Getting ahead sometimes means stepping on a few toes. | Evil |
| H13 | Sharing what I have feels better than keeping it. | Good |
| H14 | Being nice is mostly useful for getting people on your side. | Evil |
| H15 | I'd give up something I want if it meant someone else got what they needed. | Good |
| H16 | Other people's problems aren't mine to lose sleep over. | Evil |

## Scoring

Each axis score is the sum of (answer x direction) divided by the maximum possible, giving -1 to +1.
Scores within 0.25 of zero count as Neutral on that axis. Both axes Neutral = True Neutral.
Agreeing with every statement lands exactly at True Neutral, because each axis has 8 statements keyed each way.
