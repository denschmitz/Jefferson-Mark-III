# Jefferson Mark III

Repository for a constitutional charter that proposes a different model of governance: modular instead of centralized, consent-based instead of permanently delegated, and explicitly designed to make power narrower, more reviewable, and harder to entrench.

The Charter starts from a simple premise: people should be able to coordinate at scale without handing permanent blank-check authority to institutions that inevitably drift, sprawl, and concentrate power. It is meant to be practical, not utopian. Authorities can be created, but only for bounded functions. Representation can scale, but only with caps and diminishing influence. Rights remain binding across the whole system.

## Why It Is Interesting

This Charter tries to solve familiar political problems with structural design instead of good intentions alone.

- It reduces gerrymandering pressure by centering representation on delegable tokens and functional authority rather than fixed winner-take-all territorial districts.
- It pushes back on political monopolies by capping concentrated representation and treating coordinated coalitions as a single actor when appropriate.
- It limits bureaucratic sprawl by requiring bounded scope, periodic review, renewal, and consolidation audits.
- It handles emergencies without normalizing indefinite exceptional power by using hard time limits, public logging, and judicial review.
- It makes narrow majorities possible but less durable by tying the lifespan of laws to the size of their support.

## A Few Distinctive Features

- Authorities have sealed scope. They cannot just keep expanding because they exist.
- Coercive powers require a much higher approval threshold than non-coercive functions.
- Sortition is used throughout the system for courts, assemblies, oversight bodies, and temporary councils.
- Representation is delegable and reversible, but not instantly gameable.
- The system separates coordination, adjudication, and enforcement instead of letting them collapse into one center.

## What This Repo Contains

The canonical Charter lives in [charter/charter.md](/C:/Data/dev/Jefferson-Mark-III/charter/charter.md). The rest of the repository exists to make the Charter easier to study, critique, explain, and simulate.

## Structure

```text
jefferson-mark-iii/
├── README.md
├── LICENSE
├── charter/
│   ├── charter.md
│   ├── charter.pdf
│   └── versioning.md
├── derivatives/
│   ├── simulation/
│   │   ├── charter_sim.yaml
│   │   ├── schema.md
│   │   └── examples/
│   └── explainers/
│       ├── plain_language.md
│       ├── deep_explainer.md
│       └── faq.md
├── annotations/
│   └── annotated_charter.md
└── governance/
    ├── contribution_guidelines.md
    └── change_proposal_template.md
```

## Purpose

- `charter/` holds the canonical charter and its formal version history.
- `derivatives/` holds adapted formats for simulation, education, and external communication.
- `annotations/` holds rationale and commentary tied to the charter text.
- `governance/` defines how the repository evolves.
