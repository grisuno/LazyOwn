from cli.commands.redteam_gym import RedTeamGymCommandSet


def test_gym_ms2_chains_lists_index(capsys):
    RedTeamGymCommandSet().do_gym_ms2("chains")
    out = capsys.readouterr().out
    assert "gym_metasploitable_ms2_dvwa_sqli" in out
    assert "ms2_dvwa_sqli" in out
