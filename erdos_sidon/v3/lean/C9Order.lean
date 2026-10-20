import Mathlib.Data.ZMod.Basic
import Mathlib.GroupTheory.OrderOfElement
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

/-!
# C9 Lemma O1, step 3: the multiplier `p` has order exactly `3k` modulo `m = q² + q + 1`, `q = p^k`.
-/

namespace C9Order

lemma cube_identity (x : ℕ) (hx : 1 ≤ x) : x ^ 3 = (x - 1) * (x ^ 2 + x + 1) + 1 := by
  obtain ⟨y, rfl⟩ : ∃ y, x = y + 1 := ⟨x - 1, by omega⟩
  simp only [Nat.add_sub_cancel]
  ring

theorem orderOf_p (p k : ℕ) (hp : 2 ≤ p) (hk : 1 ≤ k) :
    orderOf (p : ZMod (p ^ (2 * k) + p ^ k + 1)) = 3 * k := by
  set m := p ^ (2 * k) + p ^ k + 1 with hm
  have hx : 1 ≤ p ^ k := Nat.one_le_pow _ _ (by omega)
  have hsq : p ^ (2 * k) = (p ^ k) ^ 2 := by rw [← pow_mul, mul_comm]
  -- p^(3k) = 1 in ZMod m
  have h1 : (p : ZMod m) ^ (3 * k) = 1 := by
    have e : p ^ (3 * k) = (p ^ k - 1) * m + 1 := by
      rw [hm, hsq, ← cube_identity _ hx, ← pow_mul, mul_comm]
    have : ((p ^ (3 * k) : ℕ) : ZMod m) = 1 := by
      rw [e]; push_cast; rw [ZMod.natCast_self]; ring
    exact_mod_cast this
  have hdvd : orderOf (p : ZMod m) ∣ 3 * k := orderOf_dvd_of_pow_eq_one h1
  have hpos : 0 < orderOf (p : ZMod m) :=
    orderOf_pos_iff.mpr (isOfFinOrder_iff_pow_eq_one.mpr ⟨3 * k, by omega, h1⟩)
  set d := orderOf (p : ZMod m) with hd
  by_contra hne
  -- d is a proper divisor of 3k, so 2d ≤ 3k, hence d ≤ 2k
  obtain ⟨e, he⟩ := hdvd
  have he2 : 2 ≤ e := by
    rcases Nat.lt_or_ge e 2 with h | h
    · rcases (by omega : e = 0 ∨ e = 1) with rfl | rfl
      · rw [mul_zero] at he; omega
      · rw [mul_one] at he; exact absurd he.symm hne
    · exact h
  have hd2k : d ≤ 2 * k := by nlinarith
  -- m ∣ p^d - 1
  have hpd : (p : ZMod m) ^ d = 1 := pow_orderOf_eq_one _
  have hge : 1 ≤ p ^ d := Nat.one_le_pow _ _ (by omega)
  have hz : (((p ^ d - 1 : ℕ)) : ZMod m) = 0 := by
    rw [Nat.cast_sub hge]; push_cast; rw [hpd]; ring
  rw [ZMod.natCast_eq_zero_iff] at hz
  have hlt : p ^ d - 1 < m := by
    have : p ^ d ≤ p ^ (2 * k) := Nat.pow_le_pow_right (by omega) hd2k
    omega
  have hpos' : 0 < p ^ d - 1 := by
    have : p ≤ p ^ d := Nat.le_self_pow (by omega) _
    omega
  exact absurd (Nat.le_of_dvd hpos' hz) (by omega)

end C9Order
