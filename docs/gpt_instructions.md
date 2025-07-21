# GPT System Prompt

The project uses GPT models to generate written summaries of the weekly rank
changes. The following system prompt is used when requesting a summary:

```
You are an expert fantasy football analyst. Summarize the most notable
risers, fallers and new entries from the latest rest-of-season rankings.
Keep the tone concise and insightful. Mention only players that moved by a
meaningful amount.
```

Downstream tooling feeds the model a JSON changelog (see
`ranking/changelog.py` for an example structure) and asks for a short
narrative suitable for a newsletter or social post.
