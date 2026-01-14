"""
Floquet Transmon-Lattice Engine with Thermodynamic-Neuron Readout (Boolean Linear Separator)

Simulates Floquet-driven qubits with time-dependent dissipation and produces
a dashboard of entanglement + information geometry + thermodynamic proxies.
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Floquet-Based Transmon-Inspired MultiQubit Engine — Boolean Linear Separator

Public skeleton (structure only): implementation bodies intentionally removed.

Source file (private): quantum_unified_revised_v109_complete.py

Original module description (kept for context):
quantum_unified_revised_v109.py

v89.1 FINAL FINAL:
- Robust ngrok shutdown (Ctrl+C safe)
- timezone-aware UTC timestamps for plot-data manifests


4-Qubit (16×16) Transmon-Lattice Dashboard with:

- Full GLOBAL density-matrix evolution (16×16) so genuine entanglement can exist.
- Pairwise log-negativity traces for all 6 qubit pairs, computed from the global state.
- OSEE (Operator-Space Entanglement Entropy) replacing Von Neumann entropy in diagnostics.
- Bures-length rate + lagged-Bures "memory current" hotspot diagnostics (ported from bures_hotspots.py).
- J_cap (capacitive / exchange-like XX+YY) and J_ind (inductive / ZZ) couplings.
- A lightweight "ControlDaemon" that can do GRAPE-ish pulse shaping (SPSA gradient ascent)
  to improve coherence / QFI and reduce memory loss. (Optional; disabled by default.)

Dependencies:
  pip install numpy matplotlib

Optional (for prettier Wigner plots):
  pip install qutip

Optional (for faster GIF writing):
  pip install imageio

Optional (for sharing dashboard):
  pip install pyngrok

Run:
  python quantum_unified_revised_v89_1_final_final.py

v89.1 FINAL FINAL:
- Robust ngrok shutdown (Ctrl+C safe)
- timezone-aware UTC timestamps for plot-data manifests
 --mode lattice --bath_enable

Run with daemon optimization (slow):
  python quantum_unified_revised_v89_1_final_final.py

v89.1 FINAL FINAL:
- Robust ngrok shutdown (Ctrl+C safe)
- timezone-aware UTC timestamps for plot-data manifests
 --mode lattice --bath_enable --daemon

Notes:
- This is a research-grade *prototype*. "GRAPE" here is implemented as a
  GRAPE-style *gradient ascent on piecewise-constant pulses*, using SPSA
  (finite-simulations gradient estimates). It is not a full analytic-gradient
  open-system GRAPE implementation.
- Berry curvature/QGT for mixed states is subtle. We provide a *proxy* based on
  Bloch-sphere geometry of the lattice-mean Bloch direction.
"""
from __future__ import annotations
import argparse
import sys
import json
import math
import socketserver
import threading
import time
import shutil
import subprocess
import signal
import os
import datetime
from contextlib import contextmanager, nullcontext
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from mpl_toolkits.mplot3d import Axes3D
HAVE_QUTIP = False
try:
    from qutip import Qobj
    from qutip.wigner import wigner as qutip_wigner
    HAVE_QUTIP = True
except Exception:
    Qobj = None
    qutip_wigner = None
HAVE_IMAGEIO = False
try:
    import imageio
    HAVE_IMAGEIO = True
except Exception:
    imageio = None
HAVE_NGROK = False
try:
    from pyngrok import ngrok
    HAVE_NGROK = True
except Exception:
    ngrok = None
kB = 1.380649e-23
h = 6.62607015e-34
Id2 = ...
sigma_x = ...
sigma_y = ...
sigma_z = ...
BLOCH_SCALE = 3.5
BLOCH_RADIUS = ...
BLOCH_AXIS_LIM = ...
BLOCH_ZOOM = 4.8
BLOCH_VEC_LW = ...
BLOCH_TRAIL_LW = ...
BLOCH_TRAIL_ALPHA = 0.9
DASHBOARD_TITLE_FS = 42
BLOCH_QTITLE_FS = 24
BLOCH_SUBTITLE_FS = 24
BLOCH_INFO_FS = 16
PANEL_TITLE_FS = 13
PLOT_TITLE_FS = ...
SMALL_TITLE_FS = 11
LEGEND_FS = 9
TICK_FS = 9
DENSITY_HEIGHT_SCALE = 1.1
QUBIT_COLORS = ...
TL_COLORS = ...
COLOR_PHASE_BAR = '#A6D6FF'
COLOR_PHASE_DOT = '#0055A4'
COLOR_DENS_BAR = '#800000'
COLOR_DENS_EDGE = 'black'

def _herm(mat: np.ndarray) -> np.ndarray:
    ...

def ewma(x: np.ndarray, alpha: float) -> np.ndarray:
    ...

def _static_ylim(arrays, positive_floor: bool=False, pad: float=0.1):
    ...

def find_peak_indices(y: np.ndarray, *, thr: float=0.6, max_peaks: int=12, top_k: Optional[int]=None, min_sep: int=4) -> np.ndarray:
    ...

@contextmanager
def _sigint_guard(ignore_sigint: bool=True):
    ...

def convert_gif_to_mp4(gif_path: str, *, mp4_path: Optional[str]=None, fps_out: int=40, fps: Optional[int]=None, fps_in: Optional[int]=None, crf: int=18, preset: str='medium', interpolate: bool=False, scale: Optional[int]=None, overwrite: bool=True) -> Optional[str]:
    ...

def _ffmpeg_bin() -> Optional[str]:
    ...

def compile_mp4_from_frames(frames_dir: Path, mp4_path: str, *, fps: int=18, crf: int=18, preset: str='medium', thread_queue_size: int=512, overwrite: bool=True) -> Optional[str]:
    ...

def compile_gif_from_frames(frames_dir: Path, gif_path: str, *, fps: int=18, thread_queue_size: int=512, overwrite: bool=True) -> Optional[str]:
    ...

def _ensure_dir(p: Path) -> Path:
    ...

def _to_serializable(x):
    ...

def write_series_csv_json(out_dir: Path, name: str, series: Dict[str, np.ndarray], *, meta: Optional[Dict]=None) -> Tuple[str, str]:
    ...

def write_matrix_csv_json(out_dir: Path, name: str, mat: np.ndarray, *, x: Optional[np.ndarray]=None, y: Optional[np.ndarray]=None, meta: Optional[Dict]=None) -> Tuple[str, str]:
    ...

def export_dashboard_plot_data(out_base: Path, *, t: np.ndarray, blochs: np.ndarray, phases: np.ndarray, cohs: np.ndarray, pes: np.ndarray, pur: np.ndarray, qfi: np.ndarray, bures_all: np.ndarray, choi_purity: np.ndarray, choi_lambda_min: np.ndarray, echo: np.ndarray, osee: np.ndarray, Sigma: np.ndarray, mi_01_23: np.ndarray, logneg: np.ndarray, concurrence: np.ndarray, spec_01: np.ndarray, berry_norm: np.ndarray, qgt_norm: np.ndarray, curv_norm: np.ndarray, dLBdt_global: np.ndarray, Jsep_memloss: np.ndarray, Jret_memgain: np.ndarray, Jsep_qubit_raw: np.ndarray, Jsep_qubit_norm: np.ndarray, Jret_qubit_raw: np.ndarray, Jret_qubit_norm: np.ndarray, Dlag_global: np.ndarray, Hhot_norm: np.ndarray, Hret_norm: np.ndarray, ent_cycle: np.ndarray, cycle_times: np.ndarray, export_wigner: bool=False, wigner_snapshots: int=3, rho_red: Optional[np.ndarray]=None, trans_w01: Optional[np.ndarray]=None, trans_alpha: Optional[np.ndarray]=None, trans_EJ_over_EC: Optional[np.ndarray]=None, trans_leak_risk: Optional[np.ndarray]=None, fid_global: Optional[np.ndarray]=None, otoc_floquet: Optional[np.ndarray]=None, scramble_floquet: Optional[np.ndarray]=None, otto_eta_q: Optional[np.ndarray]=None, otto_eta_lattice: Optional[np.ndarray]=None, otto_Qhot_q: Optional[np.ndarray]=None, otto_Qcold_q: Optional[np.ndarray]=None, otto_Wout_q: Optional[np.ndarray]=None, otto_Qhot_lattice: Optional[np.ndarray]=None, otto_Qcold_lattice: Optional[np.ndarray]=None, otto_Wout_lattice: Optional[np.ndarray]=None, heat_J: Optional[np.ndarray]=None, heat_J_lattice: Optional[np.ndarray]=None) -> None:
    ...

def kron_all(ops: Sequence[np.ndarray]) -> np.ndarray:
    ...

def op_on_qubit(op2: np.ndarray, q: int, n_qubits: int) -> np.ndarray:
    ...

def partial_trace(rho: np.ndarray, keep: Sequence[int], dims: Sequence[int]) -> np.ndarray:
    ...

def bloch_vector(rho: np.ndarray) -> np.ndarray:
    ...

def fidelity_qubit_from_bloch(r: np.ndarray, s: np.ndarray) -> np.ndarray:
    ...

def bures_distance_from_fidelity(F: np.ndarray) -> np.ndarray:
    ...

def bures_distance_qubit_from_bloch(r: np.ndarray, s: np.ndarray) -> np.ndarray:
    ...

def fidelity_qubit_bloch(rho: np.ndarray, sigma: np.ndarray) -> float:
    ...

def bures_angle_qubit(rho: np.ndarray, sigma: np.ndarray) -> float:
    ...

@dataclass(frozen=True)
class HotspotMetricsBloch:
    dLB_dt: np.ndarray
    D_lag: np.ndarray
    J_sep: np.ndarray
    J_ret: np.ndarray
    H_sep_norm: np.ndarray

def compute_hotspot_metrics_bloch(ts: np.ndarray, vec: np.ndarray, *, tau_steps: int=35, smooth_alpha: float=0.2) -> HotspotMetricsBloch:
    ...

def qfi_state_sensitivity_qubit(rho: np.ndarray, G: np.ndarray) -> float:
    ...

def virtual_temperature_from_pe(pe: float, DeltaE: float) -> float:
    ...

def berry_phase_rate_proxy_from_bloch(vec: np.ndarray, dt: float) -> np.ndarray:
    ...

def qgt_metric_proxy_from_bloch(vec: np.ndarray, dt: float) -> np.ndarray:
    ...

def curvature_proxy_from_path(vec: np.ndarray, dt: float) -> np.ndarray:
    ...

def sqrtm_psd(mat: np.ndarray) -> np.ndarray:
    ...

def fidelity_general(rho: np.ndarray, sigma: np.ndarray) -> float:
    ...

def bures_distance_general(rho: np.ndarray, sigma: np.ndarray) -> float:
    ...

def osee_bits(rho: np.ndarray, cut: int, dims: Sequence[int]) -> float:
    ...

def partial_transpose_twoqubit(rho: np.ndarray, sys: int=1, dims: Tuple[int, int]=(2, 2)) -> np.ndarray:
    ...

def log_negativity(rho_ab: np.ndarray, sys: int=1, base: float=2.0) -> float:
    ...

@dataclass
class SeriesStats:
    max: float
    argmax: int
    area: float

def _series_stats(x: np.ndarray, t: Optional[np.ndarray]=None) -> SeriesStats:
    ...

def vn_entropy_bits(rho: np.ndarray) -> float:
    ...

def partial_transpose_general(rho: np.ndarray, sys: Tuple[int, ...], dims: Tuple[int, ...]) -> np.ndarray:
    ...

def log_negativity_general(rho: np.ndarray, sys: Tuple[int, ...], dims: Tuple[int, ...]) -> float:
    ...

def log_negativity_pairs(rho: np.ndarray, dims: Tuple[int, ...]) -> Dict[Tuple[int, int], float]:
    ...

def concurrence_two_qubit(rho_2: np.ndarray) -> float:
    ...

def concurrence_pairs(rho: np.ndarray, dims: Tuple[int, ...]) -> Dict[Tuple[int, int], float]:
    ...

def mutual_information(rho: np.ndarray, A: List[int], B: List[int], dims: Tuple[int, ...]) -> float:
    ...

def entanglement_spectrum(rho: np.ndarray, A: List[int], dims: Tuple[int, ...]) -> np.ndarray:
    ...

def series_log_negativity_pair_mean(rhos: Sequence[np.ndarray], dims: Tuple[int, ...], t: Optional[np.ndarray]=None):
    ...

def series_concurrence_pair_mean(rhos: Sequence[np.ndarray], dims: Tuple[int, ...], t: Optional[np.ndarray]=None):
    ...

def series_mutual_info(rhos: Sequence[np.ndarray], A: List[int], B: List[int], dims: Tuple[int, ...], t: Optional[np.ndarray]=None):
    ...

def run_entanglement_unit_tests(verbose: bool=True) -> None:
    ...

@dataclass(frozen=True)
class HotspotMetricsDensity:
    dLB_dt: np.ndarray
    D_lag: np.ndarray
    dD_lag_dt: np.ndarray
    J_sep: np.ndarray
    J_ret: np.ndarray
    H_sep_norm: np.ndarray
    H_ret_norm: np.ndarray

def compute_hotspot_metrics_density(ts: np.ndarray, rhos: np.ndarray, *, tau_steps: int=35, smooth_alpha: float=0.2) -> HotspotMetricsDensity:
    ...

@dataclass
class GKSLParams:
    Omega0: float = 4.0
    Omega_drive: float = 2.2
    phi_drive: float = 0.0
    phi_rate: float = 0.35
    DeltaE: float = ...
    gam_relax: float = 0.055
    gamma_phi: float = 0.06
    T_bath: float = 0.01
    dt: float = 0.02
    tmax: float = 12.0
    psi0: np.ndarray = ...
    noise_enable: bool = True
    noise_strength: float = 0.16
    noise_tau: float = 0.9
    drift_strength: float = 0.08
    seed: int = 0
    reset_enable: bool = True
    reset_period: float = 4.0
    reset_width: float = 0.8
    reset_phase: float = 0.0
    transmon_EC: float = 0.2
    transmon_flux_amp: float = 0.12
    transmon_flux_use_bath: bool = True

@dataclass
class BathSchedule:
    enable: bool = True
    period: float = 4.0
    duty: float = 0.35
    amp_T: float = 0.04
    amp_gamma: float = 0.35
    amp_drive: float = 0.3
    gamma_scale: float = 1.0
    drive_scale: float = 1.0
    waveform: str = 'square'
    phase_per_qubit: float = ...
    global_phase: float = 0.0

    def wave(self, t: float, q_index: int=0) -> float:
        ...

@dataclass
class CouplingParams:
    """Two-qubit couplings for the 4-qubit lattice."""
    J_cap: float = 0.1
    J_ind: float = 0.06
    ent_boost: float = 20.0
    ent_pulse_amp: float = 0.4
    adjacency: np.ndarray = ...

@dataclass
class PulseSchedule:
    """Piecewise-constant amplitude modulation per qubit:"""
    n_qubits: int
    n_pulses: int
    tmax: float
    amp: np.ndarray
    amp_clip: float = 0.8

    def __post_init__(self):
        ...

    def amp_at(self, t: float) -> np.ndarray:
        ...

@dataclass
class DaemonConfig:
    enable: bool = False
    iterations: int = 12
    n_pulses: int = 24
    seed: int = 0
    a: float = 0.2
    c: float = 0.08
    alpha: float = 0.602
    gamma: float = 0.101
    optimize_pulses: bool = True
    optimize_gamma_phi: bool = True
    optimize_noise_strength: bool = True
    gamma_phi_scale_bounds: Tuple[float, float] = ...
    noise_scale_bounds: Tuple[float, float] = ...
    w_coh: float = 1.0
    w_qfi: float = 0.6
    w_ent: float = 0.8
    w_memloss: float = 0.6
    w_osee: float = 0.1
    w_bures_speed: float = 0.1
    w_entangled_bures: float = 0.08
    w_berry_var: float = 0.02
    w_pulse_l2: float = 0.02

@dataclass
class LatticeOps:
    n: int
    dims: List[int]
    I: np.ndarray
    sx: List[np.ndarray]
    sy: List[np.ndarray]
    sz: List[np.ndarray]
    sm: List[np.ndarray]
    sp: List[np.ndarray]
    P0: List[np.ndarray]
    P1: List[np.ndarray]
    edges: List[Tuple[int, int]]
    XXpYY: List[np.ndarray]
    ZZ: List[np.ndarray]

def build_lattice_ops(n_qubits: int, adjacency: np.ndarray) -> LatticeOps:
    ...

def _coherent_unitary_from_H(H: np.ndarray, dt: float) -> np.ndarray:
    ...

def _apply_dephase_full(rho: np.ndarray, p: float, Z_i: np.ndarray) -> np.ndarray:
    ...

def _apply_amp_down_full(rho: np.ndarray, g: float, P0_i: np.ndarray, P1_i: np.ndarray, sm_i: np.ndarray) -> np.ndarray:
    ...

def _apply_amp_up_full(rho: np.ndarray, g: float, P0_i: np.ndarray, P1_i: np.ndarray, sp_i: np.ndarray) -> np.ndarray:
    ...

def _kraus_dephase_qubit(p: float) -> List[np.ndarray]:
    ...

def _kraus_amp_down_qubit(g: float) -> List[np.ndarray]:
    ...

def _kraus_amp_up_qubit(g: float) -> List[np.ndarray]:
    ...

def _compose_kraus_chain(maps: List[List[np.ndarray]]) -> List[np.ndarray]:
    ...

def _choi_from_kraus(kraus_ops: List[np.ndarray]) -> np.ndarray:
    ...

def _choi_purity_from_kraus(kraus_ops: List[np.ndarray]) -> float:
    ...

def _choi_lambda_min_from_kraus(kraus_ops: List[np.ndarray]) -> float:
    ...

def _make_initial_global_state(base_p: GKSLParams, n_qubits: int) -> np.ndarray:
    ...

def _make_per_qubit_params(base_p: GKSLParams, n_qubits: int) -> List[GKSLParams]:
    ...

def evolve_lattice_global(base_p: GKSLParams, bath: BathSchedule, couplings: CouplingParams, *, pulse: Optional[PulseSchedule]=None, gamma_phi_scales: Optional[np.ndarray]=None, noise_scales: Optional[np.ndarray]=None, n_qubits: int=4, store_global_rho: bool=True) -> Dict[str, np.ndarray]:
    ...

def _pack_theta(pulse_amp: np.ndarray, gamma_phi_scales: np.ndarray, noise_scales: np.ndarray, cfg: DaemonConfig) -> np.ndarray:
    ...

def _unpack_theta(theta: np.ndarray, n_qubits: int, n_pulses: int, cfg: DaemonConfig) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    ...

def _clip_knobs(pulse_amp: np.ndarray, gamma_phi_scales: np.ndarray, noise_scales: np.ndarray, cfg: DaemonConfig) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    ...

def compute_objective(res: Dict[str, np.ndarray], cfg: DaemonConfig) -> float:
    ...

def run_control_daemon_spsa(base_p: GKSLParams, bath: BathSchedule, couplings: CouplingParams, cfg: DaemonConfig, *, n_qubits: int=4) -> Tuple[PulseSchedule, np.ndarray, np.ndarray]:
    ...

def _make_bloch_sphere(ax, color: str):
    ...

class BlochTrail3D:
    """A simple 3D trail inside a Bloch sphere."""

    def __init__(self, ax, color: str, *, enable: bool=True):
        ...

    def clear(self):
        ...

    def update(self, pt: np.ndarray):
        ...
HOTSPOT_LOSS_COLOR = 'tab:purple'
HOTSPOT_GAIN_COLOR = 'magenta'
HOTSPOT_COLOR = ...
HOTSPOT_TRAIL_LW_BASE = 2.0
HOTSPOT_TRAIL_LW_SCALE = 6.0
HOTSPOT_TRAIL_ALPHA = 0.95
HOTSPOT_VIS_EXP = 1.8
HOTSPOT_MAX_SEGMENTS = 1200

class HotspotTrail3D:
    """Draw only the 'hot' segments of a 3D trajectory as a separate overlay."""

    def __init__(self, ax, *, enable: bool=True, color: str=HOTSPOT_COLOR, max_segments: int=HOTSPOT_MAX_SEGMENTS, lw_base: float=HOTSPOT_TRAIL_LW_BASE, lw_scale: float=HOTSPOT_TRAIL_LW_SCALE, alpha: float=HOTSPOT_TRAIL_ALPHA):
        ...

    def clear(self):
        ...

    def add_segment(self, p0: np.ndarray, p1: np.ndarray, intensity: float):
        ...

class Wigner3DHelper:

    def __init__(self, ax, title: Optional[str]=None, zoom_dist: float=1.4, N: int=72, N_ho: int=14, d_max: Optional[int]=None, xlim: Tuple[float, float]=(-3.5, 3.5), plim: Tuple[float, float]=(-3.5, 3.5), smooth_alpha: float=0.35, interp_frames: int=2, enable: bool=True, zlim: Tuple[float, float]=(-0.4, 0.4)):
        ...

    @staticmethod
    def _gen_laguerre(n: int, k: int, x: np.ndarray) -> np.ndarray:
        ...

    def _precompute_wigner_basis(self) -> None:
        ...

    def _compute_wigner(self, rho: np.ndarray) -> Optional[np.ndarray]:
        ...

    def update(self, rho2: np.ndarray, *, compute_target: bool=True) -> None:
        ...

def animate_lattice_dashboard(base_p: GKSLParams, out_gif: str, bath: BathSchedule, couplings: CouplingParams, *, daemon_cfg: Optional[DaemonConfig]=None, fps: int=18, fps_out: Optional[int]=None, dpi: int=72, fig_w: float=32.0, fig_h: float=18.0, viz_scale: float=1.0, height_boost: float=1.1, render_skip: int=2, enable_wigner: bool=True, wigner_every: int=5, wigner_N_qubit: int=72, wigner_N_collective: int=84, wigner_smooth_alpha: float=0.55, heartbeat_s: float=20.0, render_frames: bool=True, resume_frames: bool=True, keep_frames: bool=False, hotspot_thr: float=0.7, leak_warn: float=0.0625, leak_warn_frac: float=0.7, enable_hotspot_trails: bool=True, enable_hotspot_flares: bool=True, enable_hotspot_tl: bool=True, export_plot_data: bool=True, export_wigner_snapshots: int=3, show_choi_per_qubit: bool=False, ignore_sigint: bool=True) -> str:
    ...

def write_plot_data_index(out_dir: Path, plot_dir: Path, stem: str) -> Tuple[Optional[str], Optional[str]]:
    ...

def thermodynamic_neuron_logic_tests() -> Dict[str, Dict]:
    ...

def write_index_html(out_dir: Path, gif_name: str, logic_data: Dict[str, Dict], mp4_name: Optional[str]=None) -> None:
    ...

def start_server(path: Path, port: int=8000):
    ...

def main():
    ...
if __name__ == '__main__':
    ...
