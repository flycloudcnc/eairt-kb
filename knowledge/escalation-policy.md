# Escalation policy (shared)

Reachable at `knowledge://system/escalation-policy.md` by every tenant.

Section 10 gives `knowledge://` two roots - `system` and `tenant/current` -
and only one of them is resolved against the execution context. A namespace
with a single root would make "the backend translates this using the trusted
context" true of everything by accident rather than by design, and there would
be nothing to assert the tenant resolution against.

## Contents

A run that cannot obtain the evidence its task contract requires escalates
rather than answering from what it has. A run that needs a capability its
envelope does not carry is suspended for a human, and does not negotiate.
