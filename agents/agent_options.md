# Getting an AI coding agent

*[Page created using Claude by Professor Reynolds]*

For the next several projects, we have an opportunity to build with an **AI coding agent**: a tool that
reads files, runs commands in a terminal, writes and fixes code, and can explain what it's doing along the
way. That's different from a chatbot you paste code into. Examples include Claude Code, OpenAI Codex, GitHub
Copilot agent mode and Google Antigravity.

**Monday's class (10/12) is set aside for this.** Bring your laptop. We'll spend the time asking questions,
comparing options, deciding, and getting into an agent coding environment together. The hope is that
everyone leaves Monday set up for success with agent coding, with access to more than a trivial number of
tokens.

*Prices and free limits change often. This was gathered in October 2026; if you find something that has
changed, please share it so the page can be updated for everyone.*

## Professor Reynolds' recommendation: Claude Pro ($20/month)

- **Claude Pro** is $20/month ($17/month billed yearly) and includes **Claude Code** (terminal, VS Code
  extension and desktop app). This is what Professor Reynolds uses every day.
- Sign up at [claude.ai](https://claude.ai), then install Claude Code from
  [claude.com/claude-code](https://claude.com/claude-code).

## Recommended free option: OpenAI Codex (+ $100 in student credits)

- **Codex** works with a **free ChatGPT account** (CLI, VS Code extension and web). The free allowance is
  small and resets every few hours, with a weekly cap.
- **Codex for Students:** verified university students in the US and Canada can claim **$100 in Codex
  credits** (2,500 credits), verified through SheerID with a BYU email. Search "Codex for Students" on
  openai.com, or see OpenAI's help article on Codex credits for students. One claim per student.
- **BYU's ChatGPT Edu license:** BYU's pages currently describe ChatGPT Edu for faculty and staff, and access
  for students may be rolling out (possibly to student employees first). It's worth trying: sign in at
  [chatgpt.com](https://chatgpt.com) with your BYU email and look for the BYU / Church Educational System
  workspace. If it works for you, please share how, so classmates can benefit.
- Paid ChatGPT plans raise the Codex limits: Go ($8/month) and Plus ($20/month).

## Other free options

| Tool | Free for students? | Notes |
|---|---|---|
| **GitHub Copilot Student** | Yes, with GitHub Education verification | Agent mode in VS Code, plus a coding agent that works on GitHub issues. 200 AI credits a month; the model is chosen automatically. Apply at [github.com/education/students](https://github.com/education/students). Verification can take a few days, so applying early helps. |
| **Google Antigravity** | Free individual tier (any Gmail account) | Agent-first editor with a weekly agent quota. (Gemini CLI no longer serves free personal accounts.) |
| **Cursor** (Hobby) | Free tier | Polished editor with an agent; the free tier runs out quickly with heavy use. |
| **Cline / OpenCode** | Free, open source | Bring your own model or API key. The cost depends on the model provider; some models are inexpensive or free. |

Free tiers can run out partway through a project. Some students find it helps to start projects early in
the week, or to set up two tools (say Codex + Copilot) so hitting one limit doesn't stop progress.

## Paid options

| Plan | Price |
|---|---|
| Claude Pro (Professor Reynolds' first recommendation) | $20/month ($17 billed yearly) |
| Claude Max | $100 or $200/month |
| ChatGPT Go / Plus | $8 / $20 per month |
| ChatGPT Pro | from $100/month |
| GitHub Copilot Pro | $10/month |
| Cursor Pro | $20/month |

If the free options don't work for you, or you've already used up a free trial, one of these may be the
way to go.

## A note on secrets

Giving an agent access to secrets (API keys, database passwords, tokens) can speed up what it's able to
create and build for you. Handling secrets well is also a skill worth growing, and your agent can teach you
about ways to handle them safely.

A useful question to ask about any secret: *what could someone do with this?* And then: *how can I make sure
it doesn't reach someone who shouldn't have the access it gives?*

Some common practices worth exploring:

- Keeping keys in a `.env` file (listed in `.gitignore`) or a secret manager, rather than in source code.
- What happens when a key gets committed to git, and why rotating the key is the usual response.
- What files and commands your agent can see, and what its permission prompts are asking you to approve.
- Why some services offer both a public key and a secret key (for example, Supabase's anon key vs. its
  service-role key), and which one belongs in a web page.

Try asking your agent about any of these. Learning by practicing, and discovering what works for you, is
the point.
