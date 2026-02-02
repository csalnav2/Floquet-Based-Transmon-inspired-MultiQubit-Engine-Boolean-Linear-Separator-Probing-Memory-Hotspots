## ⚛️ Physics & Mathematical Model

### 1. The Hamiltonian (Transmon Lattice)
The system consists of 4 Transmon qubits modeled as Duffing oscillators truncated to the qubit subspace, driven by time-dependent fields. The lattice Hamiltonian $H(t)$ is defined as:

$$H(t) = \sum_{j=1}^4 \left[ \frac{\omega_{01,j}(t)}{2} \sigma_z^{(j)} + \frac{\Omega_d(t)}{2} \left( \sigma_x^{(j)} \cos(\phi_j(t)) + \sigma_y^{(j)} \sin(\phi_j(t)) \right) \right] + H_{\text{int}}$$

The interaction term includes capacitive (exchange) and inductive coupling:

$$H_{\text{int}} = \sum_{\langle i,j \rangle} \left[ J_{\text{cap}} \, \left( \sigma_x^{(i)}\sigma_x^{(j)} + \sigma_y^{(i)}\sigma_y^{(j)} \right) + J_{\text{ind}} \, \sigma_z^{(i)}\sigma_z^{(j)} \right]$$

### 2. Open System Dynamics (GKSL)
The system evolves according to the Lindblad master equation:

$$\frac{d\rho}{dt} = -i [H(t), \rho] + \sum_{j=1}^4 \left( \gamma_{\downarrow,j} \mathcal{D}[\sigma_-^{(j)}] \rho + \gamma_{\uparrow,j} \mathcal{D}[\sigma_+^{(j)}] \rho + \gamma_{\phi,j} \mathcal{D}[\sigma_z^{(j)}] \rho \right)$$

where the dissipator is $\mathcal{D}[L]\rho = L\rho L^\dagger - \frac{1}{2}\{L^\dagger L, \rho\}$. The relaxation rates $\gamma_{\uparrow/\downarrow}$ obey detailed balance determined by the instantaneous bath temperature $T_b(t)$:

$$\frac{\gamma_{\uparrow}}{\gamma_{\downarrow}} = e^{-\Delta E / k_B T_b(t)}$$

### 3. Thermodynamic Diagnostics

* **Heat Current ($J$):** Local heat current flowing into qubit $j$:
    $$J_j(t) = \text{Tr}\left[ H(t) \mathcal{L}_j(\rho(t)) \right]$$
* **Otto Efficiency ($\eta$):** For a Floquet cycle with distinct strokes:
    $$\eta = \frac{W_{\text{out}}}{Q_{\text{hot}}} = \frac{-\oint \text{Tr}(\rho \dot{H}) dt}{\int_{\text{hot}} \text{Tr}(H \dot{\rho}_{\text{diss}}) dt}$$

### 4. Entanglement & Geometry

* **Logarithmic Negativity:** A computable measure of entanglement for mixed states:
    $$E_N(\rho) = \log_2 || \rho^{T_B} ||_1$$
* **OSEE (Operator-Space Entanglement Entropy):** Measures density matrix complexity:
    $$S_{\text{OSEE}} = - \sum_k s_k^2 \log_2 (s_k^2)$$
* **Geometric Phase Proxy:** Rate based on the solid angle $\Omega$ swept by the Bloch vector:
    $$\dot{\gamma}_g \propto \frac{1}{2} (1 - \cos \theta) \dot{\phi}$$

### 5. Boolean Linear Separation (Thermodynamic Logic)
The simulation tests for **thermodynamic neural processing**. The quantum lattice maps low-dimensional inputs into a high-dimensional Hilbert space (**Quantum Feature Lift**).

* **Linear Gates:** Tested on separable functions (AND, OR) via bath drives.
* **Non-Linear Upgrades (XOR):** Upgrades the readout to utilize non-linear metrics (Log-Negativity, $ZZ$-correlations) to solve non-linearly separable functions.

---

## 📊 Dashboard Visualization
The simulation generates high-resolution diagnostics (GIF/MP4):
1.  **3D Bloch Spheres:** Trajectories, "memory hotspot" trails, and leakage warnings.
2.  **Phase Space:** 3D Wigner function surfaces (single-qubit and collective).

3.  **Metrics:** Real-time Coherence, Purity, Bell-correlations, and Bures distance.
4.  **Thermodynamics:** Virtual temperatures, heat currents, and Otto efficiency.

---

## 🚀 Usage

To run the verification skeleton:
```bash
python Floquet_Transmon_MultiQubit_Engine_Boolean_Linear_Separator_PUBLIC_SKELETON.py

## 📚 References
Core Concepts

Thermodynamic Computing: Lipka‑Bartosik et al., Science Advances 10(36), 2024

Transmon Theory: Koch et al., Phys. Rev. A 76, 042319 (2007)

Lindblad Dynamics: Gorini et al., J. Math. Phys. 17, 821 (1976) | Lindblad, Commun. Math. Phys. 48, 119 (1976)

Floquet & Entanglement
Floquet Theory: Shirley, Phys. Rev. 138, B979 (1965) | Sambe, Phys. Rev. A 7, 2203 (1973)

Log-Negativity: Vidal & Werner, Phys. Rev. A 65, 032314 (2002)

OSEE: Prosen & Pižorn, Phys. Rev. A 76, 032316 (2007)

Berry Phase: Berry, Proc. R. Soc. A 392, 45 (1984)

Geometry & Fidelity
Fidelity: Uhlmann, Rep. Math. Phys. 9, 273 (1976) | Jozsa, J. Mod. Opt. 41, 2315 (1994)

Thermodynamic Length: Crooks, Phys. Rev. Lett. 99, 100602 (2007)

⚠️ Disclaimer: This is a research/visualization prototype exploring Floquet dynamics and thermodynamic diagnostics. It is not a hardware-validated engineering blueprint.

> **⚠️ Disclaimer** > This repository is **not** a hardware-validated transmon simulator and should not be treated as an engineering blueprint. It is a research/visualization prototype exploring ideas at the intersection of Floquet dynamics, open systems, and thermodynamic/information diagnostics.
