# Floquet-Based Transmon-Inspired MultiQubit Engine — Boolean Linear Separator (Public Skeleton)

This repository contains a **structure-only, redacted “public skeleton”** of a research prototype that explores a **Floquet-driven, transmon-inspired multi-qubit lattice** coupled to thermal environments, with a dashboard-style visualization and a battery of thermodynamic / information-theoretic diagnostics.

> **Why a skeleton?**  
> The intent is to share the **architecture, module layout, and metric definitions** without exposing implementation details (function bodies are intentionally omitted).

---

## What’s in this repo

### Public (this repo)
- `Floquet_Transmon_MultiQubit_Engine_Boolean_Linear_Separator_PUBLIC_SKELETON.py`  
  Main architecture outline: lattice evolution, metrics, dashboard assembly, export hooks, and optional control-daemon scaffolding.

- `quantum_unified_revised_v109_complete_PUBLIC_SKELETON.py`  
  Alternate/legacy “unified” layout (also redacted).

- `TransmonLatticeFloquetBreal_PUBLIC_SKELETON.py`  
  Notebook-origin variant (also redacted).

> **Note:** The public skeleton files **do not run** (no bodies). They are meant for readers to understand the **structure** and **interfaces**.

### Private (not included)
A runnable implementation that:
- evolves a 4‑qubit global density matrix,
- computes entanglement + geometry + thermodynamic diagnostics,
- renders an animated dashboard (GIF/MP4),
- exports time-series plot data and Wigner snapshots,
- optionally runs a lightweight “control daemon” optimization loop.

---

## Suggested file header for your private runnable code

Paste something like this at the top of your private file:

```python
# Floquet-Based Transmon-Inspired MultiQubit Engine — Boolean Linear Separator
# --------------------------------------------------------------------------
# Research-grade simulation prototype of a Floquet-driven, transmon-inspired
# multi-qubit lattice coupled to thermal environments, with dashboard visualization
# and thermodynamic / quantum-information diagnostics.
#
# Public repository note:
#   This file has a structure-only public skeleton counterpart on GitHub.
```

---

## Conceptual pipeline

1. **Model construction**
   - Build local single-qubit operators and lattice interaction operators.
   - Specify Floquet/bath schedules and coupling parameters.

2. **Global open-system evolution**
   - Evolve the **global density matrix** ρ(t) with discrete-time maps
     (unitary + noise channels + bath-inspired amplitude/dephasing).

3. **Diagnostics**
   - Per-qubit Bloch vectors, purity, coherence proxies, excited-state population.
   - Two-qubit and global entanglement indicators (log-negativity, concurrence, mutual information).
   - Operator-space entanglement entropy (OSEE).
   - Geometry proxies (Berry-rate proxy, QGT proxy, curvature proxy).
   - Bures-distance “memory currents” and hotspot scores.
   - Heat / work / entropy-production proxies (Otto-like bookkeeping).

4. **Visualization**
   - Animated dashboard with Bloch spheres, time-series, and optional Wigner panels.

5. **Export & sharing**
   - CSV/JSON plot-data bundles + an `index.html` convenience page.
   - Optional local server and ngrok tunnel for sharing.

## Definitions used by the prototype

Below are the **definitions used by the prototype** (or close “physics-standard” definitions when a proxy is used).

## Definitions used by the prototype

Below are the **definitions used by the prototype** (or close “physics-standard” definitions when a proxy is used).

### 1) Qubit state and Bloch vector

For a single qubit reduced state $ \rho \in \mathbb{C}^{2\times 2} $:
$$
\rho = \frac{1}{2}\left(I + \mathbf{r}\cdot\boldsymbol{\sigma}\right),
\qquad
\mathbf{r} = (x,y,z),
\qquad
x=\mathrm{Tr}(\rho\,\sigma_x),\;y=\mathrm{Tr}(\rho\,\sigma_y),\;z=\mathrm{Tr}(\rho\,\sigma_z).
$$

### 2) SU(2) Wigner function for a spin‑1/2 (Bloch sphere)

A Stratonovich–Weyl form is:
$$
W(\Omega) = \mathrm{Tr}\!\big[\rho\,\Delta(\Omega)\big],
$$
where $\Omega=(\theta,\phi)$ and $\Delta(\Omega)$ is the SU(2) Stratonovich–Weyl kernel.

For spin‑$1/2$, a common normalized convention gives:
$$
W(\theta,\phi)
= \frac{1}{4\pi}\Big(1+\sqrt{3}\,\mathbf{r}\cdot\mathbf{n}(\theta,\phi)\Big),
\quad
\mathbf{n}(\theta,\phi)=(\sin\theta\cos\phi,\sin\theta\sin\phi,\cos\theta).
$$

> Conventions vary by factors of $\sqrt{3}$ and $4\pi$; the key point is that $W$ is an affine function of the Bloch vector on the sphere.

### 3) HO-embedded (harmonic oscillator) Wigner function

When a qubit is **embedded** into a truncated oscillator space (e.g., the $|0\rangle,|1\rangle$ subspace of an $N_{\rm ho}$-dimensional Fock space),
the phase-space Wigner function can be computed with the standard oscillator definition:

**Integral form:**
$$
W(x,p)=\frac{1}{\pi}\int_{-\infty}^{\infty}dy\;
e^{2ipy}\,\langle x-y|\rho|x+y\rangle .
$$

**Displacement–parity form (often used numerically):**
$$
W(\alpha)=\frac{2}{\pi}\,\mathrm{Tr}\!\left[\rho\,D(2\alpha)\,\Pi\,D^\dagger(2\alpha)\right],
$$
where $D(\alpha)$ is the displacement operator and $\Pi$ is parity.

**Per-qubit Wigner:** embed each reduced $2\times2$ state $\rho_i$ into $N_{\rm ho}\times N_{\rm ho}$.  
**Collective Wigner:** embed either an averaged reduced state $\bar\rho=\frac{1}{N}\sum_i\rho_i$ or a reduced collective state (implementation-dependent).

### 4) Heat current (open quantum systems)

If the dynamics decomposes into Liouvillian contributions:
$$
\dot\rho = -i[H(t),\rho] + \sum_k \mathcal{L}_k(\rho),
$$
then the (bath-associated) heat current from channel $k$ is often defined as:
$$
J_k(t) \equiv \dot Q_k(t) = \mathrm{Tr}\!\left[H(t)\,\mathcal{L}_k(\rho(t))\right].
$$

A **local per-qubit** heat current proxy can be written:
$$
J_i(t)=\mathrm{Tr}\!\left[H_i(t)\,\mathcal{L}_i(\rho(t))\right],
\qquad
J_{\rm lattice}(t)=\sum_i J_i(t).
$$

**Otto-like bookkeeping (qubit proxy):** if energy is approximated by:
$$
E(t)\approx \omega(t)\,p_e(t) = \frac{\omega(t)}{2}\bigl(1-z(t)\bigr),
$$
then one convenient split is:
$$
\dot Q(t) = -\frac{\omega(t)}{2}\,\dot z(t),
\qquad
\dot W(t) = \frac{1-z(t)}{2}\,\dot\omega(t),
\qquad
\dot E(t)=\dot Q(t)+\dot W(t).
$$

### 5) Von Neumann entropy and mutual information

**Von Neumann entropy (bits):**
$$
S(\rho)=-\mathrm{Tr}\big(\rho\log_2\rho\big).
$$

**Mutual information between subsystems $A$ and $B$:**
$$
I(A\!:\!B)=S(\rho_A)+S(\rho_B)-S(\rho_{AB}).
$$

### 6) Concurrence (two qubits)

For a two-qubit state $\rho$, define the spin-flipped state:
$$
\tilde\rho = (\sigma_y\otimes\sigma_y)\,\rho^*\,(\sigma_y\otimes\sigma_y),
$$
and let $\lambda_1\ge \lambda_2\ge \lambda_3\ge \lambda_4$ be the square-roots of the eigenvalues of $\rho\tilde\rho$. Then:
$$
C(\rho)=\max\bigl(0,\lambda_1-\lambda_2-\lambda_3-\lambda_4\bigr).
$$

### 7) Log-negativity (two qubits)

Let $\rho^{T_B}$ be the partial transpose with respect to subsystem $B$. The log-negativity is:
$$
E_\mathcal{N}(\rho)=\log_2\left\|\rho^{T_B}\right\|_1,
$$
where $\|X\|_1=\mathrm{Tr}\sqrt{X^\dagger X}$.

### 8) Operator-Space Entanglement Entropy (OSEE)

Treat the density operator as a vector in Liouville space, $|\rho\rangle\rangle$, and Schmidt-decompose across a bipartition:
$$
|\rho\rangle\rangle=\sum_k s_k\,|A_k\rangle\rangle\otimes|B_k\rangle\rangle,
\qquad
\sum_k s_k^2 = 1 \;\; (\text{after normalization}).
$$
Then OSEE (bits) is:
$$
S_{\rm OSEE} = -\sum_k s_k^2\,\log_2(s_k^2).
$$

### 9) Fidelity, Bures distance, and Bures length

**Uhlmann fidelity:**
$$
F(\rho,\sigma)=\left(\mathrm{Tr}\sqrt{\sqrt{\rho}\,\sigma\,\sqrt{\rho}}\right)^2.
$$

**Bures distance:**
$$
D_B(\rho,\sigma)=\sqrt{2\left(1-\sqrt{F(\rho,\sigma)}\right)}.
$$

**Discrete Bures path length (thermodynamic/geometric length proxy):**
$$
L_B \approx \sum_{k=1}^{T} D_B\bigl(\rho_{k},\rho_{k-1}\bigr),
\qquad
\frac{dL_B}{dt}\Big|_{t_k}\approx \frac{D_B(\rho_k,\rho_{k-1})}{\Delta t}.
$$

### 10) “Memory current” and hotspot scores (Bures-lag method)

Define a lagged Bures distance:
$$
D_{\rm lag}(t)=D_B\!\bigl(\rho(t),\rho(t-\tau)\bigr)
\quad (\text{or use }\rho(0)\text{ when }t<\tau).
$$

Define “separation” and “return” currents as the positive/negative parts of the time derivative:
$$
J_{\rm sep}(t)=\max\!\left(0,\frac{d}{dt}D_{\rm lag}(t)\right),
\qquad
J_{\rm ret}(t)=\max\!\left(0,-\frac{d}{dt}D_{\rm lag}(t)\right).
$$

A simple hotspot score is then:
$$
H_{\rm sep}(t)=\left(\frac{dL_B}{dt}\right)J_{\rm sep}(t),
\qquad
H_{\rm ret}(t)=\left(\frac{dL_B}{dt}\right)J_{\rm ret}(t),
$$
typically normalized for visualization.

### 11) Berry-rate and geometry proxies (Bloch-path based)

For a **unit Bloch direction** $\hat{\mathbf{n}}(t)=\mathbf{r}(t)/\|\mathbf{r}(t)\|$,
a discrete solid angle from three successive points $\hat{\mathbf{n}}_{k-1},\hat{\mathbf{n}}_k,\hat{\mathbf{n}}_{k+1}$ can be computed via:
$$
\Omega_k
=
2\,\arctan\!\left(
\frac{\det[\hat{\mathbf{n}}_{k-1},\hat{\mathbf{n}}_k,\hat{\mathbf{n}}_{k+1}]}
{1+\hat{\mathbf{n}}_{k-1}\!\cdot\!\hat{\mathbf{n}}_k+\hat{\mathbf{n}}_k\!\cdot\!\hat{\mathbf{n}}_{k+1}+\hat{\mathbf{n}}_{k+1}\!\cdot\!\hat{\mathbf{n}}_{k-1}}
\right).
$$

For spin‑$1/2$, the Berry phase increment magnitude proxy is:
$$
|\Delta\gamma_k|\approx \frac{|\Omega_k|}{2},
\qquad
\dot\gamma(t_k)\approx \frac{|\Delta\gamma_k|}{\Delta t}.
$$

A simple QGT-norm proxy and curvature proxy can be built from finite differences of $\hat{\mathbf{n}}(t)$, e.g.:
$$
\|\dot{\hat{\mathbf{n}}}\|^2 \approx \frac{\|\hat{\mathbf{n}}_{k}-\hat{\mathbf{n}}_{k-1}\|^2}{\Delta t^2},
\qquad
\kappa \approx \frac{\|\dot{\hat{\mathbf{n}}}\times \ddot{\hat{\mathbf{n}}}\|}{\|\dot{\hat{\mathbf{n}}}\|^3}
$$
(with careful regularization when $\|\dot{\hat{\mathbf{n}}}\|\to 0$)..

## “Boolean Linear Separator” note

The “Boolean Linear Separator” name references the fact that the prototype includes a **perceptron-style / thermodynamic-neuron-style** logic self-test for **linearly separable** boolean functions (e.g., NOT / NOR / 3‑MAJORITY).  
This is inspired by thermodynamic computing models that implement linearly separable functions with heat currents and auxiliary reservoirs.

---

## References (core)

- **Thermodynamic computing / thermodynamic neuron:**  
  Lipka‑Bartosik, Perarnau‑Llobet, Brunner, *Thermodynamic computing via autonomous quantum thermal machines*, **Science Advances** 10(36):eadm8792 (2024). DOI: 10.1126/sciadv.adm8792

- **Transmon qubit:**  
  Koch *et al.*, *Charge-insensitive qubit design derived from the Cooper pair box*, **Phys. Rev. A** 76, 042319 (2007). DOI: 10.1103/PhysRevA.76.042319

- **GKSL / Lindblad master equation:**  
  Gorini, Kossakowski, Sudarshan, *Completely positive dynamical semigroups of N-level systems*, **J. Math. Phys.** 17, 821 (1976). DOI: 10.1063/1.522979  
  Lindblad, *On the generators of quantum dynamical semigroups*, **Commun. Math. Phys.** 48, 119 (1976). DOI: 10.1007/BF01608499

- **Floquet theory:**  
  Shirley, *Solution of the Schrödinger equation with a Hamiltonian periodic in time*, **Phys. Rev.** 138, B979 (1965). DOI: 10.1103/PhysRev.138.B979  
  Sambe, *Steady states and quasienergies of a quantum-mechanical system in an oscillating field*, **Phys. Rev. A** 7, 2203 (1973). DOI: 10.1103/PhysRevA.7.2203

- **SU(2) Wigner / Stratonovich–Weyl phase space:**  
  Klimov, Romero, de Guise, *Generalized SU(2) covariant Wigner functions and some of their applications*, **J. Phys. A** 50, 323001 (2017). DOI: 10.1088/1751-8121/50/32/323001

- **OSEE:**  
  Prosen, Pižorn, *Operator space entanglement entropy in a transverse Ising chain*, **Phys. Rev. A** 76, 032316 (2007). DOI: 10.1103/PhysRevA.76.032316

- **Concurrence:**  
  Wootters, *Entanglement of formation of an arbitrary state of two qubits*, **Phys. Rev. Lett.** 80, 2245 (1998). DOI: 10.1103/PhysRevLett.80.2245

- **Log-negativity:**  
  Vidal, Werner, *Computable measure of entanglement*, **Phys. Rev. A** 65, 032314 (2002). DOI: 10.1103/PhysRevA.65.032314

- **Bures distance / fidelity:**  
  Uhlmann, *The “transition probability” in the state space of a *‑algebra*, **Rep. Math. Phys.** 9, 273 (1976). DOI: 10.1016/0034-4877(76)90060-4  
  Jozsa, *Fidelity for mixed quantum states*, **J. Mod. Opt.** 41, 2315 (1994). DOI: 10.1080/09500349414552171  
  Braunstein, Caves, *Statistical distance and the geometry of quantum states*, **Phys. Rev. Lett.** 72, 3439 (1994). DOI: 10.1103/PhysRevLett.72.3439

- **Thermodynamic length:**  
  Crooks, *Measuring thermodynamic length*, **Phys. Rev. Lett.** 99, 100602 (2007). DOI: 10.1103/PhysRevLett.99.100602  
  Scandi, Perarnau‑Llobet, *Thermodynamic length in open quantum systems*, **Quantum** 3, 197 (2019). DOI: 10.22331/q-2019-10-24-197

- **Berry phase:**  
  Berry, *Quantal phase factors accompanying adiabatic changes*, **Proc. R. Soc. A** 392, 45 (1984). DOI: 10.1098/rspa.1984.0023

- **QuTiP (optional numerical backend):**  
  Johansson, Nation, Nori, **Comput. Phys. Commun.** 183, 1760 (2012). DOI: 10.1016/j.cpc.2012.02.021  
  Johansson, Nation, Nori, **Comput. Phys. Commun.** 184, 1234 (2013). DOI: 10.1016/j.cpc.2012.11.019

---

## Disclaimer

This repository is **not** a hardware-validated transmon simulator and should not be treated as an engineering blueprint.  
It is a research/visualization prototype exploring ideas at the intersection of Floquet dynamics, open systems, and thermodynamic/information diagnostics.
