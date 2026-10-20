import Mathlib.GroupTheory.GroupAction.CardCommute
import Mathlib.GroupTheory.GroupAction.SubMulAction
import Mathlib.Data.ZMod.Basic
import Mathlib.Algebra.BigOperators.Ring.Finset

/-!
# C9 Lemma O1: free multiplier action

If `u` is a unit of `ZMod m` with `u • S = S`, then `⟨u⟩` acts freely on the set of triples
`(a,b,c) ∈ S³` with `b - a` a unit and `c - a = ρ (b - a)`. Hence `orderOf u` divides the
number of such triples. For a Singer set with multiplier `p` (normalised so that `pS = S`),
`orderOf p = 3k`, which gives `3k ∣ N(ρ)`.
-/

open MulAction

namespace C9Orbit

variable {m : ℕ} [NeZero m]

abbrev X (m : ℕ) := ZMod m × ZMod m × ZMod m

/-- Triples with unit difference `b - a` and ratio `ρ`. -/
def T (S : Finset (ZMod m)) (ρ : ZMod m) : Set (X m) :=
  {t | t.1 ∈ S ∧ t.2.1 ∈ S ∧ t.2.2 ∈ S ∧ IsUnit (t.2.1 - t.1) ∧
    t.2.2 - t.1 = ρ * (t.2.1 - t.1)}

omit [NeZero m] in
lemma natpow_mem {S : Finset (ZMod m)} {u : (ZMod m)ˣ}
    (hS : ∀ x, x ∈ S ↔ (u : ZMod m) * x ∈ S) (n : ℕ) :
    ∀ x, x ∈ S ↔ ((u ^ n : (ZMod m)ˣ) : ZMod m) * x ∈ S := by
  induction n with
  | zero => intro x; simp
  | succ n ih => intro x; rw [pow_succ', Units.val_mul, mul_assoc, ← hS]; exact ih x

omit [NeZero m] in
lemma zpow_mem {S : Finset (ZMod m)} {u : (ZMod m)ˣ}
    (hS : ∀ x, x ∈ S ↔ (u : ZMod m) * x ∈ S) (n : ℤ) :
    ∀ x, x ∈ S ↔ ((u ^ n : (ZMod m)ˣ) : ZMod m) * x ∈ S := by
  cases n with
  | ofNat k => intro x; rw [Int.ofNat_eq_natCast, zpow_natCast]; exact natpow_mem hS k x
  | negSucc k =>
    intro x
    rw [zpow_negSucc]
    have h := natpow_mem hS (k + 1) ((((u ^ (k + 1))⁻¹ : (ZMod m)ˣ) : ZMod m) * x)
    rw [← mul_assoc, ← Units.val_mul, mul_inv_cancel, Units.val_one, one_mul] at h
    exact h.symm

/-- The set `T S ρ` as a sub-`MulAction` of `zpowers u`. -/
def TA (S : Finset (ZMod m)) (ρ : ZMod m) (u : (ZMod m)ˣ)
    (hS : ∀ x, x ∈ S ↔ (u : ZMod m) * x ∈ S) :
    SubMulAction (Subgroup.zpowers u) (X m) where
  carrier := T S ρ
  smul_mem' := by
    rintro ⟨g, hg⟩ ⟨a, b, c⟩ ⟨ha, hb, hc, hu, hr⟩
    obtain ⟨n, rfl⟩ := Subgroup.mem_zpowers_iff.mp hg
    have key := zpow_mem hS n
    dsimp only at ha hb hc hu hr
    refine ⟨(key a).mp ha, (key b).mp hb, (key c).mp hc, ?_, ?_⟩
    · have e : IsUnit (((u ^ n : (ZMod m)ˣ) : ZMod m) * b - ((u ^ n : (ZMod m)ˣ) : ZMod m) * a) := by
        rw [← mul_sub]; exact (Units.isUnit _).mul hu
      exact e
    · have e : ((u ^ n : (ZMod m)ˣ) : ZMod m) * c - ((u ^ n : (ZMod m)ˣ) : ZMod m) * a =
          ρ * (((u ^ n : (ZMod m)ˣ) : ZMod m) * b - ((u ^ n : (ZMod m)ˣ) : ZMod m) * a) := by
        rw [← mul_sub, ← mul_sub, hr]; exact mul_left_comm _ _ _
      exact e

/-- Freeness: only the identity fixes a triple. -/
lemma stab_trivial (S : Finset (ZMod m)) (ρ : ZMod m) (u : (ZMod m)ˣ)
    (hS : ∀ x, x ∈ S ↔ (u : ZMod m) * x ∈ S) (t : TA S ρ u hS) :
    stabilizer (Subgroup.zpowers u) t = ⊥ := by
  rw [eq_bot_iff]
  rintro ⟨g, hg⟩ hfix
  rw [mem_stabilizer_iff] at hfix
  have h1 := congrArg (fun s : TA S ρ u hS => (s : X m).1) hfix
  have h2 := congrArg (fun s : TA S ρ u hS => (s : X m).2.1) hfix
  simp only [SubMulAction.val_smul, Prod.smul_fst, Prod.smul_snd] at h1 h2
  have hu : IsUnit ((t : X m).2.1 - (t : X m).1) := t.2.2.2.2.1
  have : ((g : ZMod m)) * ((t : X m).2.1 - (t : X m).1) = 1 * ((t : X m).2.1 - (t : X m).1) := by
    rw [one_mul, mul_sub]
    exact congrArg₂ (· - ·) h2 h1
  have hg1 : (g : ZMod m) = 1 := hu.mul_left_inj.mp this
  show (⟨g, hg⟩ : Subgroup.zpowers u) ∈ (⊥ : Subgroup (Subgroup.zpowers u))
  rw [Subgroup.mem_bot]
  exact Subtype.ext (Units.ext hg1)

/-- **Lemma O1.** `orderOf u` divides the number of triples. -/
theorem orderOf_dvd_card (S : Finset (ZMod m)) (ρ : ZMod m) (u : (ZMod m)ˣ)
    (hS : ∀ x, x ∈ S ↔ (u : ZMod m) * x ∈ S) :
    orderOf u ∣ Nat.card (TA S ρ u hS) := by
  classical
  let _ : Fintype (TA S ρ u hS) := Fintype.ofFinite _
  rw [Nat.card_eq_fintype_card,
    MulAction.card_eq_sum_card_group_div_card_stabilizer (Subgroup.zpowers u) (TA S ρ u hS)]
  apply Finset.dvd_sum
  intro ω _
  have hst : Fintype.card (stabilizer (Subgroup.zpowers u) ω.out) = 1 := by
    rw [← Nat.card_eq_fintype_card, stab_trivial S ρ u hS ω.out, Subgroup.card_bot]
  rw [hst, Nat.div_one, Fintype.card_zpowers]

end C9Orbit
