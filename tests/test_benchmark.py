import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from policy_assistant import benchmark
from policy_assistant.core import load_policies

class ResumeTests(unittest.TestCase):
    def test_resume_keeps_success_without_repeating_request(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            (root/'evaluation').mkdir()
            (root/'docs/data').mkdir(parents=True)
            (root/'COMPARISON.md').write_text('Paragraph one.\n\nParagraph two.\n')
            question={'id':'q01','question':'How many days may I work remotely?','expected_policy_ids':[],'category':'test','split':'test','expected_answer':'Manager approval required.'}
            (root/'evaluation/questions.json').write_text(json.dumps([question]))
            with patch.object(benchmark,'ROOT',root):
                first=benchmark.run(['rules'],0)
                before=json.loads((first/'results.json').read_text())
                with patch.object(benchmark,'rules_answer',side_effect=AssertionError('Successful result repeated')):
                    second=benchmark.run(['rules'],0,first.name)
                after=json.loads((second/'results.json').read_text())
                self.assertEqual(before['records'],after['records'])
                self.assertEqual(after['resumed_from'],first.name)
                self.assertEqual(json.loads((first/'results.json').read_text()),before)
