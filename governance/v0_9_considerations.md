# Charter v0.9 Considerations

This document lists design issues worth considering for `v0.9`. It is not a rewrite proposal by itself. The aim is to identify places where the current Charter is ambiguous, underspecified, or likely to face stress under real political use.

## Highest-Priority Clarifications

1. Complete the weighting formula in Article VII.
   The current text gives `W = R^0.75` but leaves several mathematical conditions incomplete. Because representation weighting is central to the system's anti-concentration design, this is not a cosmetic issue. The Charter should state the intended domain, normalization rule, and any constraints on aggregation precisely enough for both legal and simulation use.

2. Define how Subscriber approval is measured.
   Several Articles rely on percentages of Subscribers, but the Charter does not yet fully specify denominator rules, quorum rules, abstention handling, eligibility timing, or how approval is counted during periods of rapid membership change. These choices will materially affect legitimacy thresholds.

3. Clarify the relationship between raw delegation, weighted delegation, and voting power.
   The Charter caps both raw and weighted concentration, but it does not fully spell out where each measure controls actual decision outcomes. `v0.9` should make clear when institutions use raw counts, weighted counts, or both.

4. Tighten the definition of National Decision.
   Article XVIII defines National Decision as sixty percent of all Subscribers unless otherwise specified, but the mechanics of how that is reached remain thin. `v0.9` should define whether this means all registered Subscribers, all active Subscribers, or all eligible Subscribers at a fixed snapshot date.

## Institutional Design Questions

5. Specify how Authorities are initially proposed, debated, and voted into existence.
   The Charter sets approval thresholds, but not the full lifecycle for Authority creation. A clearer formation pipeline would reduce contestation over who drafts first-stage Authority Charters and how rival proposals compete.

6. Clarify what counts as a coercive Authority.
   The 75% threshold is important, but the boundary between coercive and non-coercive functions may become politically contested. `v0.9` should add criteria or a classification procedure.

7. Define the mechanics of sealed scope more concretely.
   "Sealed scope" is a strong concept, but scope boundaries are likely to be the system's main site of conflict. The Charter would benefit from more explicit tests for implied powers, incidental powers, and overlap handling before disputes reach the Charter Court.

8. Clarify how Temporary Authorities are governed.
   Article IX allows Temporary Authorities when no existing Authority claims scope over a Draft Act. `v0.9` should specify how these bodies are staffed, limited, funded, reviewed, and dissolved, because they could otherwise become a loophole around the normal formation process.

9. Revisit the governance credit limit.
   One Authority per fifty-thousand Subscribers is a strong anti-sprawl rule, but it may be too rigid across very different functional environments. `v0.9` should consider whether this remains a constitutional rule, becomes a presumptive default, or gets tied to a more nuanced capacity metric.

10. Define "satisfaction rating" institutionally.
   Mandatory reauthorization review below forty percent for twelve months is meaningful only if satisfaction is measured by a trusted and constitutionally specified process. `v0.9` should define source, sampling method, cadence, and anti-gaming safeguards.

## Representation And Anti-Capture

11. Reconsider the two-changes-per-year delegation rule.
   The current limit stabilizes the system, but it may also trap Subscribers with failing or abusive Representatives for too long. `v0.9` could consider emergency exceptions, fraud carve-outs, or special release mechanisms.

12. Clarify how fractional delegation works in practice.
   Fractional delegation is permitted, but the Charter does not specify granularity, rounding, minimum units, or whether fractions may be split across many Representatives. These details matter for usability and concentration effects.

13. Define coalition detection standards more concretely.
   The consolidated-persona rule is important but potentially contentious. `v0.9` should specify evidentiary standards, burdens of proof, and whether coordinated behavior alone is enough to aggregate actors.

14. Examine whether the one-percent cap is too low, too high, or scale-dependent.
   The cap is a major anti-oligarchy feature, but its effect will vary dramatically across population size and political culture. `v0.9` should test whether it creates healthy pluralism or excessive fragmentation.

15. Clarify the stabilization trigger's operational logic.
   The Charter delays delegation shifts if more than five percent of tokens are scheduled to activate within fourteen days. `v0.9` should define whether rolling extensions can cascade indefinitely and what happens when multiple windows overlap.

## Legislative Process And Agenda Formation

16. Specify more of the legislative pipeline.
   The Charter says Acts pass by simple majority and ties duration to approval levels, but it says less about introduction, amendment, committee-like review, publication timing, and reconciliation of competing drafts.

17. Reconsider petition thresholds.
   The `0.1% or 10,000 supporters` trigger may behave very differently at different scales. `v0.9` should test whether it is too permissive for large polities or too restrictive for small ones.

18. Clarify what the Deliberation Assembly can actually do.
   It evaluates scope, feasibility, and rights compliance, but the text does not fully define whether it may amend proposals, merge proposals, reject on prudential grounds, or only certify them.

19. Define how substantially similar petitions are merged.
   This is a sensible anti-spam rule, but politically sensitive. `v0.9` should specify who decides similarity, under what standard, and whether petition backers can appeal.

20. Consider whether law duration should depend only on approval percentage.
   The current design rewards broad support, which is attractive, but some Acts may need shorter or longer lifespans because of subject matter rather than margin alone. `v0.9` could consider whether some classes of Acts need special duration rules.

## Emergency And Security Design

21. Clarify how a Lead Emergency Authority is recognized when multiple Authorities act at once.
   The ECO recognizes the first Authority with functional jurisdiction, but edge cases are easy to imagine. `v0.9` should define tie-break rules and mistaken-claim procedures.

22. Tighten the boundary between provisional emergency action and ordinary emergency power.
   The seventy-two-hour window is useful, but `v0.9` should define reporting requirements, allowable measures, and remedies for misuse more fully.

23. Revisit emergency extension beyond ninety days.
   Requiring all affected Authorities to approve extensions may be appropriately strict, but it may also create veto deadlock in genuine crises. `v0.9` should test whether there needs to be a structured fallback.

24. Clarify domestic defense edge cases.
   The Defense Authority may not act domestically except under a validated emergency, but boundary cases such as cyber operations, border incidents, and intelligence spillovers may need more explicit treatment.

## Judicial And Oversight Design

25. Define the appointment and removal logic around lot-selected bodies more fully.
   Sortition is a major strength of the Charter, but `v0.9` should specify recusals, disqualifications, vacancies, incapacity rules, and replacement procedures for courts, juries, councils, and boards.

26. Clarify the standard of review used by the Charter Court.
   The Court has broad authority over rights and scope conflicts, but the Charter does not yet specify review tests in much detail. `v0.9` could identify at least a small number of constitutional standards for scope, emergency action, and rights burdens.

27. Revisit the finality of clemency decisions.
   Finality prevents endless relitigation, but procedural-defect-only review may be too narrow if clemency itself becomes politicized or inconsistent. `v0.9` could consider limited substantive review or published decision standards.

28. Clarify how CAES functions when Authorities obstruct passively rather than directly.
   The Charter bars obstruction, but execution design may need more precision around non-cooperation, resource denial, or jurisdictional stalling.

## Rights And Constitutional Theory

29. Clarify the interaction between baseline rights and unalienable rights.
   The two-tier structure is conceptually strong, but `v0.9` should clarify whether the distinction changes remedies, scrutiny, amendability, or emergency exceptions.

30. Define privacy-protected information more operationally.
   The Charter deliberately protects privacy at a high level, but implementation will eventually need clearer handling of metadata, anonymized data, algorithmic inference, and compelled disclosure.

31. Consider adding an explicit anti-retaliation principle.
   The Charter protects participation rights, but `v0.9` could consider a clearer rule against retaliation for petitioning, delegation changes, whistleblowing, or refusal to politically align.

## Fiscal And Administrative Design

32. Expand Article XV from compressed category statements into fuller constitutional rules.
   Treasury design is clearly important, but much of the Article is summarized at a high level. `v0.9` should decide whether to keep this compact style or restore more detailed fiscal language directly in the Charter.

33. Clarify how Authority funding interacts with dissolution, consolidation, and emergency action.
   The current text identifies funding channels and restrictions, but transitional money-flow rules remain thin.

34. Define the operational role of ACBs in greater detail.
   ACB independence is crucial because so many offices rely on Qualified Persons. `v0.9` should specify competition among ACBs, appeals, recertification, discipline, and anti-cartel safeguards.

## Transitional And Adoption Risks

35. Revisit the simplified-majority transitional rule for initial Authorities.
   This helps bootstrapping, but it also creates a path for weakly legitimated institutions to shape the early regime. `v0.9` should consider stronger sunset, narrower scope, or mandatory early reauthorization.

36. Clarify when the transition period truly ends.
   "First full consolidation cycle or ten years" is a useful outer boundary, but `v0.9` should define what counts as a completed first cycle and how unresolved transition disputes are handled.

## Meta-Level Design Question

37. Decide how much of the system belongs in the Charter versus Authority Charters or subordinate Acts.
   The current text mixes high constitutional principles with fairly specific institutional mechanisms. That can be a strength, but it also raises amendment costs. `v0.9` should make a deliberate choice about constitutional granularity instead of inheriting it piecemeal.

## Suggested Prioritization For Drafting

- First-pass `v0.9` candidates:
  weighting formula, Subscriber approval mechanics, National Decision denominator, Temporary Authority rules, coercive Authority test, satisfaction rating measurement, and Article XV expansion.
- Second-pass `v0.9` candidates:
  coalition detection standards, Deliberation Assembly powers, emergency extension fallback, Charter Court review standards, and ACB governance.
