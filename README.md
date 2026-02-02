# Floquet Transmon Multi-Qubit Engine & Boolean Linear Separator

A research-grade simulation prototype for a 4-qubit Transmon-inspired lattice. This project implements a **Floquet-driven open quantum system** to explore thermodynamic cycles, entanglement dynamics, and thermodynamic logic gates.

The system is modeled using the **GKSL (Gorini-Kossakowski-Sudarshan-Lindblad)** master equation, featuring tunable capacitive ($XX+YY$) and inductive ($ZZ$) couplings, periodic bath drives (Floquet engineering), and a "control daemon" for pulse shaping.

## 📂 Repository Structure

* **`Floquet_Transmon_MultiQubit_Engine_Boolean_Linear_Separator_PUBLIC_SKELETON.py`**
    * The public interface file. It contains the class structures, function signatures, and configuration dataclasses used in the private implementation. Use this to understand the data flow and physics models.
* *(Private)* `quantum_unified_revised_v136.py`
    * The full implementation (redacted) which performs the 16x16 density matrix evolution, renders the dashboard, and exports metrics.

---

## ⚛️ Physics & Mathematical Model

### 1. The Hamiltonian (Transmon Lattice)
The system consists of 4 Transmon qubits modeled as Duffing oscillators truncated to the qubit subspace, driven by time-dependent fields. The lattice Hamiltonian $H(t)$ is:

$$
H(t) = \sum_{j=1}^4 \left[ \frac{\omega_{01,j}(t)}{2} \sigma_z^{(j)} + \frac{\Omega_d(t)}{2} \left( \sigma_x^{(j)} \cos(\phi_j(t)) + \sigma_y^{(j)} \sin(\phi_j(t)) \right) \right] + H_{\text{int}}
$$

where the interaction term includes capacitive (exchange) and inductive coupling:

$$
H_{\text{int}} = \sum_{\langle i,j \rangle} \left[ J_{\text{cap}} \, \left( \sigma_x^{(i)}\sigma_x^{(j)} + \sigma_y^{(i)}\sigma_y^{(j)} \right) + J_{\text{ind}} \, \sigma_z^{(i)}\sigma_z^{(j)} \right]
$$
### 2. Open System Dynamics (GKSL)
The system evolves according to the Lindblad master equation:

$$
\frac{d\rho}{dt} = -i [H(t), \rho] + \sum_{j=1}^4 \left( \gamma_{\downarrow,j} \mathcal{D}[\sigma_-^{(j)}] \rho + \gamma_{\uparrow,j} \mathcal{D}[\sigma_+^{(j)}] \rho + \gamma_{\phi,j} \mathcal{D}[\sigma_z^{(j)}] \rho \right)
$$

where the dissipator is defined as $\mathcal{D}[L]\rho = L\rho L^\dagger - \frac{1}{2}\{L^\dagger L, \rho\}$. The relaxation rates $\gamma_{\uparrow/\downarrow}$ obey detailed balance determined by the instantaneous bath temperature $T_b(t)$:

$$
\frac{\gamma_{\uparrow}}{\gamma_{\downarrow}} = e^{-\Delta E / k_B T_b(t)}
$$

### 3. Thermodynamic Diagnostics

**Heat Current ($J$):**
We define the local heat current flowing into qubit $j$ as the change in energy due to the dissipative channel $\mathcal{L}_j$:

$$
J_j(t) = \text{Tr}\left[ H(t) \mathcal{L}_j(\rho(t)) \right]
$$

**Otto Efficiency ($\eta$):**
For a Floquet cycle with distinct "hot" and "cold" strokes, we approximate the efficiency using the work output $W_{\text{out}}$ and heat absorbed $Q_{\text{hot}}$:

$$
\eta = \frac{W_{\text{out}}}{Q_{\text{hot}}} = \frac{-\oint \text{Tr}(\rho \dot{H}) dt}{\int_{\text{hot}} \text{Tr}(H \dot{\rho}_{\text{diss}}) dt}
$$

### 4. Entanglement & Geometry

**Logarithmic Negativity:**
A computable measure of entanglement for mixed states (e.g., Q1 vs Q2):

$$
E_N(\rho) = \log_2 || \rho^{T_B} ||_1
$$

**OSEE (Operator-Space Entanglement Entropy):**
Measures the complexity of the density matrix itself by Schmidt-decomposing the operator $|\rho\rangle\rangle$ in Liouville space:

$$
S_{\text{OSEE}} = - \sum_k s_k^2 \log_2 (s_k^2)
$$

**Geometric Phase Proxy:**
We compute a proxy for the geometric phase rate $\dot{\gamma}_g$ based on the solid angle $\Omega$ swept by the Bloch vector $\vec{r}(t)$:

$$
\dot{\gamma}_g \propto \frac{1}{2} (1 - \cos \theta) \dot{\phi} \approx \frac{1}{2} \text{SolidAngle}(\vec{r}_t, \vec{r}_{t+\delta})
$$

### 5. Boolean Linear Separation (Thermodynamic Logic)
The simulation includes a test for **thermodynamic neural processing**. A physical system acts as a perceptron if its steady-state or limit-cycle observable $O$ (e.g., excited population) separates input classes $u \in \{0,1\}^N$ via a hyperplane:

$$
O(u) \approx \sigma \left( \vec{w} \cdot \vec{u} + b \right)
$$

We test this by encoding inputs into the bath drives of Q1/Q2 and measuring if the lattice response can classify linearly separable logic gates (AND, OR) versus non-linear ones (XOR).

---

## 📊 Dashboard Visualization
The code generates a high-resolution dashboard (GIF/MP4) containing:
1.  **3D Bloch Spheres:** With trajectories, "memory hotspot" trails, and leakage warnings.
2.  **Phase Space:** 3D Wigner function surfaces (single-qubit and collective).
3.  **Metrics:** Real-time plots of Coherence, Purity, Bell-correlations, and Bures distance.
4.  **Thermodynamics:** Virtual temperatures, heat currents, and Otto efficiency.

We test this by encoding inputs into the bath drives of Q1/Q2 and measuring if the lattice response can classify linearly separable logic gates (AND, OR) versus non-linear ones (XOR).

---

## 📊 Dashboard Visualization
The code generates a high-resolution dashboard (GIF/MP4) containing:
1.  **3D Bloch Spheres:** With trajectories, "memory hotspot" trails, and leakage warnings.
2.  **Phase Space:** 3D Wigner function surfaces (single-qubit and collective).
3.  **Metrics:** Real-time plots of Coherence, Purity, Bell-correlations, and Bures distance.
4.  **Thermodynamics:** Virtual temperatures, heat currents, and Otto efficiency.

---

## 🚀 Usage

To run the skeleton file (verification only):
```bash
python Floquet_Transmon_MultiQubit_Engine_Boolean_Linear_Separator_PUBLIC_SKELETON.py

## 📚 References (Core)

**Thermodynamic Computing & Neurons**
* Lipka‑Bartosik, Perarnau‑Llobet, Brunner. *Thermodynamic computing via autonomous quantum thermal machines*. **Science Advances** 10(36):eadm8792 (2024).  
    [DOI: 10.1126/sciadv.adm8792](https://doi.org/10.1126/sciadv.adm8792)

**Transmon Qubit Theory**
* Koch et al. *Charge-insensitive qubit design derived from the Cooper pair box*. **Phys. Rev. A** 76, 042319 (2007).  
    [DOI: 10.1103/PhysRevA.76.042319](https://doi.org/10.1103/PhysRevA.76.042319)

**Open Systems (GKSL / Lindblad)**
* Gorini, Kossakowski, Sudarshan. *Completely positive dynamical semigroups of N-level systems*. **J. Math. Phys.** 17, 821 (1976).  
    [DOI: 10.1063/1.522979](https://doi.org/10.1063/1.522979)
* Lindblad. *On the generators of quantum dynamical semigroups*. **Commun. Math. Phys.** 48, 119 (1976).  
    [DOI: 10.1007/BF01608499](https://doi.org/10.1007/BF01608499)

**Floquet Theory**
* Shirley. *Solution of the Schrödinger equation with a Hamiltonian periodic in time*. **Phys. Rev.** 138, B979 (1965).  
    [DOI: 10.1103/PhysRev.138.B979](https://doi.org/10.1103/PhysRev.138.B979)
* Sambe. *Steady states and quasienergies of a quantum-mechanical system in an oscillating field*. **Phys. Rev. A** 7, 2203 (1973).  
    [DOI: 10.1103/PhysRevA.7.2203](https://doi.org/10.1103/PhysRevA.7.2203)

**Entanglement & Geometry Diagnostics**
* **OSEE:** Prosen, Pižorn. *Operator space entanglement entropy in a transverse Ising chain*. **Phys. Rev. A** 76, 032316 (2007).  
    [DOI: 10.1103/PhysRevA.76.032316](https://doi.org/10.1103/PhysRevA.76.032316)
* **Concurrence:** Wootters. *Entanglement of formation of an arbitrary state of two qubits*. **Phys. Rev. Lett.** 80, 2245 (1998).  
    [DOI: 10.1103/PhysRevLett.80.2245](https://doi.org/10.1103/PhysRevLett.80.2245)
* **Log-negativity:** Vidal, Werner. *Computable measure of entanglement*. **Phys. Rev. A** 65, 032314 (2002).  
    [DOI: 10.1103/PhysRevA.65.032314](https://doi.org/10.1103/PhysRevA.65.032314)
* **Berry Phase:** Berry. *Quantal phase factors accompanying adiabatic changes*. **Proc. R. Soc. A** 392, 45 (1984).  
    [DOI: 10.1098/rspa.1984.0023](https://doi.org/10.1098/rspa.1984.0023)

**Fidelity & Metric Geometry**
* Uhlmann. *The “transition probability” in the state space of a C*-algebra*. **Rep. Math. Phys.** 9, 273 (1976).  
    [DOI: 10.1016/0034-4877(76)90060-4](https://doi.org/10.1016/0034-4877(76)90060-4)
* Jozsa. *Fidelity for mixed quantum states*. **J. Mod. Opt.** 41, 2315 (1994).  
    [DOI: 10.1080/09500349414552171](https://doi.org/10.1080/09500349414552171)
* **Thermodynamic Length:** Crooks. *Measuring thermodynamic length*. **Phys. Rev. Lett.** 99, 100602 (2007).  
    [DOI: 10.1103/PhysRevLett.99.100602](https://doi.org/10.1103/PhysRevLett.99.100602)

---

> **⚠️ Disclaimer** > This repository is **not** a hardware-validated transmon simulator and should not be treated as an engineering blueprint. It is a research/visualization prototype exploring ideas at the intersection of Floquet dynamics, open systems, and thermodynamic/information diagnostics.
