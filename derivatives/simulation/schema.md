# Simulation Schema

This document explains the machine-readable representation in `charter_sim.yaml`. The YAML is a derivative of `charter/charter.md`, not an independent source of authority.

## Modeling Approach

The Charter is not a single-branch state model. It is a modular constitutional order with Subscribers, Representatives, Authorities, courts, sortition-based oversight bodies, emergency coordination, and temporal rules. The schema therefore separates:

- constitutional actors;
- Authority formation and scope;
- lawmaking and duration;
- delegation and representation constraints;
- emergency rules;
- rights constraints;
- review, renewal, and consolidation processes.

## Top-Level Fields

### `meta`

Administrative metadata for the derivative.

- `title`: Human-readable label for the derivative model.
- `version`: Version of the simulation derivative.
- `source`: Canonical source file.
- `charter_version`: Version stated in the Charter text.
- `status`: Draft, review, adopted, or ratified state for the derivative artifact.

### `polity`

Defines the governed system at the highest level.

- `sovereign_body`: The group in which sovereignty resides.
- `membership_unit`: The base political unit, here the Subscriber.
- `representation_unit`: The delegable token held by each Subscriber.
- `national_decision_threshold`: Default national approval threshold unless otherwise overridden.

### `actors`

Defines recurring actor types used throughout the model.

Expected actor categories include:

- Subscribers
- Representatives
- Authorities
- Charter Court
- ECO
- CAES
- temporary councils, assemblies, juries, and oversight bodies

### `authority_rules`

Encodes how Authorities are created, bounded, reviewed, renewed, and dissolved.

- `formation_thresholds`: Approval levels by Authority type.
- `scope_rules`: Rules for sealed scope, non-enumerated power, and invalid out-of-scope acts.
- `renewal`: Five-year review and majority renewal logic.
- `dissolution_and_merger`: References to Authority Charter procedures plus consolidation mechanisms.

### `legislation`

Represents ordinary lawmaking.

- `default_pass_threshold`: Usually simple majority.
- `duration_bands`: Mapping from approval levels to law duration.
- `conflict_resolution`: Harmonization and territorial fallback rules.

### `emergency`

Represents Article V mechanics.

- `qualifying_conditions`: Conditions that count as emergencies.
- `lead_authority_rules`: Who may act first and for how long.
- `extension_rules`: Approval requirements for extended emergencies.
- `provisional_activation`: Short immediate-response pathway.
- `review_constraints`: Court review and rights checks.

### `representation`

Represents delegation, weighting, caps, and stabilization.

- `delegation_delay_days`: Delay before a new delegation activates.
- `weighting_function`: Formula plus interpretive notes.
- `change_frequency_limit`: Maximum changes per period.
- `cap_rules`: Representative concentration limits.
- `stabilization_rules`: Automatic delay and anti-manipulation logic.

### `petitions`

Represents petition origination and deliberative assembly workflow.

- `support_threshold`: Threshold for advancing a petition.
- `assembly_selection`: Random selection design.
- `cooling_period_days`: Delay before legislative consideration.
- `temporary_authority_rule`: Creates a temporary Authority when no existing Authority has scope.

### `rights`

Represents both baseline and unalienable rights as constraints on Authority action.

- `baseline_rights`: Participation, due process, transparency, and anti-compulsion protections.
- `unalienable_rights`: Bodily autonomy, conscience, privacy, and anti-coercion protections.
- `civil_and_procedural_rights`: Redress, participation, assembly, and movement.

### `judiciary`

Represents judicial interpretation and execution of judicial outcomes.

- `charter_court`: Composition, powers, and voting rules.
- `authority_courts`: Internal courts plus appeal conditions.
- `caes`: Court-order execution constraints.
- `clemency`: Emergency stays and clemency procedures.

### `coordination_and_defense`

Represents ECO and the Defense Authority.

- `eco`: Cross-Authority logistical and informational coordination.
- `defense_authority`: External defense, intelligence, oversight, and domestic limits.

### `treasury`

Represents fiscal administration.

- `treasury_authority`: Role and limitations.
- `tax_categories`: Permitted tax families.
- `prohibited_taxation`: Forbidden tax forms.
- `distribution_rules`: Transfers to Authorities and individuals.
- `transparency_and_audit`: Ledger and audit rules.

### `supremacy_and_transition`

Represents constitutional supremacy, adoption, and temporary transition rules.

- `supremacy_rule`: Contradictory lower law is void.
- `adoption_rule`: National Decision requirement.
- `transition_rules`: Initial Subscriber, ACB, Qualified Person, and Authority bootstrapping logic.

## Mapping Guidance

- The Charter remains the only canonical source.
- If the Charter and YAML diverge, correct the YAML.
- Preserve ambiguity when the Charter itself is ambiguous; do not invent constitutional certainty in the derivative.
- Record substantive simulation-derivative changes in `charter/versioning.md`.
