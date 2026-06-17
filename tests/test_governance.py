import pytest
import hashlib
import json
import numpy as np
from src.governance_engine.gsri_scoring_engine import GSRIScoringEngine
from src.governance_engine.zkml_pipeline_verifier import ZKMLPipelineVerifier
from src.governance_engine.asa_drift_monitor import ASADriftMonitor, DecisionContext, AttributionScore
from src.infrastructure.pqc_worm_logger import PQCWormLogger

def test_gsri_scoring():
    engine = GSRIScoringEngine()
    telemetry = {"alignment_drift": 0.1, "compute_anomaly": 0.05}
    score = engine.calculate_gsri(telemetry)
    assert 0 <= score <= 100
    assert engine.evaluate_posture(score) in ["GREEN", "AMBER", "RED"]

def test_gsri_metrics():
    engine = GSRIScoringEngine()
    telemetry = {"alignment_drift": 0.1, "compute_anomaly": 0.05}
    metrics = engine.get_risk_metrics(telemetry)
    assert "gsri_score" in metrics
    assert "uncertainty_band" in metrics
    assert "as_of" in metrics
    assert metrics["gsri_score"] > 0

def test_gsri_halt_threshold():
    engine = GSRIScoringEngine(alpha_prior=50, beta_prior=10)
    score = engine.calculate_gsri({"high_risk": 0.9})
    assert score > 40.0
    assert engine.should_halt(score) is True

def test_zkml_fairness_verification():
    # Set lower min_sample_size for easier testing
    verifier = ZKMLPipelineVerifier(min_sample_size=10)
    test_results = {
        "selection_rates": {
            "group_A": 0.50,
            "group_B": 0.51,
            "group_C": 0.49
        },
        "sample_sizes": {
            "group_A": 20,
            "group_B": 20,
            "group_C": 20
        }
    }
    is_fair = verifier.verify_demographic_parity("node_01", test_results, ["group_A", "group_B", "group_C"])
    assert is_fair is True
    assert "node_01" in verifier.get_attestation_report()["verified_nodes"]

def test_zkml_fairness_insufficient_n():
    verifier = ZKMLPipelineVerifier(min_sample_size=100)
    test_results = {
        "selection_rates": {"group_A": 0.5, "group_B": 0.5},
        "sample_sizes": {"group_A": 50, "group_B": 50}
    }
    is_fair = verifier.verify_demographic_parity("node_low_n", test_results, ["group_A", "group_B"])
    assert is_fair is False

def test_zkml_fairness_failure():
    verifier = ZKMLPipelineVerifier(min_sample_size=10)
    test_results = {
        "selection_rates": {
            "group_A": 0.80,
            "group_B": 0.20
        },
        "sample_sizes": {
            "group_A": 20,
            "group_B": 20
        }
    }
    is_fair = verifier.verify_demographic_parity("node_02", test_results, ["group_A", "group_B"])
    assert is_fair is False

def test_zkml_multi_group_parity():
    verifier = ZKMLPipelineVerifier(min_sample_size=10)
    # Check that it catches bias in any group pair
    test_results = {
        "selection_rates": {
            "group_A": 0.50,
            "group_B": 0.52,
            "group_C": 0.65  # Bias here (>0.05 from A)
        },
        "sample_sizes": {"group_A": 20, "group_B": 20, "group_C": 20}
    }
    is_fair = verifier.verify_demographic_parity("node_multi", test_results, ["group_A", "group_B", "group_C"])
    assert is_fair is False

def test_asa_cae_generation():
    monitor = ASADriftMonitor()
    context: DecisionContext = {
        "model_version": "v1",
        "input_schema_version": "1.0",
        "regulatory_jurisdiction": "HK",
        "decision_timestamp": "2026-06-17",
        "goal": "test",
        "top_feature": "f1",
        "confidence": 0.9
    }
    attrs = [{"feature": "f1", "score": 1.0}]
    cae = monitor.generate_cae("agent_x", context, attrs)
    assert cae["agent_id"] == "agent_x"
    assert "attribution" in cae
    assert cae["attribution"]["primary_driver"] == "f1"
    assert "verificationHash" in cae

def test_asa_cae_integrity():
    monitor = ASADriftMonitor()
    context: DecisionContext = {
        "model_version": "v1",
        "input_schema_version": "1.0",
        "regulatory_jurisdiction": "HK",
        "decision_timestamp": "2026-06-17",
        "goal": "test",
        "top_feature": "f1",
        "confidence": 0.9
    }
    attrs = [{"feature": "f1", "score": 1.0}]
    cae = monitor.generate_cae("agent_hash", context, attrs)

    # Manually verify SHA-256
    verification_hash = cae.pop("verificationHash")
    payload_str = json.dumps(cae, sort_keys=True)
    expected_hash = hashlib.sha256(payload_str.encode()).hexdigest()
    assert verification_hash == expected_hash

def test_asa_cae_integrity_violation():
    monitor = ASADriftMonitor()
    context: DecisionContext = {
        "model_version": "v1",
        "input_schema_version": "1.0",
        "regulatory_jurisdiction": "HK",
        "decision_timestamp": "2026-06-17",
        "goal": "test",
        "top_feature": "f1",
        "confidence": 0.9
    }
    attrs = [{"feature": "f1", "score": 1.0}]
    cae = monitor.generate_cae("agent_tamper", context, attrs)

    orig_hash = cae["verificationHash"]

    # Tamper with context
    cae["context"]["confidence"] = 0.0

    # Verify new hash would be different
    tampered_cae = cae.copy()
    tampered_cae.pop("verificationHash")
    new_hash = hashlib.sha256(json.dumps(tampered_cae, sort_keys=True).encode('utf-8')).hexdigest()
    assert orig_hash != new_hash

def test_asa_cae_normalization_edge_case():
    monitor = ASADriftMonitor()
    context: DecisionContext = {
        "model_version": "v1", "input_schema_version": "1", "regulatory_jurisdiction": "",
        "decision_timestamp": "", "goal": "", "top_feature": "", "confidence": 0.0
    }
    # All zeros
    attrs = [{"feature": "f1", "score": 0.0}, {"feature": "f2", "score": 0.0}]
    cae = monitor.generate_cae("agent_zero", context, attrs)
    detailed = cae["detailed_attributions"]
    assert detailed[0]["score"] == 0.0
    assert detailed[1]["score"] == 0.0

def test_pqc_worm_logging():
    logger = PQCWormLogger()
    events = [{"event": "TEST_EVENT", "status": "OK"}]
    result = logger.commit_batch("batch_test", events)
    assert result["batch_id"] == "batch_test"
    assert result["status"] == "COMMITTED"
    assert len(result["hash"]) == 128  # SHA3-512 hex length

if __name__ == "__main__":
    pytest.main([__file__])
