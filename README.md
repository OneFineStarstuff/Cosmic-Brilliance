# Omni-Sentinel Cognitive Execution Environment 🌌

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14652254.svg)](https://doi.org/10.5281/zenodo.14652254)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Security Policy](https://img.shields.io/badge/Security-Policy-blue.svg)](SECURITY.md)

Omni-Sentinel is a high-assurance governance and execution framework designed for cognitive agents and AI systems. It provides a multi-layered defense-in-depth architecture (The G-Stack) anchored in hardware trust, Bayesian risk monitoring, and post-quantum cryptographic (PQC) audit trails.

## 🚀 Overview

The system is built to ensure that cognitive tasks are executed within safe, measurable, and immutable boundaries. It integrates advanced hardware attestation with real-time risk scoring to mitigate alignment drift and systemic risks.

## 🏗️ Architecture (The G-Stack)

1.  **Hardware Root of Trust**: TEE/TPM with PCR_MATCH enforcement. Verifies the integrity of the execution environment.
2.  **Cognitive Control Plane**: Bayesian G-SRI (Global Systemic Risk Index) scoring engine regulating model execution based on real-time telemetry.
3.  **Immutable Evidence Store**: PQC-signed (ML-DSA / CRYSTALS-Dilithium) WORM (Write-Once-Read-Many) audit logs stored in an immutable substrate.

## 📁 Project Structure

- `src/governance_engine/`: Core Bayesian scoring and ZKML fairness verification logic.
- `src/infrastructure/`: Hardware attestation and PQC-signed immutable logging.
- `REPORTS/`: Comprehensive regulatory gap analysis and compliance reports.
- `tests/`: Automated test suite for validating governance logic and fairness proofs.

## 🛠️ Getting Started

### Prerequisites

- Python 3.10+
- NumPy, SciPy (for Bayesian engine)
- `oqs-python` / `liboqs` (for ML-DSA signing)
- `pytest` (for testing)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/OneFineStarstuff/Cosmic-Brilliance.git
   cd Cosmic-Brilliance
   ```

2. Install dependencies:
   ```bash
   pip install numpy scipy oqs-python pytest
   ```

### Usage

#### G-SRI Scoring
```python
from src.governance_engine.gsri_scoring_engine import GSRIScoringEngine

engine = GSRIScoringEngine()
telemetry = {"alignment_drift": 0.1, "compute_anomaly": 0.05}
gsri = engine.calculate_gsri(telemetry)
print(f"G-SRI: {gsri}")
```

#### PQC-WORM Logging
```python
from src.infrastructure.pqc_worm_logger import PQCWormLogger

logger = PQCWormLogger()
logger.commit_batch("batch_001", [{"event": "GSRI_CHECK", "value": 15.5}])
```

## 🧪 Testing

Run the test suite:

```bash
python3 -m pytest tests/test_governance.py
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute. Security-sensitive changes to cryptographic modules require mandatory peer review.

## 📝 Citation

If you use this software in your research, please cite it as follows:

```bibtex
@software{omni_sentinel_2026,
  author = {One Fine Starstuff},
  title = {Omni-Sentinel Cognitive Execution Environment},
  version = {1.1.0},
  year = {2026},
  url = {https://github.com/OneFineStarstuff/Cosmic-Brilliance},
  doi = {10.5281/zenodo.14652254}
}
```
