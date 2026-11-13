"""
Exhaustive Study Guide Content for Member 1:
Mathematical Foundations, Problem Modeling & Exact Offline Optimization.
"""

from reportlab.platypus import Paragraph, Spacer, KeepTogether, HRFlowable
from reportlab.lib.units import inch
from .styles import make_callout, make_code_box, make_styled_table


def build_member1_content(story, styles):
    # Header Banner
    story.append(Paragraph("MEMBER 1: COMPREHENSIVE VIVA STUDY GUIDE", styles['DocTitle']))
    story.append(Paragraph("Specialization: Mathematical Foundations, Problem Formalization & Exact Offline Optimization", styles['DocSubtitle']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=styles['DocTitle'].textColor, spaceAfter=10))

    # SECTION A
    story.append(Paragraph("A. Section Overview", styles['SectionH1']))
    story.append(Paragraph(
        "This section establishes the theoretical bedrock and formal mathematical foundations of the entire emergency dispatch study. "
        "As Member 1, you own the formalization of the real-world problem, the construction of the bipartite eligibility graph, "
        "the derivation of edge utility weights, the formulation of the exact Integer Linear Program (ILP), "
        "and the formal proof that under zero fairness penalty (&mu; = 0), the offline problem reduces to Maximum-Weight b-Matching, "
        "which is solvable in polynomial time via Minimum Cost Flow.",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>Why this section is critical:</b> In any optimization and algorithmic project, without a rigorous mathematical model "
        "and an exact offline benchmark (OPT), it is impossible to evaluate online heuristics or compute competitive ratios. "
        "You define what constitutes a valid solution and provide the upper bound against which all other team members measure success.",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>Connection to other members:</b><br/>"
        "• <i>To Member 2:</i> Your offline OPT is the denominator in Member 2's competitive ratio formula (ALG / OPT).<br/>"
        "• <i>To Member 3:</i> Member 3's learning-augmented algorithm takes your exact Min-Cost Flow solver and runs it on predicted sequences to generate dispatch advice.<br/>"
        "• <i>To Member 4:</i> Your eligibility filters and capacity constraints form the core invariants in Member 4's simulation engine and unit test suite.",
        styles['Body']
    ))

    # SECTION B
    story.append(Spacer(1, 4))
    story.append(Paragraph("B. Conceptual Understanding", styles['SectionH1']))
    story.append(Paragraph(
        "<b>1. The Real-World Emergency Dispatch Setting:</b><br/>"
        "In sudden medical crises such as Out-of-Hospital Cardiac Arrest (OHCA), irreversible brain damage occurs within 4–6 minutes. "
        "Municipal emergency ambulances often take 8–12 minutes to arrive. Alerting verified community volunteers (e.g., doctors, nurses, off-duty EMTs) "
        "who are already physically proximate can bridge this critical survival window.",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>2. Offline vs. Online Paradigms:</b><br/>"
        "• <i>Offline Problem:</i> All requests across the entire shift (locations, skills, priorities, arrival times) are known in advance. "
        "The dispatcher can solve a global optimization problem in one shot.<br/>"
        "• <i>Online Problem:</i> Incidents arrive sequentially. An irrevocable decision must be made immediately without knowing future demand. "
        "The offline problem represents the 'ideal benchmark' (OPT).",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>3. Bipartite Matching vs. b-Matching:</b><br/>"
        "In classical bipartite matching, each vertex can be matched at most once. In <i>b-matching</i>, each volunteer vertex <i>v</i> "
        "has an integer capacity &kappa;<sub>v</sub> &ge; 1, permitting up to &kappa;<sub>v</sub> distinct incident assignments over the horizon.",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>4. Total Unimodularity (TUM):</b><br/>"
        "A matrix is totally unimodular if every square submatrix has determinant 0, +1, or -1. "
        "The incidence matrix of a directed network flow graph is totally unimodular, which guarantees that the extreme points of "
        "the Linear Programming (LP) relaxation are guaranteed to be integer-valued!",
        styles['Body']
    ))

    # SECTION C
    story.append(Spacer(1, 4))
    story.append(Paragraph("C. Technical Explanation & Mathematical Formulations", styles['SectionH1']))
    story.append(Paragraph(
        "<b>1. Mathematical Sets & Parameters:</b><br/>"
        "• <i>V</i> = {v<sub>1</sub>, ..., v<sub>n</sub>}: Set of registered volunteers.<br/>"
        "• <i>R</i> = {r<sub>1</sub>, ..., r<sub>m</sub>}: Set of emergency requests.<br/>"
        "• <i>S<sub>v</sub></i> &sube; &Sigma;: Certified skill set of volunteer <i>v</i>.<br/>"
        "• <i>Q<sub>r</sub></i> &sube; &Sigma;: Skill set required by request <i>r</i>.<br/>"
        "• &kappa;<sub>v</sub> &isin; &#8484;<sub>&gt;0</sub>: Maximum assignment capacity of volunteer <i>v</i>.<br/>"
        "• <i>u<sub>r</sub></i> &gt; 0: Priority utility of request <i>r</i>.<br/>"
        "• <i>c<sub>vr</sub></i> &ge; 0: Travel time from volunteer <i>v</i> to request <i>r</i>.<br/>"
        "• &theta;<sub>r</sub> &gt; 0: Maximum acceptable response deadline.<br/>"
        "• &lambda; &ge; 0: Travel cost penalty weight; &mu; &ge; 0: Workload fairness penalty weight.",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>2. Bipartite Eligibility Graph E:</b><br/>"
        "An edge (v, r) exists in <i>E</i> if and only if three strict conditions hold:<br/>"
        "&nbsp;&nbsp;1. <b>Skill Containment:</b> <i>Q<sub>r</sub></i> &sube; <i>S<sub>v</sub></i><br/>"
        "&nbsp;&nbsp;2. <b>Travel Feasibility:</b> <i>c<sub>vr</sub></i> &le; &theta;<sub>r</sub><br/>"
        "&nbsp;&nbsp;3. <b>Positive Net Weight:</b> <i>w<sub>vr</sub></i> = <i>u<sub>r</sub></i> - &lambda;<i>c<sub>vr</sub></i> &gt; 0",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>3. Exact Integer Linear Programming (ILP) Formulation:</b><br/>"
        "Let binary variable <i>x<sub>vr</sub></i> &isin; {0, 1} indicate whether volunteer <i>v</i> is assigned to request <i>r</i>. "
        "Let continuous variable <i>L</i> &ge; 0 represent the peak workload assigned to any volunteer.",
        styles['Body']
    ))

    ilp_box = (
        "Maximize:   &sum;_{(v, r) &isin; E} w_{vr} x_{vr} - &mu; L<br/><br/>"
        "Subject to:<br/>"
        "  (1) &sum;_{v: (v,r) &isin; E} x_{vr} &le; 1       &forall; r &isin; R    [At most one volunteer per request]<br/>"
        "  (2) &sum;_{r: (v,r) &isin; E} x_{vr} &le; &kappa;_{v}   &forall; v &isin; V    [Volunteer capacity limit]<br/>"
        "  (3) &sum;_{r: (v,r) &isin; E} x_{vr} &le; L        &forall; v &isin; V    [Max load fairness upper bound]<br/>"
        "  (4) x_{vr} &isin; {0, 1} &forall; (v,r) &isin; E,   L &ge; 0"
    )
    story.append(make_code_box(ilp_box, styles))
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "<b>4. Proof of Polynomial Solvability via Min-Cost Flow (&mu; = 0):</b><br/>"
        "When &mu; = 0, constraint (3) vanishes. We construct a directed flow network <i>G' = (V', E')</i>:<br/>"
        "1. Create supersource <i>S</i> and supersink <i>T</i>.<br/>"
        "2. Add arc (S, v) for each volunteer <i>v</i> with capacity &kappa;<sub>v</sub> and cost 0.<br/>"
        "3. Add arc (v, r) for each eligible pair (v, r) &isin; <i>E</i> with capacity 1 and cost -<i>w<sub>vr</sub></i>.<br/>"
        "4. Add arc (r, T) for each request <i>r</i> with capacity 1 and cost 0.<br/>"
        "5. Add bypass arc (v, T) with capacity &kappa;<sub>v</sub> and cost 0 to allow volunteers to remain partially loaded.<br/>"
        "6. Set supply at <i>S</i> to &sum;<sub>v</sub> &kappa;<sub>v</sub> and demand at <i>T</i> to &sum;<sub>v</sub> &kappa;<sub>v</sub>.<br/>"
        "Because the network incidence matrix is totally unimodular, the optimal min-cost flow is guaranteed to be integer. "
        "Hence, the offline problem with &mu; = 0 is solvable in polynomial time O(|V'|<sup>2</sup> |E'|) via standard network simplex.",
        styles['Body']
    ))

    # SECTION D
    story.append(Spacer(1, 4))
    story.append(Paragraph("D. Step-by-Step Working & Numerical Trace Example", styles['SectionH1']))
    story.append(Paragraph(
        "Consider an illustrative instance with 3 volunteers and 3 incoming requests in a 10 km grid (&lambda; = 0.5):",
        styles['Body']
    ))

    trace_data = [
        ["Entity", "Location", "Skills / Requirements", "Capacity / &theta;", "Utility (u)"],
        ["Volunteer v1", "(0, 0)", "{CPR, FirstAid}", "&kappa; = 1", "N/A"],
        ["Volunteer v2", "(4, 0)", "{CPR, TraumaCare}", "&kappa; = 1", "N/A"],
        ["Volunteer v3", "(0, 6)", "{CPR, FirstAid, TraumaCare}", "&kappa; = 2", "N/A"],
        ["Request r1", "(0, 2)", "{CPR}", "&theta; = 5.0", "u = 20.0"],
        ["Request r2", "(3, 0)", "{TraumaCare}", "&theta; = 4.0", "u = 25.0"],
        ["Request r3", "(0, 5)", "{FirstAid}", "&theta; = 3.0", "u = 18.0"]
    ]
    story.append(make_styled_table(trace_data, [1.1*inch, 1.0*inch, 2.2*inch, 1.3*inch, 1.4*inch], styles))
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "<b>Eligibility & Weight Evaluation:</b><br/>"
        "• <i>(v1, r1):</i> dist = 2.0 &le; 5.0; CPR &sube; {CPR, FirstAid}; weight = 20 - 0.5(2.0) = <b>19.0</b>. (Eligible)<br/>"
        "• <i>(v2, r2):</i> dist = 1.0 &le; 4.0; Trauma &sube; {CPR, TraumaCare}; weight = 25 - 0.5(1.0) = <b>24.5</b>. (Eligible)<br/>"
        "• <i>(v3, r3):</i> dist = 1.0 &le; 3.0; FirstAid &sube; S_v3; weight = 18 - 0.5(1.0) = <b>17.5</b>. (Eligible)<br/>"
        "• <i>(v1, r2):</i> Missing TraumaCare &rArr; Ineligible!<br/>"
        "<b>Optimal Offline Solution:</b> Flow solver matches v1 &rarr; r1, v2 &rarr; r2, v3 &rarr; r3. "
        "Total Utility = 63.0, Total Travel Time = 4.0, Net Objective = 63.0 - 0.5(4.0) = <b>61.0</b>.",
        styles['Body']
    ))

    # SECTION E
    story.append(Spacer(1, 4))
    story.append(Paragraph("E. Important Decisions & Justifications", styles['SectionH1']))
    story.append(Paragraph(
        "<b>Decision 1: Why solve &mu; = 0 via Min-Cost Flow instead of general ILP solvers?</b><br/>"
        "<i>Justification:</i> Network flow solvers run in low polynomial time O(V<sup>2</sup> E) using NetworkX, "
        "avoiding exponential branch-and-bound overhead. This allows instant offline solving on thousands of requests.",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>Decision 2: Why define edge weight as w_{vr} = u_r - &lambda; c_{vr} rather than dividing utility by distance?</b><br/>"
        "<i>Justification:</i> Additive net utility has linear units (dollars or life-years gained minus travel penalty). "
        "A ratio objective u_r / c_{vr} creates a non-linear Fractional Programming problem, destroying unimodularity and convexity.",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>Decision 3: Why model L as a continuous variable in the MILP?</b><br/>"
        "<i>Justification:</i> Because each x_{vr} is binary, &sum;_r x_{vr} is an integer. "
        "Since L is minimized and bounded from below by integer sums, L naturally takes the integer value of the maximum volunteer load.",
        styles['Body']
    ))

    # SECTION F: VIVA QUESTIONS
    story.append(Spacer(1, 4))
    story.append(Paragraph("F. Comprehensive Viva Preparation & Defense", styles['SectionH1']))

    qas = [
        ("Q1: What is the exact mathematical formulation of the offline volunteer dispatch problem?",
         "It is an Integer Linear Program: Maximize &sum;_{(v,r) &isin; E} w_{vr} x_{vr} - &mu; L, subject to: (1) each request matched at most once, (2) each volunteer assigned at most &kappa;<sub>v</sub> requests, (3) each volunteer assigned at most L requests, with x_{vr} &isin; {0, 1} and L &ge; 0."),

        ("Q2: How do you mathematically determine if an edge (v, r) exists in the eligibility graph?",
         "Three simultaneous conditions must hold: (1) Skill inclusion: Q_r &sube; S_v, (2) Distance threshold: c_{vr} &le; &theta;_r, and (3) Positive net value: w_{vr} = u_r - &lambda; c_{vr} &gt; 0."),

        ("Q3: Why is the offline problem solvable in polynomial time when &mu; = 0?",
         "Because with &mu; = 0, the problem is Maximum Weight b-Matching on a bipartite graph. This reduces to Minimum Cost Flow on a directed graph whose incidence matrix is totally unimodular (TUM). TUM guarantees all vertices of the LP polytope are integral, allowing exact solution via network simplex in polynomial time."),

        ("Q4: What happens mathematically when &mu; &gt; 0?",
         "When &mu; &gt; 0, the objective includes a penalty on L = max_v load(v). This introduces a global coupling constraint across all volunteer loads, similar to min-max makespan scheduling. We solve it as an exact Mixed-Integer Linear Program (MILP) using SciPy's HiGHS solver."),

        ("Q5: What is the significance of the parameter &lambda;?",
         "&lambda; represents the marginal trade-off between incident utility and travel delay. When &lambda; = 0, distance does not penalize utility (as long as c_{vr} &le; &theta;_r). As &lambda; increases, long-distance dispatches become unprofitable (w_{vr} &le; 0) and are pruned from the eligibility graph."),

        ("Q6: If all capacities &kappa;_v = 1 and &mu; = 0, what classical problem do you get?",
         "We get the classical Maximum Weight Bipartite Matching problem (also known as the Assignment Problem), solvable in O(n^3) using the Hungarian Algorithm."),

        ("Q7: Why did you not formulate the offline problem as a Travelling Salesperson Problem (TSP) or Vehicle Routing Problem (VRP)?",
         "In emergency response, volunteers respond immediately to a single urgent incident from their current location. They do not visit a tour of multiple victims in a planned vehicle circuit, because victims in cardiac arrest cannot wait for a sequential multi-stop tour."),

        ("Q8: How does your code represent and solve the Min-Cost Flow problem?",
         "In `src/offline_solver.py`, we construct a directed graph in NetworkX with supersource S and supersink T. Capacities represent volunteer &kappa;_v and request bounds (1). Arc weights are set to -round(w_{vr} * 10000) to convert maximization into integer min-cost flow."),

        ("Q9: What is the computational complexity of solving the Min-Cost Flow model?",
         "Using NetworkX's capacity-scaling or network simplex, the complexity is O(V^2 E log(V)), where V is the total number of volunteers plus requests, and E is the number of eligible pairs. It takes less than 20 milliseconds for 100 requests on standard hardware."),

        ("Q10: Challenging Follow-up: Is the offline problem NP-hard if each request requires TWO volunteers simultaneously?",
         "Yes! If a request requires a team of two volunteers simultaneously (e.g. two-person CPR), the problem reduces to Maximum Weight 3-Dimensional Matching (3DM) or Set Packing, which is a known NP-hard problem.")
    ]

    for q, a in qas:
        story.append(Paragraph(q, styles['Question']))
        story.append(Paragraph(a, styles['Answer']))

    # SECTION G: PRACTICAL UNDERSTANDING
    story.append(Spacer(1, 4))
    story.append(Paragraph("G. Practical Understanding & Code Implementation", styles['SectionH1']))
    story.append(Paragraph(
        "<b>Key Source Files Owned by Member 1:</b><br/>"
        "• `src/models.py`: Defines dataclasses `Volunteer`, `Request`, and class `ProblemInstance`. "
        "Implements caching for travel times and lazy evaluation of edge eligibility.<br/>"
        "• `src/offline_solver.py`: Contains `OfflineSolver.solve_flow()` (NetworkX Min-Cost Flow) "
        "and `OfflineSolver.solve_milp()` (SciPy HiGHS MILP).",
        styles['Body']
    ))

    code_snippet = (
        "# Eligibility check in src/models.py\n"
        "def is_eligible(self, v_id: int, r_id: int) -> bool:\n"
        "    vol, req = self.v_map[v_id], self.r_map[r_id]\n"
        "    if not req.required_skills.issubset(vol.skills):\n"
        "        return False\n"
        "    c_vr = self.compute_travel_time(v_id, r_id)\n"
        "    if c_vr > req.max_travel_time:\n"
        "        return False\n"
        "    w_vr = req.utility - self.lambda_cost * c_vr\n"
        "    return w_vr > 0"
    )
    story.append(make_code_box(code_snippet, styles))
    story.append(Spacer(1, 4))

    # SECTION H: QUICK REVISION
    story.append(Paragraph("H. Quick Revision & Formula Sheet", styles['SectionH1']))
    rev_table = [
        ["Concept", "Formula / Formal Definition", "Complexity / Invariant"],
        ["Travel Time", "c_{vr} = ||(x_v, y_v) - (x_r, y_r)||_2 / v_{speed}", "O(1) computation"],
        ["Edge Weight", "w_{vr} = u_r - &lambda; c_{vr}", "Positive weights only"],
        ["Eligibility", "Q_r &sube; S_v &and; c_{vr} &le; &theta;_r &and; w_{vr} &gt; 0", "Prunes non-viable arcs"],
        ["Exact Offline (&mu;=0)", "Max-Weight b-Matching &rarr; Min-Cost Flow", "Polynomial: O(V^2 E)"],
        ["Exact Offline (&mu;&gt;0)", "MILP with continuous L upper envelope", "Solved via SciPy HiGHS"]
    ]
    story.append(make_styled_table(rev_table, [1.5*inch, 3.2*inch, 2.3*inch], styles))
    story.append(Spacer(1, 6))

    story.append(make_callout(
        "Always emphasize to the professor: <b>'When &mu; = 0, our offline problem is in P, not NP-hard! "
        "The hardness of our problem stems entirely from the ONLINE arrival of requests and incomplete information.'</b> "
        "This demonstrates superior mastery over common student misconceptions.",
        styles,
        callout_type="tip",
        title="Key Viva Defense Punchline"
    ))
