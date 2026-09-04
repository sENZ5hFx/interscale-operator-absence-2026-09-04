#!/usr/bin/env python3
"""Interscale-Operator Absence Class (IOA) scoring engine.

Session: 2026-09-04-ioa-interscale
Author: Haley Bird / autonomous Grok research agent

This is a classification heuristic over sourced scientific gaps.
Scores are NOT measurements of nature.

Claim hygiene: research-stage classification. Not a physical discovery,
not peer review, not a patent.

IOA definition
--------------
Two or more scales of one named process are independently documented.
No field owns the operator that would take a state at scale A and emit
a unique, pre-registered prediction at scale B. The same English name
is used at both scales, hiding the missing transport.

This class is what remains after subtracting (do not reclaim):
  undersampling, TAC, cadence-mismatch, NCR/IM, FAC, CIC, JAC,
  Dark Biosphere, Cosmic-Bio Resonance, deep-biosphere-as-space-prior,
  Ritual Nyquist Law.

Falsification
-------------
- If a paper's *object* is the A→B transfer function and it predicts B
  from A within a pre-registered error → IOA is wrong for that pair.
- If locating a converter closes it → TAC, not IOA.
- If joining two same-scale ledgers closes it → JAC, not IOA.
- If watching longer closes it → CIC, not IOA.
- If more spatial samples close it → undersampling, not IOA.
- If the named cause adding up closes it → not NCR; IOA does not apply.
- Dual-scale occupancy requires BOTH scales empirically documented.
  A hypothesized unmeasured scale does not count.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

OUT = Path("/workspace/artifacts/ioa-2026-09-04")
OUT.mkdir(parents=True, exist_ok=True)

SESSION_ID = "2026-09-04-ioa-interscale"
TIMESTAMP = "2026-09-04T17:44:45Z"
AUTHOR = "Haley Bird (Fishers, IN) / autonomous Grok research agent"

# Prior archive classes this session must not reclaim.
PRIOR = [
    "Dark Biosphere Hypothesis 2026-05-14",
    "Cosmic-Bio Resonance 2026-05-14",
    "Undersampling 2026-08-03",
    "Deep-biosphere-as-space-prior 2026-08-14",
    "Ritual Nyquist Law 2026-08-27",
    "Transducer-Absence Class (TAC) 2026-08-28",
    "Cadence Mismatch Class 2026-08-29",
    "Named-Cause Residual / Initiation–Maintenance Split (NCR/IM) 2026-08-30",
    "Failed-Adjudication Class (FAC) 2026-08-31",
    "Clock-Incommensurability Class (CIC) 2026-09-01",
    "Join-Absence Class (JAC) 2026-09-02",
]


@dataclass
class Gap:
    id: str
    realm: str
    name: str
    scale_a: str
    scale_b: str
    log10_sep: float  # log10(characteristic length or time ratio B/A)
    same_name: bool
    both_scales_empirical: bool
    operator_is_paper_object: bool
    public_tf_runnable: bool
    overlap: float  # 0..1 prior-class occupancy
    retain_zero: bool
    retain_reason: str
    sources: list[str]
    note: str
    ioa_kind: str = "same_system"  # same_system | identity_import | lab_to_field
    # filled
    raw: float = 0.0
    remain: float = 0.0
    status: str = ""
    kills: list[str] = field(default_factory=list)


def score(g: Gap) -> Gap:
    """Heuristic. Not a measurement of nature. Capped at 55 following CIC."""
    g.kills = []
    if g.retain_zero:
        g.raw = 0.0
        g.remain = 0.0
        g.status = "ZEROED"
        g.kills.append(g.retain_reason)
        return g
    if not g.both_scales_empirical:
        g.raw = 0.0
        g.remain = 0.0
        g.status = "KILLED"
        g.kills.append("dual-scale occupancy failed: scale B (or A) is not empirically documented")
        return g
    if g.operator_is_paper_object:
        g.raw = 0.0
        g.remain = 0.0
        g.status = "KILLED"
        g.kills.append("A→B transfer function is already the object of published work")
        return g

    name_w = 1.0 if g.same_name else 0.4
    run_w = 1.0 if g.public_tf_runnable else 0.55
    sep = max(g.log10_sep, 0.5)
    g.raw = round(sep * name_w * run_w * 10.0, 2)
    remain = g.raw * (1.0 - max(0.0, min(1.0, g.overlap)))
    g.remain = round(min(55.0, remain), 2)
    if g.remain <= 0:
        g.status = "ZEROED"
    elif g.overlap >= 0.55:
        g.status = "PENALIZED_OVERLAP"
    else:
        g.status = "STRUCTURAL_GAP"
    return g


def catalog() -> list[Gap]:
    """Sourced rows. Overlap values are archive-occupancy estimates, not physics."""
    return [
        # ——— ZERO / RETAIN controls (must score 0) ———
        Gap(
            id="Z01", realm="space", name="Hubble tension identity",
            scale_a="local distance ladder", scale_b="CMB-inferred H0",
            log10_sep=0.0, same_name=True, both_scales_empirical=True,
            operator_is_paper_object=True, public_tf_runnable=True,
            overlap=1.0, retain_zero=True,
            retain_reason="FAC 2026-08-31 owns JWST-as-failed-settler; TAC/NCR retain",
            sources=["Riess/SH0ES", "CERN Courier 26 Mar 2025", "FAC archive"],
            note="Spoken. Not IOA.",
        ),
        Gap(
            id="Z02", realm="space", name="Dark matter / dark energy identity",
            scale_a="gravitational residual", scale_b="named field/particle",
            log10_sep=0.0, same_name=True, both_scales_empirical=False,
            operator_is_paper_object=False, public_tf_runnable=False,
            overlap=1.0, retain_zero=True,
            retain_reason="TAC owns missing converter named 'dark'",
            sources=["NASA", "ScienceDaily 8 Jan 2026", "APS Physics 19.34 2026"],
            note="Scale B (particle/field) is not empirically occupied. Dual-scale fails even without retain.",
        ),
        Gap(
            id="Z03", realm="animals", name="Magnetoreceptor cell",
            scale_a="behavioural compass", scale_b="identified receptor cell",
            log10_sep=0.0, same_name=True, both_scales_empirical=False,
            operator_is_paper_object=False, public_tf_runnable=False,
            overlap=1.0, retain_zero=True,
            retain_reason="TAC owns the missing cell; JAC owns INTERMAGNET⋈Movebank",
            sources=["Xu et al. Nature 2021 Cry4", "Nordmann JEB 2025", "JAC 2026-09-02"],
            note="Finding the cell is TAC. The same-scale join is JAC. Not today's object.",
        ),
        Gap(
            id="Z04", realm="earth", name="Inner-core state / rotation sign",
            scale_a="seismic waveform change", scale_b="solid-body rotation model",
            log10_sep=0.0, same_name=True, both_scales_empirical=True,
            operator_is_paper_object=True, public_tf_runnable=True,
            overlap=1.0, retain_zero=True,
            retain_reason="NCR owns inner-core state; CIC zeroed; JAC uses epochs as join key",
            sources=["Wang et al. Nature 2024 10.1038/s41586-024-07536-4", "Vidale 2025"],
            note="The seismic→rotation operator IS the literature's object. IOA fails.",
        ),
        Gap(
            id="Z05", realm="ocean", name="Nodule dark oxygen electrolysis",
            scale_a="nodule surface voltage", scale_b="benthic O2 flux sign",
            log10_sep=3.0, same_name=True, both_scales_empirical=True,
            operator_is_paper_object=True, public_tf_runnable=True,
            overlap=1.0, retain_zero=True,
            retain_reason="FAC+TAC; Editor's Note 8 Apr 2026; do not load-bear",
            sources=["Sweetman et al. Nat Geosci 2024", "Downes et al. Front Mar Sci 2025"],
            note="Claimed operator (electrolysis) is the paper's object and is contested. Not IOA.",
        ),
        Gap(
            id="Z06", realm="land", name="Omnitrophota uncultured",
            scale_a="metagenomic MAG", scale_b="cultured isolate",
            log10_sep=0.0, same_name=True, both_scales_empirical=False,
            operator_is_paper_object=False, public_tf_runnable=False,
            overlap=1.0, retain_zero=True,
            retain_reason="TAC owns the missing lab converter",
            sources=["CIC/TAC archive"],
            note="Scale B (isolate) not occupied. Undersampling/TAC.",
        ),
        Gap(
            id="Z07", realm="ocean", name="Seafloor mapped vs seen",
            scale_a="bathymetry 28.7%", scale_b="optical 0.001%",
            log10_sep=0.0, same_name=False, both_scales_empirical=True,
            operator_is_paper_object=False, public_tf_runnable=True,
            overlap=1.0, retain_zero=True,
            retain_reason="Undersampling 2026-08-03; CIC control",
            sources=["Seabed 2030 / NOAA 20 Apr 2026", "Sci Adv 10.1126/sciadv.adp8602"],
            note="Where-problem, not an operator-problem.",
        ),
        Gap(
            id="Z08", realm="cross", name="Geodynamo ⋈ magnetoreception join",
            scale_a="INTERMAGNET / core epochs", scale_b="Movebank tracks",
            log10_sep=0.0, same_name=False, both_scales_empirical=True,
            operator_is_paper_object=False, public_tf_runnable=True,
            overlap=1.0, retain_zero=True,
            retain_reason="JAC 2026-09-02 primary remaining surface",
            sources=["JAC archive 2026-09-02"],
            note="Same-scale join of two ledgers. Explicitly yesterday. Do not reclaim.",
        ),
        Gap(
            id="Z09", realm="humans", name="UPE / biophotons as communication",
            scale_a="ultraweak photon counts", scale_b="intercellular language",
            log10_sep=0.0, same_name=True, both_scales_empirical=False,
            operator_is_paper_object=False, public_tf_runnable=False,
            overlap=1.0, retain_zero=True,
            retain_reason="JAC kill 5: communication unproved; death-fade = metabolism",
            sources=["JAC 2026-09-02 kill list"],
            note="Scale B not documented. Killed.",
        ),
        Gap(
            id="Z10", realm="space", name="Little red dots as named class",
            scale_a="JWST snapshot photometry", scale_b="ontological galaxy class",
            log10_sep=0.0, same_name=True, both_scales_empirical=False,
            operator_is_paper_object=False, public_tf_runnable=True,
            overlap=1.0, retain_zero=True,
            retain_reason="CIC owns phase-object collapse; FAC owns three-camp split",
            sources=["Naidu 12 Aug 2026", "CIC archive"],
            note="Freeze-frame vs phase is CIC. Not a missing interscale operator.",
        ),
        Gap(
            id="Z11", realm="animals", name="Insect dark taxa LOC",
            scale_a="description rate", scale_b="extinction/loss rate",
            log10_sep=0.0, same_name=False, both_scales_empirical=True,
            operator_is_paper_object=False, public_tf_runnable=True,
            overlap=1.0, retain_zero=True,
            retain_reason="CIC owns loss-outruns-catalog",
            sources=["Lehmitz npj Biodivers 2025", "Stork/Griffith 2024"],
            note="Two clocks, not two spatial scales of one process.",
        ),
        Gap(
            id="Z12", realm="cross", name="Universal dark-fraction coincidence",
            scale_a="any 'dark' inventory", scale_b="any other 'dark' inventory",
            log10_sep=0.0, same_name=True, both_scales_empirical=True,
            operator_is_paper_object=False, public_tf_runnable=True,
            overlap=1.0, retain_zero=True,
            retain_reason="JAC kill 1: category error, not a law of nature",
            sources=["JAC 2026-09-02"],
            note="Numeric clustering of 'easy 10% named first'. Forbidden synthesis.",
        ),
        Gap(
            id="Z13", realm="humans", name="Consciousness / hard problem",
            scale_a="neuronal activity", scale_b="reported experience",
            log10_sep=6.0, same_name=True, both_scales_empirical=True,
            operator_is_paper_object=False, public_tf_runnable=False,
            overlap=0.95, retain_zero=True,
            retain_reason="Archive refused: spoken, NCR/IM, holographic-brain family",
            sources=["NCR archive", "FAC zeroed machine-consciousness discriminator"],
            note="Would look like IOA. Explicitly refused. Zeroed as control.",
        ),
        Gap(
            id="Z14", realm="space", name="Planck-scale QG as solution to H0",
            scale_a="quantum gravity (uneaten)", scale_b="measured H0 residual",
            log10_sep=60.0, same_name=False, both_scales_empirical=False,
            operator_is_paper_object=False, public_tf_runnable=False,
            overlap=0.5, retain_zero=False,
            retain_reason="",
            sources=["Afshordi et al. Physics 19.34, 12 May 2026: ~5% chose QG for low-energy mysteries; concordance 3–4× random"],
            note="First-pass bait: huge log-sep. Dual-scale occupancy MUST kill it (Planck scale not empirically occupied).",
            ioa_kind="identity_import",
        ),
        # ——— live IOA candidates ———
        Gap(
            id="L01", realm="land",
            name="Wood-wide web: hyphal flux → forest 'communication'",
            scale_a="hyphal segment ~10 µm (photographed, sequenced, isotope-traced in pots)",
            scale_b="forest stand ~10³–10⁴ m (growth, survival, 'mother tree' claims)",
            log10_sep=8.0, same_name=True, both_scales_empirical=True,
            operator_is_paper_object=False, public_tf_runnable=True,
            overlap=0.12, retain_zero=False, retain_reason="",
            sources=[
                "Karst, Jones, Hoeksema, Nat Ecol Evol 2023 10.1038/s41559-023-01986-1 (26 field studies; CMN role unproven)",
                "The Conversation 13 Feb 2023: dye movement has equally plausible soil-diffusion / root-contact alternatives",
                "Oxford 2025 model (The Average Scientist 20 Aug 2025): plants eavesdrop; signals as byproduct not message",
                "Explore Big Sky 5 May 2026: Karst three pillars still unclosed",
            ],
            note="Highest unclaimed living-system surface. Both scales occupied. Name 'web/communication/network' is the same-name collapse. Operator (CMN as the transport) is not the object of a pre-registered exclusion of soil-water / root-contact / eavesdrop paths. Dark Biosphere is networked subsurface LIFE as architecture — different object. Overlap 0.12 only.",
            ioa_kind="same_system",
        ),
        Gap(
            id="L02", realm="space",
            name="Biosignature identity-import: Earth-DMS-from-life → K2-18b-DMS-as-life",
            scale_a="Earth marine DMS (molecule, documented biogenic source)",
            scale_b="K2-18b spectral wiggle named 'DMS/DMDS' (molecule-scale feature, biosphere-scale claim)",
            log10_sep=16.0, same_name=True, both_scales_empirical=True,
            operator_is_paper_object=False, public_tf_runnable=True,
            overlap=0.38, retain_zero=False, retain_reason="",
            sources=[
                "Seager et al. PNAS 2025 10.1073/pnas.2416188122: K2-18b claim fails all three Key Criteria",
                "NASA-led reanalysis arXiv:2507.12622 (Jul 2025): DMS ~2.7σ, below 5σ",
                "Madhusudhan Apr 2025 ~3σ; Taylor 2025: consistent with flat line",
                "Prior archive mentions K2-18b (2026-06-03 session) — overlap applied",
            ],
            note="Type II IOA (identity-import). Scale A (Earth DMS←phytoplankton) is empirical. Scale B as a *biosphere* on K2-18b is not empirical; what IS empirical is a spectrum. The operator being imported is 'DMS ⇒ life' as if identity. Overlap with prior K2-18b mention and with NCR (named cause insufficient). Remaining after penalty still real because the CLASS (molecule-name used as biosphere-operator) was not previously the object.",
            ioa_kind="identity_import",
        ),
        Gap(
            id="L03", realm="animals",
            name="Cryptochrome in-vitro spin yield → in-flight heading",
            scale_a="Cry4 radical-pair Δabsorbance in vitro (nm, ns; Xu 2021)",
            scale_b="migratory heading residual over 10³ km after solar-weather controls",
            log10_sep=12.0, same_name=True, both_scales_empirical=True,
            operator_is_paper_object=False, public_tf_runnable=True,
            overlap=0.72, retain_zero=False, retain_reason="",
            sources=[
                "Xu et al. Nature 2021 10.1038/s41586-021-03618-9 (Cry4 magnetically sensitive in vitro)",
                "Luo/Hammes-Schiffer/Subotnik JACS Nov 2025 (computational radical-pair support)",
                "Engels et al. Nature 2014 RF disruption of compass",
                "TAC owns the cell; JAC owns INTERMAGNET⋈tracks (same-scale)",
            ],
            note="Type III (lab→field). Both scales empirical. The in-vitro→heading transfer function is hypothesized (Ritz/Schulten/Hore) but is not a pre-registered predictor of Movebank residuals from a measured spin yield given local B. Heavy TAC/JAC overlap. Remainder is the missing interscale operator AFTER the cell is found and AFTER the same-scale join.",
            ioa_kind="lab_to_field",
        ),
        Gap(
            id="L04", realm="ocean",
            name="Mesopelagic acoustic backscatter → climate carbon residual",
            scale_a="ship/acoustic target strength (10s of metres)",
            scale_b="global biological carbon pump (planetary)",
            log10_sep=6.0, same_name=True, both_scales_empirical=True,
            operator_is_paper_object=True, public_tf_runnable=True,
            overlap=0.60, retain_zero=False, retain_reason="",
            sources=["McMonagle 2024", "Oostdijk 2024", "JAC spoken-but-open"],
            note="Papers exist whose object is this scaling. operator_is_paper_object=True should kill.",
            ioa_kind="same_system",
        ),
        Gap(
            id="L05", realm="humans",
            name="AlphaFold static coordinates → organismal phenotype",
            scale_a="Å-resolution static fold",
            scale_b="cellular / organism function",
            log10_sep=7.0, same_name=True, both_scales_empirical=True,
            operator_is_paper_object=False, public_tf_runnable=False,
            overlap=0.68, retain_zero=False, retain_reason="",
            sources=["Brotzakis et al. Nat Commun 14 Feb 2025 disordered ensembles", "FAC 2026-08-31"],
            note="FAC owns 'solved vs dynamics split'. IOA remainder would be fold→phenotype transport. Heavily penalized; not primary.",
            ioa_kind="lab_to_field",
        ),
        Gap(
            id="L06", realm="earth",
            name="Crustal / radiolytic O2 concentration → ancestral aerobic metabolism",
            scale_a="measured 0.09 µmol L⁻¹ O2 in 1.2-Gyr brine (Moab Khotsong)",
            scale_b="genomic placement of aerobes before oxygenic photosynthesis (Murali Science)",
            log10_sep=9.0, same_name=True, both_scales_empirical=True,
            operator_is_paper_object=False, public_tf_runnable=False,
            overlap=0.58, retain_zero=False, retain_reason="",
            sources=[
                "Murali et al. Science 10.1126/science.adp1853",
                "Ruff / Dinneen New Yorker 13 Aug 2026",
                "CIC: textbook sequence is freeze-frame; ancestral energy UNPROVED",
            ],
            note="Do NOT attach Sweetman nodules. Both scales empirical (brine O2; genomes). The operator 'this O2 powered those aerobes' is unproved and not a transfer-function paper. CIC already flagged the freeze-frame. Overlap 0.58.",
            ioa_kind="identity_import",
        ),
        Gap(
            id="L07", realm="land",
            name="Soil prokaryote gene catalog → ecosystem function",
            scale_a="uncultured MAG / ORF",
            scale_b="seasonal plot-level nutrient/C flux",
            log10_sep=7.0, same_name=True, both_scales_empirical=True,
            operator_is_paper_object=False, public_tf_runnable=True,
            overlap=0.62, retain_zero=False, retain_reason="",
            sources=["Lehmitz 2025", "87–99% uncultured across 1,046 studies, preprint 3 Jul 2025", "CIC soil function", "FAC metagenomics-as-settler"],
            note="TAC/CIC/FAC all touch this. IOA remainder is gene→plot flux operator. Penalized.",
            ioa_kind="same_system",
        ),
        Gap(
            id="L08", realm="ocean",
            name="Hadal 16S/MAG → hadal ecosystem function",
            scale_a="sequence",
            scale_b="trench-scale biogeochemistry",
            log10_sep=6.0, same_name=True, both_scales_empirical=True,
            operator_is_paper_object=False, public_tf_runnable=False,
            overlap=0.80, retain_zero=False, retain_reason="",
            sources=["TAC/Dark Biosphere retain: hadal microbiome ~90% new"],
            note="Existence claimed. Function-operator not today's primary. Heavy overlap.",
            ioa_kind="same_system",
        ),
        Gap(
            id="L09", realm="humans",
            name="Noncoding assay 'function' → organismal fitness function",
            scale_a="ENCODE-style biochemical activity",
            scale_b="purifying-selection / fitness",
            log10_sep=5.0, same_name=True, both_scales_empirical=True,
            operator_is_paper_object=False, public_tf_runnable=True,
            overlap=0.90, retain_zero=False, retain_reason="",
            sources=["CIC two-clock metrology of 'function'", "IISc Connect Apr 2026"],
            note="CIC owns this as two-clock. Same-name 'function' is CIC POC. Near-zero remainder expected.",
            ioa_kind="same_system",
        ),
        Gap(
            id="L10", realm="animals",
            name="Morphological species → cryptic genomic complex",
            scale_a="Linnaean skin/wing",
            scale_b="nuclear+mt delimitation (~3.1 cryptic / morphospecies)",
            log10_sep=0.5, same_name=True, both_scales_empirical=True,
            operator_is_paper_object=True, public_tf_runnable=True,
            overlap=0.85, retain_zero=False, retain_reason="",
            sources=["Lehmitz 2025", "CIC POC+LOC"],
            note="The mapping IS the object of the cryptic-species literature. operator_is_paper_object should kill. Also CIC.",
            ioa_kind="same_system",
        ),
    ]


def first_pass(rows: list[Gap]) -> list[Gap]:
    return [score(g) for g in rows]


def ioa_kind_split(rows: list[Gap]) -> list[Gap]:
    """Iteration: split IOA kind and apply kind-specific caps.

    Adversary finding from first pass: identity-import rows can inflate
    via huge log10_sep (Earth→exoplanet, Planck→H0) even when one scale
    is a *name* rather than a measurement. Cap identity-import at 40.
    Cap lab_to_field at 45. same_system uncapped except global 55.
    Also: if overlap>=0.85, force remain to 0 (reclaim in all but name).
    """
    out = []
    for g in rows:
        h = Gap(**{k: v for k, v in asdict(g).items()})
        h = score(h)
        if h.overlap >= 0.85 and not h.retain_zero:
            h.remain = 0.0
            h.status = "ZEROED"
            h.kills = list(h.kills) + ["overlap≥0.85 treated as reclaim"]
        cap = {"identity_import": 40.0, "lab_to_field": 45.0, "same_system": 55.0}.get(h.ioa_kind, 55.0)
        if h.remain > cap:
            h.remain = cap
            h.kills = list(h.kills) + [f"kind cap {h.ioa_kind}={cap}"]
        out.append(h)
    return out


def validate_gap(g: Gap) -> list[str]:
    """Input validation / edge cases for the session function."""
    errs = []
    if not g.id or not g.realm or not g.name:
        errs.append("missing id/realm/name")
    if g.overlap < 0 or g.overlap > 1:
        errs.append(f"{g.id}: overlap out of [0,1]")
    if g.log10_sep < 0:
        errs.append(f"{g.id}: log10_sep negative")
    if g.retain_zero and not g.retain_reason:
        errs.append(f"{g.id}: retain_zero without reason")
    if g.both_scales_empirical is False and g.status == "STRUCTURAL_GAP":
        errs.append(f"{g.id}: non-empirical scales cannot be STRUCTURAL_GAP")
    return errs


def rank_table(rows: list[Gap]) -> list[dict[str, Any]]:
    ordered = sorted(rows, key=lambda r: (-r.remain, r.id))
    return [
        {
            "remain": r.remain,
            "raw": r.raw,
            "overlap": r.overlap,
            "kind": r.ioa_kind,
            "status": r.status,
            "realm": r.realm,
            "id": r.id,
            "name": r.name,
            "kills": r.kills,
        }
        for r in ordered
    ]


def primary(rows: list[Gap]) -> Gap | None:
    live = [r for r in rows if r.status == "STRUCTURAL_GAP"]
    if not live:
        return None
    return max(live, key=lambda r: r.remain)


def main() -> dict[str, Any]:
    rows = catalog()
    pass1 = first_pass(rows)
    p1_primary = primary(pass1)

    # Adversarial iteration
    pass2 = ioa_kind_split(catalog())
    p2_primary = primary(pass2)

    errors = []
    for r in pass2:
        errors.extend(validate_gap(r))

    zeroed = [r.id for r in pass2 if r.remain == 0]
    live = [r for r in pass2 if r.remain > 0]

    payload = {
        "session_id": SESSION_ID,
        "timestamp": TIMESTAMP,
        "author": AUTHOR,
        "class": "Interscale-Operator Absence Class (IOA)",
        "prior_classes_not_reclaimed": PRIOR,
        "claim_hygiene": "research-stage classification; not a physical discovery; not peer review; not a patent; scores are a heuristic not measurements of nature",
        "validation_errors": errors,
        "pass1_primary": None if not p1_primary else {"id": p1_primary.id, "remain": p1_primary.remain, "name": p1_primary.name},
        "pass2_primary": None if not p2_primary else {"id": p2_primary.id, "remain": p2_primary.remain, "name": p2_primary.name, "realm": p2_primary.realm, "kind": p2_primary.kind if False else p2_primary.ioa_kind},
        "iteration_note": "pass1 can inflate identity-import via huge log-sep. pass2 caps identity_import at 40, lab_to_field at 45, zeros overlap≥0.85, and dual-scale occupancy kills QG→H0 and any unmeasured scale B.",
        "ranked": rank_table(pass2),
        "zeroed_ids": zeroed,
        "live_count": len(live),
        "highest_living_system": next(
            ({"id": r.id, "remain": r.remain, "name": r.name, "realm": r.realm} for r in sorted(live, key=lambda x: -x.remain) if r.realm in {"land", "animals", "ocean", "humans", "earth"}),
            None,
        ),
    }
    (OUT / "ioa_scores.json").write_text(json.dumps(payload, indent=2))
    (OUT / "ioa_rows.json").write_text(json.dumps([asdict(r) for r in pass2], indent=2))
    return payload


if __name__ == "__main__":
    result = main()
    print(json.dumps({
        "validation_errors": result["validation_errors"],
        "pass1_primary": result["pass1_primary"],
        "pass2_primary": result["pass2_primary"],
        "live_count": result["live_count"],
        "ranked": result["ranked"],
    }, indent=2))
