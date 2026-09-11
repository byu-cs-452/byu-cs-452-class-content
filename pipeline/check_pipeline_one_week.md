# Pipeline Check-In — One Week Later

How is your pipeline working? If it failed, when and why did that happen? If it is succeeding how can you prove that there were no gaps?

## Deliverable

**One 30-second video.** No slides, no polish — just you, your dashboard/query results, and a straight answer to the questions below.

## If it's still running 🟢

1. **Fresh data** — run your liveness query or show your dashboard. Roughly how many new records arrived since the demo?
2. **Continuity** — did it run continuously, or are there gaps in the week? If there are gaps (a missed run, an API outage, a quota pause), point at one and explain what happened. A week with zero anomalies is rare — if yours looks perfect, say how you verified that.


## If it's broken 🔴

Congratulations — you now get to do an incident post-mortem, which is a more valuable skill than anything on the green path. Cover:

1. **When did it die?** Use your data to find the time of death — the last successfully ingested record is your first clue.
2. **What was the cause?** Chase it down: expired credential? Quota exhausted? Laptop went to sleep? API changed or went down? Free-tier resource paused itself? Silent exception your job swallowed? "I don't know" is acceptable *only* with evidence of a real investigation — show the logs you checked and where the trail went cold.
3. **What would the fix be?** One sentence. You don't have to implement it — just demonstrate you know what it is. Bonus reflection: would you have caught this earlier with an alert, and what would that alert watch?

## Clean up 🧹

Tear it down! Don't leave something running against public APIs or they won't be free anymore. Nice work!

