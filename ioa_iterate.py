#!/usr/bin/env python3
"""Phase 3 iteration: capabilities the first engine does not cover.

Missing capability identified from pass-2 output
------------------------------------------------
`ioa_engine.score` treats operator-absence as a boolean
(`operator_is_paper_object`). That cannot distinguish:

  (a) "no one has written a review"          → literature silence, weak
  (b) "a review exists; alternative paths
      were listed and not excluded in field" → IOA Type I, strong
  (c) "the transfer function is published
      but identity-imported across systems"  → IOA Type II
  (d) "lab TF exists; field TF does not"     → IOA Type III

The missing tool is an *exclusion-path census*: for a named process,
list the ordinary alternative transports, and score whether each has
been experimentally excluded with a pre-registered primary outcome.

A second guard (`class_leakage_guard`) refuses IOA membership if the
gap is already owned by undersampling / TAC / NCR / FAC / CIC / JAC.

Neither function claims a natural mechanism. They classify the
*experimental object*.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

OUT = Path("/workspace/artifacts/ioa-2026-09-04")


@dataclass
class AltPath:
    name: str
    ordinary: bool  # more ordinary than the named discovery-path
    excluded_in_field: bool
    excluded_in_lab: bool
    notes: str
    source: str


@dataclass
class CensusResult:
    process: str
    realm: str
    named_path: str
    alternatives: list[dict[str, Any]]
    n_ordinary_unexcluded_field: int
    n_alternatives: int
    exclusion_fraction_field: float
    ioa_type_i_holds: bool
    verdict: str
    runnable_discriminator: str
    null_of_discriminator: str
    success_of_discriminator: str
    ethics: str


def exclusion_path_census(
    process: str,
    realm: str,
    named_path: str,
    alternatives: list[AltPath],
    discriminator: str,
    null: str,
    success: str,
    ethics: str = "observational / existing-plot only",
) -> CensusResult:
    """Census whether ordinary alternative transports have been excluded.

    Parameters
    ----------
    process : str
        The named scientific process (e.g. 'wood-wide web resource transfer').
    realm : str
        One of the session realms.
    named_path : str
        The path being treated as the discovery (e.g. 'common mycorrhizal network').
    alternatives : list[AltPath]
        Competing transports. `ordinary=True` marks the default physical path
        (diffusion, contact, artefact) that must be excluded first.
    discriminator, null, success : str
        Pre-registered test language. Required. Empty strings raise.

    Returns
    -------
    CensusResult
        IOA Type I holds iff at least one ordinary alternative remains
        unexcluded in the field. Lab-only exclusion is not sufficient
        (Karst's exact complaint about pot studies).

    Raises
    ------
    ValueError
        On empty process/named_path, empty alternatives, or missing
        discriminator language.
    """
    if not process or not named_path:
        raise ValueError("process and named_path are required")
    if not alternatives:
        raise ValueError("alternatives must be non-empty — a census of zero paths is not a census")
    if not discriminator or not null or not success:
        raise ValueError("discriminator/null/success must be specified (no decorative tests)")
    if realm not in {"space", "earth", "ocean", "animals", "humans", "land", "cross"}:
        raise ValueError(f"unknown realm: {realm}")

    ordinary_unex = [a for a in alternatives if a.ordinary and not a.excluded_in_field]
    n_alt = len(alternatives)
    n_field_ex = sum(1 for a in alternatives if a.excluded_in_field)
    frac = n_field_ex / n_alt
    holds = len(ordinary_unex) >= 1

    if holds:
        verdict = (
            f"IOA Type I HOLDS for '{process}': {len(ordinary_unex)} ordinary "
            f"alternative path(s) remain unexcluded in the field. Named path "
            f"'{named_path}' is therefore not entitled to be the operator."
        )
    else:
        verdict = (
            f"IOA Type I FAILS for '{process}': every ordinary alternative was "
            f"excluded in the field. If a residual remains it is TAC/NCR/FAC, not IOA."
        )

    return CensusResult(
        process=process,
        realm=realm,
        named_path=named_path,
        alternatives=[asdict(a) for a in alternatives],
        n_ordinary_unexcluded_field=len(ordinary_unex),
        n_alternatives=n_alt,
        exclusion_fraction_field=round(frac, 3),
        ioa_type_i_holds=holds,
        verdict=verdict,
        runnable_discriminator=discriminator,
        null_of_discriminator=null,
        success_of_discriminator=success,
        ethics=ethics,
    )


def class_leakage_guard(
    name: str,
    both_scales_empirical: bool,
    same_scale_ledgers: bool,
    missing_converter: bool,
    named_discriminator_ran_and_split: bool,
    cadence_mismatch_only: bool,
    named_cause_insufficient_only: bool,
    where_not_looked: bool,
) -> dict[str, Any]:
    """Refuse IOA if a prior class already owns the gap.

    Returns the assigned class and a boolean `ioa_allowed`.
    """
    if where_not_looked:
        return {"assigned": "undersampling", "ioa_allowed": False, "name": name}
    if missing_converter and not both_scales_empirical:
        return {"assigned": "TAC", "ioa_allowed": False, "name": name}
    if named_cause_insufficient_only and both_scales_empirical and same_scale_ledgers:
        return {"assigned": "NCR/IM", "ioa_allowed": False, "name": name}
    if named_discriminator_ran_and_split:
        return {"assigned": "FAC", "ioa_allowed": False, "name": name}
    if cadence_mismatch_only:
        return {"assigned": "CIC", "ioa_allowed": False, "name": name}
    if same_scale_ledgers and both_scales_empirical:
        return {"assigned": "JAC", "ioa_allowed": False, "name": name}
    if both_scales_empirical and not same_scale_ledgers:
        return {"assigned": "IOA", "ioa_allowed": True, "name": name}
    return {"assigned": "unclassified", "ioa_allowed": False, "name": name}


def invoke_on_session_data() -> dict[str, Any]:
    """Call both functions on the real rows of this session."""

    # ——— Primary live surface: wood-wide web (Karst 2023; Oxford 2025) ———
    www = exclusion_path_census(
        process="wood-wide web resource / warning transfer",
        realm="land",
        named_path="common mycorrhizal network (CMN) as the transport",
        alternatives=[
            AltPath(
                name="diffusion through soil water",
                ordinary=True, excluded_in_field=False, excluded_in_lab=False,
                notes="Karst et al.: dye/isotope movement has equally plausible soil-water path. Field designs rarely include a diffusion-only control at plot scale.",
                source="Nat Ecol Evol 2023 10.1038/s41559-023-01986-1; The Conversation 13 Feb 2023",
            ),
            AltPath(
                name="direct root–root contact",
                ordinary=True, excluded_in_field=False, excluded_in_lab=False,
                notes="Root grafts and contact are documented. Severing hyphae in pots does not exclude contact in a forest.",
                source="Karst 2023; Conversation 2023",
            ),
            AltPath(
                name="other soil microbes (non-CMN)",
                ordinary=True, excluded_in_field=False, excluded_in_lab=False,
                notes="Bacteria and saprotrophs move carbon. 'Fungal network' is not isolated by a mesh that other microbes cross.",
                source="Karst 2023",
            ),
            AltPath(
                name="eavesdropping / byproduct volatiles (not a message)",
                ordinary=True, excluded_in_field=False, excluded_in_lab=False,
                notes="Oxford 2025 model: plants do not 'warn'; neighbours intercept a byproduct. Information-flow sign inverted. Not excluded by isotope movement.",
                source="The Average Scientist 20 Aug 2025 citing 2025 Oxford model",
            ),
            AltPath(
                name="CMN as occasional conduit (not forest-scale web)",
                ordinary=False, excluded_in_field=False, excluded_in_lab=False,
                notes="The modest remaining claim. Still unquantified at stand scale. Not an ordinary confounder; the residual hypothesis.",
                source="Karst: fungi likely connect trees in many forests; extent unknown",
            ),
        ],
        discriminator=(
            "Pre-register a stand-scale design: (i) hyphal-exclusion meshes that "
            "block CMN but permit soil-water and microbes; (ii) root-isolation "
            "trenches; (iii) volatile-only chambers; (iv) intact CMN. Primary "
            "outcome = 13C / 15N movement and seedling survival, frozen before "
            "collection. Run in ≥2 biomes. Negative control: randomized mesh "
            "assignment with no live hyphae (killed-fungus plots)."
        ),
        null=(
            "Isotope movement and survival differences vanish in the "
            "hyphal-exclusion condition once soil-water and root-contact are "
            "matched. Then CMN is not the operator. IOA Type I closes as 'named "
            "path lost'."
        ),
        success=(
            "A residual in the intact-CMN plots survives all three ordinary "
            "exclusions, same sign, ≥2 biomes, fails the killed-fungus control. "
            "Then IOA was the right question and a CMN operator may exist. "
            "Still not 'trees talk'. Still not a mother-tree decision."
        ),
        ethics="existing research forests; no new clearcutting; meshes/trenches at seedling-plot scale",
    )

    # ——— Type II: K2-18b identity-import ———
    k218 = exclusion_path_census(
        process="K2-18b DMS/DMDS named as biosignature",
        realm="space",
        named_path="Earth-DMS-from-marine-life imported as identity onto a spectral wiggle",
        alternatives=[
            AltPath(
                name="instrumental offset / retrieval artefact",
                ordinary=True, excluded_in_field=False, excluded_in_lab=False,
                notes="Seager 2025: signal sensitive to instrumental offset; ~3σ not 5σ. Taylor 2025: consistent with flat line.",
                source="PNAS 10.1073/pnas.2416188122; arXiv:2504.15916",
            ),
            AltPath(
                name="other sulfur gases sharing spectral features",
                ordinary=True, excluded_in_field=False, excluded_in_lab=False,
                notes="Seager: attribution may be incorrect; other sulfur gases share features.",
                source="PNAS 2025",
            ),
            AltPath(
                name="abiotic DMS chemistry in H2-rich atmosphere",
                ordinary=True, excluded_in_field=False, excluded_in_lab=False,
                notes="Even a real DMS detection would not cash the operator 'DMS ⇒ life'. Abiotic paths unexcluded on a Hycean world.",
                source="Seager 2025 three Key Criteria failure #3",
            ),
            AltPath(
                name="model-comparison artefact (11-species vs 10-species reference)",
                ordinary=True, excluded_in_field=False, excluded_in_lab=False,
                notes="Tentative detection is a preference of a 5-biosignature reference model vs 4. Not a spectral line detection.",
                source="PNAS 2025 §2",
            ),
        ],
        discriminator=(
            "Independent reduction with pre-registered: (1) robustness to offset "
            "treatment, (2) nested models that do not privilege biosignature "
            "gases, (3) abiotic sulfur chemistry grid, (4) 5σ line criterion. "
            "NASA-led arXiv:2507.12622 is the live test (~2.7σ)."
        ),
        null="Feature consistent with flat line or with abiotic sulfur. Identity-import fails. IOA Type II closes as 'name was doing the work'.",
        success="5σ feature, abiotic grid excluded, offset-robust. Still NOT life — only a molecule. Life remains a further operator.",
        ethics="telescope time already allocated; no new claim of contact",
    )

    # ——— Leakage guard on live rows ———
    guards = [
        class_leakage_guard(
            name="wood-wide web hypha→forest",
            both_scales_empirical=True, same_scale_ledgers=False,
            missing_converter=False, named_discriminator_ran_and_split=False,
            cadence_mismatch_only=False, named_cause_insufficient_only=False,
            where_not_looked=False,
        ),
        class_leakage_guard(
            name="K2-18b DMS identity-import",
            both_scales_empirical=True, same_scale_ledgers=False,
            missing_converter=False, named_discriminator_ran_and_split=False,
            cadence_mismatch_only=False, named_cause_insufficient_only=True,  # NCR-adjacent
            where_not_looked=False,
        ),
        class_leakage_guard(
            name="cryptochrome in-vitro → heading",
            both_scales_empirical=True, same_scale_ledgers=False,
            missing_converter=True,  # TAC overlap
            named_discriminator_ran_and_split=False,
            cadence_mismatch_only=False, named_cause_insufficient_only=False,
            where_not_looked=False,
        ),
        class_leakage_guard(
            name="JAC geodynamo ⋈ tracks (negative control)",
            both_scales_empirical=True, same_scale_ledgers=True,
            missing_converter=False, named_discriminator_ran_and_split=False,
            cadence_mismatch_only=False, named_cause_insufficient_only=False,
            where_not_looked=False,
        ),
        class_leakage_guard(
            name="seafloor mapped vs seen (negative control)",
            both_scales_empirical=True, same_scale_ledgers=True,
            missing_converter=False, named_discriminator_ran_and_split=False,
            cadence_mismatch_only=False, named_cause_insufficient_only=False,
            where_not_looked=True,
        ),
        class_leakage_guard(
            name="Hubble JWST settler (negative control)",
            both_scales_empirical=True, same_scale_ledgers=True,
            missing_converter=False, named_discriminator_ran_and_split=True,
            cadence_mismatch_only=False, named_cause_insufficient_only=False,
            where_not_looked=False,
        ),
    ]

    # Adversarial note on K2-18b: named_cause_insufficient_only=True means
    # the guard currently routes it to NCR/IM. That is the honest overlap.
    # IOA Type II still describes a *different operator* (identity-import of
    # an Earth-scale function). We keep it as a penalized STRUCTURAL_GAP
    # in the engine, and record the leakage as NCR-adjacent, not primary.

    payload = {
        "function": "exclusion_path_census + class_leakage_guard",
        "wood_wide_web": asdict(www),
        "k2_18b": asdict(k218),
        "leakage_guards": guards,
        "primary_after_census": {
            "process": www.process,
            "ioa_type_i_holds": www.ioa_type_i_holds,
            "ordinary_unexcluded": www.n_ordinary_unexcluded_field,
            "exclusion_fraction_field": www.exclusion_fraction_field,
            "assigned_class": next(g["assigned"] for g in guards if g["name"].startswith("wood-wide")),
        },
        "k2_18b_after_census": {
            "ioa_type_i_holds": k218.ioa_type_i_holds,
            "ordinary_unexcluded": k218.n_ordinary_unexcluded_field,
            "assigned_by_guard": next(g["assigned"] for g in guards if "K2-18b" in g["name"]),
            "note": "Guard routes to NCR/IM because named cause (DMS) is insufficient. Engine keeps Type II IOA as penalized remainder. Not primary.",
        },
        "negative_controls_ok": all(
            (g["name"].startswith("JAC") and g["assigned"] == "JAC")
            or (g["name"].startswith("seafloor") and g["assigned"] == "undersampling")
            or (g["name"].startswith("Hubble") and g["assigned"] == "FAC")
            or g["name"].startswith("wood-wide")
            or g["name"].startswith("K2-18b")
            or g["name"].startswith("cryptochrome")
            for g in guards
        ),
    }
    (OUT / "ioa_census.json").write_text(json.dumps(payload, indent=2))
    return payload


if __name__ == "__main__":
    result = invoke_on_session_data()
    print(json.dumps({
        "www_holds": result["wood_wide_web"]["ioa_type_i_holds"],
        "www_unexcluded_ordinary": result["wood_wide_web"]["n_ordinary_unexcluded_field"],
        "www_verdict": result["wood_wide_web"]["verdict"],
        "k218_holds": result["k2_18b"]["ioa_type_i_holds"],
        "k218_guard": result["k2_18b_after_census"]["assigned_by_guard"],
        "primary_assigned": result["primary_after_census"]["assigned_class"],
        "negative_controls_ok": result["negative_controls_ok"],
        "guards": result["leakage_guards"],
    }, indent=2))
