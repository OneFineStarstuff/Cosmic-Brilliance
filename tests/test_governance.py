import pytest
from src.governance_engine.gsri_scoring_engine import GSRIScoringEngine
from src.governance_engine.zkml_pipeline_verifier import ZKMLPipelineVerifier
from src.governance_engine.asa_drift_monitor import ASADriftMonitor
from src.infrastructure.pqc_worm_logger import PQCWormLogger

def test_gsri_scoring():
    engine = GSRIScoringEngine()
    telemetry = {"alignment_drift": 0.1, "compute_anomaly": 0.05}
    score = engine.calculate_gsri(telemetry)
    assert 0 <= score <= 100
    assert engine.evaluate_posture(score) in ["GREEN", "AMBER", "RED"]

def test_gsri_halt_threshold():
    engine = GSRIScoringEngine(alpha_prior=50, beta_prior=10)
    score = engine.calculate_gsri({"high_risk": 0.9})
    assert score > 40.0
    assert engine.should_halt(score) is True

def test_zkml_fairness_verification():
    verifier = ZKMLPipelineVerifier()
    test_results = {
        "selection_rates": {
            "group_A": 0.50,
            "group_B": 0.51,
            "group_C": 0.49
        }
    }
    is_fair = verifier.verify_demographic_parity("node_01", test_results, ["group_A", "group_B", "group_C"])
    assert is_fair is True
    assert "node_01" in verifier.get_attestation_report()["verified_nodes"]

def test_zkml_fairness_failure():
    verifier = ZKMLPipelineVerifier()
    test_results = {
        "selection_rates": {
            "group_A": 0.80,
            "group_B": 0.20
        }
    }
    is_fair = verifier.verify_demographic_parity("node_02", test_results, ["group_A", "group_B"])
    assert is_fair is False

def test_asa_cae_generation():
    monitor = ASADriftMonitor()
    context = {"top_feature": "latency", "confidence": 0.95, "goal": "performance"}
    cae = monitor.generate_cae("agent_x", context)
    assert cae["agent_id"] == "agent_x"
    assert "attribution" in cae
    assert cae["attribution"]["primary_driver"] == "latency"

def test_pqc_worm_logging():
    logger = PQCWormLogger()
    events = [{"event": "TEST_EVENT", "status": "OK"}]
    result = logger.commit_batch("batch_test", events)
    assert result["batch_id"] == "batch_test"
    assert result["status"] == "COMMITTED"
    assert len(result["hash"]) == 128  # SHA3-512 hex length

if __name__ == "__main__":
    pytest.main([__file__])
