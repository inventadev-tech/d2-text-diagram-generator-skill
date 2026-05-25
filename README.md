# D2 Text Diagram Generator Skill

Skill for AI coding agents and development chats to generate D2 diagrams and render them as Unicode text.

The agent generates a D2 diagram after big code changes or while explaining code flow, then a wrapper script renders text output that fits directly in a chat answer.

## Preview

These examples were rendered with the skill.

### C4 Container Diagram

From `examples/c4-container.d2`, an invented hiking trip planner app named TrailKit:

```text
                           ┌─────────┐
                           │Traveler │
                           │         │
                           └─────────┘
                                 │
                            plans hikes
                                 │
                                 ▼
                       ┌─────────────────────┐
                       │Trip Planner Web App │
                       │                     │
                       └─────────────────────┘
                            │         ▲
                            │         │
                            │ returns itinerary
                       HTTPS JSON     │
                            │         │
                            ▼         │
                       ┌───────────────────┐
                       │   TrailKit API    │
                       │                   │
                       └───────────────────┘
                           │   │   │   │
         ┌─────────────────┘   │   │   └────────────┐
         │                     │   │                │
         │                ┌────┘   └────┐           │
         │                │             │           │
      trails              │             │        invites
         │                │             │           │
         │            forecast        trips         │
         │                │             │           │
         ▼                ▼             ▼           ▼
 ┌────────────────┐┌────────────┐  ┌─────────┐ ┌────────┐
 │Catalog Service ││Weather API │  │Trips DB │ │ Email  │
 │                ││            │  │         │ │        │
 └────────────────┘└────────────┘  └─────────┘ └────────┘
```

### Component Diagram

From `examples/component-diagram.d2`, the inside of the TrailKit API trip creation flow:

```text
     ┌───────────┐
     │Controller │
     │           │
     └───────────┘
           │
    checks session
           │
           ▼
       ┌───────┐
       │ Auth  │
       │       │
       └───────┘
           │
    allows request
           │
           ▼
     ┌──────────┐
     │Validator │
     │          │
     └──────────┘
           │
   valid trip draft
           │
           ▼
      ┌────────┐
      │Planner │
      │        │
      └────────┘
           │
     loads trails
           │
           ▼
   ┌───────────────┐
   │Catalog Client │
   │               │
   └───────────────┘
           │
   enriches forecast
           │
           ▼
   ┌────────────────┐
   │Forecast Client │
   │                │
   └────────────────┘
           │
   stores itinerary
           │
           ▼
     ┌───────────┐
     │Repository │
     │           │
     └───────────┘
           │
publishes trip.created
           │
           ▼
   ┌────────────────┐
   │Event Publisher │
   │                │
   └────────────────┘
```

### Code Diagram

From `examples/code-diagram.d2`, a small service-level code dependency diagram:

```text
                  ┌──────────┐
                  │TripDraft │
                  │          │
                  └──────────┘
                        │
                      input
                        │
                        ▼
                  ┌──────────┐
                  │ Planner  │
                  │          │
                  └──────────┘
                     │  │  │
        ┌─find trails┘  │  └───creates───┐
        │               │                │
        │         score weather          │
        │               │                │
        ▼               ▼                ▼
 ┌─────────────┐ ┌─────────────┐ ┌───────────────┐
 │Catalog port │ │Weather port │ │Trip aggregate │
 │             │ │             │ │               │
 └─────────────┘ └─────────────┘ └───────────────┘
                                      │        │
                                    save     emits
                                      │        │
                                      ▼        ▼
                            ┌───────────┐  ┌────────┐
                            │Repository │  │ Event  │
                            │           │  │        │
                            └───────────┘  └────────┘
```

### OAuth2 On-Behalf-Of Sequence

From `examples/oauth2-obo-sequence.d2`, a sequence diagram for OAuth2 authentication with an on-behalf-of token exchange:

```text
 ┌─────────┐    ┌──────────┐    ┌────────┐     ┌────────┐     ┌──────────┐
 │  User   │    │ Web SPA  │    │  API   │     │  IdP   │     │Graph API │
 │         │    │          │    │        │     │        │     │          │
 └─────────┘    └──────────┘    └────────┘     └────────┘     └──────────┘
      │               │              │               │              │
      │───Open app───▶│              │               │              │
      │               │              │               │              │
      │               │───────────Auth code─────────▶│              │
      │               │              │               │              │
      │               │◀──────────API token──────────│              │
      │               │              │               │              │
      │               │─Bearer token▶│               │              │
      │               │              │               │              │
      │               │              │───Validate───▶│              │
      │               │              │               │              │
      │               │              │──OBO request─▶│              │
      │               │              │               │              │
      │               │              │◀─Graph token──│              │
      │               │              │               │              │
      │               │              │───────────User call─────────▶│
      │               │              │               │              │
      │               │              │◀────────────Data─────────────│
      │               │              │               │              │
      │               │◀────JSON─────│               │              │
      │               │              │               │              │
      │◀──Dashboard───│              │               │              │
      │               │              │               │              │
```

## Installation

Add this skill to your workspace using:

```bash
npx skills add inventadev-tech/skills-flow-diagram/skills/d2-text-diagram-generator
```

The subpath keeps repository-only files, such as `examples/`, `tests/`, and project metadata, out of the installed skill.

## Usage

Render a D2 file to Unicode text:

```powershell
python skills\d2-text-diagram-generator\scripts\d2_unicode_wrapper.py examples\c4-container.d2
```

Render from stdin on PowerShell:

```powershell
Get-Content examples\c4-container.d2 | python skills\d2-text-diagram-generator\scripts\d2_unicode_wrapper.py
```

Render with standard ASCII instead of Unicode box drawing:

```powershell
python skills\d2-text-diagram-generator\scripts\d2_unicode_wrapper.py --ascii-mode standard examples\c4-container.d2
```



## How to collaborate

Run the test suite and syntax check before changing release-facing behavior:

```powershell
uv run pytest
python -m py_compile skills\d2-text-diagram-generator\scripts\d2_unicode_wrapper.py
```

When D2 is installed, also run a manual render:

```powershell
python skills\d2-text-diagram-generator\scripts\d2_unicode_wrapper.py examples\c4-container.d2
```

The wrapper calls the external D2 CLI:

```powershell
d2 input.d2 output.txt
```

D2 must be installed separately and available on `PATH`.


## Structure

```text
skills/
  d2-text-diagram-generator/
    SKILL.md
    scripts/
      d2_unicode_wrapper.py
examples/
  c4-container.d2
  component-diagram.d2
  code-diagram.d2
  oauth2-obo-sequence.d2
tests/
```

