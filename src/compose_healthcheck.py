"""Analyze Docker Compose service dependency readiness."""
import argparse,json,sys
from pathlib import Path
try:
 import yaml
except ImportError:
 yaml=None

def analyze(data):
 services=data.get("services") or {}; issues=[]; graph={}
 for name,service in services.items():
  deps=service.get("depends_on",{})
  if isinstance(deps,list): deps={x:{} for x in deps}
  graph[name]=sorted(deps)
  if not service.get("healthcheck"):
   issues.append({"service":name,"kind":"missing_healthcheck","message":"No healthcheck configured."})
  for dep,condition in deps.items():
   if dep not in services: issues.append({"service":name,"kind":"unknown_dependency","dependency":dep})
   cond=condition.get("condition") if isinstance(condition,dict) else None
   if cond=="service_started": issues.append({"service":name,"kind":"startup_only_dependency","dependency":dep,"message":"service_started does not guarantee readiness."})
 visiting=set(); visited=set()
 def visit(node):
  if node in visiting: issues.append({"service":node,"kind":"dependency_cycle"}); return
  if node in visited: return
  visiting.add(node)
  for dep in graph.get(node,[]):
   if dep in graph: visit(dep)
  visiting.remove(node); visited.add(node)
 for node in graph: visit(node)
 return issues

def main(argv=None):
 p=argparse.ArgumentParser(description="Audit Compose healthchecks and dependency readiness.")
 p.add_argument("compose_file"); a=p.parse_args(argv)
 if yaml is None: p.error("Install PyYAML: pip install 'compose-healthcheck[yaml]'")
 try: data=yaml.safe_load(Path(a.compose_file).read_text(encoding="utf-8")) or {}
 except (OSError,yaml.YAMLError) as e: print(str(e),file=sys.stderr); return 2
 issues=analyze(data); print(json.dumps(issues,indent=2)); return int(bool(issues))
if __name__=="__main__": sys.exit(main())
