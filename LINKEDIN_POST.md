Safe to Send · Ep 19 — Insights that never leave your laptop

The fastest way to kill an AI tool in a marketing team: ask people to upload customer data to use it.

So this repo analyses campaign results locally, and proves it. The whole analysis runs inside a guard that makes any network connection or DNS lookup throw an error, even from a library it imports. A test checks that on every push.

On a synthetic Black Friday results file across 8 markets, it flagged exactly one thing:

Greece. Open rate normal. Click rate normal. Unsubscribe rate 0.95%, against 0.14% for everyone else.

A dashboard sorted by opens would have buried it, because it sits mid-table on every engagement metric. A spike like that usually points at the send itself: a late hour, a wrong price format, the wrong audience.

Local-first isn't a feature you claim in a slide. It's one you can test.

Repo: https://github.com/sghatge/safe-to-send-19-local-first-insights

#SafeToSend #DataPrivacy #MarTech #Analytics
