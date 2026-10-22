"""In-process smoke tests for the rational_circle MCP server (fastmcp Client)."""
import asyncio, json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fastmcp import Client
from rational_circle_mcp import mcp

def j(r):
    return r.data if hasattr(r, "data") and r.data is not None else json.loads(r.content[0].text)

async def main():
    async with Client(mcp) as c:
        tools = await c.list_tools(); print("tools:", [t.name for t in tools])
        res = await c.list_resources(); print("resources:", [str(r.uri) for r in res])
        pr = await c.list_prompts(); print("prompts:", [p.name for p in pr])
        t0=time.time(); r = j(await c.call_tool("paper_overview", {})); print("overview:", r["title"][:60], "| stages", r["verification_stages"])
        r = j(await c.call_tool("evaluate_configuration", {"rows": [[1,1,1],[1,1,-1],[1,1,0],[1,0,1]], "tan_half_angles": ["1/2","1/3","2/5"]}))
        print("evaluate D1 generic:", r["sines"], r["admissible"], r["reason"])
        r = j(await c.call_tool("evaluate_configuration", {"rows": [[1,1,1],[1,1,-1],[1,1,0],[1,0,1]], "tan_half_angles": ["1","0","inf"]}))
        print("evaluate D1 torsion:", r["sines"], "systems", len(r["signed_systems_satisfied"]), r["degeneracies"])
        r = j(await c.call_tool("enumerate_configurations", {"r": 3})); print("r=3:", r["vectors"], r["full_depth_sets"], r["orbits"])
        r = j(await c.call_tool("two_prime_coverage", {"k": 4, "l": 4})); print("two-prime (4,4):", {k:v for k,v in r.items() if k!='representatives_m_n'}, r["representatives_m_n"])
        r = j(await c.call_tool("genus5_point_search", {"height": 200})); print("search:", r["points"], r["seconds"], "s")
        r = j(await c.call_tool("reconstruct_d1_point", {"h": "1"})); print("reconstruct h=1:", r["Y"], r["admissible"], r.get("reason"), r["offsets"])
        r = j(await c.call_tool("reconstruct_d1_point", {"h": "2/3"})); print("reconstruct h=2/3:", r)
        r = j(await c.call_tool("genus5_quotient_structure", {})); print("quotients identities:", r["identities_verified"]); 
        for k,v in r["quotients"].items(): print("  ",k, v.get("ainvs"), v.get("small_point") or v.get("point_from_known_h=1"), v.get("infinite_order"), v["lmfdb"]["lmfdb"], "iso", v["lmfdb"]["isomorphism_verified"], "u=", v["lmfdb"]["isomorphism_scaling_u"])
        r = j(await c.call_tool("three_parameter_orbit_table", {})); print("orbits:", [(o["label"],o["status"]) for o in r["orbits"]])
        r = j(await c.call_tool("list_verification_stages", {})); print("stages:", len(r["core_stages"]), len(r["four_prime_stages"]))
        r = j(await c.call_tool("run_verification_stage", {"stage": "D1_normalization_and_descent"})); print("stage run:", r["stage"], r["passed"], r["seconds"])
        r = j(await c.call_tool("four_parameter_sweep", {"orbit_index": 0, "height": 2})); print("r4 sweep orbit0 H2:", r["returncode"], r["admissible_points_found"], (r["stats"] or {}).get("systems_checked"))
        r = j(await c.call_tool("list_specialist_reports", {})); print("reports:", r)
        print("elapsed", round(time.time()-t0,1))
asyncio.run(main())
