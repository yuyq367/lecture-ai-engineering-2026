from types import SimpleNamespace

from app import ask as ask_module


def test_ask_prints_input_and_output_token_counts(monkeypatch, capsys):
    class FakeClient:
        def __init__(self, api_key):
            self.models = self

        def generate_content(self, model, contents):
            return SimpleNamespace(
                text="回答",
                usage_metadata=SimpleNamespace(
                    prompt_token_count=12,
                    candidates_token_count=34,
                ),
            )

    monkeypatch.setattr(ask_module.genai, "Client", FakeClient)
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")

    assert ask_module.ask("質問") == "回答"
    output = capsys.readouterr().out
    assert "入力: 12" in output
    assert "出力: 34" in output