"""
Exhaustive Study Guide Content for Member 3:
Learning-Augmented Online Algorithms & Adaptive Safeguards.
"""

from reportlab.platypus import Paragraph, Spacer, KeepTogether, HRFlowable
from reportlab.lib.units import inch
from .styles import make_callout, make_code_box, make_styled_table


def build_member3_content(story, styles):
    story.append(Paragraph("MEMBER 3: COMPREHENSIVE VIVA STUDY GUIDE", styles['DocTitle']))
    story.append(Paragraph("Specialization: Learning-Augmented Online Algorithms & Adaptive Safeguards", styles['DocSubtitle']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=styles['DocTitle'].textColor, spaceAfter=10))

    # SECTION A
    story.append(Paragraph("A. Section Overview", styles['SectionH1']))
    story.append(Paragraph(
        "This section represents the core algorithmic research innovation of the project: the <i>Learning-Augmented Online Algorithm</i> framework. "
        "As Member 3, you own the formalization of machine-learned predictions under uncertainty, the definition of the normalized prediction "
        "error metric &eta;, the architecture and implementation of the proposed algorithm: <b>Follow-the-Prediction with Safeguard (FTPS)</b>, "
        "the formulation of the trust parameter &beta; &isin; [0, 1], and the theoretical proofs of Consistency, Robustness, and Smoothness.",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>Why this section is critical:</b> Classical online algorithms are fundamentally shackled by pessimistic worst-case barriers "
        "(deterministic 1/2, randomized 1 - 1/e &approx; 0.632). However, modern 911 dispatch centres have access to historical incident data "
        "and predictive AI models that can forecast emergency demand. You bridge the gap between machine learning and worst-case competitive analysis, "
        "proving that our algorithm can achieve near 1.0 competitive ratio under good predictions while remaining provably safe under bad predictions.",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>Connection to other members:</b><br/>"
        "• <i>To Member 1:</i> You take Member 1's exact Min-Cost Flow solver and execute it upfront on the predicted sequence &circ;R.<br/>"
        "• <i>To Member 2:</i> You use Member 2's robust online baselines (Water-Filling and Ranking) as your algorithmic fallback safeguard.<br/>"
        "• <i>To Member 4:</i> Member 4 tests your algorithm across the entire spectrum of prediction errors &eta; &isin; [0, 1] in Experiment 1.",
        styles['Body']
    ))

    # SECTION B
    story.append(Spacer(1, 4))
    story.append(Paragraph("B. Conceptual Understanding", styles['SectionH1']))
    story.append(Paragraph(
        "<b>1. The 'Algorithms with Predictions' Paradigm:</b><br/>"
        "Historically, algorithm design suffered from a dichotomy: machine learning models perform excellently on average but possess "
        "no worst-case safety guarantees, while classical online algorithms provide worst-case guarantees but are overly pessimistic. "
        "Pioneered by Lykouris &amp; Vassilvitskii (2021) and Purohit et al. (2018), <i>learning-augmented algorithms</i> augment online decisions "
        "with an unverified, potentially faulty 'oracle' or ML predictor.",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>2. The Golden Triad of Guarantees:</b><br/>"
        "Every valid learning-augmented algorithm must satisfy three formal properties:<br/>"
        "• <b>Consistency:</b> When the prediction is perfectly accurate (&eta; = 0), the competitive ratio should be close to 1.0 (near-optimal).<br/>"
        "• <b>Robustness:</b> Even if the prediction is malicious, adversarial, or completely wrong (&eta; = 1), the competitive ratio must never fall "
        "below a guaranteed fraction of the best classical online baseline.<br/>"
        "• <b>Smoothness:</b> As prediction error &eta; increases from 0 to 1, the competitive ratio must degrade gracefully without catastrophic cliff drops.",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>3. Prediction Error Metric (&eta;):</b><br/>"
        "Let <i>R</i> be the actual sequence of emergency requests, and let &circ;R be the predicted sequence. "
        "Following Choo et al. (ICML 2024), we define the normalized prediction error &eta; as:",
        styles['Body']
    ))

    eta_box = "&eta; = 1 - [ |R &cap; &circ;R| / |R| ] &isin; [0, 1]"
    story.append(make_code_box(eta_box, styles))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "where |R &cap; &circ;R| represents the count of requests whose predicted types (required skills and geographic eligibility) "
        "match the true incoming requests. When &eta; = 0, predictions are perfect; when &eta; = 1, predictions are completely disjoint.",
        styles['Body']
    ))

    # SECTION C
    story.append(Spacer(1, 4))
    story.append(Paragraph("C. Technical Explanation & Algorithm Architecture", styles['SectionH1']))
    story.append(Paragraph(
        "<b>1. Architecture of Follow-the-Prediction with Safeguard (FTPS):</b><br/>"
        "FTPS operates in two distinct computational stages:<br/>"
        "<b>Stage 1: Offline Pre-Matching on Advice:</b><br/>"
        "Before the shift begins, the dispatcher receives predicted request sequence &circ;R. "
        "FTPS constructs a virtual problem instance (<i>V</i>, &circ;R) and solves the exact Maximum Weight b-Matching using Member 1's "
        "Min-Cost Flow solver. This produces an optimal planned dispatch map: <i>M*<sub>pred</sub>: &circ;r<sub>i</sub> &rarr; v*</i>.<br/>"
        "<b>Stage 2: Online Execution with Adaptive Error Tracking:</b><br/>"
        "As real requests <i>r</i><sub>1</sub>, ..., <i>r<sub>m</sub></i> arrive sequentially at times <i>t</i> = 1, ..., <i>m</i>:<br/>"
        "1. Compare <i>r<sub>t</sub></i> with predicted counterpart &circ;r<sub>t</sub>. If skills or locations mismatch, increment <i>mismatches</i>.<br/>"
        "2. Compute empirical running error: &circ;&eta;<sub>t</sub> = <i>mismatches</i> / <i>t</i>.<br/>"
        "3. Evaluate trust threshold: &tau;(&beta;) = 1 - 0.5 &beta;, where &beta; &isin; [0, 1] is the user-configured trust parameter.<br/>"
        "4. <b>Dispatch Decision:</b><br/>"
        "&nbsp;&nbsp;&bull; If &circ;&eta;<sub>t</sub> &le; &tau;(&beta;) AND predicted volunteer <i>v*</i> = <i>M*<sub>pred</sub>[&circ;r<sub>t</sub>]</i> is available and eligible for <i>r<sub>t</sub></i>: "
        "<b>Dispatch v*</b> (Follow the prediction!).<br/>"
        "&nbsp;&nbsp;&bull; Else: <b>Trigger Safeguard Fallback</b>. Execute Member 2's Water-Filling rule: "
        "<i>v' = argmin_{v &isin; eligible(r_t)} ( current_load(v), -w_{v, r_t} )</i>.",
        styles['Body']
    ))

    story.append(Paragraph(
        "<b>2. Theoretical Analysis & Proof Sketches:</b><br/>"
        "<b>Theorem 3 (Consistency):</b> <i>As &eta; &rarr; 0, CR(FTPS) &rarr; 1.0.</i><br/>"
        "<i>Proof Sketch:</i> When &eta; = 0, &circ;R &equiv; R. The running error &circ;&eta;<sub>t</sub> = 0 &le; &tau;(&beta;) for all <i>t</i>. "
        "Every real request matches its predicted counterpart, and its assigned volunteer <i>v*</i> is always available and eligible. "
        "Hence, the online execution replicates the optimal offline flow matching <i>M*<sub>pred</sub> &equiv; M*<sub>true</sub></i>. "
        "Thus ALG = OPT, yielding CR = 1.0.<br/><br/>"
        "<b>Theorem 4 (Robustness):</b> <i>For any adversarial error &eta; = 1, CR(FTPS) &ge; &gamma;<sub>robust</sub> - &epsilon;(&beta;).</i><br/>"
        "<i>Proof Sketch:</i> When &eta; = 1, every incoming request produces a mismatch. "
        "The running error &circ;&eta;<sub>t</sub> rapidly crosses the threshold &tau;(&beta;). Once crossed, the prediction check evaluates to false, "
        "and FTPS routes all remaining decisions through the robust Water-Filling / Ranking fallback. "
        "At most a small initial prefix of &tau;(&beta;) &middot; m decisions can be affected before the safeguard locks in, "
        "bounding worst-case loss and guaranteeing baseline competitive performance.",
        styles['Body']
    ))

    # SECTION D
    story.append(Spacer(1, 4))
    story.append(Paragraph("D. Step-by-Step Working & Trace of Safeguard Activation", styles['SectionH1']))
    story.append(Paragraph(
        "Let us trace FTPS on an emergency sequence with trust parameter &beta; = 0.8 (&rArr; error threshold &tau; = 1 - 0.5(0.8) = 0.60):",
        styles['Body']
    ))

    ftps_table = [
        ["Time t", "Real Incident r_t", "Predicted &circ;r_t", "Match?", "Running &circ;&eta;_t", "Safeguard State", "Final Dispatch Action"],
        ["t = 1", "{CPR}, (10, 20)", "{CPR}, (10, 20)", "YES", "0 / 1 = 0.00", "Normal (&le; 0.60)", "Dispatches planned v1"],
        ["t = 2", "{Trauma}, (30, 40)", "{FirstAid}, (50, 50)", "NO", "1 / 2 = 0.50", "Normal (&le; 0.60)", "Target busy &rarr; Fallback to v3"],
        ["t = 3", "{Hazmat}, (70, 80)", "{CPR}, (10, 20)", "NO", "2 / 3 = 0.67", "<b>TRIGGERED (&gt; 0.60)</b>", "<b>Safeguard locks: Fallback v4</b>"],
        ["t = 4", "{CPR}, (15, 25)", "{Trauma}, (40, 40)", "NO", "3 / 4 = 0.75", "<b>TRIGGERED</b>", "<b>Safeguard locks: Fallback v2</b>"]
    ]
    story.append(make_styled_table(ftps_table, [0.7*inch, 1.2*inch, 1.2*inch, 0.7*inch, 0.9*inch, 1.1*inch, 1.2*inch], styles))
    story.append(Spacer(1, 4))

    # SECTION E
    story.append(Paragraph("E. Important Decisions & Justifications", styles['SectionH1']))
    story.append(Paragraph(
        "<b>Decision 1: Why use an adaptive running error tracker rather than a static coin flip?</b><br/>"
        "<i>Justification:</i> Some learning-augmented papers use a static coin flip (trust prediction with probability &beta;, use baseline with 1 - &beta;). "
        "A static coin flip guarantees that even when predictions are 100% correct, you still make wrong decisions 1 - &beta; of the time! "
        "Our dynamic error tracker monitors empirical performance in real time, achieving 1.0 ratio when advice is accurate.",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>Decision 2: Why define threshold &tau;(&beta;) = 1 - 0.5 &beta;?</b><br/>"
        "<i>Justification:</i> When &beta; = 1.0 (maximum trust), &tau; = 0.50, allowing moderate deviations before distrusting advice. "
        "When &beta; &rarr; 0 (zero trust), &tau; &rarr; 1.0, but the algorithm immediately switches to pure baseline, providing an intuitive dial for dispatchers.",
        styles['Body']
    ))

    # SECTION F: VIVA QUESTIONS
    story.append(Spacer(1, 4))
    story.append(Paragraph("F. Comprehensive Viva Preparation & Defense", styles['SectionH1']))

    qas = [
        ("Q1: What is a learning-augmented algorithm, and why is it needed in emergency dispatch?",
         "A learning-augmented algorithm integrates predictions (from machine learning models or historical forecasts) into an online decision process. In emergency response, cities have strong historical priors regarding incident locations and times, but worst-case online algorithms ignore this data. Learning-augmented algorithms allow dispatchers to exploit predictive data while maintaining provable worst-case safety nets."),

        ("Q2: Define Consistency and Robustness formally.",
         "• Consistency: The competitive ratio achieved when the prediction is perfectly accurate (&eta; = 0). An algorithm is strictly consistent if CR &rarr; 1.0 as &eta; &rarr; 0.\n• Robustness: The minimum competitive ratio guaranteed even under arbitrarily bad, noisy, or adversarial predictions (&eta; = 1). The algorithm must never fall below &gamma; * CR_baseline."),

        ("Q3: How is prediction error &eta; defined in our project?",
         "&eta; = 1 - |R &cap; &circ;R| / |R|, where R is the real request sequence, &circ;R is the predicted sequence, and a match requires identical skill requirements and spatial feasibility. &eta; &isin; [0, 1], where 0 represents zero error and 1 represents completely mismatched predictions."),

        ("Q4: How does Follow-the-Prediction with Safeguard (FTPS) work step by step?",
         "Step 1: Compute the offline optimal matching M*_{pred} on the predicted sequence &circ;R using Min-Cost Flow.\nStep 2: When real request r_t arrives, check if it matches predicted request &circ;r_t and update the running error rate &circ;&eta;_t.\nStep 3: If running error is within threshold &tau;(&beta;) and the planned volunteer is free and eligible, dispatch that volunteer.\nStep 4: If error exceeds threshold or planned volunteer is unavailable, fall back to the robust online baseline (Water-Filling)."),

        ("Q5: What is the role of the trust parameter &beta; &isin; [0, 1]?",
         "&beta; controls the trade-off between consistency and robustness. A high &beta; (e.g. 0.85) places heavy trust in predictions, maximizing performance when ML models are reliable. A lower &beta; (e.g. 0.3) enforces a tighter safeguard, switching quickly to robust fallbacks in volatile environments."),

        ("Q6: What happens if the prediction is completely adversarial (&eta; = 1)?",
         "The error counter increments on every request. The running error &circ;&eta;_t rapidly exceeds &tau;(&beta;) on the very first few requests. The algorithm permanently disables prediction trust and executes the robust Water-Filling baseline, achieving a competitive ratio of &ge; 0.92 on random instances and &ge; 0.60 on adversarial instances."),

        ("Q7: In your empirical results (Table 1), what competitive ratio did FTPS achieve at &eta; = 0?",
         "At &eta; = 0.0, FTPS achieved a competitive ratio of 0.9903 across 10 random seeds, outperforming pure online heuristics by nearly 7 percentage points and proving theoretical consistency!"),

        ("Q8: In Table 1, what competitive ratio did FTPS achieve at &eta; = 1.0?",
         "At &eta; = 1.0, FTPS achieved 0.9208, exactly matching the robust Water-Filling baseline. This proved empirical robustness: even with 100% false advice, the algorithm was never worse than the online baseline."),

        ("Q9: What is 'Smoothness' in a learning-augmented algorithm?",
         "Smoothness means that the competitive ratio degrades gracefully as a continuous function of error &eta;, rather than collapsing abruptly when &eta; crosses a small threshold."),

        ("Q10: Challenging Follow-up: Why can't we simply recompute the offline matching on future predictions every time a request arrives?",
         "Re-solving offline matching on every step is called 'Model Predictive Control' (MPC) or 'Rolling Horizon'. While viable, solving a large Min-Cost Flow at every millisecond step creates significant latency in real-time 911 dispatch. FTPS computes the flow only once upfront, making online dispatch an O(1) table lookup with O(V) fallback!")
    ]

    for q, a in qas:
        story.append(Paragraph(q, styles['Question']))
        story.append(Paragraph(a, styles['Answer']))

    # SECTION G: PRACTICAL UNDERSTANDING
    story.append(Spacer(1, 4))
    story.append(Paragraph("G. Practical Understanding & Code Implementation", styles['SectionH1']))
    story.append(Paragraph(
        "<b>Key Source Files Owned by Member 3:</b><br/>"
        "• `src/learning_augmented.py`: Contains class `FollowThePredictionWithSafeguard`.<br/>"
        "• `src/generator.py`: Contains `InstanceGenerator.generate_predictions()` with error injection.",
        styles['Body']
    ))

    code_snippet = (
        "# Safeguard logic in src/learning_augmented.py\n"
        "current_error_rate = num_mismatches / total_seen\n"
        "safeguard_active = current_error_rate > self.error_threshold\n"
        "\n"
        "if not safeguard_active and pred_req.id in planned_dispatch:\n"
        "    target_v_id = planned_dispatch[pred_req.id]\n"
        "    if instance.v_map[target_v_id].is_available() and \\\n"
        "       instance.is_eligible(target_v_id, real_req.id):\n"
        "        assigned_v_id = target_v_id  # Trust prediction\n"
        "\n"
        "if assigned_v_id is None:\n"
        "    # Fallback to robust baseline (Water-Filling)\n"
        "    assigned_v_id = min(candidates, key=lambda v: (v.current_load, -weight)).id"
    )
    story.append(make_code_box(code_snippet, styles))
    story.append(Spacer(1, 4))

    # SECTION H: QUICK REVISION
    story.append(Paragraph("H. Quick Revision & Theorem Sheet", styles['SectionH1']))
    rev_table = [
        ["Metric / Property", "Mathematical Condition", "Observed Experimental Value"],
        ["Consistency", "lim_{&eta;&rarr;0} CR(FTPS) = 1.0", "<b>0.9903</b> (near-optimal)"],
        ["Robustness", "CR(FTPS) &ge; CR_{baseline} as &eta;&rarr;1.0", "<b>0.9208</b> (matches Water-Filling)"],
        ["Smoothness", "CR(&eta;) decays monotonically", "Smooth monotonic curve across all &eta;"],
        ["Trust Parameter", "&beta; &isin; [0, 1]; &tau;(&beta;) = 1 - 0.5&beta;", "Optimal default: &beta; = 0.70 - 0.85"]
    ]
    story.append(make_styled_table(rev_table, [1.6*inch, 2.7*inch, 2.7*inch], styles))
    story.append(Spacer(1, 6))

    story.append(make_callout(
        "Key phrase to summarize your contribution to the professor: "
        "<b>'FTPS achieves the best of both worlds: the near-1.0 optimality of machine learning under accurate forecasts, "
        "and the uncompromising safety of worst-case competitive online algorithms under complete prediction failure.'</b>",
        styles,
        callout_type="tip",
        title="Elevator Pitch for Viva"
    ))
