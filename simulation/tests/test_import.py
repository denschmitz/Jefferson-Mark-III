import jefferson_sim
import jefferson_sim.engine
import jefferson_sim.mesa_adapter


def test_simulation_package_imports() -> None:
    assert jefferson_sim.__version__ == "0.1.0"
