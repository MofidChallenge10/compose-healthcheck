import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from compose_healthcheck import analyze
class Tests(unittest.TestCase):
 def test_missing_healthcheck(self):
  self.assertIn("missing_healthcheck",{x["kind"] for x in analyze({"services":{"api":{}}})})
 def test_started_warning(self):
  d={"services":{"db":{"healthcheck":{}}, "api":{"healthcheck":{},"depends_on":{"db":{"condition":"service_started"}}}}}
  self.assertIn("startup_only_dependency",{x["kind"] for x in analyze(d)})
 def test_unknown_dep(self):
  self.assertIn("unknown_dependency",{x["kind"] for x in analyze({"services":{"api":{"depends_on":["missing"]}}})})
if __name__=="__main__": unittest.main()
