# Design Alignment Log

Use this document to keep project design choices explainable. It should help a
new contributor, maintainer, or agent understand the principles guiding
the project, the systems and processes used to build it, and how those choices
support the principles.

## Guiding Principles

| Principle ID | Principle | Why It Matters | Evidence / Signals |
| --- | --- | --- | --- |
| DP-001 | <short principle> | <project value, user value, or constraint> | <observable signals, tests, docs, or examples> |

## System, Element, And Process Map

| Entry ID | Type | Name | Used For | Reinforces Principles | Plain-Language Explanation |
| --- | --- | --- | --- | --- | --- |
| DAL-001 | <System, Element, Process, Tool, Pattern, Library> | <name> | <purpose in this project> | <DP-001, DP-002, or N/A> | <plain-language explanation of why this belongs here> |

## Request Updates

| Date | Request ID | What Changed | Alignment Impact | Follow-Up |
| --- | --- | --- | --- | --- |
| <YYYY-MM-DD> | <request_id> | <new or changed design-relevant choice> | <how the change supports, weakens, or revises principles> | <request_id, decision_id, or N/A> |

## Teaching Notes

- Core mental model: <one-paragraph explanation of how the project is put together>
- Useful entry points: <files, commands, diagrams, examples, or N/A>
- Common misconceptions: <things a reader may misunderstand and the correction>
- Open design questions: <unresolved tensions, tradeoffs, or N/A>

## Maintenance Rules

- Update this log when a request adds, removes, or changes a design principle.
- Update this log when a request introduces a meaningful system, element,
  process, library, pattern, or workflow.
- Link request IDs and decision IDs instead of relying on titles alone.
- Prefer plain language over insider shorthand. The goal is to make the project
  inspectable, not merely documented.
