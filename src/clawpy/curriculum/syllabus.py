"""HSC syllabus structure — verified against official NCTB textbooks.

Sources:
- NCTB official textbook pages (nctb.gov.bd)
- Ensiner HSC course syllabi (ensiner.com)
- SattAcademy chapter structure (sattacademy.com)
- 10 Minute School chapter listings (10minuteschool.com)
- Cross-validated with 37,039 SattAcademy admission questions tags

NCTB HSC Science Stream — 1st Paper = Class XI, 2nd Paper = Class XII

Physics:   1st Paper (10 chapters) + 2nd Paper (11 chapters)
Chemistry: 1st Paper (5 chapters)  + 2nd Paper (5 chapters)
Biology:   1st Paper (12 chapters) + 2nd Paper (12 chapters)
Higher Math: 1st Paper (10 chapters) + 2nd Paper (10 chapters)
"""

from __future__ import annotations

from .models import (
    Difficulty,
    Lesson,
    SubjectCurriculum,
    SubjectId,
    TargetExam,
    Unit,
)


def _lesson(
    id: str,
    title: str,
    title_bn: str,
    desc: str,
    desc_bn: str,
    difficulty: Difficulty = Difficulty.MEDIUM,
    order: int = 0,
    concepts: list[str] | None = None,
    prereqs: list[str] | None = None,
    minutes: int = 10,
) -> Lesson:
    return Lesson(
        id=id,
        title=title,
        title_bn=title_bn,
        description=desc,
        description_bn=desc_bn,
        difficulty=difficulty,
        order=order,
        concepts=concepts or [],
        prerequisites=prereqs or [],
        estimated_minutes=minutes,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# PHYSICS — 1st Paper (Class XI): 10 chapters, 2nd Paper (Class XII): 11 chapters
# ═══════════════════════════════════════════════════════════════════════════════

PHYSICS = SubjectCurriculum(
    subject=SubjectId.PHYSICS,
    title="Physics",
    title_bn="পদার্থবিজ্ঞান",
    icon="⚛️",
    target_exams=[TargetExam.BUET, TargetExam.DU, TargetExam.MEDICAL, TargetExam.GST],
    units=[
        # ── 1st Paper (Class XI) ──
        Unit(
            id="phy1-ch01", title="Measurement", title_bn="ভৌত জগৎ ও পরিমাপ",
            description="Physical quantities, units, dimensions, measurement errors",
            description_bn="ভৌত রাশি, একক, মাত্রা, পরিমাপের ত্রুটি",
            icon="📏", nctb_chapter="1", nctb_class="XI", order=1,
            lessons=[
                _lesson("phy1-01-01", "Physical Quantities & SI Units", "ভৌত রাশি ও SI একক",
                        "Fundamental & derived quantities, SI system", "মৌলিক ও লব্ধ রাশি, SI পদ্ধতি",
                        Difficulty.EASY, 1, ["SI units", "dimensional analysis"]),
                _lesson("phy1-01-02", "Measurement & Errors", "পরিমাপ ও ত্রুটি",
                        "Vernier, screw gauge, errors, significant figures",
                        "ভার্নিয়ার, স্ক্রু গেজ, ত্রুটি, সার্থক অঙ্ক",
                        Difficulty.EASY, 2, ["vernier caliper", "significant figures"]),
            ],
        ),
        Unit(
            id="phy1-ch02", title="Vectors", title_bn="ভেক্টর",
            description="Vector algebra, addition, resolution, scalar & vector products",
            description_bn="ভেক্টর বীজগণিত, যোগ, বিভাজন, স্কেলার ও ভেক্টর গুণন",
            icon="➡️", nctb_chapter="2", nctb_class="XI", order=2,
            lessons=[
                _lesson("phy1-02-01", "Vector Addition & Resolution", "ভেক্টর যোগ ও বিভাজন",
                        "Parallelogram law, triangle law, components",
                        "সামান্তরিক সূত্র, ত্রিভুজ সূত্র, উপাংশ",
                        Difficulty.MEDIUM, 1, ["parallelogram law", "components"]),
                _lesson("phy1-02-02", "Scalar & Vector Products", "স্কেলার ও ভেক্টর গুণন",
                        "Dot product, cross product, applications",
                        "ডট গুণন, ক্রস গুণন, প্রয়োগ",
                        Difficulty.MEDIUM, 2, ["dot product", "cross product"]),
            ],
        ),
        Unit(
            id="phy1-ch03", title="Dynamics", title_bn="গতিবিদ্যা",
            description="Kinematics, equations of motion, free fall, graphs",
            description_bn="সরলরৈখিক গতি, গতির সমীকরণ, মুক্ত পতন, লেখচিত্র",
            icon="🏃", nctb_chapter="3", nctb_class="XI", order=3,
            lessons=[
                _lesson("phy1-03-01", "Rectilinear Motion", "সরলরৈখিক গতি",
                        "Displacement, velocity, acceleration, equations of motion",
                        "সরণ, বেগ, ত্বরণ, গতির সমীকরণ",
                        Difficulty.EASY, 1, ["v=u+at", "s=ut+½at²"]),
                _lesson("phy1-03-02", "Motion Graphs & Relative Motion", "গতির লেখচিত্র ও আপেক্ষিক গতি",
                        "v-t graphs, s-t graphs, relative velocity",
                        "v-t লেখচিত্র, s-t লেখচিত্র, আপেক্ষিক বেগ",
                        Difficulty.MEDIUM, 2, ["v-t graph", "relative motion"]),
            ],
        ),
        Unit(
            id="phy1-ch04", title="Newtonian Mechanics", title_bn="নিউটনীয় বলবিদ্যা",
            description="Newton's laws, friction, circular motion, FBD",
            description_bn="নিউটনের সূত্র, ঘর্ষণ, বৃত্তাকার গতি, মুক্তবস্তু চিত্র",
            icon="⚙️", nctb_chapter="4", nctb_class="XI", order=4,
            lessons=[
                _lesson("phy1-04-01", "Newton's Laws of Motion", "নিউটনের গতিসূত্র",
                        "Three laws, inertia, F=ma, action-reaction",
                        "তিনটি সূত্র, জড়তা, F=ma, ক্রিয়া-প্রতিক্রিয়া",
                        Difficulty.MEDIUM, 1, ["F=ma", "inertia", "FBD"]),
                _lesson("phy1-04-02", "Friction & Circular Motion", "ঘর্ষণ ও বৃত্তাকার গতি",
                        "Static & kinetic friction, centripetal force, banking",
                        "স্থিতি ও গতি ঘর্ষণ, কেন্দ্রমুখী বল, ব্যাংকিং",
                        Difficulty.MEDIUM, 2, ["friction coefficient", "centripetal force"]),
            ],
        ),
        Unit(
            id="phy1-ch05", title="Work, Energy & Power", title_bn="কাজ, শক্তি ও ক্ষমতা",
            description="Work-energy theorem, KE, PE, conservation, power",
            description_bn="কাজ-শক্তি উপপাদ্য, গতিশক্তি, বিভবশক্তি, সংরক্ষণ, ক্ষমতা",
            icon="⚡", nctb_chapter="5", nctb_class="XI", order=5,
            lessons=[
                _lesson("phy1-05-01", "Work & Energy", "কাজ ও শক্তি",
                        "Work by constant/variable force, KE, PE, conservation",
                        "ধ্রুব/পরিবর্তনশীল বলের কাজ, গতিশক্তি, বিভবশক্তি",
                        Difficulty.MEDIUM, 1, ["W=Fd", "KE=½mv²", "conservation"]),
                _lesson("phy1-05-02", "Power & Collisions", "ক্ষমতা ও সংঘর্ষ",
                        "Power, elastic/inelastic collisions, momentum",
                        "ক্ষমতা, স্থিতিস্থাপক/অস্থিতিস্থাপক সংঘর্ষ, ভরবেগ",
                        Difficulty.HARD, 2, ["P=Fv", "elastic collision"]),
            ],
        ),
        Unit(
            id="phy1-ch06", title="Gravitation", title_bn="মহাকর্ষ ও অভিকর্ষ",
            description="Newton's law of gravitation, g, satellite motion, Kepler's laws",
            description_bn="নিউটনের মহাকর্ষ সূত্র, g, উপগ্রহের গতি, কেপলারের সূত্র",
            icon="🌍", nctb_chapter="6", nctb_class="XI", order=6,
            lessons=[
                _lesson("phy1-06-01", "Gravitation", "মহাকর্ষ ও অভিকর্ষ",
                        "Universal gravitation, g variation, escape velocity, satellites",
                        "বিশ্বজনীন মহাকর্ষ, g এর পরিবর্তন, মুক্তি বেগ, উপগ্রহ",
                        Difficulty.MEDIUM, 1, ["F=GMm/r²", "g=GM/R²", "Kepler"]),
            ],
        ),
        Unit(
            id="phy1-ch07", title="Elasticity & Fluids", title_bn="পদার্থের গাঠনিক ধর্ম",
            description="Stress, strain, Young's modulus, fluid pressure, Bernoulli",
            description_bn="পীড়ন, বিকৃতি, ইয়ংয়ের গুণাঙ্ক, প্রবাহী চাপ, বার্নুলি",
            icon="💧", nctb_chapter="7", nctb_class="XI", order=7,
            lessons=[
                _lesson("phy1-07-01", "Elasticity & Fluid Mechanics", "স্থিতিস্থাপকতা ও প্রবাহী বলবিদ্যা",
                        "Stress-strain, moduli, fluid pressure, viscosity, Bernoulli",
                        "পীড়ন-বিকৃতি, গুণাঙ্ক, প্রবাহী চাপ, সান্দ্রতা, বার্নুলি",
                        Difficulty.MEDIUM, 1, ["Young's modulus", "Bernoulli"]),
            ],
        ),
        Unit(
            id="phy1-ch08", title="Periodic Motion", title_bn="পর্যায়বৃত্তিক গতি",
            description="SHM, pendulum, springs, energy in SHM",
            description_bn="সরল ছন্দিত গতি, দোলক, স্প্রিং, SHM-এ শক্তি",
            icon="🔄", nctb_chapter="8", nctb_class="XI", order=8,
            lessons=[
                _lesson("phy1-08-01", "Simple Harmonic Motion", "সরল ছন্দিত গতি",
                        "SHM equation, period, amplitude, energy, pendulum",
                        "SHM সমীকরণ, পর্যায়কাল, বিস্তার, শক্তি, দোলক",
                        Difficulty.MEDIUM, 1, ["x=Asin(ωt)", "T=2π√(l/g)"]),
            ],
        ),
        Unit(
            id="phy1-ch09", title="Waves", title_bn="তরঙ্গ",
            description="Wave properties, sound, Doppler effect, superposition",
            description_bn="তরঙ্গের ধর্ম, শব্দ, ডপলার ক্রিয়া, উপরিপাতন",
            icon="🌊", nctb_chapter="9", nctb_class="XI", order=9,
            lessons=[
                _lesson("phy1-09-01", "Wave Properties", "তরঙ্গের ধর্ম",
                        "Transverse, longitudinal, wavelength, frequency, speed",
                        "অনুপ্রস্থ, অনুদৈর্ঘ্য, তরঙ্গদৈর্ঘ্য, কম্পাঙ্ক, বেগ",
                        Difficulty.EASY, 1, ["v=fλ"]),
                _lesson("phy1-09-02", "Sound & Doppler Effect", "শব্দ ও ডপলার ক্রিয়া",
                        "Sound waves, resonance, beats, Doppler effect",
                        "শব্দ তরঙ্গ, অনুনাদ, বীট, ডপলার ক্রিয়া",
                        Difficulty.MEDIUM, 2, ["Doppler", "beats"]),
            ],
        ),
        Unit(
            id="phy1-ch10", title="Ideal Gas & Kinetic Theory", title_bn="আদর্শ গ্যাস ও গতিতত্ত্ব",
            description="Gas laws, ideal gas equation, kinetic theory, temperature",
            description_bn="গ্যাস সূত্র, আদর্শ গ্যাস সমীকরণ, গতিতত্ত্ব, তাপমাত্রা",
            icon="🌡️", nctb_chapter="10", nctb_class="XI", order=10,
            lessons=[
                _lesson("phy1-10-01", "Gas Laws & Kinetic Theory", "গ্যাস সূত্র ও গতিতত্ত্ব",
                        "Boyle's, Charles', ideal gas, rms speed, temperature",
                        "বয়েলের, চার্লসের সূত্র, আদর্শ গ্যাস, rms বেগ, তাপমাত্রা",
                        Difficulty.MEDIUM, 1, ["PV=nRT", "KE=3/2kT"]),
            ],
        ),

        # ── 2nd Paper (Class XII) ──
        Unit(
            id="phy2-ch01", title="Thermodynamics", title_bn="তাপগতিবিদ্যা",
            description="Laws of thermodynamics, heat engines, entropy",
            description_bn="তাপগতিবিদ্যার সূত্র, তাপ ইঞ্জিন, এনট্রপি",
            icon="🔥", nctb_chapter="1", nctb_class="XII", order=11,
            lessons=[
                _lesson("phy2-01-01", "Laws of Thermodynamics", "তাপগতিবিদ্যার সূত্র",
                        "1st & 2nd law, heat engines, Carnot cycle, entropy",
                        "১ম ও ২য় সূত্র, তাপ ইঞ্জিন, কার্নো চক্র, এনট্রপি",
                        Difficulty.HARD, 1, ["ΔU=Q-W", "Carnot", "entropy"]),
            ],
        ),
        Unit(
            id="phy2-ch02", title="Static Electricity", title_bn="স্থির তড়িৎ",
            description="Coulomb's law, electric field, potential, capacitance",
            description_bn="কুলম্বের সূত্র, তড়িৎ ক্ষেত্র, বিভব, ধারকত্ব",
            icon="⚡", nctb_chapter="2", nctb_class="XII", order=12,
            lessons=[
                _lesson("phy2-02-01", "Coulomb's Law & Electric Field", "কুলম্বের সূত্র ও তড়িৎ ক্ষেত্র",
                        "Point charges, field lines, Gauss's law",
                        "বিন্দু চার্জ, ক্ষেত্র রেখা, গাউসের সূত্র",
                        Difficulty.MEDIUM, 1, ["F=kq₁q₂/r²", "E=F/q"]),
                _lesson("phy2-02-02", "Electric Potential & Capacitance", "তড়িৎ বিভব ও ধারকত্ব",
                        "Potential, PE, capacitors, series/parallel",
                        "বিভব, বিভবশক্তি, ধারক, শ্রেণী/সমান্তরাল",
                        Difficulty.MEDIUM, 2, ["V=kq/r", "C=Q/V"]),
            ],
        ),
        Unit(
            id="phy2-ch03", title="Current Electricity", title_bn="চল তড়িৎ",
            description="Ohm's law, Kirchhoff's rules, Wheatstone, potentiometer",
            description_bn="ওহমের সূত্র, কির্শফের সূত্র, হুইটস্টোন, পটেনশিওমিটার",
            icon="🔌", nctb_chapter="3", nctb_class="XII", order=13,
            lessons=[
                _lesson("phy2-03-01", "DC Circuits", "সমবর্তনী",
                        "Ohm's law, Kirchhoff's rules, series/parallel, Wheatstone bridge",
                        "ওহমের সূত্র, কির্শফের সূত্র, শ্রেণী/সমান্তরাল, হুইটস্টোন ব্রিজ",
                        Difficulty.MEDIUM, 1, ["V=IR", "Kirchhoff"]),
            ],
        ),
        Unit(
            id="phy2-ch04", title="Magnetic Effect of Current", title_bn="তড়িৎ প্রবাহের চৌম্বক ক্রিয়া ও চুম্বকত্ব",
            description="Biot-Savart, Ampere's law, Lorentz force, solenoid",
            description_bn="বায়ো-স্যাভার্ট, অ্যাম্পিয়ারের সূত্র, লরেঞ্জ বল, সলিনয়েড",
            icon="🧲", nctb_chapter="4", nctb_class="XII", order=14,
            lessons=[
                _lesson("phy2-04-01", "Magnetic Fields & Forces", "চুম্বক ক্ষেত্র ও বল",
                        "Biot-Savart, Ampere's law, force on current, Lorentz force",
                        "বায়ো-স্যাভার্ট, অ্যাম্পিয়ার, তড়িৎবাহী তারের ওপর বল, লরেঞ্জ বল",
                        Difficulty.HARD, 1, ["F=qvB", "B=μ₀nI"]),
            ],
        ),
        Unit(
            id="phy2-ch05", title="Electromagnetic Induction & AC", title_bn="তড়িৎ চুম্বকীয় আবেশ ও দিক পরিবর্তী প্রবাহ",
            description="Faraday's law, Lenz's law, AC generator, transformer",
            description_bn="ফ্যারাডের সূত্র, লেঞ্জের সূত্র, AC জেনারেটর, ট্রান্সফর্মার",
            icon="🔄", nctb_chapter="5", nctb_class="XII", order=15,
            lessons=[
                _lesson("phy2-05-01", "EM Induction & AC", "তড়িৎ চুম্বকীয় আবেশ ও AC",
                        "Faraday's law, Lenz's law, self/mutual inductance, AC, transformer",
                        "ফ্যারাডের সূত্র, লেঞ্জের সূত্র, স্ব/পারস্পরিক আবেশ, AC, ট্রান্সফর্মার",
                        Difficulty.HARD, 1, ["emf=-dΦ/dt", "transformer"]),
            ],
        ),
        Unit(
            id="phy2-ch06", title="Geometrical Optics", title_bn="জ্যামিতিক আলোকবিজ্ঞান",
            description="Reflection, refraction, Snell's law, lenses, instruments",
            description_bn="প্রতিফলন, প্রতিসরণ, স্নেলের সূত্র, লেন্স, যন্ত্র",
            icon="🔍", nctb_chapter="6", nctb_class="XII", order=16,
            lessons=[
                _lesson("phy2-06-01", "Reflection & Refraction", "প্রতিফলন ও প্রতিসরণ",
                        "Snell's law, TIR, lenses, mirror formula, optical instruments",
                        "স্নেলের সূত্র, পূর্ণ অভ্যন্তরীণ প্রতিফলন, লেন্স, আয়না সূত্র",
                        Difficulty.MEDIUM, 1, ["n₁sinθ₁=n₂sinθ₂", "1/f=1/v-1/u"]),
            ],
        ),
        Unit(
            id="phy2-ch07", title="Physical Optics", title_bn="ভৌত আলোকবিজ্ঞান",
            description="Interference, diffraction, polarization",
            description_bn="ব্যতিচার, অপবর্তন, সমবর্তন",
            icon="🌈", nctb_chapter="7", nctb_class="XII", order=17,
            lessons=[
                _lesson("phy2-07-01", "Interference & Diffraction", "ব্যতিচার ও অপবর্তন",
                        "Young's double slit, single slit diffraction, polarization",
                        "ইয়ংয়ের দ্বি-চির পরীক্ষা, একক চির অপবর্তন, সমবর্তন",
                        Difficulty.HARD, 1, ["path difference", "fringe width"]),
            ],
        ),
        Unit(
            id="phy2-ch08", title="Modern Physics", title_bn="আধুনিক পদার্থবিজ্ঞানের সূচনা",
            description="Photoelectric effect, X-rays, de Broglie, uncertainty",
            description_bn="আলোক তড়িৎ ক্রিয়া, এক্স-রে, দ্য ব্রগলি, অনিশ্চয়তা",
            icon="✨", nctb_chapter="8", nctb_class="XII", order=18,
            lessons=[
                _lesson("phy2-08-01", "Photoelectric Effect & Quantum", "আলোক তড়িৎ ক্রিয়া ও কোয়ান্টাম",
                        "Einstein's equation, work function, de Broglie wavelength",
                        "আইনস্টাইনের সমীকরণ, কার্যঅপেক্ষক, দ্য ব্রগলি তরঙ্গদৈর্ঘ্য",
                        Difficulty.MEDIUM, 1, ["E=hf", "KE=hf-φ", "λ=h/p"]),
            ],
        ),
        Unit(
            id="phy2-ch09", title="Atomic Model & Nuclear Physics", title_bn="পরমাণুর মডেল ও নিউক্লীয় পদার্থবিজ্ঞান",
            description="Bohr model, hydrogen spectrum, radioactivity, fission, fusion",
            description_bn="বোর মডেল, হাইড্রোজেন বর্ণালী, তেজস্ক্রিয়তা, বিভাজন, সংযোজন",
            icon="☢️", nctb_chapter="9", nctb_class="XII", order=19,
            lessons=[
                _lesson("phy2-09-01", "Atomic Models & Nuclear Physics", "পরমাণু মডেল ও নিউক্লীয় পদার্থবিজ্ঞান",
                        "Bohr model, energy levels, radioactivity, half-life, E=mc²",
                        "বোর মডেল, শক্তিস্তর, তেজস্ক্রিয়তা, অর্ধায়ু, E=mc²",
                        Difficulty.HARD, 1, ["Bohr", "half-life", "E=mc²"]),
            ],
        ),
        Unit(
            id="phy2-ch10", title="Semiconductor & Electronics", title_bn="সেমিকন্ডাক্টর ও ইলেকট্রনিক্স",
            description="p-n junction, diodes, transistors, logic gates",
            description_bn="p-n সংযোগ, ডায়োড, ট্রানজিস্টর, লজিক গেট",
            icon="💻", nctb_chapter="10", nctb_class="XII", order=20,
            lessons=[
                _lesson("phy2-10-01", "Semiconductors & Electronics", "সেমিকন্ডাক্টর ও ইলেকট্রনিক্স",
                        "Band theory, p-n junction, diodes, transistors, logic gates",
                        "ব্যান্ড তত্ত্ব, p-n সংযোগ, ডায়োড, ট্রানজিস্টর, লজিক গেট",
                        Difficulty.MEDIUM, 1, ["p-n junction", "transistor"]),
            ],
        ),
        Unit(
            id="phy2-ch11", title="Astronomy", title_bn="জ্যোতির্বিজ্ঞান",
            description="Solar system, stars, galaxies, cosmology",
            description_bn="সৌরজগৎ, নক্ষত্র, ছায়াপথ, মহাবিশ্বতত্ত্ব",
            icon="🔭", nctb_chapter="11", nctb_class="XII", order=21,
            lessons=[
                _lesson("phy2-11-01", "Astronomy & Cosmology", "জ্যোতির্বিজ্ঞান ও মহাবিশ্বতত্ত্ব",
                        "Solar system, stellar evolution, Hubble's law, Big Bang",
                        "সৌরজগৎ, নক্ষত্রের বিবর্তন, হাবলের সূত্র, বিগ ব্যাং",
                        Difficulty.EASY, 1, ["light year", "Hubble's law"]),
            ],
        ),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════════
# CHEMISTRY — 1st Paper (5 chapters) + 2nd Paper (5 chapters)
# ═══════════════════════════════════════════════════════════════════════════════

CHEMISTRY = SubjectCurriculum(
    subject=SubjectId.CHEMISTRY,
    title="Chemistry",
    title_bn="রসায়ন",
    icon="⚗️",
    target_exams=[TargetExam.BUET, TargetExam.DU, TargetExam.MEDICAL, TargetExam.GST],
    units=[
        # ── 1st Paper ──
        Unit(
            id="chem1-ch01", title="Safe Use of Laboratory", title_bn="ল্যাবরেটরির নিরাপদ ব্যবহার",
            description="Lab safety, equipment, experimental techniques",
            description_bn="ল্যাব নিরাপত্তা, যন্ত্রপাতি, পরীক্ষামূলক কৌশল",
            icon="🥼", nctb_chapter="1", nctb_class="XI", order=1,
            lessons=[
                _lesson("chem1-01-01", "Laboratory Safety & Equipment", "ল্যাবরেটরি নিরাপত্তা ও যন্ত্রপাতি",
                        "Safety rules, common equipment, basic techniques",
                        "নিরাপত্তা নিয়ম, সাধারণ যন্ত্রপাতি, মৌলিক কৌশল",
                        Difficulty.EASY, 1, ["lab safety"]),
            ],
        ),
        Unit(
            id="chem1-ch02", title="Qualitative Chemistry", title_bn="গুণগত রসায়ন",
            description="Atomic structure, quantum numbers, electron configuration, periodic table",
            description_bn="পরমাণু গঠন, কোয়ান্টাম সংখ্যা, ইলেকট্রন বিন্যাস, পর্যায় সারণী",
            icon="⚛️", nctb_chapter="2", nctb_class="XI", order=2,
            lessons=[
                _lesson("chem1-02-01", "Atomic Structure & Quantum Numbers", "পরমাণু গঠন ও কোয়ান্টাম সংখ্যা",
                        "Atomic models, quantum numbers, electron configuration, orbitals",
                        "পরমাণু মডেল, কোয়ান্টাম সংখ্যা, ইলেকট্রন বিন্যাস, অরবিটাল",
                        Difficulty.MEDIUM, 1, ["aufbau", "Hund's rule", "Pauli"]),
                _lesson("chem1-02-02", "Radioactivity & Isotopes", "তেজস্ক্রিয়তা ও আইসোটোপ",
                        "Radioactive decay, isotopes, half-life, nuclear reactions",
                        "তেজস্ক্রিয় ক্ষয়, আইসোটোপ, অর্ধায়ু, নিউক্লিয় বিক্রিয়া",
                        Difficulty.MEDIUM, 2, ["alpha", "beta", "gamma"]),
            ],
        ),
        Unit(
            id="chem1-ch03", title="Periodic Properties & Chemical Bonding", title_bn="মৌলের পর্যায়বৃত্ত ধর্ম ও রাসায়নিক বন্ধন",
            description="Periodic trends, ionic/covalent/metallic bonds, VSEPR",
            description_bn="পর্যায়বৃত্ত প্রবণতা, আয়নিক/সমযোজী/ধাতব বন্ধন, VSEPR",
            icon="🔗", nctb_chapter="3", nctb_class="XI", order=3,
            lessons=[
                _lesson("chem1-03-01", "Periodic Properties", "পর্যায়বৃত্ত ধর্ম",
                        "Ionization energy, electron affinity, electronegativity, atomic radius",
                        "আয়নীকরণ শক্তি, ইলেকট্রন আসক্তি, তড়িৎ ঋণাত্মকতা, পারমাণবিক ব্যাসার্ধ",
                        Difficulty.MEDIUM, 1, ["periodic trends"]),
                _lesson("chem1-03-02", "Chemical Bonding", "রাসায়নিক বন্ধন",
                        "Ionic, covalent, metallic, hydrogen bonds, VSEPR, hybridization",
                        "আয়নিক, সমযোজী, ধাতব, হাইড্রোজেন বন্ধন, VSEPR, সংকরায়ন",
                        Difficulty.HARD, 2, ["ionic", "covalent", "VSEPR", "sp³"]),
            ],
        ),
        Unit(
            id="chem1-ch04", title="Chemical Changes", title_bn="রাসায়নিক পরিবর্তন",
            description="Chemical reactions, equilibrium, oxidation-reduction, acids & bases",
            description_bn="রাসায়নিক বিক্রিয়া, সাম্যাবস্থা, জারণ-বিজারণ, অম্ল ও ক্ষার",
            icon="🔬", nctb_chapter="4", nctb_class="XI", order=4,
            lessons=[
                _lesson("chem1-04-01", "Chemical Equilibrium", "রাসায়নিক সাম্যাবস্থা",
                        "Kp, Kc, Le Chatelier's principle, equilibrium calculations",
                        "Kp, Kc, লা শাতেলিয়ের নীতি, সাম্যাবস্থা গণনা",
                        Difficulty.MEDIUM, 1, ["Kc", "Le Chatelier"]),
                _lesson("chem1-04-02", "Oxidation-Reduction & Acids-Bases", "জারণ-বিজারণ ও অম্ল-ক্ষার",
                        "Redox reactions, acid-base theories, pH, titration",
                        "রেডক্স বিক্রিয়া, অম্ল-ক্ষার তত্ত্ব, pH, টাইট্রেশন",
                        Difficulty.MEDIUM, 2, ["pH=-log[H+]", "redox"]),
            ],
        ),
        Unit(
            id="chem1-ch05", title="Applied Chemistry", title_bn="কর্মমুখী রসায়ন",
            description="Industrial chemistry, polymers, everyday applications",
            description_bn="শিল্প রসায়ন, পলিমার, দৈনন্দিন প্রয়োগ",
            icon="🏭", nctb_chapter="5", nctb_class="XI", order=5,
            lessons=[
                _lesson("chem1-05-01", "Applied & Industrial Chemistry", "কর্মমুখী ও শিল্প রসায়ন",
                        "Industrial processes, polymers, food chemistry, pharmaceuticals",
                        "শিল্প প্রক্রিয়া, পলিমার, খাদ্য রসায়ন, ঔষধ",
                        Difficulty.EASY, 1, ["industrial chemistry"]),
            ],
        ),

        # ── 2nd Paper ──
        Unit(
            id="chem2-ch01", title="Environmental Chemistry", title_bn="পরিবেশ রসায়ন",
            description="Atmosphere, gas laws, acid rain, greenhouse effect, water quality",
            description_bn="বায়ুমণ্ডল, গ্যাস সূত্র, এসিড বৃষ্টি, গ্রিনহাউস প্রভাব, পানির গুণমান",
            icon="🌍", nctb_chapter="1", nctb_class="XII", order=6,
            lessons=[
                _lesson("chem2-01-01", "Gas Laws & Atmosphere", "গ্যাস সূত্র ও বায়ুমণ্ডল",
                        "Boyle's, Charles', ideal gas, kinetic theory, atmosphere",
                        "বয়েলের, চার্লসের সূত্র, আদর্শ গ্যাস, গতিতত্ত্ব, বায়ুমণ্ডল",
                        Difficulty.MEDIUM, 1, ["PV=nRT", "kinetic theory"]),
                _lesson("chem2-01-02", "Environmental Issues", "পরিবেশ সমস্যা",
                        "Acid rain, greenhouse effect, ozone depletion, water pollution",
                        "এসিড বৃষ্টি, গ্রিনহাউস প্রভাব, ওজোন ক্ষয়, পানি দূষণ",
                        Difficulty.EASY, 2, ["acid rain", "greenhouse", "CFC"]),
            ],
        ),
        Unit(
            id="chem2-ch02", title="Organic Chemistry", title_bn="জৈব রসায়ন",
            description="IUPAC naming, hydrocarbons, functional groups, isomerism, reactions",
            description_bn="IUPAC নামকরণ, হাইড্রোকার্বন, কার্যকরী গ্রুপ, সমাণুতা, বিক্রিয়া",
            icon="🧪", nctb_chapter="2", nctb_class="XII", order=7,
            lessons=[
                _lesson("chem2-02-01", "IUPAC Naming & Classification", "IUPAC নামকরণ ও শ্রেণিবিভাগ",
                        "Naming rules, functional groups, classification of organic compounds",
                        "নামকরণ নিয়ম, কার্যকরী গ্রুপ, জৈব যৌগের শ্রেণিবিভাগ",
                        Difficulty.MEDIUM, 1, ["IUPAC", "functional group"]),
                _lesson("chem2-02-02", "Hydrocarbons & Reactions", "হাইড্রোকার্বন ও বিক্রিয়া",
                        "Alkanes, alkenes, alkynes, benzene, isomerism, reactions",
                        "অ্যালকেন, অ্যালকিন, অ্যালকাইন, বেনজিন, সমাণুতা, বিক্রিয়া",
                        Difficulty.HARD, 2, ["isomerism", "substitution", "addition"]),
            ],
        ),
        Unit(
            id="chem2-ch03", title="Quantitative Chemistry", title_bn="পরিমাণগত রসায়ন",
            description="Mole concept, stoichiometry, titration, gas calculations",
            description_bn="মোল ধারণা, স্টইকিওমেট্রি, টাইট্রেশন, গ্যাস গণনা",
            icon="⚖️", nctb_chapter="3", nctb_class="XII", order=8,
            lessons=[
                _lesson("chem2-03-01", "Mole Concept & Stoichiometry", "মোল ধারণা ও স্টইকিওমেট্রি",
                        "Mole, Avogadro's number, molar mass, balanced equations, yield",
                        "মোল, অ্যাভোগাড্রো সংখ্যা, মোলার ভর, সুষম সমীকরণ",
                        Difficulty.MEDIUM, 1, ["mole", "Avogadro", "stoichiometry"]),
            ],
        ),
        Unit(
            id="chem2-ch04", title="Electrochemistry", title_bn="তড়িৎ রসায়ন",
            description="Electrochemical cells, Nernst equation, electrolysis, batteries",
            description_bn="তড়িৎ রাসায়নিক কোষ, নার্ন্স্ট সমীকরণ, তড়িৎ বিশ্লেষণ, ব্যাটারি",
            icon="🔋", nctb_chapter="4", nctb_class="XII", order=9,
            lessons=[
                _lesson("chem2-04-01", "Electrochemistry", "তড়িৎ রসায়ন",
                        "Galvanic cells, electrolysis, Nernst equation, Faraday's laws",
                        "গ্যালভানিক কোষ, তড়িৎ বিশ্লেষণ, নার্ন্স্ট সমীকরণ, ফ্যারাডের সূত্র",
                        Difficulty.HARD, 1, ["E°cell", "Nernst", "Faraday"]),
            ],
        ),
        Unit(
            id="chem2-ch05", title="Economic Chemistry", title_bn="অর্থনৈতিক রসায়ন",
            description="Industrial processes, fertilizers, glass, cement, metals",
            description_bn="শিল্প প্রক্রিয়া, সার, কাচ, সিমেন্ট, ধাতু",
            icon="💰", nctb_chapter="5", nctb_class="XII", order=10,
            lessons=[
                _lesson("chem2-05-01", "Industrial & Economic Chemistry", "শিল্প ও অর্থনৈতিক রসায়ন",
                        "Manufacturing processes, fertilizers, glass, cement, metallurgy",
                        "উৎপাদন প্রক্রিয়া, সার, কাচ, সিমেন্ট, ধাতুবিদ্যা",
                        Difficulty.EASY, 1, ["Haber process", "metallurgy"]),
            ],
        ),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════════
# HIGHER MATH — 1st Paper (10 chapters) + 2nd Paper (10 chapters)
# ═══════════════════════════════════════════════════════════════════════════════

HIGHER_MATH = SubjectCurriculum(
    subject=SubjectId.HIGHER_MATH,
    title="Higher Mathematics",
    title_bn="উচ্চতর গণিত",
    icon="📐",
    target_exams=[TargetExam.BUET, TargetExam.DU, TargetExam.GST],
    units=[
        # ── 1st Paper ──
        Unit(
            id="hm1-ch01", title="Matrices & Determinants", title_bn="ম্যাট্রিক্স ও নির্ণায়ক",
            description="Matrix operations, inverse, determinants, Cramer's rule",
            description_bn="ম্যাট্রিক্স ক্রিয়া, বিপরীত, নির্ণায়ক, ক্র্যামারের সূত্র",
            icon="🔢", nctb_chapter="1", nctb_class="XI", order=1,
            lessons=[
                _lesson("hm1-01-01", "Matrices & Determinants", "ম্যাট্রিক্স ও নির্ণায়ক",
                        "Matrix types, operations, inverse, det, Cramer's rule",
                        "ম্যাট্রিক্সের প্রকার, ক্রিয়া, বিপরীত, নির্ণায়ক, ক্র্যামারের সূত্র",
                        Difficulty.MEDIUM, 1, ["det(A)", "inverse", "Cramer"]),
            ],
        ),
        Unit(
            id="hm1-ch02", title="Vectors", title_bn="ভেক্টর",
            description="Vector algebra, dot/cross product, applications in geometry",
            description_bn="ভেক্টর বীজগণিত, ডট/ক্রস গুণন, জ্যামিতিতে প্রয়োগ",
            icon="➡️", nctb_chapter="2", nctb_class="XI", order=2,
            lessons=[
                _lesson("hm1-02-01", "Vector Algebra", "ভেক্টর বীজগণিত",
                        "Position vectors, dot product, cross product, applications",
                        "অবস্থান ভেক্টর, ডট গুণন, ক্রস গুণন, প্রয়োগ",
                        Difficulty.MEDIUM, 1, ["dot product", "cross product"]),
            ],
        ),
        Unit(
            id="hm1-ch03", title="Straight Lines", title_bn="সরলরেখা",
            description="Equations, slope, distance, angle between lines, intersection",
            description_bn="সমীকরণ, ঢাল, দূরত্ব, রেখাদ্বয়ের কোণ, ছেদবিন্দু",
            icon="📏", nctb_chapter="3", nctb_class="XI", order=3,
            lessons=[
                _lesson("hm1-03-01", "Straight Lines", "সরলরেখা",
                        "Slope forms, distance, angle, concurrent lines, family of lines",
                        "ঢাল রূপ, দূরত্ব, কোণ, সমবিন্দু রেখা, রেখা পরিবার",
                        Difficulty.MEDIUM, 1, ["y=mx+c", "ax+by+c=0"]),
            ],
        ),
        Unit(
            id="hm1-ch04", title="Circles", title_bn="বৃত্ত",
            description="Circle equations, tangent, normal, intersection",
            description_bn="বৃত্তের সমীকরণ, স্পর্শক, অভিলম্ব, ছেদ",
            icon="⭕", nctb_chapter="4", nctb_class="XI", order=4,
            lessons=[
                _lesson("hm1-04-01", "Circles", "বৃত্ত",
                        "Standard form, general form, tangent, chord, radical axis",
                        "আদর্শ রূপ, সাধারণ রূপ, স্পর্শক, জ্যা, মৌলিক অক্ষ",
                        Difficulty.MEDIUM, 1, ["x²+y²=r²"]),
            ],
        ),
        Unit(
            id="hm1-ch05", title="Permutations & Combinations", title_bn="বিন্যাস ও সমাবেশ",
            description="nPr, nCr, counting principles, applications",
            description_bn="nPr, nCr, গণনা নীতি, প্রয়োগ",
            icon="🎯", nctb_chapter="5", nctb_class="XI", order=5,
            lessons=[
                _lesson("hm1-05-01", "Permutations & Combinations", "বিন্যাস ও সমাবেশ",
                        "Fundamental counting, nPr, nCr, applications",
                        "মৌলিক গণনা, nPr, nCr, প্রয়োগ",
                        Difficulty.MEDIUM, 1, ["nCr=n!/(r!(n-r)!)"]),
            ],
        ),
        Unit(
            id="hm1-ch06", title="Trigonometric Ratios", title_bn="ত্রিকোণমিতিক অনুপাত",
            description="Basic ratios, identities, specific angles, general values",
            description_bn="মৌলিক অনুপাত, অভেদ, নির্দিষ্ট কোণ, সাধারণ মান",
            icon="📐", nctb_chapter="6", nctb_class="XI", order=6,
            lessons=[
                _lesson("hm1-06-01", "Trigonometric Ratios & Identities", "ত্রিকোণমিতিক অনুপাত ও অভেদ",
                        "sin, cos, tan, identities, specific angles",
                        "sin, cos, tan, অভেদ, নির্দিষ্ট কোণ",
                        Difficulty.MEDIUM, 1, ["sin²+cos²=1"]),
            ],
        ),
        Unit(
            id="hm1-ch07", title="Compound Angles", title_bn="সংযুক্ত কোণের ত্রিকোণমিতিক অনুপাত",
            description="Compound angle formulas, multiple angle, submultiple angle",
            description_bn="যৌগিক কোণের সূত্র, গুণিতক কোণ, উপগুণিতক কোণ",
            icon="🔺", nctb_chapter="7", nctb_class="XI", order=7,
            lessons=[
                _lesson("hm1-07-01", "Compound & Multiple Angles", "যৌগিক ও গুণিতক কোণ",
                        "sin(A±B), cos(A±B), double/triple angles, product-sum",
                        "sin(A±B), cos(A±B), দ্বিগুণ/তিনগুণ কোণ, গুণন-যোগ",
                        Difficulty.MEDIUM, 1, ["sin(A+B)", "cos2A"]),
            ],
        ),
        Unit(
            id="hm1-ch08", title="Functions & Graphs", title_bn="ফাংশন ও ফাংশনের লেখচিত্র",
            description="Domain, range, types of functions, graphing",
            description_bn="ডোমেইন, রেঞ্জ, ফাংশনের প্রকার, লেখচিত্র",
            icon="📊", nctb_chapter="8", nctb_class="XI", order=8,
            lessons=[
                _lesson("hm1-08-01", "Functions & Graphs", "ফাংশন ও লেখচিত্র",
                        "Domain, range, inverse, composition, graphs of standard functions",
                        "ডোমেইন, রেঞ্জ, বিপরীত, যৌগিক, আদর্শ ফাংশনের লেখচিত্র",
                        Difficulty.MEDIUM, 1, ["domain", "range", "inverse"]),
            ],
        ),
        Unit(
            id="hm1-ch09", title="Differentiation", title_bn="অন্তরীকরণ",
            description="Limits, derivatives, chain rule, applications",
            description_bn="সীমা, অন্তরকলন, শৃঙ্খল নিয়ম, প্রয়োগ",
            icon="∂", nctb_chapter="9", nctb_class="XI", order=9,
            lessons=[
                _lesson("hm1-09-01", "Limits & Differentiation", "সীমা ও অন্তরীকরণ",
                        "Limits, first principles, rules (power, product, quotient, chain)",
                        "সীমা, মূলনীতি, নিয়ম (ঘাত, গুণন, ভাগ, শৃঙ্খল)",
                        Difficulty.MEDIUM, 1, ["chain rule", "product rule"]),
                _lesson("hm1-09-02", "Applications of Derivatives", "অন্তরকলনের প্রয়োগ",
                        "Maxima/minima, tangent/normal, rate of change",
                        "চরম/অবম মান, স্পর্শক/অভিলম্ব, পরিবর্তনের হার",
                        Difficulty.HARD, 2, ["maxima", "minima", "tangent"]),
            ],
        ),
        Unit(
            id="hm1-ch10", title="Integration", title_bn="যোগজীকরণ",
            description="Indefinite & definite integrals, techniques, area",
            description_bn="অনির্দিষ্ট ও নির্দিষ্ট সমাকলন, কৌশল, ক্ষেত্রফল",
            icon="∫", nctb_chapter="10", nctb_class="XI", order=10,
            lessons=[
                _lesson("hm1-10-01", "Integration Basics", "সমাকলনের মূলনীতি",
                        "Basic integrals, substitution, by parts",
                        "মৌলিক সমাকলন, প্রতিস্থাপন, খণ্ডসমাকলন",
                        Difficulty.MEDIUM, 1, ["∫xⁿdx", "substitution"]),
                _lesson("hm1-10-02", "Definite Integrals & Area", "নির্দিষ্ট সমাকলন ও ক্ষেত্রফল",
                        "Definite integrals, area under curve, properties",
                        "নির্দিষ্ট সমাকলন, বক্ররেখার ক্ষেত্রফল, ধর্ম",
                        Difficulty.HARD, 2, ["area under curve"]),
            ],
        ),

        # ── 2nd Paper ──
        Unit(
            id="hm2-ch01", title="Real Numbers & Inequalities", title_bn="বাস্তব সংখ্যা ও অসমতা",
            description="Number properties, inequalities, absolute value",
            description_bn="সংখ্যার ধর্ম, অসমতা, পরমমান",
            icon="🔢", nctb_chapter="1", nctb_class="XII", order=11,
            lessons=[
                _lesson("hm2-01-01", "Real Numbers & Inequalities", "বাস্তব সংখ্যা ও অসমতা",
                        "Number line, inequalities, absolute value, AM-GM",
                        "সংখ্যারেখা, অসমতা, পরমমান, AM-GM",
                        Difficulty.MEDIUM, 1, ["AM-GM", "inequalities"]),
            ],
        ),
        Unit(
            id="hm2-ch02", title="Linear Programming", title_bn="যোগাশ্রয়ী প্রোগ্রাম",
            description="Linear constraints, optimization, graphical method",
            description_bn="রৈখিক সীমাবদ্ধতা, সর্বোত্তমকরণ, লেখচিত্র পদ্ধতি",
            icon="📈", nctb_chapter="2", nctb_class="XII", order=12,
            lessons=[
                _lesson("hm2-02-01", "Linear Programming", "যোগাশ্রয়ী প্রোগ্রাম",
                        "Constraints, feasible region, optimization, simplex",
                        "সীমাবদ্ধতা, সম্ভাব্য অঞ্চল, সর্বোত্তমকরণ",
                        Difficulty.MEDIUM, 1, ["feasible region", "maximize"]),
            ],
        ),
        Unit(
            id="hm2-ch03", title="Complex Numbers", title_bn="জটিল সংখ্যা",
            description="Argand diagram, polar form, De Moivre's theorem",
            description_bn="আর্গান্ড চিত্র, পোলার রূপ, দ্য ময়ভ্রের উপপাদ্য",
            icon="🌀", nctb_chapter="3", nctb_class="XII", order=13,
            lessons=[
                _lesson("hm2-03-01", "Complex Numbers", "জটিল সংখ্যা",
                        "Argand diagram, modulus, polar form, De Moivre, roots of unity",
                        "আর্গান্ড চিত্র, মডুলাস, পোলার রূপ, দ্য ময়ভ্র, একের মূল",
                        Difficulty.HARD, 1, ["i²=-1", "De Moivre"]),
            ],
        ),
        Unit(
            id="hm2-ch04", title="Polynomials & Equations", title_bn="বহুপদী ও বহুপদী সমীকরণ",
            description="Polynomial roots, factor theorem, synthetic division",
            description_bn="বহুপদীর মূল, উৎপাদক উপপাদ্য, কৃত্রিম ভাগ",
            icon="🔤", nctb_chapter="4", nctb_class="XII", order=14,
            lessons=[
                _lesson("hm2-04-01", "Polynomials & Equations", "বহুপদী ও সমীকরণ",
                        "Factor theorem, remainder theorem, roots, Vieta's formulas",
                        "উৎপাদক উপপাদ্য, ভাগশেষ উপপাদ্য, মূল, ভিয়েতার সূত্র",
                        Difficulty.MEDIUM, 1, ["factor theorem"]),
            ],
        ),
        Unit(
            id="hm2-ch05", title="Binomial Expansion", title_bn="দ্বিপদী বিস্তৃতি",
            description="Binomial theorem, general term, middle term, applications",
            description_bn="দ্বিপদী উপপাদ্য, সাধারণ পদ, মধ্যম পদ, প্রয়োগ",
            icon="📑", nctb_chapter="5", nctb_class="XII", order=15,
            lessons=[
                _lesson("hm2-05-01", "Binomial Expansion", "দ্বিপদী বিস্তৃতি",
                        "Binomial theorem, general/middle term, Pascal's triangle",
                        "দ্বিপদী উপপাদ্য, সাধারণ/মধ্যম পদ, প্যাসক্যালের ত্রিভুজ",
                        Difficulty.MEDIUM, 1, ["(a+b)ⁿ", "nCr"]),
            ],
        ),
        Unit(
            id="hm2-ch06", title="Conics", title_bn="কণিক",
            description="Parabola, ellipse, hyperbola — equations and properties",
            description_bn="পরাবৃত্ত, উপবৃত্ত, অধিবৃত্ত — সমীকরণ ও ধর্ম",
            icon="🥚", nctb_chapter="6", nctb_class="XII", order=16,
            lessons=[
                _lesson("hm2-06-01", "Conics", "কণিক",
                        "Parabola, ellipse, hyperbola, eccentricity, tangent/normal",
                        "পরাবৃত্ত, উপবৃত্ত, অধিবৃত্ত, উৎকেন্দ্রিকতা, স্পর্শক/অভিলম্ব",
                        Difficulty.HARD, 1, ["e<1 ellipse", "e>1 hyperbola"]),
            ],
        ),
        Unit(
            id="hm2-ch07", title="Trigonometric Functions", title_bn="ত্রিকোণমিতিক ফাংশন",
            description="Inverse trig, trigonometric equations, general solutions",
            description_bn="বিপরীত ত্রিকোণমিতি, ত্রিকোণমিতিক সমীকরণ, সাধারণ সমাধান",
            icon="📐", nctb_chapter="7", nctb_class="XII", order=17,
            lessons=[
                _lesson("hm2-07-01", "Inverse Trig & Equations", "বিপরীত ত্রিকোণমিতি ও সমীকরণ",
                        "sin⁻¹, cos⁻¹, tan⁻¹, general solutions, principal values",
                        "sin⁻¹, cos⁻¹, tan⁻¹, সাধারণ সমাধান, মুখ্য মান",
                        Difficulty.HARD, 1, ["general solution", "principal value"]),
            ],
        ),
        Unit(
            id="hm2-ch08", title="Statics", title_bn="স্থিতিবিদ্যা",
            description="Forces in equilibrium, moments, centre of gravity, friction",
            description_bn="সাম্যাবস্থায় বল, ভ্রামক, ভরকেন্দ্র, ঘর্ষণ",
            icon="⚖️", nctb_chapter="8", nctb_class="XII", order=18,
            lessons=[
                _lesson("hm2-08-01", "Statics", "স্থিতিবিদ্যা",
                        "Equilibrium, moments, Lami's theorem, centre of gravity",
                        "সাম্যাবস্থা, ভ্রামক, ল্যামির উপপাদ্য, ভরকেন্দ্র",
                        Difficulty.HARD, 1, ["Lami's theorem", "moments"]),
            ],
        ),
        Unit(
            id="hm2-ch09", title="Motion in a Plane", title_bn="সমতলে বস্তুকণার গতি",
            description="Projectile motion, relative motion, circular motion",
            description_bn="প্রক্ষেপ গতি, আপেক্ষিক গতি, বৃত্তাকার গতি",
            icon="🎯", nctb_chapter="9", nctb_class="XII", order=19,
            lessons=[
                _lesson("hm2-09-01", "Projectile & Circular Motion", "প্রক্ষেপ ও বৃত্তাকার গতি",
                        "Projectile range/height/time, circular motion, relative motion",
                        "প্রক্ষেপ পাল্লা/উচ্চতা/সময়, বৃত্তাকার গতি, আপেক্ষিক গতি",
                        Difficulty.HARD, 1, ["R=u²sin2θ/g"]),
            ],
        ),
        Unit(
            id="hm2-ch10", title="Dispersion & Probability", title_bn="বিস্তার পরিমাপ ও সম্ভাব্যতা",
            description="Standard deviation, variance, probability, Bayes theorem",
            description_bn="পরিমিত ব্যবধান, ভেদাঙ্ক, সম্ভাব্যতা, বেইজ উপপাদ্য",
            icon="🎲", nctb_chapter="10", nctb_class="XII", order=20,
            lessons=[
                _lesson("hm2-10-01", "Statistics & Probability", "পরিসংখ্যান ও সম্ভাব্যতা",
                        "Variance, SD, probability axioms, conditional, Bayes",
                        "ভেদাঙ্ক, পরিমিত ব্যবধান, সম্ভাব্যতার স্বতঃসিদ্ধ, শর্তাধীন, বেইজ",
                        Difficulty.MEDIUM, 1, ["P(A|B)", "Bayes"]),
            ],
        ),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════════
# BIOLOGY — 1st Paper (12 chapters) + 2nd Paper (12 chapters)
# ═══════════════════════════════════════════════════════════════════════════════

BIOLOGY = SubjectCurriculum(
    subject=SubjectId.BIOLOGY,
    title="Biology",
    title_bn="জীববিজ্ঞান",
    icon="🧬",
    target_exams=[TargetExam.MEDICAL, TargetExam.DU, TargetExam.GST],
    units=[
        # ── 1st Paper (Botany / উদ্ভিদবিজ্ঞান) ──
        Unit(
            id="bio1-ch01", title="Cell & Its Structure", title_bn="কোষ ও এর গঠন",
            description="Prokaryotic vs eukaryotic, organelles, cell membrane",
            description_bn="প্রোক্যারিওটিক বনাম ইউক্যারিওটিক, অঙ্গাণু, কোষ ঝিল্লি",
            icon="🔬", nctb_chapter="1", nctb_class="XI", order=1,
            lessons=[
                _lesson("bio1-01-01", "Cell Structure & Organelles", "কোষ গঠন ও অঙ্গাণু",
                        "Cell types, organelles, membrane, transport",
                        "কোষের প্রকার, অঙ্গাণু, ঝিল্লি, পরিবহন",
                        Difficulty.EASY, 1, ["mitochondria", "ribosome", "nucleus"]),
            ],
        ),
        Unit(
            id="bio1-ch02", title="Cell Division", title_bn="কোষ বিভাজন",
            description="Mitosis, meiosis, cell cycle, significance",
            description_bn="মাইটোসিস, মিয়োসিস, কোষ চক্র, তাৎপর্য",
            icon="🧫", nctb_chapter="2", nctb_class="XI", order=2,
            lessons=[
                _lesson("bio1-02-01", "Mitosis & Meiosis", "মাইটোসিস ও মিয়োসিস",
                        "Cell cycle, mitosis phases, meiosis, crossing over",
                        "কোষ চক্র, মাইটোসিসের ধাপ, মিয়োসিস, ক্রসিং ওভার",
                        Difficulty.MEDIUM, 1, ["prophase", "metaphase", "crossing over"]),
            ],
        ),
        Unit(
            id="bio1-ch03", title="Cell Chemistry", title_bn="কোষ রসায়ন",
            description="Carbohydrates, proteins, lipids, nucleic acids, enzymes",
            description_bn="শর্করা, প্রোটিন, লিপিড, নিউক্লিক এসিড, এনজাইম",
            icon="🧬", nctb_chapter="3", nctb_class="XI", order=3,
            lessons=[
                _lesson("bio1-03-01", "Biomolecules", "জৈব অণু",
                        "Carbohydrates, proteins, lipids, nucleic acids, enzymes",
                        "শর্করা, প্রোটিন, লিপিড, নিউক্লিক এসিড, এনজাইম",
                        Difficulty.MEDIUM, 1, ["DNA", "RNA", "enzyme"]),
            ],
        ),
        Unit(
            id="bio1-ch04", title="Microorganisms", title_bn="অণুজীব",
            description="Bacteria, viruses, fungi basics, microbial diseases",
            description_bn="ব্যাকটেরিয়া, ভাইরাস, ছত্রাক মূলনীতি, অণুজীবজনিত রোগ",
            icon="🦠", nctb_chapter="4", nctb_class="XI", order=4,
            lessons=[
                _lesson("bio1-04-01", "Microorganisms", "অণুজীব",
                        "Bacteria, viruses, structure, reproduction, diseases",
                        "ব্যাকটেরিয়া, ভাইরাস, গঠন, প্রজনন, রোগ",
                        Difficulty.MEDIUM, 1, ["virus", "bacteria"]),
            ],
        ),
        Unit(
            id="bio1-ch05", title="Algae & Fungi", title_bn="শৈবাল ও ছত্রাক",
            description="Classification, structure, reproduction of algae & fungi",
            description_bn="শ্রেণিবিভাগ, গঠন, শৈবাল ও ছত্রাকের প্রজনন",
            icon="🍄", nctb_chapter="5", nctb_class="XI", order=5,
            lessons=[
                _lesson("bio1-05-01", "Algae & Fungi", "শৈবাল ও ছত্রাক",
                        "Types, structure, reproduction, economic importance",
                        "প্রকার, গঠন, প্রজনন, অর্থনৈতিক গুরুত্ব",
                        Difficulty.EASY, 1, ["algae", "fungi"]),
            ],
        ),
        Unit(
            id="bio1-ch06", title="Bryophyta & Pteridophyta", title_bn="ব্রায়োফাইটা ও টেরিডোফাইটা",
            description="Mosses, ferns — structure, life cycle, alternation of generations",
            description_bn="মস, ফার্ন — গঠন, জীবনচক্র, জনুক্রম",
            icon="🌱", nctb_chapter="6", nctb_class="XI", order=6,
            lessons=[
                _lesson("bio1-06-01", "Bryophyta & Pteridophyta", "ব্রায়োফাইটা ও টেরিডোফাইটা",
                        "Mosses, ferns, life cycle, alternation of generations",
                        "মস, ফার্ন, জীবনচক্র, জনুক্রম",
                        Difficulty.MEDIUM, 1, ["alternation of generations"]),
            ],
        ),
        Unit(
            id="bio1-ch07", title="Gymnosperms & Angiosperms", title_bn="নগ্নবীজী ও আবৃতবীজী উদ্ভিদ",
            description="Seed plants, flowers, fruits, plant classification",
            description_bn="বীজ উদ্ভিদ, ফুল, ফল, উদ্ভিদ শ্রেণিবিভাগ",
            icon="🌺", nctb_chapter="7", nctb_class="XI", order=7,
            lessons=[
                _lesson("bio1-07-01", "Seed Plants", "বীজ উদ্ভিদ",
                        "Gymnosperms, angiosperms, flower structure, classification",
                        "নগ্নবীজী, আবৃতবীজী, ফুলের গঠন, শ্রেণিবিভাগ",
                        Difficulty.MEDIUM, 1, ["monocot", "dicot"]),
            ],
        ),
        Unit(
            id="bio1-ch08", title="Tissues & Tissue Systems", title_bn="টিস্যু ও টিস্যুতন্ত্র",
            description="Simple, complex, meristematic, permanent tissues",
            description_bn="সরল, জটিল, ভাজক, স্থায়ী টিস্যু",
            icon="🧱", nctb_chapter="8", nctb_class="XI", order=8,
            lessons=[
                _lesson("bio1-08-01", "Plant Tissues", "উদ্ভিদ টিস্যু",
                        "Meristematic, parenchyma, xylem, phloem, vascular bundles",
                        "ভাজক, প্যারেনকাইমা, জাইলেম, ফ্লোয়েম, ভাস্কুলার বান্ডেল",
                        Difficulty.MEDIUM, 1, ["xylem", "phloem"]),
            ],
        ),
        Unit(
            id="bio1-ch09", title="Plant Physiology", title_bn="উদ্ভিদ শারীরতত্ত্ব",
            description="Photosynthesis, respiration, transpiration, mineral nutrition",
            description_bn="সালোকসংশ্লেষণ, শ্বসন, প্রস্বেদন, খনিজ পুষ্টি",
            icon="🌿", nctb_chapter="9", nctb_class="XI", order=9,
            lessons=[
                _lesson("bio1-09-01", "Photosynthesis", "সালোকসংশ্লেষণ",
                        "Light reactions, Calvin cycle, C3/C4/CAM, factors",
                        "আলোক বিক্রিয়া, ক্যালভিন চক্র, C3/C4/CAM, প্রভাবক",
                        Difficulty.MEDIUM, 1, ["6CO₂+6H₂O→C₆H₁₂O₆+6O₂"]),
                _lesson("bio1-09-02", "Respiration & Transpiration", "শ্বসন ও প্রস্বেদন",
                        "Glycolysis, Krebs, ETC, transpiration, mineral absorption",
                        "গ্লাইকোলাইসিস, ক্রেবস, ETC, প্রস্বেদন, খনিজ শোষণ",
                        Difficulty.HARD, 2, ["glycolysis", "Krebs", "ATP"]),
            ],
        ),
        Unit(
            id="bio1-ch10", title="Plant Reproduction", title_bn="উদ্ভিদ প্রজনন",
            description="Asexual, sexual reproduction, pollination, fertilization",
            description_bn="অযৌন, যৌন প্রজনন, পরাগায়ন, নিষেক",
            icon="🌸", nctb_chapter="10", nctb_class="XI", order=10,
            lessons=[
                _lesson("bio1-10-01", "Plant Reproduction", "উদ্ভিদ প্রজনন",
                        "Asexual methods, flower structure, pollination, double fertilization",
                        "অযৌন পদ্ধতি, ফুলের গঠন, পরাগায়ন, দ্বি-নিষেক",
                        Difficulty.MEDIUM, 1, ["pollination", "double fertilization"]),
            ],
        ),
        Unit(
            id="bio1-ch11", title="Biotechnology", title_bn="জীবপ্রযুক্তি",
            description="Genetic engineering, PCR, cloning, GMO, applications",
            description_bn="জিনগত প্রকৌশল, PCR, ক্লোনিং, GMO, প্রয়োগ",
            icon="🧪", nctb_chapter="11", nctb_class="XI", order=11,
            lessons=[
                _lesson("bio1-11-01", "Biotechnology", "জীবপ্রযুক্তি",
                        "Recombinant DNA, PCR, cloning, GMO, gene therapy",
                        "রিকম্বিনেন্ট DNA, PCR, ক্লোনিং, GMO, জিন থেরাপি",
                        Difficulty.HARD, 1, ["PCR", "recombinant DNA"]),
            ],
        ),
        Unit(
            id="bio1-ch12", title="Ecology & Conservation", title_bn="জীবের পরিবেশ, বিস্তার ও সংরক্ষণ",
            description="Ecosystems, food web, biodiversity, conservation",
            description_bn="বাস্তুতন্ত্র, খাদ্যজাল, জীববৈচিত্র্য, সংরক্ষণ",
            icon="🌍", nctb_chapter="12", nctb_class="XI", order=12,
            lessons=[
                _lesson("bio1-12-01", "Ecology & Environment", "বাস্তুবিদ্যা ও পরিবেশ",
                        "Ecosystem, food chain, energy flow, biodiversity, conservation",
                        "বাস্তুতন্ত্র, খাদ্যশৃঙ্খল, শক্তির প্রবাহ, জীববৈচিত্র্য, সংরক্ষণ",
                        Difficulty.EASY, 1, ["food chain", "biodiversity"]),
            ],
        ),

        # ── 2nd Paper (Zoology / প্রাণিবিদ্যা) ──
        Unit(
            id="bio2-ch01", title="Animal Diversity & Classification", title_bn="প্রাণীর বিভিন্নতা ও শ্রেণিবিন্যাস",
            description="Animal kingdom classification, phyla, characteristics",
            description_bn="প্রাণিজগতের শ্রেণিবিভাগ, পর্ব, বৈশিষ্ট্য",
            icon="🦋", nctb_chapter="1", nctb_class="XII", order=13,
            lessons=[
                _lesson("bio2-01-01", "Animal Classification", "প্রাণী শ্রেণিবিন্যাস",
                        "Major phyla, characteristics, examples",
                        "প্রধান পর্ব, বৈশিষ্ট্য, উদাহরণ",
                        Difficulty.MEDIUM, 1, ["Chordata", "Arthropoda"]),
            ],
        ),
        Unit(
            id="bio2-ch02", title="Animal Introduction", title_bn="প্রাণীর পরিচিতি",
            description="Grasshopper, Rohu fish, Hydra — model organisms",
            description_bn="ঘাসফড়িং, রুই মাছ, হাইড্রা — আদর্শ জীব",
            icon="🦗", nctb_chapter="2", nctb_class="XII", order=14,
            lessons=[
                _lesson("bio2-02-01", "Model Organisms", "আদর্শ জীব",
                        "Grasshopper, Rohu, Hydra — anatomy, physiology",
                        "ঘাসফড়িং, রুই, হাইড্রা — শারীরস্থান, শারীরবিদ্যা",
                        Difficulty.MEDIUM, 1, ["Hydra", "grasshopper"]),
            ],
        ),
        Unit(
            id="bio2-ch03", title="Digestion & Absorption", title_bn="মানব শারীরতত্ত্ব: পরিপাক ও শোষণ",
            description="Digestive system, enzymes, absorption, disorders",
            description_bn="পরিপাকতন্ত্র, এনজাইম, শোষণ, রোগ",
            icon="🫃", nctb_chapter="3", nctb_class="XII", order=15,
            lessons=[
                _lesson("bio2-03-01", "Digestion & Absorption", "পরিপাক ও শোষণ",
                        "GI tract, enzymes, bile, absorption, disorders",
                        "পরিপাকনালী, এনজাইম, পিত্ত, শোষণ, রোগ",
                        Difficulty.MEDIUM, 1, ["pepsin", "bile", "villi"]),
            ],
        ),
        Unit(
            id="bio2-ch04", title="Blood & Circulation", title_bn="মানব শারীরতত্ত্ব: রক্ত ও সঞ্চালন",
            description="Heart, blood groups, cardiac cycle, blood vessels",
            description_bn="হৃৎপিণ্ড, রক্তের গ্রুপ, হৃৎচক্র, রক্তনালী",
            icon="🫀", nctb_chapter="4", nctb_class="XII", order=16,
            lessons=[
                _lesson("bio2-04-01", "Blood & Circulation", "রক্ত ও সঞ্চালন",
                        "Blood components, heart anatomy, cardiac cycle, blood groups",
                        "রক্তের উপাদান, হৃৎপিণ্ডের গঠন, হৃৎচক্র, রক্তের গ্রুপ",
                        Difficulty.MEDIUM, 1, ["ABO blood group", "cardiac cycle"]),
            ],
        ),
        Unit(
            id="bio2-ch05", title="Respiration & Breathing", title_bn="মানব শারীরতত্ত্ব: শ্বাসক্রিয়া ও শ্বসন",
            description="Respiratory system, gas exchange, lung function",
            description_bn="শ্বসনতন্ত্র, গ্যাস বিনিময়, ফুসফুসের কাজ",
            icon="🫁", nctb_chapter="5", nctb_class="XII", order=17,
            lessons=[
                _lesson("bio2-05-01", "Respiration", "শ্বসন",
                        "Lungs, gas exchange, breathing mechanism, disorders",
                        "ফুসফুস, গ্যাস বিনিময়, শ্বাস-প্রশ্বাস প্রক্রিয়া, রোগ",
                        Difficulty.MEDIUM, 1, ["alveoli", "gas exchange"]),
            ],
        ),
        Unit(
            id="bio2-ch06", title="Excretion", title_bn="মানব শারীরতত্ত্ব: বর্জ্য ও নিষ্কাশন",
            description="Kidney, nephron, urine formation, osmoregulation",
            description_bn="কিডনি, নেফ্রন, মূত্র গঠন, অভিস্রবণ নিয়ন্ত্রণ",
            icon="🫘", nctb_chapter="6", nctb_class="XII", order=18,
            lessons=[
                _lesson("bio2-06-01", "Excretion", "রেচন",
                        "Kidney structure, nephron, filtration, reabsorption",
                        "কিডনির গঠন, নেফ্রন, পরিস্রাবণ, পুনঃশোষণ",
                        Difficulty.MEDIUM, 1, ["nephron", "filtration"]),
            ],
        ),
        Unit(
            id="bio2-ch07", title="Movement & Locomotion", title_bn="মানব শারীরতত্ত্ব: চলন ও অঙ্গচালনা",
            description="Skeletal system, muscles, joints, movement disorders",
            description_bn="কঙ্কালতন্ত্র, পেশী, জোড়া, চলন সমস্যা",
            icon="💪", nctb_chapter="7", nctb_class="XII", order=19,
            lessons=[
                _lesson("bio2-07-01", "Movement & Locomotion", "চলন ও অঙ্গচালনা",
                        "Bones, joints, muscle types, skeletal disorders",
                        "অস্থি, জোড়া, পেশীর প্রকার, কঙ্কাল সমস্যা",
                        Difficulty.EASY, 1, ["skeletal muscle", "joints"]),
            ],
        ),
        Unit(
            id="bio2-ch08", title="Coordination & Control", title_bn="মানব শারীরতত্ত্ব: সমন্বয় ও নিয়ন্ত্রণ",
            description="Nervous system, endocrine system, hormones, reflex",
            description_bn="স্নায়ুতন্ত্র, অন্তঃক্ষরা তন্ত্র, হরমোন, প্রতিবর্ত ক্রিয়া",
            icon="🧠", nctb_chapter="8", nctb_class="XII", order=20,
            lessons=[
                _lesson("bio2-08-01", "Nervous System", "স্নায়ুতন্ত্র",
                        "Neurons, brain, spinal cord, reflex arc, synapse",
                        "নিউরন, মস্তিষ্ক, সুষুম্নাকাণ্ড, প্রতিবর্ত চাপ, সাইন্যাপস",
                        Difficulty.MEDIUM, 1, ["action potential", "reflex"]),
                _lesson("bio2-08-02", "Endocrine System", "অন্তঃক্ষরা তন্ত্র",
                        "Pituitary, thyroid, adrenal, pancreas hormones, feedback",
                        "পিটুইটারি, থাইরয়েড, অ্যাড্রেনাল, অগ্ন্যাশয় হরমোন, ফিডব্যাক",
                        Difficulty.MEDIUM, 2, ["insulin", "thyroid"]),
            ],
        ),
        Unit(
            id="bio2-ch09", title="Continuity of Human Life", title_bn="মানব জীবনের ধারাবাহিকতা",
            description="Reproductive system, gametogenesis, fertilization, embryology",
            description_bn="প্রজননতন্ত্র, গ্যামিটোজেনেসিস, নিষেক, ভ্রূণবিদ্যা",
            icon="👶", nctb_chapter="9", nctb_class="XII", order=21,
            lessons=[
                _lesson("bio2-09-01", "Human Reproduction", "মানব প্রজনন",
                        "Male/female reproductive system, gametogenesis, fertilization",
                        "পুরুষ/স্ত্রী প্রজননতন্ত্র, গ্যামিটোজেনেসিস, নিষেক",
                        Difficulty.MEDIUM, 1, ["spermatogenesis", "oogenesis"]),
            ],
        ),
        Unit(
            id="bio2-ch10", title="Human Immunity", title_bn="মানবদেহের প্রতিরক্ষা",
            description="Innate, adaptive immunity, antibodies, vaccines",
            description_bn="সহজাত, অভিযোজিত প্রতিরক্ষা, অ্যান্টিবডি, টিকা",
            icon="🛡️", nctb_chapter="10", nctb_class="XII", order=22,
            lessons=[
                _lesson("bio2-10-01", "Immunity", "প্রতিরক্ষা",
                        "Innate, adaptive, antibodies, T/B cells, vaccines, AIDS",
                        "সহজাত, অভিযোজিত, অ্যান্টিবডি, T/B কোষ, টিকা, AIDS",
                        Difficulty.MEDIUM, 1, ["antibody", "T-cell", "vaccine"]),
            ],
        ),
        Unit(
            id="bio2-ch11", title="Genetics & Evolution", title_bn="জিনতত্ত্ব ও বিবর্তন",
            description="Mendelian genetics, DNA, mutations, natural selection",
            description_bn="মেন্ডেলের জিনতত্ত্ব, DNA, মিউটেশন, প্রাকৃতিক নির্বাচন",
            icon="🧬", nctb_chapter="11", nctb_class="XII", order=23,
            lessons=[
                _lesson("bio2-11-01", "Mendelian Genetics", "মেন্ডেলের জিনতত্ত্ব",
                        "Monohybrid, dihybrid, Punnett square, linked genes, sex-linked",
                        "একসংকর, দ্বিসংকর, পানেট স্কোয়ার, সংযুক্ত জিন, লিঙ্গ-সংযুক্ত",
                        Difficulty.MEDIUM, 1, ["3:1 ratio", "Punnett"]),
                _lesson("bio2-11-02", "DNA & Evolution", "DNA ও বিবর্তন",
                        "DNA structure, replication, transcription, translation, evolution",
                        "DNA গঠন, প্রতিলিপি, ট্রান্সক্রিপশন, ট্রান্সলেশন, বিবর্তন",
                        Difficulty.HARD, 2, ["central dogma", "natural selection"]),
            ],
        ),
        Unit(
            id="bio2-ch12", title="Animal Behavior", title_bn="প্রাণীর আচরণ",
            description="Innate, learned behavior, social behavior, communication",
            description_bn="সহজাত, শিক্ষিত আচরণ, সামাজিক আচরণ, যোগাযোগ",
            icon="🐾", nctb_chapter="12", nctb_class="XII", order=24,
            lessons=[
                _lesson("bio2-12-01", "Animal Behavior", "প্রাণীর আচরণ",
                        "Innate, imprinting, conditioning, social behavior, migration",
                        "সহজাত, ইমপ্রিন্টিং, শর্তায়ন, সামাজিক আচরণ, পরিযান",
                        Difficulty.EASY, 1, ["instinct", "imprinting"]),
            ],
        ),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════════
# GENERAL MATH (for DU, Medical — non-Higher Math)
# ═══════════════════════════════════════════════════════════════════════════════

GENERAL_MATH = SubjectCurriculum(
    subject=SubjectId.GENERAL_MATH,
    title="General Mathematics",
    title_bn="সাধারণ গণিত",
    icon="➕",
    target_exams=[TargetExam.DU, TargetExam.MEDICAL, TargetExam.GST],
    units=[
        # ── পাটিগণিত (Arithmetic) ──
        Unit(
            id="gmath-ch01", title="Number System", title_bn="সংখ্যাতত্ত্ব",
            description="Natural, integer, rational, irrational numbers, LCM, HCF, divisibility",
            description_bn="স্বাভাবিক, পূর্ণ, মূলদ, অমূলদ সংখ্যা, ল.সা.গু, গ.সা.গু, বিভাজ্যতা",
            icon="🔢", nctb_chapter="1", nctb_class="XI", order=1,
            lessons=[
                _lesson("gm-01-01", "Types of Numbers & Properties", "সংখ্যার প্রকারভেদ ও ধর্ম",
                        "Natural, whole, integer, rational, irrational, real numbers",
                        "স্বাভাবিক, পূর্ণ, মূলদ, অমূলদ, বাস্তব সংখ্যা",
                        Difficulty.EASY, 1, ["prime", "composite", "divisibility"]),
                _lesson("gm-01-02", "LCM, HCF & Divisibility", "ল.সা.গু, গ.সা.গু ও বিভাজ্যতা",
                        "LCM, HCF by factoring and division, divisibility rules",
                        "উৎপাদক ও ভাগ পদ্ধতিতে ল.সা.গু, গ.সা.গু, বিভাজ্যতার নিয়ম",
                        Difficulty.EASY, 2, ["LCM", "HCF"]),
            ],
        ),
        Unit(
            id="gmath-ch02", title="Indices & Surds", title_bn="সূচক ও করণী",
            description="Laws of indices, surds, rationalization",
            description_bn="সূচকের নিয়ম, করণী, মূলদকরণ",
            icon="📐", nctb_chapter="2", nctb_class="XI", order=2,
            lessons=[
                _lesson("gm-02-01", "Laws of Indices", "সূচকের নিয়মাবলি",
                        "Product, quotient, power rules, zero & negative exponents",
                        "গুণ, ভাগ, ঘাত নিয়ম, শূন্য ও ঋণাত্মক সূচক",
                        Difficulty.EASY, 1, ["aᵐ × aⁿ = aᵐ⁺ⁿ"]),
                _lesson("gm-02-02", "Surds & Rationalization", "করণী ও মূলদকরণ",
                        "Simplification, addition, multiplication, rationalization of surds",
                        "সরলীকরণ, যোগ, গুণ, করণীর মূলদকরণ",
                        Difficulty.MEDIUM, 2, ["conjugate surds"]),
            ],
        ),
        Unit(
            id="gmath-ch03", title="Percentage & Commercial Math", title_bn="শতকরা ও বাণিজ্যিক গণিত",
            description="Percentage, profit-loss, discount, commission",
            description_bn="শতকরা, লাভ-ক্ষতি, ছাড়, কমিশন",
            icon="💰", nctb_chapter="3", nctb_class="XI", order=3,
            lessons=[
                _lesson("gm-03-01", "Percentage", "শতকরা",
                        "Percentage calculation, increase/decrease, successive percentage",
                        "শতকরা হিসাব, বৃদ্ধি/হ্রাস, পরপর শতকরা",
                        Difficulty.EASY, 1, ["successive %"]),
                _lesson("gm-03-02", "Profit, Loss & Discount", "লাভ, ক্ষতি ও ছাড়",
                        "Cost price, selling price, profit%, loss%, marked price, discount",
                        "ক্রয়মূল্য, বিক্রয়মূল্য, লাভ%, ক্ষতি%, চিহ্নিত মূল্য, ছাড়",
                        Difficulty.EASY, 2, ["SP = CP(1 + P%/100)"]),
            ],
        ),
        Unit(
            id="gmath-ch04", title="Simple & Compound Interest", title_bn="সরল ও চক্রবৃদ্ধি সুদ",
            description="Simple interest, compound interest, installment",
            description_bn="সরল সুদ, চক্রবৃদ্ধি সুদ, কিস্তি",
            icon="🏦", nctb_chapter="4", nctb_class="XI", order=4,
            lessons=[
                _lesson("gm-04-01", "Simple Interest", "সরল সুদ",
                        "SI formula, mixed problems, time-rate-principal",
                        "সরল সুদের সূত্র, মিশ্র সমস্যা, সময়-হার-আসল",
                        Difficulty.EASY, 1, ["I = Pnr/100"]),
                _lesson("gm-04-02", "Compound Interest", "চক্রবৃদ্ধি সুদ",
                        "CI formula, half-yearly/quarterly compounding, installment",
                        "চক্রবৃদ্ধি সুদের সূত্র, অর্ধবার্ষিক/ত্রৈমাসিক, কিস্তি",
                        Difficulty.MEDIUM, 2, ["A = P(1 + r/100)ⁿ"]),
            ],
        ),
        Unit(
            id="gmath-ch05", title="Ratio, Proportion & Variation", title_bn="অনুপাত, সমানুপাত ও ভেদ",
            description="Ratio, proportion, direct/inverse variation, partnership",
            description_bn="অনুপাত, সমানুপাত, সরল/ব্যস্ত ভেদ, অংশীদারি ব্যবসা",
            icon="⚖️", nctb_chapter="5", nctb_class="XI", order=5,
            lessons=[
                _lesson("gm-05-01", "Ratio & Proportion", "অনুপাত ও সমানুপাত",
                        "Ratio, proportion, componendo-dividendo, k-method",
                        "অনুপাত, সমানুপাত, যোজন-বিভাজন, k-পদ্ধতি",
                        Difficulty.MEDIUM, 1, ["a:b = c:d"]),
                _lesson("gm-05-02", "Variation & Partnership", "ভেদ ও অংশীদারি ব্যবসা",
                        "Direct, inverse, joint variation, partnership profit sharing",
                        "সরল, ব্যস্ত, সংযুক্ত ভেদ, অংশীদারি লাভ বণ্টন",
                        Difficulty.MEDIUM, 2, ["y ∝ x", "y ∝ 1/x"]),
            ],
        ),
        Unit(
            id="gmath-ch06", title="Time, Work & Distance", title_bn="সময়, কাজ ও দূরত্ব",
            description="Time-work, speed-distance, boats-streams, trains, age problems",
            description_bn="সময়-কাজ, বেগ-দূরত্ব, নৌকা-স্রোত, ট্রেন, বয়স সংক্রান্ত",
            icon="⏱️", nctb_chapter="6", nctb_class="XI", order=6,
            lessons=[
                _lesson("gm-06-01", "Time & Work", "সময় ও কাজ",
                        "Work rate, combined work, pipes & cisterns, alternating work",
                        "কাজের হার, মিলিত কাজ, পাইপ ও চৌবাচ্চা, পর্যায়ক্রমিক কাজ",
                        Difficulty.MEDIUM, 1),
                _lesson("gm-06-02", "Speed, Distance & Boats-Streams", "বেগ, দূরত্ব ও নৌকা-স্রোত",
                        "Average speed, relative speed, boats-streams, train problems",
                        "গড় বেগ, আপেক্ষিক বেগ, নৌকা-স্রোত, ট্রেন সমস্যা",
                        Difficulty.MEDIUM, 2, ["d = s × t"]),
                _lesson("gm-06-03", "Age Problems & Mixtures", "বয়স ও মিশ্রণ সমস্যা",
                        "Age relationship, alligation, mixture ratio problems",
                        "বয়সের সম্পর্ক, সংকরণ, মিশ্রণের অনুপাত",
                        Difficulty.MEDIUM, 3),
            ],
        ),
        # ── বীজগণিত (Algebra) ──
        Unit(
            id="gmath-ch07", title="Algebraic Expressions", title_bn="বীজগাণিতিক রাশি",
            description="Factoring, simplification, algebraic fractions",
            description_bn="উৎপাদক, সরলীকরণ, বীজগাণিতিক ভগ্নাংশ",
            icon="🅰️", nctb_chapter="7", nctb_class="XI", order=7,
            lessons=[
                _lesson("gm-07-01", "Factoring & Identities", "উৎপাদক ও অভেদ",
                        "Algebraic identities, factoring polynomials, remainder theorem",
                        "বীজগাণিতিক অভেদ, বহুপদীর উৎপাদক, অবশেষ উপপাদ্য",
                        Difficulty.MEDIUM, 1, ["a²-b² = (a+b)(a-b)"]),
                _lesson("gm-07-02", "Algebraic Fractions & Simplification", "বীজগাণিতিক ভগ্নাংশ ও সরলীকরণ",
                        "Simplification of complex algebraic fractions, LCM of expressions",
                        "জটিল বীজগাণিতিক ভগ্নাংশের সরলীকরণ, রাশির ল.সা.গু",
                        Difficulty.MEDIUM, 2),
            ],
        ),
        Unit(
            id="gmath-ch08", title="Equations", title_bn="সমীকরণ",
            description="Linear, quadratic, simultaneous equations, word problems",
            description_bn="সরল, দ্বিঘাত, যুগপৎ সমীকরণ, ব্যবহারিক সমস্যা",
            icon="🟰", nctb_chapter="8", nctb_class="XI", order=8,
            lessons=[
                _lesson("gm-08-01", "Linear & Simultaneous Equations", "সরল ও যুগপৎ সমীকরণ",
                        "Solving linear equations, simultaneous equations by elimination/substitution",
                        "সরল সমীকরণ সমাধান, লোপ/প্রতিস্থাপন পদ্ধতিতে যুগপৎ সমীকরণ",
                        Difficulty.EASY, 1),
                _lesson("gm-08-02", "Quadratic Equations", "দ্বিঘাত সমীকরণ",
                        "Factoring, completing square, quadratic formula, discriminant",
                        "উৎপাদক, বর্গ পূর্ণ করা, দ্বিঘাত সূত্র, নিষ্পত্তিকারক",
                        Difficulty.MEDIUM, 2, ["x = (-b ± √(b²-4ac)) / 2a"]),
                _lesson("gm-08-03", "Word Problems & Applications", "ব্যবহারিক সমস্যা",
                        "Translating word problems to equations, admission-style problems",
                        "ব্যবহারিক সমস্যা থেকে সমীকরণ তৈরি, ভর্তি পরীক্ষার ধরন",
                        Difficulty.MEDIUM, 3),
            ],
        ),
        Unit(
            id="gmath-ch09", title="Sets & Functions", title_bn="সেট ও ফাংশন",
            description="Set theory, Venn diagrams, functions, domain/range",
            description_bn="সেট তত্ত্ব, ভেন চিত্র, ফাংশন, ডোমেইন/রেঞ্জ",
            icon="{ }", nctb_chapter="9", nctb_class="XI", order=9,
            lessons=[
                _lesson("gm-09-01", "Sets & Venn Diagrams", "সেট ও ভেন চিত্র",
                        "Set notation, union, intersection, complement, Venn diagrams",
                        "সেট প্রকাশ, সংযোগ, ছেদ, পূরক, ভেন চিত্র",
                        Difficulty.MEDIUM, 1, ["A∪B", "A∩B", "A'"]),
                _lesson("gm-09-02", "Functions", "ফাংশন",
                        "Domain, range, one-to-one, onto, inverse, composite functions",
                        "ডোমেইন, রেঞ্জ, একৈক, সার্বিক, বিপরীত, যৌগিক ফাংশন",
                        Difficulty.MEDIUM, 2),
            ],
        ),
        Unit(
            id="gmath-ch10", title="Logarithms", title_bn="লগারিদম",
            description="Log properties, change of base, exponential equations",
            description_bn="লগের ধর্ম, ভিত্তি পরিবর্তন, সূচকীয় সমীকরণ",
            icon="📊", nctb_chapter="10", nctb_class="XI", order=10,
            lessons=[
                _lesson("gm-10-01", "Logarithm Properties & Applications", "লগারিদমের ধর্ম ও প্রয়োগ",
                        "Log rules, change of base, solving exponential/log equations",
                        "লগের নিয়ম, ভিত্তি পরিবর্তন, সূচকীয়/লগ সমীকরণ সমাধান",
                        Difficulty.MEDIUM, 1, ["log(ab) = log a + log b"]),
            ],
        ),
        # ── জ্যামিতি ও পরিমিতি (Geometry & Mensuration) ──
        Unit(
            id="gmath-ch11", title="Geometry", title_bn="জ্যামিতি",
            description="Lines, angles, triangles, circles, quadrilaterals",
            description_bn="রেখা, কোণ, ত্রিভুজ, বৃত্ত, চতুর্ভুজ",
            icon="📐", nctb_chapter="11", nctb_class="XII", order=11,
            lessons=[
                _lesson("gm-11-01", "Lines, Angles & Triangles", "রেখা, কোণ ও ত্রিভুজ",
                        "Parallel lines, angle properties, triangle congruence & similarity",
                        "সমান্তরাল রেখা, কোণের ধর্ম, ত্রিভুজের সর্বসমতা ও সদৃশতা",
                        Difficulty.MEDIUM, 1),
                _lesson("gm-11-02", "Circle & Quadrilateral", "বৃত্ত ও চতুর্ভুজ",
                        "Circle theorems, tangent, secant, quadrilateral properties",
                        "বৃত্তের উপপাদ্য, স্পর্শক, ছেদক, চতুর্ভুজের ধর্ম",
                        Difficulty.MEDIUM, 2, ["tangent-radius perpendicular"]),
            ],
        ),
        Unit(
            id="gmath-ch12", title="Mensuration", title_bn="পরিমিতি",
            description="Area, perimeter, volume, surface area of 2D & 3D shapes",
            description_bn="ক্ষেত্রফল, পরিসীমা, আয়তন, পৃষ্ঠতল — ২D ও ৩D আকৃতি",
            icon="📏", nctb_chapter="12", nctb_class="XII", order=12,
            lessons=[
                _lesson("gm-12-01", "Area & Perimeter (2D)", "ক্ষেত্রফল ও পরিসীমা",
                        "Triangle, rectangle, parallelogram, trapezium, circle area & perimeter",
                        "ত্রিভুজ, আয়তক্ষেত্র, সামান্তরিক, ট্র্যাপিজিয়াম, বৃত্তের ক্ষেত্রফল ও পরিসীমা",
                        Difficulty.EASY, 1, ["πr²", "½bh"]),
                _lesson("gm-12-02", "Volume & Surface Area (3D)", "আয়তন ও পৃষ্ঠতল",
                        "Cube, cuboid, cylinder, cone, sphere volume & surface area",
                        "ঘনক, আয়তাকার ঘনবস্তু, সিলিন্ডার, শঙ্কু, গোলকের আয়তন ও পৃষ্ঠতল",
                        Difficulty.MEDIUM, 2, ["4/3 πr³"]),
            ],
        ),
        # ── ত্রিকোণমিতি (Basic Trigonometry) ──
        Unit(
            id="gmath-ch13", title="Basic Trigonometry", title_bn="মৌলিক ত্রিকোণমিতি",
            description="Trigonometric ratios, identities, height & distance",
            description_bn="ত্রিকোণমিতিক অনুপাত, অভেদ, উচ্চতা ও দূরত্ব",
            icon="📊", nctb_chapter="13", nctb_class="XII", order=13,
            lessons=[
                _lesson("gm-13-01", "Trigonometric Ratios & Identities", "ত্রিকোণমিতিক অনুপাত ও অভেদ",
                        "sin, cos, tan, cot, sec, cosec, Pythagorean identities",
                        "sin, cos, tan, cot, sec, cosec, পিথাগোরাসীয় অভেদ",
                        Difficulty.MEDIUM, 1, ["sin²θ + cos²θ = 1"]),
                _lesson("gm-13-02", "Height & Distance", "উচ্চতা ও দূরত্ব",
                        "Angle of elevation/depression, practical problems",
                        "উন্নতি/অবনতি কোণ, ব্যবহারিক সমস্যা",
                        Difficulty.MEDIUM, 2),
            ],
        ),
        # ── পরিসংখ্যান ও সম্ভাব্যতা (Statistics & Probability) ──
        Unit(
            id="gmath-ch14", title="Statistics", title_bn="পরিসংখ্যান",
            description="Mean, median, mode, standard deviation, data presentation",
            description_bn="গড়, মধ্যমা, প্রচুরক, পরিমিত ব্যবধান, উপাত্ত উপস্থাপন",
            icon="📈", nctb_chapter="14", nctb_class="XII", order=14,
            lessons=[
                _lesson("gm-14-01", "Central Tendency", "কেন্দ্রীয় প্রবণতা",
                        "Arithmetic mean, median, mode for grouped/ungrouped data",
                        "সমান্তর গড়, মধ্যমা, প্রচুরক — শ্রেণিবদ্ধ/অশ্রেণিবদ্ধ উপাত্ত",
                        Difficulty.MEDIUM, 1, ["mean", "median", "mode"]),
                _lesson("gm-14-02", "Dispersion & Data Presentation", "বিস্তার পরিমাপ ও উপাত্ত উপস্থাপন",
                        "Range, variance, standard deviation, histogram, ogive",
                        "পরিসর, ভেদাংক, পরিমিত ব্যবধান, আয়তলেখ, ওজাইভ",
                        Difficulty.MEDIUM, 2, ["σ = √(Σ(x-x̄)²/n)"]),
            ],
        ),
        Unit(
            id="gmath-ch15", title="Probability", title_bn="সম্ভাব্যতা",
            description="Basic probability, permutations, combinations",
            description_bn="মৌলিক সম্ভাব্যতা, বিন্যাস, সমাবেশ",
            icon="🎲", nctb_chapter="15", nctb_class="XII", order=15,
            lessons=[
                _lesson("gm-15-01", "Basic Probability", "মৌলিক সম্ভাব্যতা",
                        "Sample space, events, probability rules, conditional probability",
                        "নমুনা ক্ষেত্র, ঘটনা, সম্ভাব্যতার নিয়ম, শর্তসাপেক্ষ সম্ভাব্যতা",
                        Difficulty.MEDIUM, 1, ["P(A∪B) = P(A) + P(B) - P(A∩B)"]),
                _lesson("gm-15-02", "Permutations & Combinations", "বিন্যাস ও সমাবেশ",
                        "nPr, nCr, circular permutation, word arrangement",
                        "nPr, nCr, বৃত্তাকার বিন্যাস, শব্দ সাজানো",
                        Difficulty.HARD, 2, ["nCr = n! / r!(n-r)!"]),
            ],
        ),
    ],
)


# ═══════════════════════════════════════════════════════════════════════════════
# Registry
# ═══════════════════════════════════════════════════════════════════════════════

ALL_SUBJECTS: dict[SubjectId, SubjectCurriculum] = {
    SubjectId.PHYSICS: PHYSICS,
    SubjectId.CHEMISTRY: CHEMISTRY,
    SubjectId.HIGHER_MATH: HIGHER_MATH,
    SubjectId.GENERAL_MATH: GENERAL_MATH,
    SubjectId.BIOLOGY: BIOLOGY,
}

EXAM_SUBJECTS: dict[TargetExam, list[SubjectId]] = {
    TargetExam.BUET: [SubjectId.PHYSICS, SubjectId.CHEMISTRY, SubjectId.HIGHER_MATH],
    TargetExam.MEDICAL: [SubjectId.BIOLOGY, SubjectId.CHEMISTRY, SubjectId.PHYSICS, SubjectId.GENERAL_MATH],
    TargetExam.DU: [SubjectId.PHYSICS, SubjectId.CHEMISTRY, SubjectId.HIGHER_MATH, SubjectId.GENERAL_MATH, SubjectId.BIOLOGY],
    TargetExam.GST: [SubjectId.PHYSICS, SubjectId.CHEMISTRY, SubjectId.HIGHER_MATH, SubjectId.BIOLOGY],
    TargetExam.GENERAL: [SubjectId.PHYSICS, SubjectId.CHEMISTRY, SubjectId.HIGHER_MATH, SubjectId.GENERAL_MATH, SubjectId.BIOLOGY],
}
