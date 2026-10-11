# Guide to use the MikroTik shell

## CRITICAL RULES — MUST FOLLOW EVERY TIME, NO EXCEPTIONS

### Rule 1: NEVER retry a command that already ran
- The MikroTik shell returns **"Succeed"** when RouterOS successfully executes a command. `Succeed` = success. DO NOT retry after seeing it.
- If a command like `/ip firewall filter add ...` was already called in this session (even if it appeared to not go through), you MUST verify with `print` first before running it again.
- **NEVER call the same command twice.** If the tool warns you about repeated calls, STOP. Do not try variations of the same command. Verify state with `print` instead.

### Rule 2: ALWAYS check existing rules before adding anything
- Before ANY `add` command, run the relevant `print` command first.
- Read the output carefully. If a matching rule already exists, DO NOT add it again.
- Consider how your new rule will interact with existing rules (order matters in MikroTik firewall chains).

### Rule 3: One command at a time, verify after
- After adding a rule, run `print` once to confirm it was applied.
- Do not add multiple rules in a row without verifying each one.
