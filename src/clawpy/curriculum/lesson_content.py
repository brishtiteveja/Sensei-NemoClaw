"""Rich lesson content — teaching plans for each lesson.

Each lesson has:
- learning_objectives: what student should understand after
- teaching_steps: ordered sequence the AI follows
- key_formulas: equations to teach
- common_mistakes: what students typically get wrong
- practice_prompts: questions to check understanding
- real_world_example: relatable analogy

The AI uses this to deliver structured, Socratic lessons instead
of random conversation.
"""

from __future__ import annotations

LESSON_CONTENT: dict[str, dict] = {
    # ══ PHYSICS — Chapter 1: Measurement ══
    "phy1-01-01": {
        "title": "Physical Quantities & SI Units",
        "learning_objectives": [
            "Distinguish between fundamental and derived quantities",
            "List the 7 SI base units with symbols",
            "Convert between unit systems",
            "Apply dimensional analysis to verify equations",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Start by asking: what do you think a 'physical quantity' means? Give an example.",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Explain fundamental vs derived quantities. Ask student to classify: length, speed, force, mass, acceleration.",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Introduce the 7 SI base units. Ask: which base unit is defined by a physical artifact? (kg was until 2019)",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Give a dimensional analysis problem: verify if v = u + at is dimensionally correct.",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "Ask: convert 72 km/h to m/s. Then ask a BUET-style MCQ from the question bank about units.",
            },
        ],
        "key_formulas": [
            "[M^a L^b T^c] — dimensional formula",
            "1 km/h = 5/18 m/s",
        ],
        "common_mistakes": [
            "Confusing fundamental and derived quantities",
            "Forgetting that radian is dimensionless",
            "Wrong conversion factors (km/h to m/s)",
        ],
        "practice_prompts": [
            "Is force a fundamental or derived quantity? Why?",
            "What is the dimensional formula of energy?",
            "Convert 100 km/h to m/s",
        ],
        "real_world_example": "Think of buying fabric — you measure length in meters (fundamental), but price per meter is derived from two quantities.",
    },

    "phy1-01-02": {
        "title": "Measurement & Errors",
        "learning_objectives": [
            "Use vernier caliper and screw gauge measurements",
            "Calculate absolute, relative, and percentage errors",
            "Apply rules of significant figures",
            "Propagate errors in calculations",
        ],
        "teaching_steps": [
            {"step": 1, "type": "intro", "prompt": "Ask: why can't any measurement be perfectly accurate? What causes errors?"},
            {"step": 2, "type": "concept", "prompt": "Explain systematic vs random errors with examples. Ask student for an example of each."},
            {"step": 3, "type": "teach", "prompt": "Teach vernier caliper reading: main scale + vernier scale × least count. Give a practice reading."},
            {"step": 4, "type": "practice", "prompt": "Problem: if length = 5.0 ± 0.1 cm and width = 3.0 ± 0.1 cm, what is the area with error?"},
            {"step": 5, "type": "mastery", "prompt": "Ask a BUET/DU MCQ about significant figures or error propagation."},
        ],
        "key_formulas": [
            "Least count of vernier = 1 MSD - 1 VSD",
            "Relative error = Δx/x",
            "% error = (Δx/x) × 100",
        ],
        "common_mistakes": [
            "Forgetting to add errors when multiplying measurements",
            "Confusing precision with accuracy",
            "Wrong significant figure rules for zeros",
        ],
        "practice_prompts": [
            "A vernier caliper reads 3.2 cm on main scale, 7th division matches. Least count = 0.01 cm. What is the reading?",
            "How many significant figures in 0.00340?",
        ],
        "real_world_example": "A tailor measures your waist as 32 inches — but is it exactly 32.000? The ± error matters when the shirt needs to fit perfectly.",
    },

    # ══ PHYSICS — Chapter 2: Vectors ══
    "phy1-02-01": {
        "title": "Vector Addition & Resolution",
        "learning_objectives": [
            "Distinguish scalar and vector quantities",
            "Add vectors using triangle and parallelogram law",
            "Resolve vectors into components",
            "Find resultant magnitude and direction",
        ],
        "teaching_steps": [
            {"step": 1, "type": "intro", "prompt": "Ask: what is the difference between 'speed' and 'velocity'? Why does direction matter?"},
            {"step": 2, "type": "concept", "prompt": "Explain scalar vs vector with examples. Ask student to classify: temperature, displacement, energy, momentum."},
            {"step": 3, "type": "teach", "prompt": "Teach parallelogram law of vector addition with the formula R = √(A² + B² + 2AB cos θ). Draw the diagram mentally."},
            {"step": 4, "type": "practice", "prompt": "Two forces 3N and 4N act at 90°. Find the resultant. Then ask: what if the angle was 60°?"},
            {"step": 5, "type": "mastery", "prompt": "Ask a BUET MCQ about vector resolution into components. Test if student can find Fx = F cos θ, Fy = F sin θ."},
        ],
        "key_formulas": [
            "R = √(A² + B² + 2AB cos θ)",
            "tan α = B sin θ / (A + B cos θ)",
            "Fx = F cos θ, Fy = F sin θ",
        ],
        "common_mistakes": [
            "Adding vector magnitudes directly without considering direction",
            "Confusing the angle in parallelogram law (angle between vectors vs angle with x-axis)",
            "Forgetting that vector subtraction = addition of negative vector",
        ],
        "practice_prompts": [
            "Two vectors of magnitude 5 and 12 are perpendicular. Find the resultant.",
            "Resolve a 10N force at 30° into horizontal and vertical components.",
        ],
        "real_world_example": "Imagine crossing a river — you swim forward but the current pushes you sideways. Your actual path is the vector sum of your swimming direction and the current.",
    },

    # ══ PHYSICS — Chapter 3: Dynamics ══
    "phy1-03-01": {
        "title": "Rectilinear Motion",
        "learning_objectives": [
            "Apply equations of motion (v=u+at, s=ut+½at², v²=u²+2as)",
            "Solve free fall problems with g=9.8 m/s²",
            "Interpret motion from v-t and s-t graphs",
            "Calculate stopping distance and time",
        ],
        "teaching_steps": [
            {"step": 1, "type": "intro", "prompt": "Ask: if you throw a ball up at 20 m/s, how long before it stops? What do you think happens to its speed each second?"},
            {"step": 2, "type": "concept", "prompt": "Teach the 3 equations of motion. Ask student which equation to use when: (a) no distance given, (b) no final velocity given, (c) no time given."},
            {"step": 3, "type": "teach", "prompt": "Solve a free fall problem together: a stone dropped from 80m height. Find time to reach ground and velocity on impact."},
            {"step": 4, "type": "practice", "prompt": "Problem: a car traveling at 72 km/h brakes with deceleration 5 m/s². Find stopping distance."},
            {"step": 5, "type": "mastery", "prompt": "Give a BUET admission MCQ about projectile or free fall. Test complete problem-solving ability."},
        ],
        "key_formulas": [
            "v = u + at",
            "s = ut + ½at²",
            "v² = u² + 2as",
            "For free fall: u=0, a=g=9.8 m/s²",
        ],
        "common_mistakes": [
            "Forgetting to convert km/h to m/s before calculating",
            "Wrong sign convention for deceleration (should be negative a)",
            "For upward throw: forgetting total time = 2 × time to reach max height",
        ],
        "practice_prompts": [
            "A ball is thrown up at 19.6 m/s. Find total time of flight.",
            "A car accelerates from rest at 2 m/s² for 10s. How far does it travel?",
        ],
        "real_world_example": "When you brake in a car at 60 km/h, you don't stop instantly — the stopping distance depends on your speed squared. That's why highway speed limits matter so much.",
    },

    "phy1-03-02": {
        "title": "Motion Graphs & Relative Motion",
        "learning_objectives": [
            "Read displacement, velocity, and acceleration from graphs",
            "Calculate displacement from area under v-t graph",
            "Solve relative velocity problems",
            "Understand reference frames",
        ],
        "teaching_steps": [
            {"step": 1, "type": "intro", "prompt": "Show a v-t graph description and ask: what does the slope mean? What does the area under the curve mean?"},
            {"step": 2, "type": "concept", "prompt": "Teach: slope of s-t = velocity, slope of v-t = acceleration, area under v-t = displacement."},
            {"step": 3, "type": "teach", "prompt": "Relative motion: if train A goes 60 km/h east and train B goes 40 km/h west, what is the velocity of A relative to B?"},
            {"step": 4, "type": "practice", "prompt": "A v-t graph shows: 0-4s velocity increases from 0 to 20 m/s, then constant for 6s. Find total displacement."},
            {"step": 5, "type": "mastery", "prompt": "Give a motion graph MCQ from the question bank."},
        ],
        "key_formulas": [
            "v_AB = v_A - v_B (relative velocity)",
            "Displacement = area under v-t graph",
            "Acceleration = slope of v-t graph",
        ],
        "common_mistakes": [
            "Confusing distance (always positive) with displacement (can be negative)",
            "Forgetting that area below the time axis in v-t graph is negative displacement",
            "Wrong sign in relative velocity when objects move in opposite directions",
        ],
        "practice_prompts": [
            "Two cars approach each other at 60 km/h and 40 km/h. What is their relative speed?",
            "From a v-t graph, how do you find the distance traveled vs displacement?",
        ],
        "real_world_example": "Sitting in a train, the trees seem to move backward — that's relative motion. Your velocity relative to the ground is different from your velocity relative to the train.",
    },

    # ══ PHYSICS — Chapter 2 (cont.): Vectors — Scalar & Vector Products ══
    "phy1-02-02": {
        "title": "Scalar & Vector Products",
        "learning_objectives": [
            "Calculate the dot product of two vectors and interpret it as projection",
            "Calculate the cross product and determine its direction using the right-hand rule",
            "Apply dot product to find work done and angle between vectors",
            "Apply cross product to find torque and area of a parallelogram",
        ],
        "teaching_steps": [
            {"step": 1, "type": "intro", "prompt": "Ask: when you pull a rickshaw at an angle, does all your force contribute to moving it forward? What part of the force actually does the work? This is where dot product comes in."},
            {"step": 2, "type": "concept", "prompt": "Teach dot product: A·B = AB cos θ = AxBx + AyBy + AzBz. It gives a scalar. Ask: what is the dot product when vectors are perpendicular? (zero) When parallel? (AB). Explain how this relates to work W = F·d = Fd cos θ."},
            {"step": 3, "type": "teach", "prompt": "Teach cross product: A×B = AB sin θ n̂ (direction by right-hand rule). In component form: A×B = (AyBz − AzBy)î + (AzBx − AxBz)ĵ + (AxBy − AyBx)k̂. Key property: A×B = −B×A (anti-commutative). Ask: what is î×ĵ? What is î×î?"},
            {"step": 4, "type": "practice", "prompt": "Problem: A = 3î + 4ĵ − 2k̂, B = 2î − ĵ + 3k̂. Find: (a) A·B, (b) angle between A and B, (c) A×B, (d) area of parallelogram formed by A and B."},
            {"step": 5, "type": "mastery", "prompt": "BUET-level: A force F = (2î + 3ĵ) N acts on a body. The body moves from position r₁ = (î − ĵ) m to r₂ = (4î + 2ĵ) m. Find the work done. Then: find the torque about the origin if the force acts at point (3, 4, 0)."},
        ],
        "key_formulas": [
            "A·B = AB cos θ = AxBx + AyBy + AzBz (scalar result)",
            "|A×B| = AB sin θ (magnitude of cross product)",
            "A×B = (AyBz − AzBy)î + (AzBx − AxBz)ĵ + (AxBy − AyBx)k̂",
            "î·î = ĵ·ĵ = k̂·k̂ = 1; î·ĵ = ĵ·k̂ = k̂·î = 0",
            "î×ĵ = k̂, ĵ×k̂ = î, k̂×î = ĵ (cyclic); î×î = 0",
            "Work: W = F·d = Fd cos θ; Torque: τ = r × F",
        ],
        "common_mistakes": [
            "Confusing when to use dot product (gives scalar — work, projection) vs cross product (gives vector — torque, area)",
            "Forgetting that cross product is anti-commutative: A×B = −B×A, so order matters unlike dot product",
            "Errors in the determinant expansion of the cross product — mixing up signs in the ĵ component (it has a negative sign in the cofactor expansion)",
        ],
        "practice_prompts": [
            "Find the angle between vectors A = 2î + 3ĵ and B = î − 2ĵ using the dot product.",
            "A force F = 5î + 2ĵ N displaces a body by d = 3î + 4ĵ m. Calculate the work done and the angle between F and d.",
            "Find the area of the triangle with vertices at A(1,2,0), B(3,0,0), C(0,1,2) using the cross product.",
        ],
        "real_world_example": "When a rickshaw puller in Dhaka pulls the handle at an angle, only the horizontal component (F cos θ) moves the rickshaw forward — that is the dot product F·d. The cross product appears in torque: when you open a door, pushing at the edge (large r) with force perpendicular to the door (sin 90° = 1) gives maximum torque. That is why door handles are placed far from the hinge.",
    },

    # ══ PHYSICS — Chapter 4: Newton's Laws of Motion ══
    "phy1-04-01": {
        "title": "Newton's Laws of Motion",
        "learning_objectives": [
            "State and apply Newton's three laws of motion with examples",
            "Draw free body diagrams (FBD) for objects in various force configurations",
            "Solve problems using F = ma in one and two dimensions",
            "Apply Newton's third law to identify action-reaction pairs correctly",
        ],
        "teaching_steps": [
            {"step": 1, "type": "intro", "prompt": "Ask: why do passengers lurch forward when a bus brakes suddenly? Why does a cricket ball hurt more when it comes at 140 km/h than 60 km/h? These are Newton's laws in action."},
            {"step": 2, "type": "concept", "prompt": "Teach all three laws: 1st law (inertia) — a body remains at rest or in uniform motion unless acted upon by a net external force. 2nd law — F = ma (net force = mass × acceleration). 3rd law — every action has an equal and opposite reaction. Ask: when you stand on the floor, what are the action-reaction pairs? Is normal force the reaction to weight?"},
            {"step": 3, "type": "teach", "prompt": "Teach free body diagrams: isolate the object, draw all forces acting ON it (weight, normal, tension, friction, applied force). Solve: a 5 kg block on a smooth surface is pulled by a 20 N force at 30° above horizontal. Draw the FBD and find acceleration. Then solve a connected blocks problem: two masses m₁ = 3 kg and m₂ = 5 kg connected by a string over a frictionless pulley (Atwood machine)."},
            {"step": 4, "type": "practice", "prompt": "Problem: In a lift, a 60 kg person stands on a weighing scale. Find the scale reading when the lift: (a) moves up with acceleration 2 m/s², (b) moves down with acceleration 2 m/s², (c) is in free fall. Draw FBD for each case."},
            {"step": 5, "type": "mastery", "prompt": "BUET-level: Three blocks of masses 1 kg, 2 kg, and 3 kg are connected by strings on a smooth horizontal surface. A force of 12 N is applied to the 3 kg block. Find: (a) acceleration of the system, (b) tension in each string. Then: if the surface has friction coefficient μ = 0.1, redo the problem."},
        ],
        "key_formulas": [
            "Newton's 2nd law: F_net = ma (vector equation)",
            "Weight: W = mg (g = 9.8 m/s²)",
            "Apparent weight in lift: W_app = m(g ± a) (+ for upward acceleration, − for downward)",
            "Atwood machine: a = (m₁ − m₂)g / (m₁ + m₂), T = 2m₁m₂g / (m₁ + m₂)",
            "Connected bodies on surface: a = F_net / (m₁ + m₂ + m₃)",
        ],
        "common_mistakes": [
            "Thinking that the normal force is always the reaction to weight — normal force and weight are NOT an action-reaction pair; they act on the SAME body. The reaction to your weight on the floor is the gravitational pull you exert on the Earth.",
            "Including forces that do not act on the body when drawing FBDs — for example, including the force the block exerts on the table instead of the force the table exerts on the block",
            "Forgetting to treat the system as a whole first to find acceleration in connected body problems, then isolating individual bodies to find internal tensions",
        ],
        "practice_prompts": [
            "A 10 kg block on a frictionless surface is pushed by a 30 N horizontal force. Find the acceleration. If a 5 kg block is placed on top of it, find the new acceleration.",
            "In an Atwood machine with masses 8 kg and 6 kg, find the acceleration and the tension in the string. Take g = 10 m/s².",
            "A person of mass 70 kg stands in a lift. What does the weighing scale read when the lift accelerates upward at 3 m/s²?",
        ],
        "real_world_example": "When a BRTC bus in Dhaka brakes suddenly, passengers lurch forward — that is Newton's 1st law (inertia). When Shakib Al Hasan bowls a cricket ball, the force from his arm gives the ball acceleration (F = ma). The ball pushes his hand backward with equal force (3rd law) — that is why fast bowlers sometimes get finger injuries.",
    },

    "phy1-04-02": {
        "title": "Friction & Circular Motion",
        "learning_objectives": [
            "Distinguish between static and kinetic friction and apply f = μN",
            "Solve problems involving friction on inclined planes",
            "Derive and apply centripetal acceleration a = v²/r and centripetal force F = mv²/r",
            "Analyze motion on banked curves and vertical circular motion",
        ],
        "teaching_steps": [
            {"step": 1, "type": "intro", "prompt": "Ask: why is it harder to start pushing a heavy almari (wardrobe) than to keep it moving? Why do cars slip on wet roads during monsoon? This is friction. And why does a motorcyclist lean inward while turning? That is circular motion."},
            {"step": 2, "type": "concept", "prompt": "Teach friction: static friction f_s ≤ μ_s N (self-adjusting up to maximum), kinetic friction f_k = μ_k N (constant, less than maximum static). On an inclined plane at angle θ: component along plane = mg sin θ, normal force N = mg cos θ, friction = μN = μmg cos θ. Condition for sliding: tan θ > μ_s (angle of repose)."},
            {"step": 3, "type": "teach", "prompt": "Teach circular motion: centripetal acceleration a_c = v²/r = ω²r directed toward center. Centripetal force F_c = mv²/r is not a separate force — it is provided by tension, gravity, friction, or normal force. For a car turning on a flat road: friction provides centripetal force, so v_max = √(μrg). For a banked road at angle θ: tan θ = v²/rg (without friction)."},
            {"step": 4, "type": "practice", "prompt": "Problem: A 2 kg block is on a rough inclined plane at 30°. μ_s = 0.5, μ_k = 0.3. (a) Will the block slide? (b) If it slides, find its acceleration. Then: a car goes around a circular track of radius 50 m. If μ = 0.4, find the maximum safe speed."},
            {"step": 5, "type": "mastery", "prompt": "BUET-level: A small ball of mass 0.5 kg is attached to a string of length 1 m and whirled in a vertical circle. Find: (a) minimum speed at the top so the string does not go slack, (b) tension at the bottom when speed at top is exactly at minimum, (c) maximum tension in the string. Use energy conservation for (b)."},
        ],
        "key_formulas": [
            "Static friction: f_s ≤ μ_s N (maximum = μ_s N)",
            "Kinetic friction: f_k = μ_k N (always less than max static friction)",
            "Angle of repose: tan θ = μ_s",
            "Centripetal acceleration: a_c = v²/r = ω²r",
            "Centripetal force: F_c = mv²/r",
            "Banked road (no friction): tan θ = v²/rg",
            "Vertical circle minimum speed at top: v_min = √(rg)",
        ],
        "common_mistakes": [
            "Treating centripetal force as a separate force in FBDs — it is not a new force but the net inward force provided by existing forces (friction, tension, gravity, normal force)",
            "Using mg instead of mg cos θ for the normal force on an inclined plane — the normal force equals mg only on a horizontal surface",
            "Confusing static and kinetic friction — applying μ_k when the object has not started moving yet, or using μ_s after motion has begun",
        ],
        "practice_prompts": [
            "A 5 kg block sits on a horizontal surface with μ_s = 0.4, μ_k = 0.3. A horizontal force is gradually increased. At what force does the block start to move? What is the acceleration once it starts?",
            "A car moves on a circular road of radius 100 m at 72 km/h. What is the minimum coefficient of friction needed to prevent skidding?",
        ],
        "real_world_example": "The Padma Bridge approach roads have banked curves so heavy trucks do not need to rely entirely on tyre friction to turn safely. During the monsoon, wet roads reduce the friction coefficient dramatically — this is why so many road accidents happen on the Dhaka-Chittagong highway during rain. The banking angle is calculated using tan θ = v²/rg to ensure vehicles can turn safely even with reduced friction.",
    },

    # ══ PHYSICS — Chapter 5: Work, Energy & Power ══
    "phy1-05-01": {
        "title": "Work & Energy",
        "learning_objectives": [
            "Calculate work done by constant and variable forces using W = Fd cos θ",
            "Derive and apply kinetic energy KE = ½mv² and the work-energy theorem",
            "Apply potential energy PE = mgh and elastic PE = ½kx²",
            "Solve problems using the law of conservation of mechanical energy",
        ],
        "teaching_steps": [
            {"step": 1, "type": "intro", "prompt": "Ask: if you carry a heavy bag horizontally across a room, do you do work on the bag? (No — force is vertical, displacement is horizontal, so W = Fd cos 90° = 0.) What if you carry it upstairs? This shows work depends on the angle between force and displacement."},
            {"step": 2, "type": "concept", "prompt": "Teach work: W = Fd cos θ = F·d (dot product). Work done by gravity on a falling body of mass m through height h: W = mgh. Work-energy theorem: net work done on a body = change in kinetic energy: W_net = ½mv² − ½mu². Ask: if a car doubles its speed, by what factor does the braking distance increase? (4 times, since KE ∝ v²)"},
            {"step": 3, "type": "teach", "prompt": "Teach potential energy: gravitational PE = mgh (with a reference level), elastic PE = ½kx² (spring). Conservation of mechanical energy: KE + PE = constant (when only conservative forces act). Demonstrate with a falling ball: at height h, KE = 0, PE = mgh. At ground, KE = mgh, PE = 0. Total energy is conserved."},
            {"step": 4, "type": "practice", "prompt": "Problem: A 2 kg ball is dropped from 20 m height. Using energy conservation (no air resistance), find: (a) speed just before hitting the ground, (b) speed at 5 m above ground, (c) the height at which KE = PE. Then: a 0.5 kg ball is thrown upward at 20 m/s. Find the maximum height using energy conservation."},
            {"step": 5, "type": "mastery", "prompt": "BUET-level: A block of mass 1 kg slides from rest down a smooth curved track from height 5 m onto a rough horizontal surface (μ = 0.2). How far does it travel on the rough surface before stopping? Then: a spring of constant k = 200 N/m is compressed by 0.1 m. A 0.5 kg ball is placed against it and released. Find the speed of the ball when it leaves the spring, and the maximum height it reaches."},
        ],
        "key_formulas": [
            "Work: W = Fd cos θ = F·d",
            "Kinetic energy: KE = ½mv²",
            "Work-energy theorem: W_net = ΔKE = ½mv² − ½mu²",
            "Gravitational PE: PE = mgh",
            "Elastic PE: PE = ½kx²",
            "Conservation of energy: KE₁ + PE₁ = KE₂ + PE₂ (no non-conservative forces)",
            "With friction: KE₁ + PE₁ = KE₂ + PE₂ + W_friction",
        ],
        "common_mistakes": [
            "Forgetting the cos θ factor in work — when a porter carries a load on his head walking horizontally, the work done by the carrying force is zero because force is vertical and displacement is horizontal",
            "Using KE = mv² instead of KE = ½mv² — missing the ½ factor is a very common calculation error",
            "Applying conservation of mechanical energy when friction is present — friction is non-conservative, so energy lost to friction must be accounted for: KE₁ + PE₁ = KE₂ + PE₂ + f×d",
        ],
        "practice_prompts": [
            "A 10 kg block is pulled 5 m along a horizontal surface by a 50 N force at 37° above horizontal. μ_k = 0.2. Find the work done by: (a) the applied force, (b) friction, (c) gravity, (d) net work done.",
            "A ball of mass 0.2 kg is dropped from 10 m. Find its speed at 4 m above the ground using energy conservation.",
            "A spring with k = 500 N/m is compressed by 0.2 m. How much energy is stored? If this energy is used to launch a 0.1 kg ball vertically, how high does the ball go?",
        ],
        "real_world_example": "The Kaptai hydroelectric dam in Rangamati stores water at a height — this is gravitational potential energy (mgh). When water falls through turbines, PE converts to KE of the water, which spins the turbine to generate electricity. The higher the dam and the more water stored, the more energy is available. This is the same principle as a ball falling from a height — energy is conserved, just transformed from one form to another.",
    },

    "phy1-05-02": {
        "title": "Power & Collisions",
        "learning_objectives": [
            "Calculate power as rate of doing work: P = W/t = Fv",
            "Distinguish between elastic and inelastic collisions using conservation laws",
            "Apply conservation of momentum and energy to solve 1D collision problems",
            "Calculate coefficient of restitution and energy lost in inelastic collisions",
        ],
        "teaching_steps": [
            {"step": 1, "type": "intro", "prompt": "Ask: two workers carry the same load up the same staircase, but one takes 1 minute and the other takes 2 minutes. Who does more work? (Same.) Who is more powerful? (The faster one.) Power is about how fast you do work."},
            {"step": 2, "type": "concept", "prompt": "Teach power: P = W/t = Fv (instantaneous power when force and velocity are parallel). Unit: Watt (1 W = 1 J/s). 1 horsepower = 746 W. Ask: a pump lifts 200 kg of water per minute to a height of 10 m. Find the power of the pump. Then introduce efficiency: η = useful power output / total power input."},
            {"step": 3, "type": "teach", "prompt": "Teach collisions. In ALL collisions, momentum is conserved: m₁u₁ + m₂u₂ = m₁v₁ + m₂v₂. In elastic collisions, KE is also conserved. In perfectly inelastic collisions, bodies stick together: m₁u₁ + m₂u₂ = (m₁ + m₂)v. Coefficient of restitution: e = (v₂ − v₁)/(u₁ − u₂). e = 1 for perfectly elastic, e = 0 for perfectly inelastic. Derive: for elastic collision, v₁ = ((m₁−m₂)u₁ + 2m₂u₂)/(m₁+m₂)."},
            {"step": 4, "type": "practice", "prompt": "Problem: A 2 kg ball moving at 6 m/s collides head-on with a 3 kg ball at rest. (a) If the collision is perfectly elastic, find velocities after collision. (b) If perfectly inelastic, find the common velocity and energy lost. (c) If e = 0.5, find final velocities."},
            {"step": 5, "type": "mastery", "prompt": "BUET-level: A bullet of mass 20 g moving at 400 m/s embeds in a 2 kg wooden block on a frictionless surface. Find: (a) velocity of block+bullet, (b) KE lost, (c) percentage of energy lost. Then: the block+bullet slides onto a rough patch (μ = 0.3). How far does it travel before stopping?"},
        ],
        "key_formulas": [
            "Power: P = W/t = Fv (unit: Watt, 1 hp = 746 W)",
            "Efficiency: η = P_output / P_input × 100%",
            "Conservation of momentum: m₁u₁ + m₂u₂ = m₁v₁ + m₂v₂",
            "Elastic collision: v₁ = ((m₁−m₂)u₁ + 2m₂u₂)/(m₁+m₂)",
            "Perfectly inelastic: v = (m₁u₁ + m₂u₂)/(m₁+m₂)",
            "Coefficient of restitution: e = (v₂ − v₁)/(u₁ − u₂)",
            "KE lost in perfectly inelastic collision: ΔKE = ½(m₁m₂/(m₁+m₂))(u₁ − u₂)²",
        ],
        "common_mistakes": [
            "Thinking kinetic energy is always conserved in collisions — KE is conserved ONLY in perfectly elastic collisions; momentum is conserved in ALL collisions (when no external force acts)",
            "Sign errors in collision problems — forgetting to assign negative velocity to objects moving in the opposite direction",
            "Confusing power with work — doing more work does not mean more power; a crane lifting a load slowly does the same work as one lifting it quickly, but the fast crane has more power",
        ],
        "practice_prompts": [
            "A pump lifts 500 liters of water per minute to a height of 15 m. Find the power of the pump in watts and horsepower. (1 liter of water = 1 kg)",
            "A 1 kg ball moving at 10 m/s hits a 2 kg ball at rest elastically. Find the final velocities of both balls.",
            "Two clay balls of masses 2 kg and 3 kg move toward each other at 4 m/s and 2 m/s respectively. They stick together. Find the velocity and KE lost.",
        ],
        "real_world_example": "In cricket, when Mashrafe or Mustafizur bowls a bouncer and it hits the batsman's helmet, it is an inelastic collision — the ball slows down dramatically and the KE lost is absorbed by the helmet (and unfortunately the batsman's head). Helmet design uses the physics of collisions to maximize the collision time and minimize the impact force. The power concept is visible in CNG auto-rickshaws: a CNG with a 10 hp engine can climb hills, but slowly; a bus with 200 hp climbs the same hill much faster.",
    },

    # ══ PHYSICS — Chapter 6: Gravitation ══
    "phy1-06-01": {
        "title": "Gravitation",
        "learning_objectives": [
            "State and apply Newton's law of universal gravitation: F = GMm/r²",
            "Derive and apply the relation g = GM/R² and its variation with altitude and depth",
            "Explain Kepler's three laws of planetary motion and derive the third law",
            "Calculate orbital velocity, escape velocity, and gravitational potential energy",
        ],
        "teaching_steps": [
            {"step": 1, "type": "intro", "prompt": "Ask: why does a mango fall downward and not sideways? Why does the Moon not fall onto the Earth? (It IS falling — constantly, toward Earth, but its tangential velocity keeps it in orbit.) Newton realized the same force that pulls the mango also keeps the Moon in orbit."},
            {"step": 2, "type": "concept", "prompt": "Teach Newton's law of gravitation: F = GMm/r² where G = 6.67 × 10⁻¹¹ Nm²/kg². Derive g = GM/R² at the Earth's surface. Show variation: g at height h: g_h = g(R/(R+h))², and at depth d: g_d = g(1 − d/R). Ask: where is g maximum — on the surface, above, or below? (On the surface.)"},
            {"step": 3, "type": "teach", "prompt": "Teach Kepler's laws: 1st — planets move in elliptical orbits with the Sun at one focus. 2nd — the line joining planet and Sun sweeps equal areas in equal times (conservation of angular momentum). 3rd — T² ∝ r³ (T²/r³ = constant for all planets). Derive: for circular orbit, GMm/r² = mv²/r, so v = √(GM/r). Also v_escape = √(2GM/R) = √(2gR) ≈ 11.2 km/s for Earth."},
            {"step": 4, "type": "practice", "prompt": "Problem: Find the acceleration due to gravity at: (a) 200 km above Earth's surface (R = 6400 km), (b) 3200 km below the surface. Then: a satellite orbits at height h = R above Earth. Find its orbital velocity and time period. Compare with a satellite at the surface."},
            {"step": 5, "type": "mastery", "prompt": "BUET-level: Two stars of masses M and 2M are separated by distance d. Find the point where the gravitational field is zero. Then: a planet has twice the radius and twice the mass of Earth. Find the escape velocity from this planet in terms of Earth's escape velocity. Finally: if a satellite's orbital radius is doubled, by what factor does its time period change? (Use Kepler's 3rd law.)"},
        ],
        "key_formulas": [
            "Newton's gravitation: F = GMm/r² (G = 6.67 × 10⁻¹¹ Nm²/kg²)",
            "Surface gravity: g = GM/R²",
            "At height h: g_h = g(R/(R+h))² ≈ g(1 − 2h/R) for h << R",
            "At depth d: g_d = g(1 − d/R)",
            "Orbital velocity: v₀ = √(GM/r) = √(gR²/r)",
            "Escape velocity: v_e = √(2GM/R) = √(2gR) ≈ 11.2 km/s",
            "Kepler's 3rd law: T² = (4π²/GM)r³, so T² ∝ r³",
            "Gravitational PE: U = −GMm/r",
        ],
        "common_mistakes": [
            "Confusing r (distance from center of Earth) with h (height above surface) — the formula F = GMm/r² uses the distance from the CENTER, not from the surface; for height h above surface, r = R + h",
            "Forgetting the negative sign in gravitational potential energy U = −GMm/r — the PE is negative because work must be done against gravity to separate masses to infinity",
            "Applying the formula g_d = g(1 − d/R) for depth and g_h = g(R/(R+h))² for height but mixing them up — at depth g decreases linearly, at height it decreases inversely with r²",
        ],
        "practice_prompts": [
            "The mass of the Moon is 1/81 of Earth's mass and its radius is 1/4 of Earth's. Find the acceleration due to gravity on the Moon's surface if g on Earth is 9.8 m/s².",
            "Calculate the escape velocity from the Moon given g_moon = 1.6 m/s² and R_moon = 1740 km.",
            "A geostationary satellite has a time period of 24 hours. If the Moon's orbital period is 27.3 days, find the ratio of the Moon's orbital radius to the geostationary orbit radius using Kepler's 3rd law.",
        ],
        "real_world_example": "Bangabandhu Satellite-1, Bangladesh's first geostationary communication satellite, orbits at about 35,786 km above the equator. At that height, its orbital period matches Earth's rotation (24 hours), so it appears stationary over Bangladesh. The orbital velocity and height are precisely calculated using v = √(GM/r) and Kepler's 3rd law — a direct application of what you are learning in this chapter.",
    },

    # ══ PHYSICS — Chapter 7: Elasticity & Fluid Mechanics ══
    "phy1-07-01": {
        "title": "Elasticity & Fluid Mechanics",
        "learning_objectives": [
            "Define stress, strain, and Young's modulus and solve problems using Y = stress/strain",
            "Distinguish between three types of elastic moduli: Young's, Bulk, and Shear modulus",
            "Apply Pascal's law and Archimedes' principle to fluid statics problems",
            "Derive and apply Bernoulli's equation and the equation of continuity",
        ],
        "teaching_steps": [
            {"step": 1, "type": "intro", "prompt": "Ask: why does a rubber band return to its original shape when stretched, but a piece of clay does not? Why does an iron rod break if bent too much? This is the study of elasticity. And why does a ship float while a nail sinks? That is fluid mechanics."},
            {"step": 2, "type": "concept", "prompt": "Teach stress (F/A, unit: Pa), strain (ΔL/L, dimensionless), and Hooke's law: stress ∝ strain within elastic limit. Young's modulus Y = stress/strain = FL/(AΔL). Also teach the stress-strain curve: proportional limit, elastic limit, yield point, breaking point. Ask: which has a higher Young's modulus — rubber or steel? (Steel — it requires more stress for the same strain.)"},
            {"step": 3, "type": "teach", "prompt": "Teach fluid statics: pressure P = F/A = ρgh (at depth h). Pascal's law: pressure applied to an enclosed fluid is transmitted equally in all directions. Archimedes' principle: buoyant force = weight of displaced fluid. Condition for floating: ρ_object < ρ_fluid. Then fluid dynamics: equation of continuity A₁v₁ = A₂v₂ and Bernoulli's equation: P + ½ρv² + ρgh = constant."},
            {"step": 4, "type": "practice", "prompt": "Problem: A steel wire of length 2 m and cross-section area 1 mm² is stretched by a 100 N force. Y for steel = 2 × 10¹¹ Pa. Find the extension. Then: a hydraulic press has pistons of area 10 cm² and 100 cm². A force of 50 N is applied on the small piston. What force acts on the large piston?"},
            {"step": 5, "type": "mastery", "prompt": "BUET-level: Water flows through a horizontal pipe. At one end, the cross-section is 40 cm², speed is 2 m/s, and pressure is 3 × 10⁵ Pa. At the other end, the cross-section is 20 cm². Find the speed and pressure at the narrow end using the equation of continuity and Bernoulli's equation. Then: a block of wood (ρ = 600 kg/m³) of volume 0.1 m³ is placed in water. What fraction is submerged? What mass must be placed on it to just submerge it fully?"},
        ],
        "key_formulas": [
            "Stress = F/A (unit: Pascal, N/m²)",
            "Strain = ΔL/L (dimensionless)",
            "Young's modulus: Y = stress/strain = FL/(AΔL)",
            "Pressure at depth: P = P₀ + ρgh",
            "Pascal's law: F₁/A₁ = F₂/A₂ (hydraulic press)",
            "Archimedes: Buoyant force = ρ_fluid × V_submerged × g",
            "Equation of continuity: A₁v₁ = A₂v₂",
            "Bernoulli's equation: P + ½ρv² + ρgh = constant",
        ],
        "common_mistakes": [
            "Confusing stress (force per unit area) with pressure — while dimensionally the same, stress is an internal restoring force per area in a solid, while pressure is the force per area exerted by a fluid",
            "Forgetting to convert units — cross-section area is often given in mm² or cm² but must be converted to m² for SI calculations; 1 mm² = 10⁻⁶ m²",
            "Applying Bernoulli's equation without checking assumptions — it requires steady, incompressible, non-viscous flow along a streamline; students often apply it to turbulent flow or compressible gases",
        ],
        "practice_prompts": [
            "A copper wire of length 3 m and diameter 1 mm is stretched by a 50 N force. Find the extension if Y for copper = 1.2 × 10¹¹ Pa.",
            "An ice cube of mass 0.5 kg floats in water. What volume of ice is above the water surface? (ρ_ice = 900 kg/m³, ρ_water = 1000 kg/m³)",
            "Water flows through a pipe at 3 m/s in a section with area 20 cm². The pipe narrows to 10 cm². Find the speed in the narrow section and, using Bernoulli's equation, the pressure difference if the pipe is horizontal.",
        ],
        "real_world_example": "The Padma Bridge's steel cables must support enormous loads without permanent deformation — engineers use Young's modulus to calculate exactly how much each cable stretches under load and ensure it stays within the elastic limit. Bernoulli's principle is why country boats (nouka) in Bangladesh's rivers move faster in narrow channels — as the river narrows, water speeds up and pressure drops, which is also why tin roofs blow off during nor'westers (kalboishakhi): fast wind over the roof creates low pressure above, and higher pressure inside pushes the roof up.",
    },

    # ══ PHYSICS — Chapter 8: Simple Harmonic Motion ══
    "phy1-08-01": {
        "title": "Simple Harmonic Motion",
        "learning_objectives": [
            "Define SHM and derive the equation x = A sin(ωt + φ) from restoring force F = −kx",
            "Calculate time period of a simple pendulum T = 2π√(l/g) and spring-mass system T = 2π√(m/k)",
            "Analyze velocity, acceleration, and energy at any position in SHM",
            "Solve problems involving combinations of springs (series and parallel)",
        ],
        "teaching_steps": [
            {"step": 1, "type": "intro", "prompt": "Ask: push a book on a table — it does not come back. But pull a pendulum and release — it swings back and forth. What is special about the restoring force that brings it back? This is simple harmonic motion: the force is proportional to displacement and directed toward the mean position."},
            {"step": 2, "type": "concept", "prompt": "Teach SHM: restoring force F = −kx (Hooke's law), so a = −ω²x where ω = √(k/m). Solution: x = A sin(ωt + φ). Velocity v = Aω cos(ωt + φ) = ω√(A² − x²). Acceleration a = −ω²x. Time period T = 2π/ω. Ask: at what position is velocity maximum? (Mean position, x = 0.) At what position is acceleration maximum? (Extreme position, x = ±A.)"},
            {"step": 3, "type": "teach", "prompt": "Teach simple pendulum: T = 2π√(l/g) — independent of mass and amplitude (for small angles). Spring-mass system: T = 2π√(m/k). Energy in SHM: KE = ½mω²(A² − x²), PE = ½mω²x², Total E = ½mω²A² = constant. At mean position: all KE. At extreme: all PE. Ask: at what position is KE = PE? (x = A/√2)."},
            {"step": 4, "type": "practice", "prompt": "Problem: A 0.5 kg mass on a spring (k = 200 N/m) oscillates with amplitude 0.1 m. Find: (a) time period, (b) maximum velocity, (c) maximum acceleration, (d) velocity and acceleration at x = 0.05 m. Then: a simple pendulum of length 1 m. Find its time period. If taken to the Moon (g_moon = g/6), what is the new period?"},
            {"step": 5, "type": "mastery", "prompt": "BUET-level: Two springs of constants k₁ = 100 N/m and k₂ = 200 N/m are connected in series and a 1 kg mass is attached. Find the effective spring constant and time period. Then repeat for parallel combination. Also: a particle in SHM has velocity 8 cm/s when at 3 cm from mean position, and velocity 6 cm/s when at 4 cm. Find the amplitude and time period."},
        ],
        "key_formulas": [
            "Restoring force: F = −kx, acceleration: a = −ω²x",
            "Displacement: x = A sin(ωt + φ)",
            "Velocity: v = Aω cos(ωt + φ) = ω√(A² − x²)",
            "Max velocity: v_max = Aω (at mean position)",
            "Max acceleration: a_max = Aω² (at extreme position)",
            "Simple pendulum: T = 2π√(l/g)",
            "Spring-mass: T = 2π√(m/k), ω = √(k/m)",
            "Energy: KE = ½mω²(A² − x²), PE = ½mω²x², Total E = ½mω²A²",
            "Springs in series: 1/k_eff = 1/k₁ + 1/k₂; in parallel: k_eff = k₁ + k₂",
        ],
        "common_mistakes": [
            "Confusing the conditions for maximum velocity and maximum acceleration — velocity is maximum at the MEAN position (x = 0), acceleration is maximum at the EXTREME position (x = ±A); students often reverse these",
            "Forgetting that the pendulum formula T = 2π√(l/g) is valid ONLY for small angle oscillations — for large angles, the period depends on amplitude",
            "Incorrectly combining springs — for springs in series, effective k is LESS than either individual k (1/k_eff = 1/k₁ + 1/k₂); for parallel, k_eff = k₁ + k₂. Students often swap these (confused with capacitor formulas)",
        ],
        "practice_prompts": [
            "A particle in SHM has amplitude 10 cm and period 2 s. Find the velocity and acceleration at x = 5 cm from the mean position.",
            "A pendulum clock keeps correct time at sea level. If taken to a hill where g is 0.1% less, how many seconds does it lose per day?",
            "At what displacement from the mean position is the kinetic energy of a particle in SHM equal to its potential energy?",
        ],
        "real_world_example": "The large pendulum clocks (ghori) you see in old Dhaka homes work on T = 2π√(l/g). If you take such a clock from Dhaka (near sea level) to the top of Keokradong (the highest peak in Bangladesh, ~1230 m), g decreases slightly and the pendulum swings slower — the clock loses time. This is also why earthquake-resistant buildings in Bangladesh are designed to avoid resonance — if the building's natural frequency matches the earthquake's frequency, oscillations amplify dangerously.",
    },

    # ══ PHYSICS — Chapter 9: Waves ══
    "phy1-09-01": {
        "title": "Wave Properties",
        "learning_objectives": [
            "Classify waves as transverse and longitudinal with examples",
            "Apply the wave equation v = fλ and relate to wave parameters (amplitude, frequency, wavelength, time period)",
            "Write and interpret the equation of a progressive wave: y = A sin(ωt − kx)",
            "Explain superposition principle, standing waves, and resonance",
        ],
        "teaching_steps": [
            {"step": 1, "type": "intro", "prompt": "Ask: when you throw a stone into a pukur (pond), you see ripples spreading outward. Does the water itself travel outward, or just the disturbance? (Just the disturbance — that is a wave.) What about sound — when someone calls you from far away, does air travel from them to you?"},
            {"step": 2, "type": "concept", "prompt": "Teach wave types: transverse (vibration perpendicular to propagation — water waves, light, string waves) vs longitudinal (vibration parallel — sound in air, compression waves in a spring). Teach wave parameters: amplitude A, wavelength λ, frequency f, time period T = 1/f, velocity v = fλ. Ask: if a wave has f = 500 Hz and λ = 0.68 m, what is its speed? (340 m/s — this is the speed of sound in air.)"},
            {"step": 3, "type": "teach", "prompt": "Teach the progressive wave equation: y = A sin(ωt − kx) where ω = 2πf (angular frequency) and k = 2π/λ (wave number). Direction: (ωt − kx) means wave travels in +x direction; (ωt + kx) means −x direction. Then teach superposition: when two waves meet, the resultant displacement is the sum. Standing waves form when two waves of equal amplitude and frequency travel in opposite directions: y = 2A sin(kx) cos(ωt). Nodes (zero displacement) at x = nλ/2, antinodes (maximum displacement) at x = (2n+1)λ/4."},
            {"step": 4, "type": "practice", "prompt": "Problem: A wave is described by y = 0.02 sin(100πt − 2πx) m. Find: (a) amplitude, (b) frequency, (c) wavelength, (d) wave speed, (e) direction of propagation. Then: a string of length 1 m is fixed at both ends. If the speed of the wave is 200 m/s, find the fundamental frequency and the first three harmonics."},
            {"step": 5, "type": "mastery", "prompt": "BUET-level: A string of length 0.5 m and mass 5 g is stretched by a tension of 80 N. Find: (a) the speed of transverse waves, (b) the fundamental frequency, (c) the frequency of the 3rd harmonic. Then: two waves y₁ = 3 sin(ωt − kx) and y₂ = 3 sin(ωt + kx) superpose. Write the equation of the resulting standing wave and find the positions of nodes and antinodes."},
        ],
        "key_formulas": [
            "Wave speed: v = fλ = λ/T",
            "Progressive wave: y = A sin(ωt − kx) (+x direction)",
            "ω = 2πf = 2π/T (angular frequency)",
            "k = 2π/λ (wave number)",
            "v = ω/k = fλ",
            "Speed on a string: v = √(T/μ) where T = tension, μ = mass per unit length",
            "Standing wave: y = 2A sin(kx) cos(ωt)",
            "String fixed at both ends: f_n = nv/(2L), n = 1, 2, 3...",
        ],
        "common_mistakes": [
            "Confusing the motion of the medium particles with the motion of the wave — in a transverse wave, particles move up and down but the wave travels horizontally; the wave carries energy, not matter",
            "Errors in reading wave equation parameters — confusing ω with f (ω = 2πf, not f), and k with 1/λ (k = 2π/λ, not 1/λ)",
            "Thinking standing waves do not carry energy — standing waves have nodes that do not move and energy is trapped between nodes; this is different from progressive waves that transport energy continuously",
        ],
        "practice_prompts": [
            "A wave has the equation y = 0.05 sin(200t − 5x) m. Find the amplitude, frequency, wavelength, and velocity.",
            "A guitar string of length 60 cm vibrates in its fundamental mode at 440 Hz. What is the speed of the wave on the string?",
            "Explain why you can hear someone around a corner but cannot see them around a corner. (Hint: diffraction depends on wavelength relative to obstacle size.)",
        ],
        "real_world_example": "During a nouka baich (boat race) in rural Bangladesh, when one person makes a wave in the water, you can see the wave travel across the river but the water itself stays roughly in place — this shows waves carry energy, not matter. The harmonics of waves on a string are what create music on the dotara or ektara (traditional Bangladeshi instruments). The different modes of vibration (fundamental, 2nd harmonic, etc.) create the rich tones that make folk music so distinctive.",
    },

    "phy1-09-02": {
        "title": "Sound & Doppler Effect",
        "learning_objectives": [
            "Explain sound as a longitudinal mechanical wave and describe its characteristics (pitch, loudness, quality)",
            "Apply the Doppler effect formula for moving source and/or observer",
            "Calculate beat frequency from two close frequencies",
            "Solve problems involving resonance in open and closed pipes",
        ],
        "teaching_steps": [
            {"step": 1, "type": "intro", "prompt": "Ask: have you noticed that a train's horn sounds higher-pitched as it approaches and lower as it moves away? Or the siren of an ambulance? This is the Doppler effect. Also: when two harmonium notes are slightly off-tune, you hear a 'wah-wah' pulsating sound — those are beats."},
            {"step": 2, "type": "concept", "prompt": "Teach sound properties: speed of sound in air ≈ 340 m/s (varies with temperature: v = 331 + 0.6T m/s where T in °C). Pitch depends on frequency, loudness on amplitude, quality/timbre on harmonics. Beats: when two waves of slightly different frequencies superpose, beat frequency f_beat = |f₁ − f₂|. Audible beats when f_beat < ~10 Hz."},
            {"step": 3, "type": "teach", "prompt": "Teach Doppler effect: f' = f × (v ± v_o)/(v ∓ v_s) where upper signs when source and observer approach, lower when they recede. Convention: v_o positive toward source, v_s positive toward observer. For source moving toward observer: f' = fv/(v − v_s). For observer moving toward source: f' = f(v + v_o)/v. Then teach resonance in pipes: open pipe harmonics f_n = nv/(2L), n = 1, 2, 3...; closed pipe (one end closed) f_n = nv/(4L), n = 1, 3, 5... (odd harmonics only)."},
            {"step": 4, "type": "practice", "prompt": "Problem: A train moving at 72 km/h sounds a whistle at 600 Hz. Find the frequency heard by a person standing ahead of the train and behind the train. (v_sound = 340 m/s.) Then: two tuning forks have frequencies 256 Hz and 260 Hz. What is the beat frequency? How many beats per second?"},
            {"step": 5, "type": "mastery", "prompt": "BUET-level: A car and an ambulance approach each other. The car moves at 20 m/s and the ambulance at 30 m/s. The siren frequency is 800 Hz. Find the frequency heard by the car driver. After they cross, find the new frequency. (v = 340 m/s.) Then: a closed pipe of length 85 cm. Find its fundamental frequency and the first two overtones (v = 340 m/s). Why are only odd harmonics produced in a closed pipe?"},
        ],
        "key_formulas": [
            "Speed of sound in air: v ≈ 331 + 0.6T m/s (T in °C)",
            "Doppler effect: f' = f(v ± v_o)/(v ∓ v_s)",
            "Source approaching: f' = fv/(v − v_s) (frequency increases)",
            "Source receding: f' = fv/(v + v_s) (frequency decreases)",
            "Beat frequency: f_beat = |f₁ − f₂|",
            "Open pipe: f_n = nv/(2L), n = 1, 2, 3... (all harmonics)",
            "Closed pipe: f_n = nv/(4L), n = 1, 3, 5... (odd harmonics only)",
            "Resonance tube: first resonance at L₁ = λ/4, second at L₂ = 3λ/4, so λ = 2(L₂ − L₁)",
        ],
        "common_mistakes": [
            "Getting the Doppler effect signs wrong — the most common error; remember: frequency INCREASES when source and observer approach (shorter wavelength), DECREASES when they separate. Use the sign convention consistently.",
            "Thinking closed pipes produce all harmonics — a closed pipe (one end closed) produces ONLY odd harmonics (1st, 3rd, 5th...) because a node must form at the closed end and an antinode at the open end",
            "Confusing beats with interference — beats occur when two waves of SLIGHTLY different frequencies superpose (temporal variation in loudness), while constructive/destructive interference occurs when waves of the SAME frequency meet at different path differences (spatial pattern)",
        ],
        "practice_prompts": [
            "A train moving at 90 km/h approaches a stationary observer and sounds a 500 Hz horn. What frequency does the observer hear? After the train passes, what frequency is heard? (v = 340 m/s)",
            "Two organ pipes have lengths 80 cm and 81 cm. Both are open. If the speed of sound is 340 m/s, find the beat frequency between their fundamentals.",
            "In a resonance tube experiment, the first and second resonance positions are at 17 cm and 51 cm. Find the wavelength and the frequency of the tuning fork used. (v = 340 m/s)",
        ],
        "real_world_example": "You hear the Doppler effect every day in Dhaka — when a bus honks and zooms past you on Mirpur Road, the pitch clearly drops as it passes. In cricket, the 'snickometer' used in DRS (Decision Review System) detects the tiny sound of ball hitting bat using sound wave analysis. Beats are used by instrument tuners — when a harmonium player in Bangladesh tunes their instrument, they listen for beats between their note and a reference pitch; when the beats disappear (f_beat = 0), the notes are perfectly in tune.",
    },

    # ══ PHYSICS — Chapter 10: Gas Laws & Kinetic Theory ══
    "phy1-10-01": {
        "title": "Gas Laws & Kinetic Theory",
        "learning_objectives": [
            "State and apply Boyle's law, Charles's law, and the ideal gas equation PV = nRT",
            "Derive the kinetic theory expression for gas pressure: P = ⅓ρc²",
            "Relate temperature to average kinetic energy: KE = (3/2)kT",
            "Explain concepts of rms speed, mean speed, and degrees of freedom",
        ],
        "teaching_steps": [
            {"step": 1, "type": "intro", "prompt": "Ask: why does a balloon expand when heated? Why does a bicycle tyre feel harder in summer than winter? Why does the pressure inside a pressure cooker increase? These are all explained by gas laws and kinetic theory."},
            {"step": 2, "type": "concept", "prompt": "Teach gas laws: Boyle's law (T constant): PV = constant (P₁V₁ = P₂V₂). Charles's law (P constant): V/T = constant (V₁/T₁ = V₂/T₂, T in Kelvin!). Gay-Lussac's law (V constant): P/T = constant. Combined: P₁V₁/T₁ = P₂V₂/T₂. Ideal gas equation: PV = nRT where R = 8.314 J/(mol·K). Ask: at STP (273 K, 1 atm), what volume does 1 mole of gas occupy? (22.4 L.)"},
            {"step": 3, "type": "teach", "prompt": "Teach kinetic theory of gases: assumptions (large number of molecules, random motion, elastic collisions, negligible intermolecular forces, volume of molecules negligible compared to container). Derive P = ⅓ρc̄² = ⅓(Nm/V)c̄² where c̄² is mean square speed. From PV = nRT and P = ⅓ρc̄², derive: ½mc̄² = (3/2)kT where k = R/Nₐ = 1.38 × 10⁻²³ J/K (Boltzmann constant). So rms speed: c_rms = √(3kT/m) = √(3RT/M)."},
            {"step": 4, "type": "practice", "prompt": "Problem: A gas at 27°C and 2 atm occupies 500 mL. Find its volume at STP. Then: find the rms speed of oxygen molecules at 27°C (M = 32 g/mol = 0.032 kg/mol, R = 8.314). Also: find the average kinetic energy of a gas molecule at 300 K."},
            {"step": 5, "type": "mastery", "prompt": "BUET-level: An ideal gas is at temperature 300 K. (a) Find the rms speed of N₂ molecules (M = 28 g/mol). (b) At what temperature would the rms speed double? (c) Find the ratio of rms speeds of H₂ and O₂ at the same temperature. (d) A container has a mixture of He and Ar. Which gas molecules have higher average KE? (Neither — average KE depends only on T, not on molecular mass.) Which have higher rms speed? (He — lighter molecules move faster.)"},
        ],
        "key_formulas": [
            "Ideal gas equation: PV = nRT (R = 8.314 J/(mol·K))",
            "Boyle's law (T const): P₁V₁ = P₂V₂",
            "Charles's law (P const): V₁/T₁ = V₂/T₂ (T in Kelvin)",
            "Kinetic theory pressure: P = ⅓ρc̄² = ⅓(nM/V)c̄²",
            "Average KE per molecule: KE = (3/2)kT (k = 1.38 × 10⁻²³ J/K)",
            "RMS speed: c_rms = √(3RT/M) = √(3kT/m)",
            "For f degrees of freedom: KE = (f/2)kT per molecule",
            "At STP (0°C, 1 atm): 1 mol of ideal gas occupies 22.4 L",
        ],
        "common_mistakes": [
            "Using Celsius instead of Kelvin in gas law calculations — ALL gas law formulas require ABSOLUTE temperature (Kelvin); T(K) = T(°C) + 273. This is the single most common error in gas problems.",
            "Confusing rms speed with average speed — rms speed (c_rms = √(3RT/M)) is always slightly higher than average speed (c_avg = √(8RT/πM)); they are different statistical measures",
            "Thinking heavier gas molecules have more kinetic energy at the same temperature — average KE = (3/2)kT depends ONLY on temperature, not on molecular mass; heavier molecules just move slower to have the same KE",
        ],
        "practice_prompts": [
            "A gas at 300 K has rms speed 500 m/s. At what temperature will the rms speed become 1000 m/s?",
            "Find the rms speed of hydrogen molecules (M = 2 g/mol) at 27°C. Compare with the speed of sound in air (340 m/s).",
            "A vessel contains a mixture of O₂ and H₂ at the same temperature. Find the ratio of their rms speeds. Which gas escapes faster through a small hole (effusion)?",
        ],
        "real_world_example": "In Bangladesh's garment factories, industrial pressure cookers (autoclaves) use Gay-Lussac's law — as the sealed container is heated, temperature rises and so does pressure (P/T = constant), which sterilizes fabrics and equipment. The kinetic theory explains why ceiling fans cool you in Bangladesh's summer — the fan does not lower air temperature but moves air faster across your skin, increasing evaporation rate. The RMS speed formula also explains why hydrogen gas rises quickly from a leaking CNG cylinder — H₂ molecules are light and move at very high speeds (~1900 m/s at room temperature), much faster than air molecules.",
    },

    # ══ CHEMISTRY — Chapter 1: পরিবেশ রসায়ন (Environmental Chemistry) ══
    "chem1-01-01": {
        "title": "Atmosphere, Pollutants & Air Quality",
        "learning_objectives": [
            "Describe the composition and layers of Earth's atmosphere",
            "Classify air pollutants as primary and secondary with examples",
            "Explain the formation of photochemical smog and acid rain with chemical equations",
            "Analyze the causes and effects of ozone layer depletion (CFCs, NOx)",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: why do you think Dhaka's air quality is among the worst in the world during winter? What gases might be responsible?",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Explain the layers of the atmosphere (troposphere, stratosphere, etc.) and where ozone is concentrated. Ask: why is ozone beneficial in the stratosphere but harmful in the troposphere?",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Teach the chemistry of acid rain: SO2 + H2O -> H2SO3, 2SO2 + O2 -> 2SO3, SO3 + H2O -> H2SO4. Also NO2 + H2O -> HNO3 + HNO2. Ask: which industries in Bangladesh release SO2?",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Problem: Write the chain reaction mechanism for ozone depletion by CFCs. Cl + O3 -> ClO + O2, ClO + O -> Cl + O2. Why is Cl called a catalyst here?",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "Ask: the pH of normal rain is about 5.6 (not 7). Why? If a rain sample has pH 3.5, calculate the [H+] concentration and identify which acids are likely responsible.",
            },
        ],
        "key_formulas": [
            "SO2 + H2O -> H2SO3 (sulfurous acid)",
            "2SO2 + O2 -> 2SO3 ; SO3 + H2O -> H2SO4 (sulfuric acid)",
            "NO2 + H2O -> HNO3 + HNO2",
            "O3 + Cl -> ClO + O2 ; ClO + O -> Cl + O2 (net: O3 + O -> 2O2)",
            "CO2 + H2O <=> H2CO3 (why normal rain is pH ~5.6)",
        ],
        "common_mistakes": [
            "Confusing primary pollutants (directly emitted: CO, SO2, NO) with secondary pollutants (formed by reaction: O3, PAN, H2SO4)",
            "Writing the ozone depletion mechanism without showing the catalytic regeneration of Cl",
            "Forgetting that normal rainwater is already slightly acidic (pH 5.6) due to dissolved CO2, not pH 7",
        ],
        "practice_prompts": [
            "A factory emits SO2 at a rate of 500 kg/day. Write the complete pathway showing how this leads to acid rain. If all SO2 converts to H2SO4, what mass of H2SO4 is produced? (S=32, O=16, H=1)",
            "Explain with equations why the greenhouse effect of CH4 is ~25 times stronger per molecule than CO2, yet CO2 is the bigger concern overall.",
            "In Dhaka, photochemical smog is worst in winter afternoons. Explain the role of sunlight, NO2, and VOCs in smog formation.",
        ],
        "real_world_example": "In Dhaka, brick kilns around the city burn coal and release SO2 and particulates. During winter, the inversion layer traps these pollutants close to the ground, making breathing difficult — this is why your eyes water and throat hurts on foggy December mornings.",
    },

    "chem1-01-02": {
        "title": "Water & Soil Pollution and Green Chemistry",
        "learning_objectives": [
            "Explain BOD, COD, and DO as indicators of water quality",
            "Describe causes and effects of eutrophication in Bangladeshi water bodies",
            "Identify major soil pollutants (pesticides, heavy metals) and their bioaccumulation",
            "Apply the 12 principles of green chemistry to reduce pollution",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: why do fish die in the Buriganga river near Old Dhaka? What do you think the tannery waste contains?",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Explain BOD (Biochemical Oxygen Demand) and DO (Dissolved Oxygen). Ask: if BOD is high, is the water clean or polluted? Why does high BOD cause fish kills?",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Teach eutrophication: excess N and P from fertilizers -> algal bloom -> algae die -> decomposition uses O2 -> aquatic life dies. Ask: which fertilizers used in Bangladesh cause this? (urea, TSP)",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Problem: A water sample has BOD of 300 mg/L. Safe drinking water BOD is <5 mg/L. Calculate by what factor the organic pollutant load must be reduced. What treatment methods can achieve this?",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "Green chemistry challenge: The Hazaribagh tanneries used Cr(VI) for leather tanning, contaminating soil. Suggest how green chemistry principles (atom economy, safer solvents) could redesign the process. What is the oxidation state change if Cr(VI) is reduced to Cr(III)?",
            },
        ],
        "key_formulas": [
            "BOD = initial DO - final DO (after 5 days at 20C)",
            "Eutrophication: excess PO4^3- / NO3^- -> algal bloom -> O2 depletion",
            "Atom economy = (MW of desired product / MW of all products) x 100%",
            "Cr2O7^2- + 14H+ + 6e- -> 2Cr^3+ + 7H2O (Cr(VI) to Cr(III) reduction)",
        ],
        "common_mistakes": [
            "Confusing BOD with COD — BOD is biological oxygen demand (5-day test), COD uses chemical oxidant (K2Cr2O7) and measures total oxidizable matter",
            "Thinking eutrophication is caused by toxic chemicals — it is actually caused by excess nutrients (N, P) leading to algal overgrowth",
            "Mixing up bioaccumulation (increase within an organism) with biomagnification (increase along the food chain)",
        ],
        "practice_prompts": [
            "The arsenic contamination in Bangladesh groundwater is a major crisis. If a tube well has As concentration of 0.15 mg/L and the WHO safe limit is 0.01 mg/L, by what percentage must arsenic be removed? Suggest a chemical method for arsenic removal (hint: co-precipitation with Fe(OH)3).",
            "Calculate the atom economy of the reaction: CH3CH2OH + CH3COOH -> CH3COOCH2CH3 + H2O. Is this reaction atom-efficient? (C=12, H=1, O=16)",
        ],
        "real_world_example": "The Buriganga river in Dhaka was once a lifeline but is now biologically dead in the dry season. Tannery waste from Hazaribagh dumped chromium compounds, dyes, and organic waste directly into the river, pushing BOD above 30 mg/L — fish cannot survive when DO drops below 4 mg/L.",
    },

    # ══ CHEMISTRY — Chapter 2: গুণগত রসায়ন (Qualitative Chemistry) ══
    "chem1-02-01": {
        "title": "Stoichiometry & Chemical Equations",
        "learning_objectives": [
            "Balance complex chemical equations including redox reactions",
            "Apply the mole concept to calculate masses, volumes, and number of particles",
            "Solve limiting reagent and percentage yield problems",
            "Use Avogadro's law and molar volume (22.4 L at STP) in gas calculations",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: if you react 10g of Zn with excess HCl, can you predict exactly how much H2 gas you will get? How? This is the power of stoichiometry.",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Review the mole concept: 1 mol = 6.022 x 10^23 particles = molar mass in grams = 22.4 L gas at STP. Ask: how many molecules are in 1.8 g of water? (H=1, O=16)",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Teach limiting reagent: if 5 mol H2 reacts with 2 mol O2 (2H2 + O2 -> 2H2O), which is limiting? Calculate moles of H2O formed and excess reactant remaining.",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Problem: 50 mL of 0.1M AgNO3 reacts with 30 mL of 0.2M NaCl. Find: (a) limiting reagent, (b) mass of AgCl precipitate, (c) concentration of excess ions. (Ag=108, Cl=35.5, N=14, O=16, Na=23)",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "BUET-level: In the thermite reaction 2Al + Fe2O3 -> Al2O3 + 2Fe, 5.4g Al reacts with 24g Fe2O3. Find the theoretical yield of Fe and the percentage yield if only 8.4g Fe is actually obtained. (Al=27, Fe=56, O=16)",
            },
        ],
        "key_formulas": [
            "n = m / M (moles = mass / molar mass)",
            "n = N / NA (moles = number of particles / Avogadro's number)",
            "PV = nRT (ideal gas: P in atm, V in L, R = 0.0821 L.atm/mol.K)",
            "At STP (0C, 1 atm): 1 mol gas = 22.4 L",
            "Percentage yield = (actual yield / theoretical yield) x 100%",
            "Molarity (M) = moles of solute / volume of solution in L",
        ],
        "common_mistakes": [
            "Forgetting to convert grams to moles before doing stoichiometric calculations",
            "Assuming the reactant present in smaller mass is always the limiting reagent — it depends on mole ratio, not mass",
            "Using 22.4 L/mol at non-STP conditions — this value is only valid at 0C and 1 atm",
        ],
        "practice_prompts": [
            "How many grams of CO2 are produced when 50g of CaCO3 is completely decomposed? (CaCO3 -> CaO + CO2). If the actual yield is 19.8g, what is the percentage yield? (Ca=40, C=12, O=16)",
            "At STP, what volume of O2 is needed to completely combust 11.2 L of CH4? (CH4 + 2O2 -> CO2 + 2H2O)",
            "A 250 mL solution contains 5.85g NaCl. Calculate the molarity. If 50 mL of this is diluted to 500 mL, what is the new concentration? (Na=23, Cl=35.5)",
        ],
        "real_world_example": "When you take an antacid tablet (500mg CaCO3) for acidity, stoichiometry tells us exactly how much stomach acid (HCl) it can neutralize: CaCO3 + 2HCl -> CaCl2 + H2O + CO2. That is why the dose matters — too little does not help, too much wastes medicine.",
    },

    "chem1-02-02": {
        "title": "Oxidation-Reduction & Balancing Redox Reactions",
        "learning_objectives": [
            "Assign oxidation numbers to atoms in compounds and ions",
            "Identify oxidizing agents and reducing agents in a reaction",
            "Balance redox equations using the ion-electron (half-reaction) method",
            "Balance redox equations using the oxidation number change method",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: when iron rusts (4Fe + 3O2 -> 2Fe2O3), is iron gaining or losing electrons? What happens to oxygen? This is the heart of redox chemistry.",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Teach oxidation number rules: free element = 0, monatomic ion = charge, O = -2 (except peroxides), H = +1 (except metal hydrides). Ask: what is the oxidation number of Mn in KMnO4? of Cr in K2Cr2O7?",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Demonstrate the ion-electron method for balancing: MnO4^- + Fe^2+ -> Mn^2+ + Fe^3+ in acidic medium. Write separate half-reactions, balance atoms and charge, then combine.",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Balance using the ion-electron method in acidic solution: Cr2O7^2- + SO3^2- -> Cr^3+ + SO4^2-. Identify the oxidizing and reducing agents.",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "BUET-level: Balance in basic medium: MnO4^- + I^- -> MnO2 + IO3^-. Verify your answer by checking that atoms and charges balance on both sides.",
            },
        ],
        "key_formulas": [
            "Oxidation = loss of electrons (OIL), Reduction = gain of electrons (RIG)",
            "Oxidizing agent is reduced, Reducing agent is oxidized",
            "In acidic medium: balance O with H2O, balance H with H+",
            "In basic medium: after balancing in acid, add OH^- to neutralize H+ on both sides",
            "KMnO4 in acidic medium: MnO4^- + 8H+ + 5e^- -> Mn^2+ + 4H2O",
            "K2Cr2O7 in acidic medium: Cr2O7^2- + 14H+ + 6e^- -> 2Cr^3+ + 7H2O",
        ],
        "common_mistakes": [
            "Forgetting to balance oxygen atoms with H2O and hydrogen atoms with H+ before balancing charge with electrons",
            "Not multiplying half-reactions to equalize electrons before adding them — electrons must cancel completely",
            "Confusing oxidizing agent with the species being oxidized — the oxidizing agent itself gets reduced",
        ],
        "practice_prompts": [
            "Assign oxidation numbers to every atom in: K2Cr2O7, Na2S2O3, H2SO4, KMnO4. What is the oxidation state of S in Na2S2O3?",
            "Balance in acidic medium: Cu + HNO3(dilute) -> Cu(NO3)2 + NO + H2O. How many moles of HNO3 react per mole of Cu?",
            "In the reaction Zn + CuSO4 -> ZnSO4 + Cu, identify which species is oxidized, which is reduced, the oxidizing agent, and the reducing agent.",
        ],
        "real_world_example": "The batteries in your phone work on redox chemistry. In a lithium-ion battery, Li is oxidized at the anode (loses electrons) and the electrons flow through the circuit to power your device before being accepted at the cathode — that current flow is what charges your phone.",
    },

    # ══ CHEMISTRY — Chapter 3: মৌলের পর্যায়বৃত্ত ধর্ম (Periodic Properties) ══
    "chem1-03-01": {
        "title": "Periodic Table & Electron Configuration",
        "learning_objectives": [
            "Write electron configurations using Aufbau principle, Hund's rule, and Pauli exclusion",
            "Relate electron configuration to position in the periodic table (block, group, period)",
            "Explain the anomalous configurations of Cr (3d5 4s1) and Cu (3d10 4s1)",
            "Predict properties of elements based on their position in the periodic table",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: if I give you the atomic number of an element, can you predict which group and period it belongs to? How? The secret is electron configuration.",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Teach the Aufbau order: 1s, 2s, 2p, 3s, 3p, 4s, 3d, 4p... Use the (n+l) rule. Ask: why does 4s fill before 3d?",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Write configurations for Fe (Z=26), Cr (Z=24), Cu (Z=29). Explain why Cr is [Ar] 3d5 4s1 not [Ar] 3d4 4s2 — extra stability of half-filled d subshell.",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Problem: Write the electron configuration of Mn^2+ (Z=25) and Fe^3+ (Z=26). Which one is more stable and why? (Hint: look at the d subshell)",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "BUET-level: An element has the configuration [Ar] 3d10 4s2 4p3. Identify the element, its block, group, period, and predict whether it is a metal, nonmetal, or metalloid. What is its highest possible oxidation state?",
            },
        ],
        "key_formulas": [
            "Aufbau order (n+l rule): 1s < 2s < 2p < 3s < 3p < 4s < 3d < 4p < 5s < 4d < 5p ...",
            "Maximum electrons in a shell: 2n^2",
            "Maximum electrons in a subshell: 2(2l+1)",
            "For ions: remove electrons from outermost shell first (4s before 3d for transition metals)",
            "Half-filled (d5) and fully-filled (d10) configurations have extra stability",
        ],
        "common_mistakes": [
            "When writing ion configurations for transition metals, removing electrons from 3d instead of 4s first — Fe^2+ is [Ar] 3d6, NOT [Ar] 3d4 4s2",
            "Forgetting the anomalous configurations of Cr and Cu due to half-filled and fully-filled d orbital stability",
            "Confusing the order of filling (4s before 3d) with the order of removing electrons (4s removed first for ions)",
        ],
        "practice_prompts": [
            "Write the electron configuration of Ni (Z=28), Ni^2+, and Cu+ (Z=29). Which of these has a completely filled d subshell?",
            "An element has the configuration [Kr] 4d5 5s1. Identify the element and explain why it does not have the configuration [Kr] 4d4 5s2.",
        ],
        "real_world_example": "The vibrant colors in fireworks come from electron configurations. When heated, electrons jump to higher energy levels and emit specific colors when they fall back — Na gives yellow, Cu gives green-blue, Sr gives red. This is why the periodic table matters even in celebrations like Pohela Boishakh fireworks.",
    },

    "chem1-03-02": {
        "title": "Periodic Trends: Radius, IE, EA & Electronegativity",
        "learning_objectives": [
            "Explain trends in atomic radius, ionic radius across periods and down groups",
            "Compare ionization energies and identify anomalies (Be>B, N>O)",
            "Distinguish electron affinity and electronegativity",
            "Use periodic trends to predict chemical behavior and bond type",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: which atom is bigger — Na or Cl? They are in the same period. What about Na or K? Why does size change across and down the table?",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Teach atomic radius trend: decreases across a period (more protons, same shell), increases down a group (more shells). Ask: why is Na+ much smaller than Na, but Cl^- is larger than Cl?",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Teach ionization energy trends and anomalies. IE increases across a period but B < Be (2p1 easier to remove than 2s2) and O < N (paired 2p4 electron easier than half-filled 2p3). Explain with orbital diagrams.",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Arrange in order of increasing first ionization energy: Na, Mg, Al, Si, P. Explain any anomalies. Then arrange O, S, Se in order of increasing electron affinity.",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "BUET-level: The first ionization energies (kJ/mol) of four consecutive elements are: 786, 1086, 1402, 1314. Identify the elements and explain why the 4th value is lower than the 3rd. Also predict which of these elements forms the most stable +2 ion.",
            },
        ],
        "key_formulas": [
            "Atomic radius: decreases L->R across period, increases top->bottom in group",
            "Ionic radius: cation < atom < anion (for same element)",
            "Isoelectronic species: more protons = smaller radius (O^2- > F^- > Na+ > Mg^2+)",
            "IE1 < IE2 < IE3 ... (successive IEs always increase)",
            "Electronegativity (Pauling): F(4.0) > O(3.5) > N(3.0) > Cl(3.0)",
            "Electron affinity: most negative (exothermic) for halogens; noble gases ~0",
        ],
        "common_mistakes": [
            "Thinking atomic radius always decreases across a period without exception — actually d-block elements show very small changes due to poor shielding by d electrons",
            "Confusing electron affinity with electronegativity — EA is energy released when an atom gains one electron (measurable), electronegativity is the tendency to attract shared electrons in a bond (relative scale)",
            "Not recognizing IE anomalies: Be > B and N > O due to subshell stability — this is a very common BUET/DU admission question",
        ],
        "practice_prompts": [
            "Arrange the following isoelectronic species in order of increasing ionic radius: Na+, F^-, O^2-, Mg^2+, N^3-. Explain your reasoning.",
            "The second ionization energy of Na is dramatically higher than its first IE, but for Mg the jump is less dramatic. Explain using electron configuration.",
            "Which has a more negative electron affinity: Cl or F? Explain why, despite F being more electronegative. (Hint: consider the small size of the 2p orbital)",
        ],
        "real_world_example": "The reason table salt (NaCl) forms so readily is explained by periodic trends. Na has very low ionization energy (easy to lose its electron) and Cl has very high electron affinity (eager to gain one). This huge difference in electronegativity across period 3 drives the formation of ionic bonds — the same chemistry that preserves fish (shutki) in Cox's Bazar.",
    },

    # ══ HIGHER MATHEMATICS — Chapter 1: সেট ও ফাংশন (Sets & Functions) ══
    "hm1-01-01": {
        "title": "Sets, Subsets & Set Operations",
        "learning_objectives": [
            "Define sets using roster and set-builder notation and identify types (finite, infinite, empty, universal)",
            "Determine subsets, proper subsets, and power sets of a given set",
            "Perform union, intersection, difference, and complement operations",
            "Apply De Morgan's laws and verify results using Venn diagrams",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: if I say 'the set of all rivers in Bangladesh', how would you list its elements? What if I say 'the set of all even numbers' — can you list them all?",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Explain roster vs set-builder notation. Ask student to write {x ∈ ℕ : x < 6} in roster form and vice versa. Introduce empty set ∅ and universal set U.",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Teach subset (⊆), proper subset (⊂), and power set P(A). Ask: if A = {1, 2, 3}, how many elements does P(A) have? Then introduce A ∪ B, A ∩ B, A − B, and A' with Venn diagrams.",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Problem: Let U = {1,2,3,...,10}, A = {1,2,3,4,5}, B = {3,4,5,6,7}. Find A ∪ B, A ∩ B, A − B, A', and verify (A ∪ B)' = A' ∩ B' (De Morgan's law).",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "BUET-level: If n(A) = 40, n(B) = 35, n(A ∪ B) = 60, n(U) = 80, find n(A ∩ B), n(A' ∩ B'), and n(A − B). Ask student to draw the Venn diagram with cardinalities in each region.",
            },
        ],
        "key_formulas": [
            "|P(A)| = 2ⁿ where n = |A|",
            "n(A ∪ B) = n(A) + n(B) − n(A ∩ B)",
            "(A ∪ B)' = A' ∩ B' and (A ∩ B)' = A' ∪ B' — De Morgan's laws",
            "n(A ∪ B ∪ C) = n(A) + n(B) + n(C) − n(A∩B) − n(B∩C) − n(A∩C) + n(A∩B∩C)",
        ],
        "common_mistakes": [
            "Confusing ∈ (element of) with ⊆ (subset of) — e.g., writing {1} ∈ {1,2} instead of {1} ⊆ {1,2}",
            "Forgetting that ∅ is a subset of every set, and every set is a subset of itself",
            "Errors in De Morgan's law — swapping union and intersection without also taking complements",
        ],
        "practice_prompts": [
            "If A = {a, b, c}, list all subsets of A. How many are proper subsets?",
            "In a class of 100 students, 60 take Physics, 50 take Math, 20 take both. How many take neither?",
            "Prove using set algebra that A − (B ∩ C) = (A − B) ∪ (A − C).",
        ],
        "real_world_example": "Think of mobile phone plans in Bangladesh — Grameenphone's 4G coverage area is set A, Robi's is set B. The intersection A ∩ B is where both have 4G. The union A ∪ B is total 4G coverage. Areas with no coverage at all are (A ∪ B)'.",
    },

    "hm1-01-02": {
        "title": "Functions, Domain & Range",
        "learning_objectives": [
            "Define a function as a special relation and distinguish from general relations",
            "Determine domain, co-domain, and range of a function",
            "Classify functions as one-one (injective), onto (surjective), and bijective",
            "Compute composite functions (f∘g) and inverse functions (f⁻¹)",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: if every student in your class is assigned exactly one roll number, is this a function? What if two students share the same roll number — is it still a function from students to roll numbers?",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Define function f: A → B as a relation where every element of A maps to exactly one element of B. Explain domain, co-domain, range. Ask: if f(x) = √(x−2), what is the domain?",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Teach one-one, onto, bijective with arrow diagrams. Then introduce composite function: if f(x) = 2x+1 and g(x) = x², find (f∘g)(x) and (g∘f)(x). Ask: are they equal?",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Problem: f(x) = (3x−2)/(x+1). Find domain of f, then find f⁻¹(x). Verify that f(f⁻¹(x)) = x.",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "BUET-level: Let f: ℝ→ℝ, f(x) = x² − 4x + 3. Find the range of f. Is f one-one? If we restrict domain to [2, ∞), find f⁻¹(x) and state its domain.",
            },
        ],
        "key_formulas": [
            "Domain of f(x) = √(g(x)) requires g(x) ≥ 0",
            "Domain of f(x) = 1/g(x) requires g(x) ≠ 0",
            "(f∘g)(x) = f(g(x))",
            "f⁻¹ exists iff f is bijective; solve y = f(x) for x to get f⁻¹(y)",
        ],
        "common_mistakes": [
            "Confusing co-domain with range — range is the actual output set, co-domain is the declared target set",
            "Assuming f∘g = g∘f — composite functions are generally not commutative",
            "Forgetting to check domain restrictions when finding inverse (e.g., for quadratics, must restrict domain first)",
        ],
        "practice_prompts": [
            "Find the domain and range of f(x) = 1/(x² − 9).",
            "If f(x) = 2x + 3 and g(x) = (x − 3)/2, show that f and g are inverses of each other.",
            "Is f(x) = |x| one-one? Is it onto when f: ℝ → ℝ? What about f: ℝ → [0, ∞)?",
        ],
        "real_world_example": "Think of your National ID card system — each citizen maps to exactly one NID number (function). If no two people share an NID, it is one-one. If every possible NID is assigned, it is onto. Bangladesh's NID is designed to be bijective — a perfect one-to-one correspondence.",
    },

    # ══ HIGHER MATHEMATICS — Chapter 2: বীজগাণিতিক রাশি (Algebraic Expressions) ══
    "hm1-02-01": {
        "title": "Polynomials & Factoring",
        "learning_objectives": [
            "Classify polynomials by degree and number of terms",
            "Apply Factor Theorem and Remainder Theorem to find factors and remainders",
            "Factor polynomials using grouping, identities, and synthetic division",
            "Solve polynomial equations and find relationships between roots and coefficients",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: what is the remainder when you divide x³ − 3x² + 2x − 5 by (x − 1)? Can you guess without doing long division?",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Teach Remainder Theorem: f(a) = remainder when f(x) ÷ (x−a). Then Factor Theorem: (x−a) is a factor iff f(a) = 0. Ask student to check if (x−2) is a factor of x³ − 6x² + 11x − 6.",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Demonstrate synthetic division to factor x³ − 6x² + 11x − 6 completely. Teach sum/product of roots: for ax² + bx + c = 0, α+β = −b/a, αβ = c/a. Extend to cubic equations.",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Problem: Factor 2x³ + x² − 13x + 6 completely. Then find all roots. Verify using sum and product of roots.",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "BUET-level: If α, β are roots of x² − 5x + 3 = 0, find the value of α³ + β³ and form the equation whose roots are α² and β². No calculator — use identities only.",
            },
        ],
        "key_formulas": [
            "Remainder Theorem: f(x) ÷ (x−a) gives remainder f(a)",
            "Factor Theorem: (x−a) | f(x) ⟺ f(a) = 0",
            "For ax² + bx + c = 0: α+β = −b/a, αβ = c/a",
            "α³ + β³ = (α+β)³ − 3αβ(α+β)",
            "For ax³ + bx² + cx + d = 0: α+β+γ = −b/a, αβ+βγ+γα = c/a, αβγ = −d/a",
        ],
        "common_mistakes": [
            "Sign error in Remainder Theorem — evaluating f(a) when divisor is (x−a), not (x+a)",
            "Forgetting the negative sign in sum of roots: α+β = −b/a (not +b/a)",
            "Incomplete factoring — stopping at one factor instead of factoring the remaining quadratic",
        ],
        "practice_prompts": [
            "Use the Factor Theorem to show (x + 3) is a factor of x³ + 27. Then factor completely.",
            "If α, β are roots of 2x² − 7x + 5 = 0, find 1/α + 1/β without solving for α, β.",
            "Find k if (x − 2) is a factor of x³ − kx² + 5x + 2.",
        ],
        "real_world_example": "When engineers at Padma Bridge calculated load distribution across supports, they used polynomial equations where the roots represent critical stress points. Factoring tells them exactly where the structure needs reinforcement.",
    },

    "hm1-02-02": {
        "title": "Partial Fractions",
        "learning_objectives": [
            "Decompose proper rational expressions into partial fractions with linear factors",
            "Handle repeated linear factors in partial fraction decomposition",
            "Decompose expressions with irreducible quadratic factors",
            "Convert improper fractions to proper form before decomposition",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: you know how to add 1/(x+1) + 2/(x−1) into a single fraction. Can you reverse the process? Given (3x−1)/((x+1)(x−1)), can you break it back into simpler fractions?",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Teach the general rule: P(x)/((x−a)(x−b)) = A/(x−a) + B/(x−b). Show the cover-up method and the method of equating coefficients. Ask student to decompose (5x+3)/((x+1)(x+2)).",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Handle repeated factors: P(x)/(x−a)² = A/(x−a) + B/(x−a)². Then irreducible quadratic: P(x)/((x−a)(x²+bx+c)) = A/(x−a) + (Bx+C)/(x²+bx+c). Solve an example of each type.",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Problem: Decompose (3x² + 5x + 2)/((x+1)²(x+2)) into partial fractions. Verify by recombining.",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "BUET-level: Decompose (x⁴ + 1)/(x(x² + 1)²) into partial fractions. Note: check if it is proper first. Then decompose handling the repeated irreducible quadratic factor.",
            },
        ],
        "key_formulas": [
            "P(x)/((x−a)(x−b)) = A/(x−a) + B/(x−b)",
            "P(x)/(x−a)ⁿ = A₁/(x−a) + A₂/(x−a)² + ... + Aₙ/(x−a)ⁿ",
            "For irreducible (ax²+bx+c): numerator is (Ax+B), not just A",
            "If degree(numerator) ≥ degree(denominator), do polynomial long division first",
        ],
        "common_mistakes": [
            "Using A/(x²+1) instead of (Ax+B)/(x²+1) for irreducible quadratic factors",
            "Forgetting to do long division when the fraction is improper (degree of numerator ≥ denominator)",
            "Arithmetic errors when equating coefficients — not checking the answer by recombining fractions",
        ],
        "practice_prompts": [
            "Decompose (2x + 3)/((x − 1)(x + 2)) into partial fractions.",
            "Find the partial fraction form of (x² + 1)/((x − 1)²(x + 1)).",
            "Decompose (x³ + x + 1)/(x²(x² + 1)). Is this proper or improper?",
        ],
        "real_world_example": "Partial fractions are like breaking a mixed curry into its individual spices — you can taste the whole dish, but to understand (or integrate) it, you need to separate each component. This technique is essential for solving differential equations used in circuit analysis at BUET EEE.",
    },

    # ══ HIGHER MATHEMATICS — Chapter 3: জ্যামিতি (Geometry / Coordinate Geometry) ══
    "hm1-03-01": {
        "title": "Straight Lines: Distance & Section Formulas",
        "learning_objectives": [
            "Apply the distance formula between two points in 2D",
            "Use section formula to find internal and external division points",
            "Calculate area of a triangle given three vertices",
            "Determine collinearity of three points using the area method",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: if you are at Motijheel (point A) and your friend is at Uttara (point B), and you know both locations on a grid map, how would you calculate the straight-line distance?",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Derive distance formula d = √((x₂−x₁)² + (y₂−y₁)²) from Pythagoras. Ask: find distance between (3, 4) and (−1, 1). Then teach the section formula for internal division: ((mx₂+nx₁)/(m+n), (my₂+ny₁)/(m+n)).",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Teach external division formula (change + to − in denominator). Then area of triangle with vertices: ½|x₁(y₂−y₃) + x₂(y₃−y₁) + x₃(y₁−y₂)|. Ask: what does area = 0 mean geometrically?",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Problem: A(2, 3), B(8, 11). Find the point dividing AB in ratio 3:1 internally and externally. Then find the midpoint and verify it equals the 1:1 division.",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "BUET-level: Show that points (1, 1), (3, 5), (5, 9) are collinear. Then find the ratio in which (3, 5) divides the line joining (1, 1) and (5, 9). Also find the area of triangle formed by (0, 0), (4, 0), (0, 3).",
            },
        ],
        "key_formulas": [
            "Distance: d = √((x₂−x₁)² + (y₂−y₁)²)",
            "Internal division: P = ((mx₂+nx₁)/(m+n), (my₂+ny₁)/(m+n))",
            "External division: P = ((mx₂−nx₁)/(m−n), (my₂−ny₁)/(m−n))",
            "Area of △ = ½|x₁(y₂−y₃) + x₂(y₃−y₁) + x₃(y₁−y₂)|",
            "Midpoint: M = ((x₁+x₂)/2, (y₁+y₂)/2)",
        ],
        "common_mistakes": [
            "Sign errors in the distance formula — forgetting that squaring eliminates negatives, so order of subtraction does not matter",
            "Mixing up internal and external division — using + in denominator for external division instead of −",
            "Forgetting the absolute value in the area formula, leading to negative area values",
        ],
        "practice_prompts": [
            "Find the distance between (−2, 5) and (4, −3).",
            "The point P(4, m) divides the line joining A(2, 3) and B(6, 7) in the ratio 1:1. Find m.",
            "Prove that the points (2, −2), (8, 4), (5, 7), (−1, 1) form a rhombus by showing all sides are equal.",
        ],
        "real_world_example": "When Bangladesh Survey maps land boundaries, they use coordinate geometry. If a piece of land has corners at known GPS coordinates, the area formula gives the exact plot area — crucial for land registration and disputes that are so common in Bangladesh.",
    },

    "hm1-03-02": {
        "title": "Equations of Straight Lines & Line Properties",
        "learning_objectives": [
            "Write equations of lines in slope-intercept, point-slope, and two-point forms",
            "Find slope, intercepts, and angle between two lines",
            "Calculate perpendicular distance from a point to a line",
            "Determine conditions for parallel and perpendicular lines",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: if a road goes uphill — for every 10 meters horizontally, it rises 3 meters. What is the slope? How would you describe the road's equation if it starts at height 5 meters?",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Teach slope m = (y₂−y₁)/(x₂−x₁). Then three forms: y = mx + c (slope-intercept), y − y₁ = m(x − x₁) (point-slope), (y−y₁)/(y₂−y₁) = (x−x₁)/(x₂−x₁) (two-point). Ask student to convert between forms.",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Teach general form ax + by + c = 0. Conditions: parallel lines have equal slopes (m₁ = m₂), perpendicular lines have m₁ × m₂ = −1. Angle between lines: tan θ = |(m₁−m₂)/(1+m₁m₂)|. Perpendicular distance: d = |ax₁+by₁+c|/√(a²+b²).",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Problem: Find the equation of the line through (3, −2) perpendicular to 2x − 3y + 5 = 0. Then find the distance from origin to this new line.",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "BUET-level: Two lines are 3x + 4y = 12 and 4x − 3y = 6. Find: (a) angle between them, (b) point of intersection, (c) equation of the line through their intersection parallel to x − 2y = 5. Use the family of lines concept: L₁ + λL₂ = 0.",
            },
        ],
        "key_formulas": [
            "Slope: m = (y₂−y₁)/(x₂−x₁) = −a/b (for ax+by+c=0)",
            "Slope-intercept: y = mx + c",
            "Point-slope: y − y₁ = m(x − x₁)",
            "Perpendicular distance: d = |ax₁ + by₁ + c| / √(a² + b²)",
            "Angle between lines: tan θ = |(m₁ − m₂)/(1 + m₁m₂)|",
            "Parallel: m₁ = m₂ | Perpendicular: m₁ × m₂ = −1",
        ],
        "common_mistakes": [
            "Computing slope as (x₂−x₁)/(y₂−y₁) instead of (y₂−y₁)/(x₂−x₁) — swapping numerator and denominator",
            "Forgetting the absolute value in perpendicular distance formula, getting negative distances",
            "For perpendicular lines, using m₁ × m₂ = 1 instead of m₁ × m₂ = −1 (missing the negative sign)",
        ],
        "practice_prompts": [
            "Find the equation of the line passing through (1, 2) and (4, 8) in all three forms.",
            "Find the perpendicular distance from the point (3, 4) to the line 3x + 4y − 5 = 0.",
            "Lines 2x + 3y = 6 and 4x + 6y = k are parallel. For what value of k is the distance between them equal to 1?",
        ],
        "real_world_example": "When BUET civil engineers design roads in Dhaka, they calculate slopes for drainage — water must flow at a minimum gradient. The perpendicular distance formula helps determine how far a building is from the road centerline, essential for setback rules in RAJUK building codes.",
    },

    # ══════════════════════════════════════════════════════════════
    # ══ BIOLOGY — Chapter 1: কোষ ও এর গঠন (Cell & Its Structure) ══
    # ══════════════════════════════════════════════════════════════

    "bio1-01-01": {
        "title": "Prokaryotic vs Eukaryotic Cells & Cell Theory",
        "learning_objectives": [
            "Compare structural differences between prokaryotic and eukaryotic cells",
            "Explain the cell theory and contributions of Schleiden, Schwann, and Virchow",
            "Identify membrane-bound organelles present only in eukaryotes",
            "Classify organisms (bacteria, cyanobacteria, fungi, protists, plants, animals) as prokaryotic or eukaryotic",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Start by asking: what do you think is the smallest living unit? Can something alive exist without a cell? Relate to bacteria in curd (doi) we eat every day.",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Explain the 3 postulates of cell theory. Ask: which scientist said 'Omnis cellula e cellula'? Then introduce the key differences — prokaryotes lack a true nucleus and membrane-bound organelles. Ask student to name 2 examples of prokaryotes.",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Compare prokaryotic and eukaryotic cells systematically: nucleus (nucleoid vs true nucleus), ribosomes (70S vs 80S), DNA (circular vs linear), cell wall composition (peptidoglycan vs cellulose/chitin), membrane-bound organelles. Draw a comparison table with the student.",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Give a classification exercise: classify these as prokaryotic or eukaryotic — E. coli, Amoeba, Nostoc (cyanobacteria), mushroom, rice plant cell, Plasmodium (malaria parasite). Ask which of these are relevant to Bangladesh (Nostoc in rice paddies, Plasmodium causing malaria).",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "Medical admission level MCQ: 'Which of the following is found in both prokaryotic and eukaryotic cells? (a) Mitochondria (b) Endoplasmic reticulum (c) Ribosome (d) Golgi body.' Follow up with: why do prokaryotes have 70S ribosomes while eukaryotes have 80S? What is the medical significance of this difference (hint: antibiotics)?",
            },
        ],
        "key_formulas": [
            "Prokaryotic ribosome: 70S (50S + 30S subunits)",
            "Eukaryotic ribosome: 80S (60S + 40S subunits)",
            "Prokaryotic DNA: single circular chromosome + plasmids",
            "Eukaryotic DNA: multiple linear chromosomes with histones",
            "Cell theory: all living things are made of cells; cell is the basic unit of life; cells arise from pre-existing cells",
        ],
        "common_mistakes": [
            "Thinking all bacteria are harmful — many are beneficial (e.g., Lactobacillus in doi/yogurt, nitrogen-fixing bacteria in rice paddies)",
            "Confusing 70S and 80S ribosome subunit values — students add 50+30=80 and think prokaryotes have 80S (Svedberg units are not additive)",
            "Forgetting that prokaryotes CAN have cell walls (peptidoglycan) — students wrongly think only plant cells have walls",
        ],
        "practice_prompts": [
            "A cell has no nuclear membrane, has 70S ribosomes, and a circular DNA. Identify the cell type and give two examples of organisms with this cell type.",
            "Explain why antibiotics like streptomycin target 70S ribosomes but do not harm human cells. What is the clinical significance?",
            "Compare the genetic material organization in E. coli and a human cheek cell. Include at least 4 differences.",
        ],
        "real_world_example": "The doi (yogurt) you eat with rice is made by Lactobacillus — a prokaryote! It converts lactose in milk to lactic acid. Meanwhile, the rice grain itself came from a eukaryotic plant cell. So in one meal of bhat-doi, you are eating products of both prokaryotic and eukaryotic life.",
    },

    "bio1-01-02": {
        "title": "Cell Organelles & Plant vs Animal Cells",
        "learning_objectives": [
            "Describe the structure and function of each major cell organelle (nucleus, mitochondria, ER, Golgi, ribosome, lysosome, chloroplast, vacuole)",
            "Explain the fluid mosaic model of cell membrane (Singer-Nicolson model)",
            "Compare plant and animal cells with at least 5 structural differences",
            "Relate organelle dysfunction to diseases (e.g., lysosomal storage diseases, mitochondrial disorders)",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: if a cell is like a factory, what would be the manager's office? The power plant? The packaging department? The waste disposal unit? Let the student guess before revealing organelle functions.",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Teach the fluid mosaic model of cell membrane — phospholipid bilayer with embedded proteins, cholesterol for fluidity, glycoproteins for recognition. Ask: why is it called 'fluid' mosaic? What makes the membrane selectively permeable?",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Go through each organelle systematically: Nucleus (double membrane, nucleolus, chromatin), Mitochondria (powerhouse, double membrane, own DNA — endosymbiotic theory), ER (rough with ribosomes for protein synthesis, smooth for lipid synthesis), Golgi (packaging & secretion, cis and trans face), Lysosome (digestive enzymes, pH 4.5-5), Chloroplast (photosynthesis, thylakoid grana, stroma). Ask after each: what happens to the cell if this organelle stops working?",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Create a comparison table: Plant cell vs Animal cell. Key differences — cell wall (present/absent), chloroplast, central vacuole (large in plant), centrioles (present in animal), lysosomes (prominent in animal), shape (fixed rectangular vs irregular). Ask: why do plant cells not need lysosomes as much as animal cells?",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "Medical admission MCQ: 'Which organelle is called the suicide bag of the cell? (a) Ribosome (b) Lysosome (c) Peroxisome (d) Glyoxysome.' Follow up: 'A cell is actively secreting proteins. Which organelles would show increased activity? List them in order of the secretory pathway.' (Answer: Nucleus -> Rough ER -> Golgi -> Cell membrane)",
            },
        ],
        "key_formulas": [
            "Cell membrane: phospholipid bilayer + integral/peripheral proteins + cholesterol + glycocalyx",
            "Mitochondria: outer membrane + inner membrane (cristae) + matrix — site of ATP synthesis via oxidative phosphorylation",
            "Chloroplast: outer membrane + inner membrane + thylakoid (grana + stroma lamellae) + stroma — site of photosynthesis",
            "Protein secretory pathway: Ribosome -> Rough ER -> Transport vesicle -> Golgi (cis to trans) -> Secretory vesicle -> Cell membrane",
            "Endosymbiotic theory: mitochondria and chloroplasts were once free-living prokaryotes (have own 70S ribosomes and circular DNA)",
        ],
        "common_mistakes": [
            "Confusing rough ER and smooth ER functions — rough ER has ribosomes for protein synthesis, smooth ER synthesizes lipids and detoxifies drugs (students mix these up)",
            "Thinking mitochondria are only in animal cells — both plant AND animal cells have mitochondria (plants need cellular respiration too!)",
            "Confusing centrioles with centromeres — centrioles are organelles for spindle formation (absent in most plant cells), centromeres are regions on chromosomes",
        ],
        "practice_prompts": [
            "Trace the path of a secretory protein from its synthesis to its release outside the cell. Name every organelle involved in order.",
            "A plant cell and an animal cell are both placed in a hypotonic solution. Predict what happens to each and explain why their fates differ.",
            "Explain the endosymbiotic theory of mitochondrial origin. Give 3 pieces of evidence that support this theory.",
        ],
        "real_world_example": "Think of a paat (jute) fiber cell — it has an extremely thick cell wall made of cellulose, which gives jute its strength for making rope and bags. The cell wall is why plants can stand upright without bones. A mango leaf cell has abundant chloroplasts for photosynthesis, while root cells of the same mango tree have no chloroplasts but many mitochondria for energy to absorb water and minerals.",
    },

    # ══════════════════════════════════════════════════════════════
    # ══ BIOLOGY — Chapter 2: কোষ বিভাজন (Cell Division) ══
    # ══════════════════════════════════════════════════════════════

    "bio1-02-01": {
        "title": "Mitosis — Stages and Significance",
        "learning_objectives": [
            "Describe each phase of the cell cycle (G1, S, G2, M) with duration and events",
            "Explain the 4 stages of mitosis (prophase, metaphase, anaphase, telophase) with key events in each",
            "Differentiate cytokinesis in plant cells (cell plate) vs animal cells (cleavage furrow)",
            "Explain the significance of mitosis in growth, repair, and asexual reproduction",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: when you cut your finger, how does the wound heal? Where do new skin cells come from? When a rice seedling grows from a small shoot to a full plant, where are the new cells coming from?",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Teach the cell cycle: Interphase (G1 — cell growth, protein synthesis; S — DNA replication, chromosome number unchanged but DNA doubles; G2 — preparation for division) and M phase (mitosis + cytokinesis). Ask: a human cell has 46 chromosomes. After S phase, how many chromosomes does it have? (Still 46, but each has 2 chromatids — students often say 92 here!)",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Walk through mitosis step by step: Prophase (chromatin condenses, nucleolus disappears, spindle forms), Metaphase (chromosomes align at metaphase plate, spindle fibers attach to kinetochore), Anaphase (centromeres split, sister chromatids pulled to poles — shortest phase), Telophase (nuclear envelope reforms, chromosomes decondense). Use mnemonic PMAT. Ask student to identify the phase from descriptions.",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Ask: what is different about cytokinesis in plant cells vs animal cells? (Cell plate vs cleavage furrow). Then: a cell with 2n=14 undergoes mitosis. How many chromosomes in each daughter cell? How many daughter cells are produced? Are they genetically identical to the parent?",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "Medical admission MCQ: 'During which phase of mitosis do chromosomes first become visible under a light microscope? (a) Interphase (b) Prophase (c) Metaphase (d) Anaphase.' Follow up: 'Why is uncontrolled mitosis dangerous? How does this relate to cancer?' Ask about the role of checkpoints (G1, G2, M checkpoints) in preventing cancer.",
            },
        ],
        "key_formulas": [
            "Cell cycle: G1 -> S -> G2 -> M (Prophase -> Metaphase -> Anaphase -> Telophase -> Cytokinesis)",
            "Mitosis: 1 parent cell (2n) -> 2 daughter cells (2n) — genetically identical",
            "After S phase: chromosome count unchanged, but each chromosome has 2 sister chromatids (DNA content doubles: 2C -> 4C)",
            "Shortest phase: Anaphase; Longest phase of mitosis: Prophase; Longest phase of cell cycle: Interphase (especially S phase)",
            "Cytokinesis: animal cells — cleavage furrow (actin-myosin ring); plant cells — cell plate (vesicles from Golgi)",
        ],
        "common_mistakes": [
            "Saying chromosome number doubles after S phase — it does NOT; each chromosome becomes 2 sister chromatids joined at centromere, but chromosome count stays the same (2n). DNA content doubles, not chromosome number.",
            "Confusing the order of mitosis phases or mixing up events — e.g., thinking chromosomes align at metaphase plate during prophase, or thinking nuclear envelope breaks in metaphase (it breaks in late prophase/prometaphase)",
            "Forgetting that cytokinesis is NOT part of mitosis itself — mitosis is nuclear division only; cytokinesis is cytoplasmic division and can be separated",
        ],
        "practice_prompts": [
            "A cell with 2n=24 is undergoing mitosis. State the chromosome number and DNA content (in terms of C) at: (i) G1 phase, (ii) after S phase, (iii) metaphase, (iv) each daughter cell after division.",
            "A student observing onion root tip cells under a microscope sees most cells in interphase and very few in anaphase. Explain why.",
            "How is cancer related to failure of cell cycle regulation? Name the phases where checkpoints occur and what each checkpoint monitors.",
        ],
        "real_world_example": "When you plant a dhan (rice) seed, it germinates and grows into a full plant with thousands of cells — all produced by mitosis from that one original seed cell. The meristematic tissue at the root tip and shoot tip is where mitosis is most active. That is why when you look at onion root tip slides in your HSC practical, you see so many dividing cells!",
    },

    "bio1-02-02": {
        "title": "Meiosis — Stages, Crossing Over & Significance",
        "learning_objectives": [
            "Describe the stages of meiosis I (especially prophase I sub-stages) and meiosis II",
            "Explain crossing over, synapsis, and chiasmata formation during prophase I",
            "Compare mitosis and meiosis with at least 6 key differences",
            "Explain the biological significance of meiosis — genetic variation, maintaining chromosome number across generations",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: why don't you look exactly like your siblings even though you have the same parents? If gametes were produced by mitosis, what would happen to chromosome number each generation? (It would double! 46 -> 92 -> 184...) This is why meiosis is essential.",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Explain meiosis I as the reductional division: homologous chromosomes pair (synapsis), form bivalents/tetrads, crossing over occurs at chiasmata. Teach prophase I sub-stages using mnemonic LZPDD: Leptotene (thin threads), Zygotene (synapsis begins), Pachytene (crossing over — thickest chromosomes), Diplotene (chiasmata visible, separation begins), Diakinesis (terminalization of chiasmata). Ask: at which sub-stage does genetic recombination actually occur?",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Complete meiosis I (metaphase I — bivalents align, independent assortment; anaphase I — homologous chromosomes separate; telophase I — two haploid cells). Then teach meiosis II — similar to mitosis but starts with haploid cells. End result: 4 haploid cells. Compare: in males all 4 become sperm; in females only 1 becomes ovum (other 3 are polar bodies). Ask: why is meiosis I called reductional and meiosis II called equational?",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Comparison exercise: make a table comparing mitosis vs meiosis on: number of divisions, number of daughter cells, chromosome number in daughters, genetic variation, where it occurs, crossing over (yes/no), synapsis (yes/no). Then ask: a cell with 2n=46 undergoes meiosis. What is the chromosome number after meiosis I? After meiosis II?",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "Medical admission MCQ: 'Crossing over occurs between: (a) sister chromatids (b) non-sister chromatids of homologous chromosomes (c) non-homologous chromosomes (d) any two chromatids.' Follow up: 'Explain how both crossing over AND independent assortment contribute to genetic variation. Calculate: with n=23 chromosomes, how many possible gamete combinations from independent assortment alone?' (2^23 = 8,388,608)",
            },
        ],
        "key_formulas": [
            "Meiosis: 1 parent cell (2n) -> 4 daughter cells (n) — genetically different",
            "Prophase I sub-stages: Leptotene -> Zygotene -> Pachytene -> Diplotene -> Diakinesis (LZPDD)",
            "Crossing over: exchange of genetic material between non-sister chromatids of homologous chromosomes at chiasmata",
            "Independent assortment: possible combinations = 2^n (where n = haploid chromosome number)",
            "Human: 2n=46, so n=23; after meiosis I: 23 chromosomes per cell; after meiosis II: 23 chromosomes per cell (but single chromatids)",
        ],
        "common_mistakes": [
            "Confusing crossing over between sister chromatids (does not produce variation) with crossing over between non-sister chromatids of homologous chromosomes (produces genetic recombination)",
            "Mixing up meiosis I and meiosis II — students forget that homologous chromosomes separate in meiosis I (reductional) while sister chromatids separate in meiosis II (equational, like mitosis)",
            "Forgetting the sub-stages of prophase I — this is a very common Medical admission question; LZPDD mnemonic is essential and students often mix up the order or events of Pachytene vs Diplotene",
        ],
        "practice_prompts": [
            "A cell with 2n=8 undergoes meiosis. Draw or describe the chromosome arrangement at: (i) metaphase I, (ii) anaphase I, (iii) metaphase II, (iv) anaphase II. State chromosome count at each stage.",
            "Explain why meiosis is called the basis of sexual reproduction. What would happen to a species if meiosis did not occur but sexual reproduction continued?",
            "During oogenesis in a human female, one primary oocyte produces how many functional ova? Explain the formation of polar bodies and their fate.",
        ],
        "real_world_example": "Think about Bangladeshi rice varieties — BRRI has developed over 100 dhan varieties (BRRI dhan28, BRRI dhan29, etc.) by cross-breeding. This works because meiosis creates genetic variation through crossing over and independent assortment. Each rice grain from a cross is genetically unique, letting breeders select for flood resistance, salt tolerance, or higher yield — all crucial for Bangladesh's food security.",
    },

    # ══════════════════════════════════════════════════════════════
    # ══ BIOLOGY — Chapter 3: কোষ রসায়ন (Cell Chemistry / Biochemistry) ══
    # ══════════════════════════════════════════════════════════════

    "bio1-03-01": {
        "title": "Carbohydrates, Lipids & Proteins — Structure and Function",
        "learning_objectives": [
            "Classify carbohydrates into monosaccharides, disaccharides, and polysaccharides with examples and bonding",
            "Describe the structure of lipids — triglycerides, phospholipids, and steroids — and distinguish saturated from unsaturated fatty acids",
            "Explain protein structure at all 4 levels (primary, secondary, tertiary, quaternary) and the role of peptide bonds",
            "Relate the structure of each biomolecule to its biological function",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: what did you eat for breakfast? Probably bhat (rice), dal (lentils), and maybe an egg or fish. Which one gives you energy quickly? Which builds your muscles? Which is stored as fat? Connect food to biomolecules — carbohydrates, proteins, lipids.",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Teach carbohydrates: general formula Cn(H2O)n. Monosaccharides (glucose, fructose, galactose — all C6H12O6 but different structures), Disaccharides (sucrose = glucose + fructose via glycosidic bond; maltose = glucose + glucose; lactose = glucose + galactose), Polysaccharides (starch — plant storage in rice/potato; glycogen — animal storage in liver/muscle; cellulose — structural in plant cell wall; chitin — in insect exoskeleton/fungal wall). Ask: why can humans digest starch but not cellulose, even though both are made of glucose?",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Teach lipids: triglyceride = glycerol + 3 fatty acids via ester bonds. Saturated (no double bonds, solid at room temperature — ghee, butter) vs unsaturated (double bonds, liquid — soyabean oil, mustard oil/sorsher tel). Phospholipids: glycerol + 2 fatty acids + phosphate group — amphipathic, forms cell membrane bilayer. Then teach proteins: amino acids joined by peptide bonds (CO-NH). 4 levels of structure: primary (sequence), secondary (alpha-helix, beta-sheet via H-bonds), tertiary (3D folding via disulfide bonds, hydrophobic interactions), quaternary (multiple polypeptides, e.g., hemoglobin has 4 subunits). Ask: what level of protein structure is disrupted when you boil an egg?",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Identification exercise: classify these as carbohydrate, lipid, or protein — hemoglobin, cellulose, cholesterol, insulin, starch, phospholipid, glycogen, keratin, chitin, triglyceride. Then ask: which bond links (a) two amino acids, (b) two monosaccharides, (c) glycerol and fatty acid? (peptide bond, glycosidic bond, ester bond)",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "Medical admission MCQ: 'Which of the following is a reducing sugar? (a) Sucrose (b) Starch (c) Maltose (d) Cellulose.' Follow up: 'Sickle cell anemia is caused by a change in which level of protein structure? Explain how a single amino acid substitution (Glu -> Val) in hemoglobin leads to the disease.' This tests understanding of how primary structure determines all higher levels.",
            },
        ],
        "key_formulas": [
            "General formula of carbohydrates: Cn(H2O)n — e.g., glucose C6H12O6",
            "Sucrose = glucose + fructose (non-reducing sugar, 1-2 glycosidic bond)",
            "Maltose = glucose + glucose (reducing sugar, 1-4 glycosidic bond)",
            "Starch: amylose (unbranched, 1-4 bonds) + amylopectin (branched, 1-4 and 1-6 bonds)",
            "Triglyceride = glycerol + 3 fatty acids (ester bonds, via condensation/dehydration reaction)",
            "Peptide bond: -CO-NH- bond between carboxyl of one amino acid and amino group of another (with release of H2O)",
            "Protein levels: primary (peptide bonds) -> secondary (H-bonds) -> tertiary (disulfide, ionic, hydrophobic) -> quaternary (multiple polypeptides)",
        ],
        "common_mistakes": [
            "Thinking sucrose is a reducing sugar — it is NOT because the glycosidic bond involves the anomeric carbons of BOTH glucose and fructose, leaving no free aldehyde/ketone group. Maltose and lactose ARE reducing sugars.",
            "Confusing starch and cellulose — both are polymers of glucose but starch has alpha-1,4 glycosidic bonds (digestible by humans) while cellulose has beta-1,4 bonds (indigestible by humans, requires cellulase enzyme found in ruminants and termites)",
            "Mixing up the 4 levels of protein structure — especially confusing secondary (local H-bonding: alpha-helix, beta-sheet) with tertiary (overall 3D shape from R-group interactions: disulfide bonds, hydrophobic interactions, ionic bonds)",
        ],
        "practice_prompts": [
            "Compare starch, glycogen, and cellulose in terms of: monomer, type of glycosidic bond, branching, biological function, and which organisms use them for what purpose.",
            "Explain why phospholipids spontaneously form bilayers in water. How does this property relate to cell membrane formation? What role does cholesterol play in the membrane?",
            "A patient has sickle cell disease. Explain the molecular basis at each level of hemoglobin structure — from the DNA mutation to the final effect on red blood cell shape and oxygen transport.",
        ],
        "real_world_example": "Your bhat (rice) is mostly starch — a polysaccharide that your amylase enzyme breaks into glucose for energy. The mach (fish) you eat with rice provides protein — amino acids for building muscle. The sorsher tel (mustard oil) your mother cooks with is a lipid — triglycerides with unsaturated fatty acids. Even the paan (betel leaf) you might see elders chewing has cellulose cell walls your body cannot digest. Every Bangladeshi meal is a biochemistry lesson!",
    },

    "bio1-03-02": {
        "title": "Nucleic Acids (DNA & RNA) and Enzymes",
        "learning_objectives": [
            "Describe the structure of DNA (double helix model of Watson & Crick) and RNA with their chemical components",
            "Explain base pairing rules (A-T with 2 H-bonds, G-C with 3 H-bonds) and Chargaff's rules",
            "Compare DNA and RNA in terms of sugar, bases, structure, location, and function",
            "Explain enzyme action using lock-and-key and induced fit models, including factors affecting enzyme activity",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: what carries the instructions to build your entire body? How does a single fertilized egg know how to become a complete human with eyes, heart, and brain? This is the role of DNA — the blueprint of life. Then ask: have you heard of DNA testing in crime investigation or paternity tests?",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Teach nucleotide structure: phosphate + sugar (deoxyribose in DNA, ribose in RNA) + nitrogenous base. Purines: Adenine (A) and Guanine (G) — double ring. Pyrimidines: Cytosine (C), Thymine (T in DNA), Uracil (U in RNA) — single ring. Mnemonic: PURe As Gold (purines = A, G). Teach Chargaff's rules: A=T, G=C, so A+G = T+C (purines = pyrimidines). Ask: if a DNA strand has 30% adenine, what percentage of guanine does it have?",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Describe the Watson-Crick double helix model: two antiparallel polynucleotide strands (5'->3' and 3'->5'), sugar-phosphate backbone on outside, bases inside paired by H-bonds (A=T with 2 H-bonds, G-C with 3 H-bonds), one complete turn = 3.4 nm with 10 base pairs, distance between base pairs = 0.34 nm, diameter = 2 nm. Then compare DNA vs RNA in a table (5 differences minimum). Then teach enzymes: biological catalysts (mostly proteins), lock-and-key model vs induced fit model, active site, substrate specificity. Factors: temperature, pH, substrate concentration, enzyme concentration, inhibitors (competitive vs non-competitive).",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Problem: A DNA sample has 20% cytosine. Calculate the percentages of all 4 bases. (C=20%, G=20%, A=30%, T=30%). Then: if one strand of DNA has the sequence 5'-ATGCCGTA-3', write the complementary strand with correct polarity. For enzymes: explain why pepsin works in the stomach (pH 2) but trypsin works in the intestine (pH 8). What happens to pepsin at pH 8?",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "Medical admission MCQ: 'Which of the following is TRUE about DNA? (a) It contains ribose sugar (b) A-T base pair has 3 hydrogen bonds (c) The two strands run in the same direction (d) One complete turn has 10 base pairs.' Follow up: 'A DNA molecule has 1000 base pairs. If 200 of them are adenine-thymine pairs, how many hydrogen bonds are in this DNA? (200 A-T pairs x 2 = 400, plus 800 G-C pairs x 3 = 2400, total = 2800 H-bonds).' For enzymes: 'Explain competitive inhibition with a medical example — how do sulfa drugs work as antibiotics?'",
            },
        ],
        "key_formulas": [
            "Nucleotide = phosphate group + pentose sugar + nitrogenous base",
            "Chargaff's rule: A = T, G = C; therefore %A + %G = %T + %C = 50%",
            "DNA double helix: 1 turn = 3.4 nm = 10 base pairs; distance between base pairs = 0.34 nm; diameter = 2 nm",
            "H-bonds: A=T (2 hydrogen bonds), G-C (3 hydrogen bonds) — GC-rich DNA is more thermally stable",
            "Total H-bonds in DNA = (2 x number of A-T pairs) + (3 x number of G-C pairs)",
            "Types of RNA: mRNA (carries genetic message), tRNA (carries amino acids, has anticodon), rRNA (structural component of ribosomes)",
            "Enzyme kinetics: Vmax = maximum rate at substrate saturation; Km = substrate concentration at half Vmax (Michaelis-Menten)",
        ],
        "common_mistakes": [
            "Applying Chargaff's rule to single-stranded RNA — Chargaff's rule (A=T, G=C) applies ONLY to double-stranded DNA, NOT to single-stranded RNA where A does not necessarily equal U",
            "Confusing the number of hydrogen bonds — A-T has 2 H-bonds (not 3) and G-C has 3 H-bonds (not 2); students frequently reverse these. Remember: C and G are 'stronger' (3 bonds) so GC-rich DNA needs higher temperature to denature",
            "Thinking enzymes are consumed in reactions — enzymes are catalysts that are NOT used up; they lower activation energy and are recycled. Also confusing competitive inhibition (blocks active site, overcome by more substrate) with non-competitive inhibition (binds allosteric site, cannot be overcome by more substrate)",
        ],
        "practice_prompts": [
            "A double-stranded DNA molecule has 1500 base pairs. If adenine constitutes 35% of total bases, calculate: (i) percentage of each base, (ii) number of each type of base pair, (iii) total number of hydrogen bonds in this DNA molecule.",
            "Compare DNA and RNA in a table with at least 6 differences covering: sugar type, bases, number of strands, location in cell, stability, and function.",
            "Explain with a diagram how a competitive inhibitor differs from a non-competitive inhibitor. Give a medical/pharmacological example of each type. Why can competitive inhibition be reversed by increasing substrate concentration but non-competitive cannot?",
        ],
        "real_world_example": "Forensic DNA testing is now used in Bangladeshi courts for paternity disputes and criminal cases. The technique works because everyone's DNA base sequence is unique (except identical twins). Enzymes are everywhere in daily life too — the papain enzyme in raw kacha papaya (pepe) tenderizes meat, which is why Bangladeshi cooks add papaya paste to tough beef before cooking. Your saliva contains amylase enzyme that starts digesting the starch in bhat right in your mouth — try chewing plain rice for 30 seconds and it starts tasting sweet as starch breaks into maltose!",
    },

    # ══ PHYSICS — Chapters 4-10 ══
    "phy1-02-02": {
        "title": "Scalar & Vector Products",
        "learning_objectives": [
                "Calculate dot product and find angle between vectors",
                "Calculate cross product and find area of parallelogram",
                "Apply scalar product in work calculations",
                "Apply vector product in torque calculations"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: when you push a box at an angle, not all your force moves it forward. How do we calculate the useful part of the force?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Teach dot product: A·B = AB cos θ (scalar result). Ask: what is the dot product when vectors are perpendicular?"
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Teach cross product: A×B = AB sin θ n̂ (vector result). Explain right-hand rule. Ask: what is cross product when vectors are parallel?"
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "Find dot product of A=(3,4) and B=(2,-1). Then find the angle between them."
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ: if A×B = 0 and A·B = AB, what is the angle between A and B?"
                }
        ],
        "key_formulas": [
                "A·B = AB cos θ = a₁b₁ + a₂b₂ + a₃b₃",
                "A×B = AB sin θ n̂",
                "|A×B| = area of parallelogram"
        ],
        "common_mistakes": [
                "Confusing dot product (scalar) with cross product (vector)",
                "Wrong sign in cross product (not commutative: A×B = -B×A)",
                "Forgetting that perpendicular vectors have zero dot product"
        ],
        "practice_prompts": [
                "If A=(1,2,3) and B=(4,-1,2), find A·B",
                "Two forces 5N and 8N act at 60°. Find A×B magnitude."
        ],
        "real_world_example": "When you pull a rickshaw with a rope at an angle, only the horizontal component (F cos θ) moves it forward — that's the dot product of force and displacement giving you work done."
},

    "phy1-04-01": {
        "title": "Newton's Laws of Motion",
        "learning_objectives": [
                "State and apply all three Newton's laws",
                "Draw free body diagrams for complex systems",
                "Solve problems with connected bodies",
                "Apply Newton's laws to lift/elevator problems"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: why does your body jerk forward when a bus suddenly stops? Which Newton's law explains this?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Teach all 3 laws with examples. 1st: inertia (bus example). 2nd: F=ma (pushing cart). 3rd: action-reaction (walking). Ask student to identify which law applies in each scenario."
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Teach free body diagrams. Draw FBD for a block on an incline. Identify normal force, weight components, friction. Solve for acceleration."
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "Two blocks (3kg and 5kg) connected by string on frictionless surface. Force 40N applied on 5kg block. Find acceleration and tension."
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "Elevator problem: a 60kg person in a lift accelerating upward at 2 m/s². What does the scale read? BUET-level."
                }
        ],
        "key_formulas": [
                "F = ma",
                "Weight W = mg",
                "Apparent weight in lift: N = m(g ± a)",
                "Connected bodies: same acceleration, tension is internal force"
        ],
        "common_mistakes": [
                "Confusing mass and weight",
                "Forgetting that action-reaction forces act on DIFFERENT bodies",
                "Not resolving forces into components on inclined planes"
        ],
        "practice_prompts": [
                "A 10kg box on a smooth surface is pushed with 50N. Find acceleration.",
                "In a lift going up with acceleration 3 m/s², what is the apparent weight of a 50kg person?"
        ],
        "real_world_example": "When a CNG auto-rickshaw suddenly brakes, you slide forward — that's Newton's 1st law. The harder the driver brakes (more force), the faster you decelerate (2nd law). Your feet push backward on the floor, floor pushes you forward (3rd law)."
},

    "phy1-04-02": {
        "title": "Friction & Circular Motion",
        "learning_objectives": [
                "Calculate static and kinetic friction",
                "Solve problems on banked roads and circular motion",
                "Apply centripetal force concept",
                "Understand the role of friction in daily life"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: why is it easier to push a box once it starts moving than to start pushing it? What's the difference between static and kinetic friction?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Teach f = μN. Static friction ≤ μₛN, kinetic friction = μₖN. Ask: why is μₛ > μₖ always?"
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Circular motion: centripetal force F = mv²/r. For car on banked road: tan θ = v²/rg. Derive step by step."
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "A car turns on a flat road (μ=0.4, r=50m). Find maximum safe speed. Then: what if the road is banked at 30°?"
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ about friction on incline or centripetal force in vertical circular motion."
                }
        ],
        "key_formulas": [
                "f = μN",
                "Centripetal force F = mv²/r",
                "Banked road: tan θ = v²/rg",
                "Min speed at top of loop: v = √(rg)"
        ],
        "common_mistakes": [
                "Using μmg for friction on incline (should be μN = μmg cos θ)",
                "Confusing centripetal (real) with centrifugal (pseudo) force",
                "Forgetting that static friction has a maximum value, not a fixed value"
        ],
        "practice_prompts": [
                "A 5kg block on a surface with μ=0.3. Find friction when 10N horizontal force applied.",
                "Find the banking angle for a road curve (r=100m) at speed 72 km/h."
        ],
        "real_world_example": "The flyover curves in Dhaka are slightly banked — the road tilts inward so cars don't need to rely only on tire friction. Same reason why cricket bowlers can make the ball curve — friction and circular motion!"
},

    "phy1-05-01": {
        "title": "Work & Energy",
        "learning_objectives": [
                "Calculate work done by constant and variable forces",
                "Apply work-energy theorem",
                "Understand potential and kinetic energy",
                "Apply conservation of energy to solve problems"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: if you carry a heavy bag horizontally across a room, have you done any work on it (in physics terms)? Why or why not?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Teach W = Fd cos θ. When θ=90°, W=0 (carrying bag horizontally). KE = ½mv², PE = mgh. Ask: what type of energy does a flying bird have?"
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Work-energy theorem: net work = change in KE. Solve: a 2kg ball falls from 10m. Find velocity just before hitting ground using energy conservation."
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "A 1000kg car accelerates from 10 m/s to 30 m/s. Find the work done by the engine."
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ: a pendulum released from height h. Find velocity at lowest point. Then: if string is cut at lowest point, what path does it follow?"
                }
        ],
        "key_formulas": [
                "W = Fd cos θ",
                "KE = ½mv²",
                "PE = mgh",
                "Conservation: KE₁ + PE₁ = KE₂ + PE₂"
        ],
        "common_mistakes": [
                "Saying you do work when carrying a bag horizontally (W=0 since F⊥d)",
                "Forgetting that work can be negative (friction does negative work)",
                "Not using energy conservation when it's simpler than force equations"
        ],
        "practice_prompts": [
                "A 50kg boy climbs 10m stairs. How much work against gravity?",
                "A spring (k=200 N/m) compressed 0.1m. Find stored PE."
        ],
        "real_world_example": "When water falls at Kaptai Dam from height h, its PE converts to KE, which spins turbines to generate electricity. The higher the dam, the more energy — that's why Kaptai was built in the hills of Rangamati."
},

    "phy1-05-02": {
        "title": "Power & Collisions",
        "learning_objectives": [
                "Calculate power as rate of work done",
                "Distinguish elastic and inelastic collisions",
                "Apply momentum conservation in collisions",
                "Solve problems involving coefficient of restitution"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: two people carry the same weight up stairs — one takes 1 minute, the other takes 5 minutes. Who does more work? Who has more power?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Power P = W/t = Fv. 1 HP = 746 W. Teach elastic (KE conserved) vs inelastic (KE not conserved) collisions."
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Collision formulas: m₁u₁ + m₂u₂ = m₁v₁ + m₂v₂. For perfectly inelastic: bodies stick together. Solve: 2kg ball at 3m/s hits stationary 1kg ball elastically."
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "A 1500kg car at 20 m/s collides with stationary 1000kg car. They stick together. Find final velocity and energy lost."
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ about collision or power calculation."
                }
        ],
        "key_formulas": [
                "P = W/t = Fv",
                "1 HP = 746 W",
                "Coefficient of restitution e = (v₂-v₁)/(u₁-u₂)",
                "Elastic: e=1, Perfectly inelastic: e=0"
        ],
        "common_mistakes": [
                "Confusing work (same for both) with power (different if time differs)",
                "Thinking momentum is not conserved in inelastic collisions (it IS, only KE isn't)",
                "Forgetting that in 2D collisions, momentum is conserved in each direction separately"
        ],
        "practice_prompts": [
                "A pump lifts 500kg water to 10m in 5 seconds. Find power in watts and HP.",
                "Two identical balls collide elastically head-on. What happens?"
        ],
        "real_world_example": "When a truck hits a small car, both have the same momentum change (Newton's 3rd law) — but the small car gets much more acceleration because F=ma and its mass is less. That's why trucks cause more damage in accidents on the Dhaka-Chittagong highway."
},

    "phy1-06-01": {
        "title": "Gravitation",
        "learning_objectives": [
                "Apply Newton's law of gravitation",
                "Calculate gravitational field strength at different altitudes",
                "Derive orbital velocity and escape velocity",
                "Apply Kepler's laws of planetary motion"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: why does the Moon orbit the Earth instead of flying away? What force keeps it in orbit?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Teach F = GMm/r². Surface gravity g = GM/R². Ask: what happens to g if you go to a mountain top? What about deep inside Earth?"
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Derive orbital velocity v = √(GM/r) and escape velocity vₑ = √(2GM/R) = √(2gR). Ask: why is escape velocity √2 times orbital velocity?"
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "Calculate g at height equal to Earth's radius. Then: find escape velocity from Earth (R=6400km, g=9.8)."
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ about satellite period or variation of g with altitude/depth."
                }
        ],
        "key_formulas": [
                "F = GMm/r²",
                "g = GM/R²",
                "Orbital velocity v₀ = √(GM/r)",
                "Escape velocity vₑ = √(2gR)",
                "Kepler's T² ∝ r³"
        ],
        "common_mistakes": [
                "Using r (distance from center) vs h (height above surface) — g at height h: g'=g(R/(R+h))²",
                "Forgetting that inside Earth, g decreases linearly with depth",
                "Confusing orbital velocity with escape velocity"
        ],
        "practice_prompts": [
                "At what height above Earth is g reduced to g/4?",
                "Find the time period of a satellite orbiting just above Earth's surface."
        ],
        "real_world_example": "Bangladesh's Bangabandhu-1 satellite orbits at 35,786 km (geostationary orbit) — at that height, it takes exactly 24 hours to orbit, so it stays over the same spot above Bangladesh. That's Kepler's third law in action!"
},

    "phy1-07-01": {
        "title": "Elasticity & Fluid Mechanics",
        "learning_objectives": [
                "Define stress, strain, and Young's modulus",
                "Apply Hooke's law within elastic limit",
                "Apply Pascal's law and Archimedes' principle",
                "Use Bernoulli's equation for fluid flow"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: why does a rubber band return to its original shape but clay doesn't? What's the difference?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Teach stress = F/A, strain = ΔL/L, Young's modulus Y = stress/strain. Hooke's law: F = kx. Ask: what happens beyond the elastic limit?"
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Fluid statics: Pascal's law (hydraulic press), Archimedes' principle (buoyancy). Bernoulli's: P + ½ρv² + ρgh = constant."
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "A steel wire (Y=2×10¹¹ Pa, L=2m, A=1mm²) stretched by 100N. Find extension."
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ about buoyancy or Bernoulli's application."
                }
        ],
        "key_formulas": [
                "Stress = F/A, Strain = ΔL/L",
                "Young's modulus Y = Stress/Strain",
                "Pascal's law: pressure transmitted equally",
                "Bernoulli: P + ½ρv² + ρgh = constant"
        ],
        "common_mistakes": [
                "Confusing stress (force per unit area) with pressure (same unit but different concept)",
                "Forgetting that Bernoulli's equation only applies to ideal (inviscid) fluids",
                "Using weight instead of mass in buoyancy calculations"
        ],
        "practice_prompts": [
                "A hydraulic press has pistons of area 10 cm² and 100 cm². Force on small piston is 50N. Find force on large piston.",
                "A block of wood (density 600 kg/m³) floats in water. What fraction is submerged?"
        ],
        "real_world_example": "The hydraulic brakes in buses work on Pascal's law — a small force on the brake pedal creates a large force on the brake pads. And country boats (নৌকা) float because of Archimedes' principle — the water pushes up with a force equal to the weight of water displaced."
},

    "phy1-08-01": {
        "title": "Simple Harmonic Motion",
        "learning_objectives": [
                "Define SHM and identify SHM systems",
                "Derive equations of SHM (displacement, velocity, acceleration)",
                "Calculate time period of simple pendulum and spring-mass system",
                "Understand energy in SHM"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: a swing in a playground goes back and forth. Is the motion uniform? What pattern does it follow?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Define SHM: acceleration proportional to displacement, directed toward mean position. a = -ω²x. Ask: is uniform circular motion related to SHM?"
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Equations: x = A sin(ωt), v = Aω cos(ωt), a = -Aω² sin(ωt). For pendulum: T = 2π√(l/g). For spring: T = 2π√(m/k)."
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "A spring (k=100 N/m) with 0.5kg mass. Find time period and maximum velocity if amplitude is 0.1m."
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ: energy variation in SHM — KE and PE as function of displacement."
                }
        ],
        "key_formulas": [
                "x = A sin(ωt + φ)",
                "T = 2π/ω",
                "Pendulum: T = 2π√(l/g)",
                "Spring: T = 2π√(m/k)",
                "Total energy E = ½kA² = ½mω²A²"
        ],
        "common_mistakes": [
                "Thinking pendulum period depends on mass (it doesn't for simple pendulum)",
                "Confusing amplitude with displacement at a given time",
                "Forgetting that at mean position KE=max and PE=0, at extreme PE=max and KE=0"
        ],
        "practice_prompts": [
                "A pendulum has T=2s. Find its length.",
                "In SHM, at what displacement is KE equal to PE?"
        ],
        "real_world_example": "The clock pendulums in old Bangladeshi homes (দেয়াল ঘড়ি) are SHM — the longer the pendulum, the slower it swings. That's why grandfather clocks are tall!"
},

    "phy1-09-01": {
        "title": "Wave Properties",
        "learning_objectives": [
                "Distinguish transverse and longitudinal waves",
                "Apply v = fλ relationship",
                "Understand superposition and standing waves",
                "Calculate frequency of vibrating strings and air columns"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: when you throw a stone in a pond, ripples spread out. Is the water actually moving outward, or is it something else?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Teach transverse (particle ⊥ wave direction) vs longitudinal (particle ∥ wave direction). v = fλ. Ask: is sound transverse or longitudinal?"
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Standing waves on string: harmonics. f_n = n(v/2L). For closed pipe: only odd harmonics. Open pipe: all harmonics."
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "A string (L=1m, μ=0.01 kg/m) under tension 40N. Find fundamental frequency and first three harmonics."
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ about standing waves in pipes or strings."
                }
        ],
        "key_formulas": [
                "v = fλ",
                "String: v = √(T/μ)",
                "String harmonics: fₙ = nv/2L",
                "Open pipe: fₙ = nv/2L (all n)",
                "Closed pipe: fₙ = nv/4L (odd n only)"
        ],
        "common_mistakes": [
                "Thinking wave speed depends on frequency (it depends on medium)",
                "Forgetting closed pipe has only odd harmonics",
                "Confusing nodes and antinodes in standing waves"
        ],
        "practice_prompts": [
                "Sound speed is 340 m/s. Find wavelength of 680 Hz sound.",
                "A closed pipe has fundamental 200 Hz. What is its 2nd overtone?"
        ],
        "real_world_example": "When a বাঁশি (bamboo flute) player covers different holes, they change the effective length of the air column — shorter column = higher frequency = higher pitch. That's standing waves in an open pipe!"
},

    "phy1-09-02": {
        "title": "Sound & Doppler Effect",
        "learning_objectives": [
                "Calculate beat frequency",
                "Apply Doppler effect formula for moving source/observer",
                "Understand resonance and its applications",
                "Solve problems on speed of sound in different media"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: why does an ambulance siren sound higher-pitched when approaching and lower when moving away?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Doppler effect: f' = f(v ± v₀)/(v ∓ vₛ). Convention: approaching = higher, receding = lower. Ask: what if both source and observer are moving?"
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Beats: when two frequencies are close, f_beat = |f₁ - f₂|. Resonance: when driving frequency = natural frequency, amplitude is maximum."
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "An ambulance (f=500Hz) moves at 30 m/s toward you. Speed of sound = 340 m/s. Find the frequency you hear."
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ about Doppler effect or beats."
                }
        ],
        "key_formulas": [
                "Doppler: f' = f(v + v₀)/(v - vₛ) (approaching)",
                "Beat frequency = |f₁ - f₂|",
                "Speed of sound in air ≈ 340 m/s at 20°C",
                "v_sound ∝ √T (temperature in Kelvin)"
        ],
        "common_mistakes": [
                "Getting signs wrong in Doppler formula (remember: approaching = higher frequency)",
                "Thinking beats frequency = average of two frequencies (it's the difference)",
                "Forgetting speed of sound changes with temperature"
        ],
        "practice_prompts": [
                "Two tuning forks of 256 Hz and 260 Hz are sounded together. How many beats per second?",
                "A train (speed 36 km/h) blows whistle at 500 Hz. Find frequency heard by stationary observer as train approaches."
        ],
        "real_world_example": "Next time you hear a motorcycle zooming past on the highway, notice how the pitch drops as it passes you — that's the Doppler effect. Astronomers use the same principle to tell if a star is moving toward or away from us (red shift/blue shift)."
},

    "phy1-10-01": {
        "title": "Gas Laws & Kinetic Theory",
        "learning_objectives": [
                "Apply ideal gas equation PV = nRT",
                "Derive kinetic energy from kinetic theory",
                "Understand Maxwell-Boltzmann distribution",
                "Apply gas laws to solve problems"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: why does a balloon expand when you heat it? What's happening to the gas molecules inside?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Teach PV = nRT. Gas laws: Boyle's (P∝1/V), Charles's (V∝T), Gay-Lussac's (P∝T). Ask: what is an ideal gas?"
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Kinetic theory: KE = (3/2)kT. RMS speed v_rms = √(3RT/M). Ask: which gas molecules move faster at same temperature — hydrogen or oxygen?"
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "2 moles of ideal gas at 300K in 10L container. Find pressure. Then: if temperature doubles at constant volume, new pressure?"
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ about KE of gas molecules or gas law application."
                }
        ],
        "key_formulas": [
                "PV = nRT (R = 8.314 J/mol·K)",
                "KE_avg = (3/2)kT",
                "v_rms = √(3RT/M)",
                "Boyle: P₁V₁ = P₂V₂",
                "Charles: V₁/T₁ = V₂/T₂"
        ],
        "common_mistakes": [
                "Using Celsius instead of Kelvin in gas law calculations",
                "Confusing R (gas constant) with k (Boltzmann constant) — k = R/Nₐ",
                "Thinking all gas molecules move at the same speed (they have a distribution)"
        ],
        "practice_prompts": [
                "Find the RMS speed of N₂ molecules at 27°C. (M=28 g/mol)",
                "A gas at 2 atm and 300K is heated to 600K at constant volume. Find new pressure."
        ],
        "real_world_example": "The pressure cooker in every Bangladeshi kitchen works on Gay-Lussac's law — as temperature increases at constant volume, pressure increases. That's why food cooks faster inside — higher pressure means higher boiling point of water!"
},


    # ══ PHYSICS — Chapters 4-10 ══
    "phy1-02-02": {
        "title": "Scalar & Vector Products",
        "learning_objectives": [
                "Calculate dot product and find angle between vectors",
                "Calculate cross product and find area of parallelogram",
                "Apply scalar product in work calculations",
                "Apply vector product in torque calculations"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: when you push a box at an angle, not all your force moves it forward. How do we calculate the useful part of the force?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Teach dot product: A·B = AB cos θ (scalar result). Ask: what is the dot product when vectors are perpendicular?"
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Teach cross product: A×B = AB sin θ n̂ (vector result). Explain right-hand rule. Ask: what is cross product when vectors are parallel?"
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "Find dot product of A=(3,4) and B=(2,-1). Then find the angle between them."
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ: if A×B = 0 and A·B = AB, what is the angle between A and B?"
                }
        ],
        "key_formulas": [
                "A·B = AB cos θ = a₁b₁ + a₂b₂ + a₃b₃",
                "A×B = AB sin θ n̂",
                "|A×B| = area of parallelogram"
        ],
        "common_mistakes": [
                "Confusing dot product (scalar) with cross product (vector)",
                "Wrong sign in cross product (not commutative: A×B = -B×A)",
                "Forgetting that perpendicular vectors have zero dot product"
        ],
        "practice_prompts": [
                "If A=(1,2,3) and B=(4,-1,2), find A·B",
                "Two forces 5N and 8N act at 60°. Find A×B magnitude."
        ],
        "real_world_example": "When you pull a rickshaw with a rope at an angle, only the horizontal component (F cos θ) moves it forward — that's the dot product of force and displacement giving you work done."
},

    "phy1-04-01": {
        "title": "Newton's Laws of Motion",
        "learning_objectives": [
                "State and apply all three Newton's laws",
                "Draw free body diagrams for complex systems",
                "Solve problems with connected bodies",
                "Apply Newton's laws to lift/elevator problems"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: why does your body jerk forward when a bus suddenly stops? Which Newton's law explains this?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Teach all 3 laws with examples. 1st: inertia (bus example). 2nd: F=ma (pushing cart). 3rd: action-reaction (walking). Ask student to identify which law applies in each scenario."
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Teach free body diagrams. Draw FBD for a block on an incline. Identify normal force, weight components, friction. Solve for acceleration."
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "Two blocks (3kg and 5kg) connected by string on frictionless surface. Force 40N applied on 5kg block. Find acceleration and tension."
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "Elevator problem: a 60kg person in a lift accelerating upward at 2 m/s². What does the scale read? BUET-level."
                }
        ],
        "key_formulas": [
                "F = ma",
                "Weight W = mg",
                "Apparent weight in lift: N = m(g ± a)",
                "Connected bodies: same acceleration, tension is internal force"
        ],
        "common_mistakes": [
                "Confusing mass and weight",
                "Forgetting that action-reaction forces act on DIFFERENT bodies",
                "Not resolving forces into components on inclined planes"
        ],
        "practice_prompts": [
                "A 10kg box on a smooth surface is pushed with 50N. Find acceleration.",
                "In a lift going up with acceleration 3 m/s², what is the apparent weight of a 50kg person?"
        ],
        "real_world_example": "When a CNG auto-rickshaw suddenly brakes, you slide forward — that's Newton's 1st law. The harder the driver brakes (more force), the faster you decelerate (2nd law). Your feet push backward on the floor, floor pushes you forward (3rd law)."
},

    "phy1-04-02": {
        "title": "Friction & Circular Motion",
        "learning_objectives": [
                "Calculate static and kinetic friction",
                "Solve problems on banked roads and circular motion",
                "Apply centripetal force concept",
                "Understand the role of friction in daily life"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: why is it easier to push a box once it starts moving than to start pushing it? What's the difference between static and kinetic friction?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Teach f = μN. Static friction ≤ μₛN, kinetic friction = μₖN. Ask: why is μₛ > μₖ always?"
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Circular motion: centripetal force F = mv²/r. For car on banked road: tan θ = v²/rg. Derive step by step."
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "A car turns on a flat road (μ=0.4, r=50m). Find maximum safe speed. Then: what if the road is banked at 30°?"
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ about friction on incline or centripetal force in vertical circular motion."
                }
        ],
        "key_formulas": [
                "f = μN",
                "Centripetal force F = mv²/r",
                "Banked road: tan θ = v²/rg",
                "Min speed at top of loop: v = √(rg)"
        ],
        "common_mistakes": [
                "Using μmg for friction on incline (should be μN = μmg cos θ)",
                "Confusing centripetal (real) with centrifugal (pseudo) force",
                "Forgetting that static friction has a maximum value, not a fixed value"
        ],
        "practice_prompts": [
                "A 5kg block on a surface with μ=0.3. Find friction when 10N horizontal force applied.",
                "Find the banking angle for a road curve (r=100m) at speed 72 km/h."
        ],
        "real_world_example": "The flyover curves in Dhaka are slightly banked — the road tilts inward so cars don't need to rely only on tire friction. Same reason why cricket bowlers can make the ball curve — friction and circular motion!"
},

    "phy1-05-01": {
        "title": "Work & Energy",
        "learning_objectives": [
                "Calculate work done by constant and variable forces",
                "Apply work-energy theorem",
                "Understand potential and kinetic energy",
                "Apply conservation of energy to solve problems"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: if you carry a heavy bag horizontally across a room, have you done any work on it (in physics terms)? Why or why not?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Teach W = Fd cos θ. When θ=90°, W=0 (carrying bag horizontally). KE = ½mv², PE = mgh. Ask: what type of energy does a flying bird have?"
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Work-energy theorem: net work = change in KE. Solve: a 2kg ball falls from 10m. Find velocity just before hitting ground using energy conservation."
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "A 1000kg car accelerates from 10 m/s to 30 m/s. Find the work done by the engine."
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ: a pendulum released from height h. Find velocity at lowest point. Then: if string is cut at lowest point, what path does it follow?"
                }
        ],
        "key_formulas": [
                "W = Fd cos θ",
                "KE = ½mv²",
                "PE = mgh",
                "Conservation: KE₁ + PE₁ = KE₂ + PE₂"
        ],
        "common_mistakes": [
                "Saying you do work when carrying a bag horizontally (W=0 since F⊥d)",
                "Forgetting that work can be negative (friction does negative work)",
                "Not using energy conservation when it's simpler than force equations"
        ],
        "practice_prompts": [
                "A 50kg boy climbs 10m stairs. How much work against gravity?",
                "A spring (k=200 N/m) compressed 0.1m. Find stored PE."
        ],
        "real_world_example": "When water falls at Kaptai Dam from height h, its PE converts to KE, which spins turbines to generate electricity. The higher the dam, the more energy — that's why Kaptai was built in the hills of Rangamati."
},

    "phy1-05-02": {
        "title": "Power & Collisions",
        "learning_objectives": [
                "Calculate power as rate of work done",
                "Distinguish elastic and inelastic collisions",
                "Apply momentum conservation in collisions",
                "Solve problems involving coefficient of restitution"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: two people carry the same weight up stairs — one takes 1 minute, the other takes 5 minutes. Who does more work? Who has more power?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Power P = W/t = Fv. 1 HP = 746 W. Teach elastic (KE conserved) vs inelastic (KE not conserved) collisions."
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Collision formulas: m₁u₁ + m₂u₂ = m₁v₁ + m₂v₂. For perfectly inelastic: bodies stick together. Solve: 2kg ball at 3m/s hits stationary 1kg ball elastically."
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "A 1500kg car at 20 m/s collides with stationary 1000kg car. They stick together. Find final velocity and energy lost."
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ about collision or power calculation."
                }
        ],
        "key_formulas": [
                "P = W/t = Fv",
                "1 HP = 746 W",
                "Coefficient of restitution e = (v₂-v₁)/(u₁-u₂)",
                "Elastic: e=1, Perfectly inelastic: e=0"
        ],
        "common_mistakes": [
                "Confusing work (same for both) with power (different if time differs)",
                "Thinking momentum is not conserved in inelastic collisions (it IS, only KE isn't)",
                "Forgetting that in 2D collisions, momentum is conserved in each direction separately"
        ],
        "practice_prompts": [
                "A pump lifts 500kg water to 10m in 5 seconds. Find power in watts and HP.",
                "Two identical balls collide elastically head-on. What happens?"
        ],
        "real_world_example": "When a truck hits a small car, both have the same momentum change (Newton's 3rd law) — but the small car gets much more acceleration because F=ma and its mass is less. That's why trucks cause more damage in accidents on the Dhaka-Chittagong highway."
},

    "phy1-06-01": {
        "title": "Gravitation",
        "learning_objectives": [
                "Apply Newton's law of gravitation",
                "Calculate gravitational field strength at different altitudes",
                "Derive orbital velocity and escape velocity",
                "Apply Kepler's laws of planetary motion"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: why does the Moon orbit the Earth instead of flying away? What force keeps it in orbit?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Teach F = GMm/r². Surface gravity g = GM/R². Ask: what happens to g if you go to a mountain top? What about deep inside Earth?"
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Derive orbital velocity v = √(GM/r) and escape velocity vₑ = √(2GM/R) = √(2gR). Ask: why is escape velocity √2 times orbital velocity?"
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "Calculate g at height equal to Earth's radius. Then: find escape velocity from Earth (R=6400km, g=9.8)."
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ about satellite period or variation of g with altitude/depth."
                }
        ],
        "key_formulas": [
                "F = GMm/r²",
                "g = GM/R²",
                "Orbital velocity v₀ = √(GM/r)",
                "Escape velocity vₑ = √(2gR)",
                "Kepler's T² ∝ r³"
        ],
        "common_mistakes": [
                "Using r (distance from center) vs h (height above surface) — g at height h: g'=g(R/(R+h))²",
                "Forgetting that inside Earth, g decreases linearly with depth",
                "Confusing orbital velocity with escape velocity"
        ],
        "practice_prompts": [
                "At what height above Earth is g reduced to g/4?",
                "Find the time period of a satellite orbiting just above Earth's surface."
        ],
        "real_world_example": "Bangladesh's Bangabandhu-1 satellite orbits at 35,786 km (geostationary orbit) — at that height, it takes exactly 24 hours to orbit, so it stays over the same spot above Bangladesh. That's Kepler's third law in action!"
},

    "phy1-07-01": {
        "title": "Elasticity & Fluid Mechanics",
        "learning_objectives": [
                "Define stress, strain, and Young's modulus",
                "Apply Hooke's law within elastic limit",
                "Apply Pascal's law and Archimedes' principle",
                "Use Bernoulli's equation for fluid flow"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: why does a rubber band return to its original shape but clay doesn't? What's the difference?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Teach stress = F/A, strain = ΔL/L, Young's modulus Y = stress/strain. Hooke's law: F = kx. Ask: what happens beyond the elastic limit?"
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Fluid statics: Pascal's law (hydraulic press), Archimedes' principle (buoyancy). Bernoulli's: P + ½ρv² + ρgh = constant."
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "A steel wire (Y=2×10¹¹ Pa, L=2m, A=1mm²) stretched by 100N. Find extension."
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ about buoyancy or Bernoulli's application."
                }
        ],
        "key_formulas": [
                "Stress = F/A, Strain = ΔL/L",
                "Young's modulus Y = Stress/Strain",
                "Pascal's law: pressure transmitted equally",
                "Bernoulli: P + ½ρv² + ρgh = constant"
        ],
        "common_mistakes": [
                "Confusing stress (force per unit area) with pressure (same unit but different concept)",
                "Forgetting that Bernoulli's equation only applies to ideal (inviscid) fluids",
                "Using weight instead of mass in buoyancy calculations"
        ],
        "practice_prompts": [
                "A hydraulic press has pistons of area 10 cm² and 100 cm². Force on small piston is 50N. Find force on large piston.",
                "A block of wood (density 600 kg/m³) floats in water. What fraction is submerged?"
        ],
        "real_world_example": "The hydraulic brakes in buses work on Pascal's law — a small force on the brake pedal creates a large force on the brake pads. And country boats (নৌকা) float because of Archimedes' principle — the water pushes up with a force equal to the weight of water displaced."
},

    "phy1-08-01": {
        "title": "Simple Harmonic Motion",
        "learning_objectives": [
                "Define SHM and identify SHM systems",
                "Derive equations of SHM (displacement, velocity, acceleration)",
                "Calculate time period of simple pendulum and spring-mass system",
                "Understand energy in SHM"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: a swing in a playground goes back and forth. Is the motion uniform? What pattern does it follow?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Define SHM: acceleration proportional to displacement, directed toward mean position. a = -ω²x. Ask: is uniform circular motion related to SHM?"
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Equations: x = A sin(ωt), v = Aω cos(ωt), a = -Aω² sin(ωt). For pendulum: T = 2π√(l/g). For spring: T = 2π√(m/k)."
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "A spring (k=100 N/m) with 0.5kg mass. Find time period and maximum velocity if amplitude is 0.1m."
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ: energy variation in SHM — KE and PE as function of displacement."
                }
        ],
        "key_formulas": [
                "x = A sin(ωt + φ)",
                "T = 2π/ω",
                "Pendulum: T = 2π√(l/g)",
                "Spring: T = 2π√(m/k)",
                "Total energy E = ½kA² = ½mω²A²"
        ],
        "common_mistakes": [
                "Thinking pendulum period depends on mass (it doesn't for simple pendulum)",
                "Confusing amplitude with displacement at a given time",
                "Forgetting that at mean position KE=max and PE=0, at extreme PE=max and KE=0"
        ],
        "practice_prompts": [
                "A pendulum has T=2s. Find its length.",
                "In SHM, at what displacement is KE equal to PE?"
        ],
        "real_world_example": "The clock pendulums in old Bangladeshi homes (দেয়াল ঘড়ি) are SHM — the longer the pendulum, the slower it swings. That's why grandfather clocks are tall!"
},

    "phy1-09-01": {
        "title": "Wave Properties",
        "learning_objectives": [
                "Distinguish transverse and longitudinal waves",
                "Apply v = fλ relationship",
                "Understand superposition and standing waves",
                "Calculate frequency of vibrating strings and air columns"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: when you throw a stone in a pond, ripples spread out. Is the water actually moving outward, or is it something else?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Teach transverse (particle ⊥ wave direction) vs longitudinal (particle ∥ wave direction). v = fλ. Ask: is sound transverse or longitudinal?"
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Standing waves on string: harmonics. f_n = n(v/2L). For closed pipe: only odd harmonics. Open pipe: all harmonics."
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "A string (L=1m, μ=0.01 kg/m) under tension 40N. Find fundamental frequency and first three harmonics."
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ about standing waves in pipes or strings."
                }
        ],
        "key_formulas": [
                "v = fλ",
                "String: v = √(T/μ)",
                "String harmonics: fₙ = nv/2L",
                "Open pipe: fₙ = nv/2L (all n)",
                "Closed pipe: fₙ = nv/4L (odd n only)"
        ],
        "common_mistakes": [
                "Thinking wave speed depends on frequency (it depends on medium)",
                "Forgetting closed pipe has only odd harmonics",
                "Confusing nodes and antinodes in standing waves"
        ],
        "practice_prompts": [
                "Sound speed is 340 m/s. Find wavelength of 680 Hz sound.",
                "A closed pipe has fundamental 200 Hz. What is its 2nd overtone?"
        ],
        "real_world_example": "When a বাঁশি (bamboo flute) player covers different holes, they change the effective length of the air column — shorter column = higher frequency = higher pitch. That's standing waves in an open pipe!"
},

    "phy1-09-02": {
        "title": "Sound & Doppler Effect",
        "learning_objectives": [
                "Calculate beat frequency",
                "Apply Doppler effect formula for moving source/observer",
                "Understand resonance and its applications",
                "Solve problems on speed of sound in different media"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: why does an ambulance siren sound higher-pitched when approaching and lower when moving away?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Doppler effect: f' = f(v ± v₀)/(v ∓ vₛ). Convention: approaching = higher, receding = lower. Ask: what if both source and observer are moving?"
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Beats: when two frequencies are close, f_beat = |f₁ - f₂|. Resonance: when driving frequency = natural frequency, amplitude is maximum."
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "An ambulance (f=500Hz) moves at 30 m/s toward you. Speed of sound = 340 m/s. Find the frequency you hear."
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ about Doppler effect or beats."
                }
        ],
        "key_formulas": [
                "Doppler: f' = f(v + v₀)/(v - vₛ) (approaching)",
                "Beat frequency = |f₁ - f₂|",
                "Speed of sound in air ≈ 340 m/s at 20°C",
                "v_sound ∝ √T (temperature in Kelvin)"
        ],
        "common_mistakes": [
                "Getting signs wrong in Doppler formula (remember: approaching = higher frequency)",
                "Thinking beats frequency = average of two frequencies (it's the difference)",
                "Forgetting speed of sound changes with temperature"
        ],
        "practice_prompts": [
                "Two tuning forks of 256 Hz and 260 Hz are sounded together. How many beats per second?",
                "A train (speed 36 km/h) blows whistle at 500 Hz. Find frequency heard by stationary observer as train approaches."
        ],
        "real_world_example": "Next time you hear a motorcycle zooming past on the highway, notice how the pitch drops as it passes you — that's the Doppler effect. Astronomers use the same principle to tell if a star is moving toward or away from us (red shift/blue shift)."
},

    "phy1-10-01": {
        "title": "Gas Laws & Kinetic Theory",
        "learning_objectives": [
                "Apply ideal gas equation PV = nRT",
                "Derive kinetic energy from kinetic theory",
                "Understand Maxwell-Boltzmann distribution",
                "Apply gas laws to solve problems"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: why does a balloon expand when you heat it? What's happening to the gas molecules inside?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Teach PV = nRT. Gas laws: Boyle's (P∝1/V), Charles's (V∝T), Gay-Lussac's (P∝T). Ask: what is an ideal gas?"
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Kinetic theory: KE = (3/2)kT. RMS speed v_rms = √(3RT/M). Ask: which gas molecules move faster at same temperature — hydrogen or oxygen?"
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "2 moles of ideal gas at 300K in 10L container. Find pressure. Then: if temperature doubles at constant volume, new pressure?"
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ about KE of gas molecules or gas law application."
                }
        ],
        "key_formulas": [
                "PV = nRT (R = 8.314 J/mol·K)",
                "KE_avg = (3/2)kT",
                "v_rms = √(3RT/M)",
                "Boyle: P₁V₁ = P₂V₂",
                "Charles: V₁/T₁ = V₂/T₂"
        ],
        "common_mistakes": [
                "Using Celsius instead of Kelvin in gas law calculations",
                "Confusing R (gas constant) with k (Boltzmann constant) — k = R/Nₐ",
                "Thinking all gas molecules move at the same speed (they have a distribution)"
        ],
        "practice_prompts": [
                "Find the RMS speed of N₂ molecules at 27°C. (M=28 g/mol)",
                "A gas at 2 atm and 300K is heated to 600K at constant volume. Find new pressure."
        ],
        "real_world_example": "The pressure cooker in every Bangladeshi kitchen works on Gay-Lussac's law — as temperature increases at constant volume, pressure increases. That's why food cooks faster inside — higher pressure means higher boiling point of water!"
},



    # ══════════════════════════════════════════════════════════════
    # ══ BIOLOGY — Chapter 4: অণুজীব (Microorganisms) ══
    # ══════════════════════════════════════════════════════════════

    "bio1-04-01": {
        "title": "Microorganisms — Viruses and Bacteria",
        "learning_objectives": [
            "Describe the general structure of viruses (nucleic acid core, protein capsid, envelope) and explain why viruses are considered non-living outside a host",
            "Classify viruses based on nucleic acid type (DNA virus, RNA virus), host range (bacteriophage, plant virus, animal virus), and shape (icosahedral, helical, complex)",
            "Describe the structure of bacteria (cell wall, cell membrane, capsule, flagella, pili, nucleoid, plasmid, ribosome 70S) and classify by shape (coccus, bacillus, spirillum, vibrio)",
            "Explain the lytic and lysogenic cycles of bacteriophage replication and compare bacterial reproduction (binary fission) with conjugation, transformation, and transduction",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: during COVID-19, we all learned about viruses. But is a virus truly alive? It cannot eat, grow, or reproduce on its own. So what exactly is it? And the bacteria in your doi (yogurt) — are they the same kind of organism as a virus?",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Teach virus structure: nucleic acid (DNA or RNA, never both) surrounded by a protein coat (capsid) made of capsomeres. Some have an outer lipid envelope with glycoprotein spikes (e.g., SARS-CoV-2 spike protein). Ask: why can\'t viruses reproduce without a host cell? (No ribosomes, no metabolic machinery). Discuss: are viruses living or non-living? They show characteristics of life only inside a host — obligate intracellular parasites.",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Teach the lytic cycle: attachment -> penetration -> biosynthesis -> assembly -> lysis (host cell bursts, releases new virions). Then lysogenic cycle: viral DNA integrates into host genome as prophage, replicates with host, can switch to lytic cycle under stress. Ask: which cycle does HIV follow initially? (Lysogenic — integrates as provirus, then activates). Then teach bacterial structure: compare with eukaryotic cell. Key features — peptidoglycan cell wall (Gram+ thick, Gram- thin with outer membrane), 70S ribosomes, single circular chromosome + plasmids. Classification by shape: coccus (gol — round), bacillus (dondo — rod), spirillum (pechano — spiral), vibrio (comma-shaped, like Vibrio cholerae that causes cholera in Bangladesh).",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Classification exercise: classify these microorganisms — Tobacco Mosaic Virus (RNA, helical, plant virus), Bacteriophage T4 (DNA, complex, bacterial virus), HIV (RNA retrovirus, animal virus), Vibrio cholerae (Gram- vibrio bacterium), Mycobacterium tuberculosis (acid-fast bacillus), Staphylococcus aureus (Gram+ coccus). Ask: which of these are particularly relevant to Bangladesh\'s public health? (Vibrio cholerae — cholera is endemic; TB is a major burden).",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "Medical admission MCQ: \'Which of the following is TRUE about viruses? (a) They have both DNA and RNA (b) They can reproduce independently (c) They have 70S ribosomes (d) They are obligate intracellular parasites.\' Follow up: \'A bacteriophage infects E. coli and its DNA integrates into the host chromosome. What is this integrated viral DNA called? (Prophage). What triggers the switch from lysogenic to lytic cycle?\' Then: \'Explain how antibiotic resistance spreads between bacteria via plasmid transfer (conjugation). Why is this a major public health concern in Bangladesh where antibiotics are sold without prescription?\'",
            },
        ],
        "key_formulas": [
            "Virus = nucleic acid (DNA or RNA, not both) + protein capsid (capsomeres) +/- lipid envelope",
            "Lytic cycle: attachment -> penetration -> biosynthesis -> assembly -> lysis (host cell dies)",
            "Lysogenic cycle: viral DNA integrates as prophage -> replicates with host -> can switch to lytic under stress",
            "Bacteria classification by shape: coccus (spherical), bacillus (rod), spirillum (spiral), vibrio (comma)",
            "Gram staining: Gram+ (thick peptidoglycan, retains crystal violet — purple) vs Gram- (thin peptidoglycan + outer membrane, takes safranin — pink)",
            "Bacterial reproduction: binary fission (asexual); gene transfer — conjugation (F pilus), transformation (free DNA uptake), transduction (via bacteriophage)",
        ],
        "common_mistakes": [
            "Saying viruses have both DNA and RNA — a virus has EITHER DNA or RNA, never both (exception: some textbooks mention cytomegalovirus having both, but for HSC exam, the rule is one or the other)",
            "Confusing the lytic and lysogenic cycles — in lysogenic, the host cell does NOT lyse immediately; the viral DNA quietly integrates and replicates with the host. Students often describe lysis occurring in the lysogenic cycle.",
            "Thinking all bacteria are harmful — beneficial bacteria include Lactobacillus (doi/yogurt), Rhizobium (nitrogen fixation in legume root nodules), E. coli (vitamin K synthesis in human gut). Only pathogenic bacteria cause disease.",
            "Confusing Gram+ and Gram- — Gram+ has a THICKER peptidoglycan wall (retains crystal violet stain), Gram- has a THINNER wall but has an additional outer membrane. Students often reverse these.",
        ],
        "practice_prompts": [
            "Compare the structure of a bacteriophage T4 with HIV in a table covering: nucleic acid type, capsid shape, envelope (present/absent), host cell, and mode of replication.",
            "A patient has cholera caused by Vibrio cholerae. Describe the shape and Gram stain result of this bacterium. Explain how it causes profuse watery diarrhea (cholera toxin activates cAMP pathway in intestinal cells).",
            "Explain why antibiotics work against bacteria but NOT against viruses. What type of drugs are used against viruses? (Antivirals like oseltamivir, remdesivir). Why is it harder to develop antiviral drugs?",
        ],
        "real_world_example": "Bangladesh has a long history with cholera — Vibrio cholerae, a comma-shaped Gram-negative bacterium, thrives in contaminated water. ICDDR,B in Dhaka developed Oral Rehydration Solution (ORS) that has saved millions of lives globally. Meanwhile, the COVID-19 pandemic showed how RNA viruses like SARS-CoV-2 can mutate rapidly. The pond water in rural Bangladesh often contains cyanobacteria (Nostoc, Anabaena) that fix nitrogen, enriching rice paddy fields naturally — these are beneficial microorganisms that boost rice yields without chemical fertilizer.",
    },

    # ══════════════════════════════════════════════════════════════
    # ══ BIOLOGY — Chapter 5: শৈবাল ও ছত্রাক (Algae & Fungi) ══
    # ══════════════════════════════════════════════════════════════

    "bio1-05-01": {
        "title": "Algae and Fungi — Structure, Classification & Reproduction",
        "learning_objectives": [
            "Describe the general characteristics of algae — photosynthetic, aquatic thallophytes with chlorophyll a as the universal pigment",
            "Classify algae into major divisions: Chlorophyta (green algae — Spirogyra, Volvox), Phaeophyta (brown algae — Sargassum, Fucus), Rhodophyta (red algae — Polysiphonia) based on pigments and storage products",
            "Describe the general characteristics of fungi — heterotrophic, cell wall of chitin, saprophytic or parasitic nutrition, reproduce by spores",
            "Classify fungi into Zygomycetes (Mucor, Rhizopus), Ascomycetes (Saccharomyces/yeast, Penicillium), Basidiomycetes (Agaricus/mushroom, Puccinia/wheat rust), and Deuteromycetes (Fungi Imperfecti)",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: have you seen green slimy stuff floating on a pond in the village? That is algae — Spirogyra and other species. And the mushrooms that people now farm commercially — those are fungi. Both are very different from higher plants. How?",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Teach algae characteristics: eukaryotic, photosynthetic (autotrophic), mostly aquatic, thallus body (no true root/stem/leaf), cell wall of cellulose. Classification by pigment: Chlorophyta (chlorophyll a, b — green), Phaeophyta (chlorophyll a, c + fucoxanthin — brown), Rhodophyta (chlorophyll a, d + phycoerythrin — red). Ask: why are red algae found in deeper ocean waters? (Phycoerythrin absorbs blue-green light that penetrates deep water). Storage products differ too: starch (green), laminarin (brown), floridean starch (red).",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Teach algal reproduction: vegetative (fragmentation — Spirogyra breaks), asexual (zoospores — motile spores), sexual (isogamy, anisogamy, oogamy). Use Spirogyra as example: scalariform conjugation (lateral/transverse). Then teach fungi: heterotrophic (no chlorophyll), body is mycelium (network of hyphae), cell wall of chitin (not cellulose!). Hyphae can be septate (Penicillium) or coenocytic/aseptate (Mucor). Nutrition: saprophytic (decomposers — Rhizopus on ruti/bread), parasitic (Puccinia on wheat), mutualistic (lichens = algae + fungi, mycorrhizae). Reproduction: vegetative (fragmentation, budding in yeast), asexual (sporangiospores — Mucor, conidia — Penicillium/Aspergillus), sexual (zygospore, ascospore, basidiospore). Classify: Zygomycetes (zygospore — Mucor, Rhizopus), Ascomycetes (ascospore in ascus — yeast, Penicillium), Basidiomycetes (basidiospore on basidium — Agaricus mushroom, Puccinia rust).",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Comparison exercise: make a table comparing algae and fungi on: nutrition mode, cell wall composition, pigments, body organization, habitat, storage product, examples. Then ask: classify these organisms — Spirogyra (Chlorophyta), Sargassum (Phaeophyta), Polysiphonia (Rhodophyta), Mucor (Zygomycetes), Penicillium (Ascomycetes), Agaricus (Basidiomycetes). Ask: which of these is used to produce antibiotics? (Penicillium — produces penicillin).",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "Medical admission MCQ: \'The cell wall of fungi is made of: (a) Cellulose (b) Peptidoglycan (c) Chitin (d) Pectin.\' Follow up: \'In the life cycle of Mucor, what type of sexual spore is formed? Describe the process of zygospore formation.\' Then: \'Lichens are indicators of air pollution — explain why. What are the two components of a lichen and what is the relationship between them (mutualism)?\' Finally: \'Explain how Saccharomyces cerevisiae (yeast) is used in both bread-making and alcohol fermentation. Write the fermentation equation.\'",
            },
        ],
        "key_formulas": [
            "Algae pigment classification: Chlorophyta (Chl a, b — green), Phaeophyta (Chl a, c + fucoxanthin — brown), Rhodophyta (Chl a, d + phycoerythrin — red)",
            "Fungal cell wall: chitin (polymer of N-acetylglucosamine) — NOT cellulose",
            "Fungi classification by sexual spore: Zygomycetes (zygospore), Ascomycetes (ascospore in ascus), Basidiomycetes (basidiospore on basidium), Deuteromycetes (no known sexual stage)",
            "Yeast fermentation: C6H12O6 -> 2C2H5OH + 2CO2 + energy (anaerobic)",
            "Lichen = algal/cyanobacterial partner (photobiont) + fungal partner (mycobiont) — mutualistic symbiosis",
            "Algal reproduction types: isogamy (similar gametes), anisogamy (dissimilar but both motile), oogamy (large non-motile egg + small motile sperm)",
        ],
        "common_mistakes": [
            "Saying fungi have cellulose cell walls like plants — fungi have CHITIN cell walls, which is the same material found in insect exoskeletons. This is a very commonly tested distinction.",
            "Confusing algae as plants — algae are thallophytes with no true roots, stems, or leaves. They lack vascular tissue. Although photosynthetic, they are classified separately from bryophytes and tracheophytes.",
            "Mixing up fungal spore types — students confuse sporangiospores (inside sporangium — Mucor), conidia (on conidiophore tips — Penicillium, Aspergillus), and basidiospores (on basidia — mushrooms). Each class has its characteristic asexual and sexual spore types.",
            "Thinking all fungi are harmful — yeast (Saccharomyces) is used in bread and fermentation, Penicillium gives us penicillin, mushrooms (Agaricus) are edible, and mycorrhizal fungi help plant roots absorb minerals.",
        ],
        "practice_prompts": [
            "A student observes a filamentous green organism under the microscope. It has a spiral chloroplast and is undergoing conjugation. Identify the organism (Spirogyra), its division (Chlorophyta), and describe the process of scalariform conjugation.",
            "Compare Mucor (Zygomycetes) and Penicillium (Ascomycetes) in terms of: hyphal structure (septate vs aseptate), asexual spores (sporangiospores vs conidia), sexual spores (zygospore vs ascospore), and economic importance.",
            "Explain why red algae can survive at greater ocean depths than green algae. Which accessory pigment is responsible, and how does it help in photosynthesis at those depths?",
        ],
        "real_world_example": "In rural Bangladesh, ponds and ditches often develop thick green mats of Spirogyra and other filamentous algae, especially during the warm monsoon season — this is called algal bloom, caused by excess nitrogen and phosphorus from fertilizer runoff into water bodies. Mushroom farming (Agaricus bisporus and oyster mushroom/Pleurotus) has become a profitable cottage industry in Bangladesh, especially in Savar and Manikganj, requiring minimal land — just a damp room with straw substrate. The antibiotic penicillin, discovered from the fungus Penicillium notatum by Alexander Fleming, has saved countless lives in Bangladesh from bacterial infections. Even the ruti (bread) you eat rises because of yeast fermentation producing CO2 gas.",
    },

    # ══════════════════════════════════════════════════════════════
    # ══ BIOLOGY — Chapter 6: ব্রায়োফাইটা ও টেরিডোফাইটা (Bryophyta & Pteridophyta) ══
    # ══════════════════════════════════════════════════════════════

    "bio1-06-01": {
        "title": "Bryophyta and Pteridophyta — Alternation of Generations",
        "learning_objectives": [
            "Describe the general characteristics of bryophytes — non-vascular, dominant gametophyte generation, require water for fertilization",
            "Explain the life cycle of a moss (Funaria) showing alternation of generations between gametophyte (n) and sporophyte (2n)",
            "Describe the general characteristics of pteridophytes — first vascular plants, dominant sporophyte generation, homosporous and heterosporous types",
            "Explain the life cycle of a fern (Dryopteris/Pteris) showing alternation of generations with independent gametophyte (prothallus)",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: have you noticed soft green cushion-like patches on old brick walls during the rainy season in Bangladesh? Those are mosses — bryophytes! And the ferns (dheki shak) that grow in shady, moist places — those are pteridophytes. Both have something special: they alternate between two completely different body forms in their life cycle. What could this mean?",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Teach the concept of alternation of generations: the plant alternates between a haploid gametophyte (n) that produces gametes by mitosis, and a diploid sporophyte (2n) that produces spores by meiosis. This is the central concept. In bryophytes: the GAMETOPHYTE is the dominant, visible, independent plant body (the green mossy part). The sporophyte is dependent on the gametophyte (it grows on top of it — like the capsule on a stalk). In pteridophytes: the SPOROPHYTE is the dominant, visible, independent plant (the fern fronds you see). The gametophyte (prothallus) is tiny, heart-shaped, and short-lived. Ask: why is this shift from dominant gametophyte to dominant sporophyte considered an evolutionary advancement?",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Teach the life cycle of Funaria (moss) in detail: Spore (n) germinates into protonema -> develops into leafy gametophyte (n) -> male (antheridium produces antherozoids/sperm) and female (archegonium produces egg) -> antherozoids swim through water to reach egg (WHY bryophytes need moist habitats!) -> fertilization -> zygote (2n) -> develops into sporophyte (foot + seta + capsule) attached to gametophyte -> meiosis in capsule produces spores (n) -> spores disperse -> cycle repeats. Key point: in Funaria, male and female gametophytes are separate plants (dioecious). Then teach fern (Dryopteris) life cycle: Sporophyte (2n, the visible fern plant) -> sporangia on underside of fronds (in sori) -> meiosis produces spores (n) -> spore germinates into prothallus (n, heart-shaped gametophyte) -> prothallus has both antheridia and archegonia (monoecious) -> antherozoids swim to egg -> fertilization -> zygote (2n) -> grows into new sporophyte. Ask: why is the fern sporophyte independent but the moss sporophyte is not?",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Comparison table: Bryophytes vs Pteridophytes — dominant generation, vascular tissue (absent vs present), true roots/stems/leaves, sporophyte dependence, examples. Then ask: in a moss life cycle diagram, identify all haploid structures and all diploid structures. Which process converts 2n to n? (Meiosis — in sporangium). Which process converts n to 2n? (Fertilization). A fern leaf shows brown dots on its underside — what are these? (Sori — clusters of sporangia).",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "Medical admission MCQ: \'In the life cycle of a fern, the gametophyte is: (a) The leafy fern plant (b) The prothallus (c) The sporangium (d) The rhizome.\' Follow up: \'Explain why bryophytes are called the amphibians of the plant kingdom. How does the requirement of water for fertilization limit their distribution?\' Then: \'What is heterospory? Which group first showed heterospory — some pteridophytes like Selaginella produce microspores (male) and megaspores (female). Explain how heterospory is considered a precursor to seed formation in higher plants.\'",
            },
        ],
        "key_formulas": [
            "Alternation of generations: Gametophyte (n) --mitosis--> gametes --fertilization--> Zygote (2n) --mitosis--> Sporophyte (2n) --meiosis--> Spores (n) --mitosis--> Gametophyte (n)",
            "Bryophytes: GAMETOPHYTE dominant (n), sporophyte dependent on gametophyte",
            "Pteridophytes: SPOROPHYTE dominant (2n), gametophyte (prothallus) is small and independent but short-lived",
            "Mosses: spore -> protonema -> leafy gametophyte -> archegonium (egg) + antheridium (sperm) -> fertilization (needs water) -> sporophyte (capsule)",
            "Ferns: sporophyte (visible fern) -> sori (sporangia) -> meiosis -> spores -> prothallus (gametophyte) -> gametes -> fertilization (needs water) -> new sporophyte",
            "Homosporous: all spores identical (most ferns); Heterosporous: microspores (male) and megaspores (female) — Selaginella, Marsilea",
        ],
        "common_mistakes": [
            "Confusing which generation is dominant — in bryophytes, GAMETOPHYTE is dominant (the green plant you see); in pteridophytes, SPOROPHYTE is dominant (the fern you see). Students frequently reverse these.",
            "Thinking spores are produced by mitosis — spores are produced by MEIOSIS (that is how the sporophyte 2n produces haploid n spores). Gametes are produced by MITOSIS from the already haploid gametophyte. This is opposite to animals where gametes come from meiosis!",
            "Forgetting that BOTH bryophytes and pteridophytes need water for fertilization (motile sperm must swim to egg). This is why they are mostly found in moist habitats. Seed plants overcame this with pollen tubes.",
            "Confusing sori with seeds or spores — sori are clusters of sporangia (spore-producing structures) found on the underside of fern fronds, not the spores themselves.",
        ],
        "practice_prompts": [
            "Draw a flow diagram of the complete life cycle of Funaria (moss), labeling all haploid (n) and diploid (2n) stages. Indicate where meiosis and fertilization occur.",
            "Explain the evolutionary significance of the shift from dominant gametophyte (bryophytes) to dominant sporophyte (pteridophytes and seed plants). What advantage does a diploid sporophyte body provide?",
            "Selaginella is heterosporous. Explain the difference between microspores and megaspores. How is heterospory in Selaginella considered a step towards seed habit? Compare with the homosporous condition in most ferns.",
        ],
        "real_world_example": "During the Bangladeshi monsoon (borsha kal), you can see mosses covering old brick walls, tin roofs, and tree bark in moist areas — these are bryophytes thriving because rain provides the water film their sperm need to swim to the egg. Dheki shak (a fern, Diplazium esculentum) is eaten as a vegetable in many parts of Bangladesh — the young coiled fronds (fiddleheads/croziers) are collected from shady, damp areas near ponds. The Sundarbans mangrove forest floor has many fern species (Acrostichum aureum — the mangrove fern) adapted to brackish water. Tree ferns are also found in the hilly forests of the Chittagong Hill Tracts and Sylhet.",
    },

    # ══════════════════════════════════════════════════════════════
    # ══ BIOLOGY — Chapter 7: নগ্নবীজী ও আবৃতবীজী উদ্ভিদ (Seed Plants) ══
    # ══════════════════════════════════════════════════════════════

    "bio1-07-01": {
        "title": "Seed Plants — Gymnosperms, Monocots and Dicots",
        "learning_objectives": [
            "Describe general characteristics of gymnosperms (naked seeds, no fruit, cones/strobili, needle-like leaves) and give examples (Pinus, Cycas, Gnetum)",
            "Describe general characteristics of angiosperms (enclosed seeds, flowers, fruit formation, double fertilization) as the most evolved and dominant plant group",
            "Distinguish monocotyledons and dicotyledons based on seed structure, root system, leaf venation, flower parts, vascular bundle arrangement, and secondary growth",
            "Explain the evolutionary progression from gymnosperms to angiosperms and why angiosperms dominate Earth\'s flora",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: think about the plants around you — dhan (rice), aam (mango), narikel (coconut), kola (banana), kadam, krishnachura. All of these produce seeds inside fruits. But some plants like pine trees produce seeds without fruits — seeds sit exposed on cone scales. What is the key difference? This leads us to gymnosperms vs angiosperms.",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Teach gymnosperms: \'gymnos\' = naked, \'sperma\' = seed. Seeds are not enclosed in an ovary/fruit. They produce cones (strobili) instead of flowers. Examples: Pinus (pine — Christmas tree), Cycas (looks like a palm, living fossil), Gnetum (found in Chittagong Hill Tracts). Characteristics: mostly evergreen trees, needle-like or scale-like leaves (xerophytic adaptation), wind-pollinated, no vessels in xylem (tracheids only — except Gnetum), no companion cells in phloem. Then teach angiosperms: \'angeion\' = vessel/container, \'sperma\' = seed. Seeds enclosed in fruit (developed from ovary). Key features: flowers (reproductive structure), double fertilization (unique to angiosperms), fruit formation, both tracheids and vessels in xylem, sieve tubes with companion cells in phloem. Ask: why are angiosperms the most successful plant group on Earth? (Flowers attract pollinators — more efficient than wind pollination; fruits protect seeds and aid dispersal; double fertilization provides endosperm nutrition for developing embryo).",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Teach the dicot vs monocot comparison in detail. This is extremely important for medical admission. Create a comprehensive comparison: (1) Cotyledons: dicot = 2, monocot = 1. (2) Root system: dicot = taproot (mango, neem), monocot = fibrous roots (rice, grass). (3) Leaf venation: dicot = reticulate/netted (mango leaf), monocot = parallel (rice leaf, banana leaf). (4) Flower parts: dicot = multiples of 4 or 5 (jaba/hibiscus has 5 petals), monocot = multiples of 3 (lily has 3+3 tepals). (5) Vascular bundles in stem: dicot = arranged in a ring with cambium (open, allows secondary growth), monocot = scattered without cambium (closed, no secondary growth — except coconut palm which grows differently). (6) Stem growth: dicot can show secondary growth (neem tree gets thicker yearly), monocot generally no secondary thickening. (7) Pollen: dicot = tricolpate (3 pores), monocot = monocolpate (1 pore). Ask student to classify common Bangladeshi plants: dhan, aam, kathal, narikel, taal, jaba, golap, kadam, kola.",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Classification exercise: classify these as gymnosperm, monocot, or dicot — Pinus (gymnosperm), rice/dhan (monocot), mango/aam (dicot), coconut/narikel (monocot), wheat (monocot), jackfruit/kathal (dicot), Cycas (gymnosperm), banana/kola (monocot), neem (dicot), bamboo/bash (monocot), jute/paat (dicot), tea/cha (dicot), tulip (monocot). Ask for the reasoning in each case. Then: draw a cross-section comparison of a dicot stem vs monocot stem showing vascular bundle arrangement.",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "Medical admission MCQ: \'Which of the following is a characteristic of monocotyledons? (a) Taproot system (b) Reticulate venation (c) Scattered vascular bundles (d) Flower parts in multiples of 5.\' Follow up: \'Coconut palm is a monocot but it grows tall and has a thick trunk — if monocots lack secondary growth (no vascular cambium), how does the coconut trunk become thick? (Primary thickening meristem + diffuse secondary growth).\' Then: \'Explain double fertilization in angiosperms. Why is this considered an evolutionary advantage over gymnosperms? What is the ploidy of the endosperm (3n) and how does it form?\'",
            },
        ],
        "key_formulas": [
            "Gymnosperm: naked seed (no fruit), cones instead of flowers, wind-pollinated, tracheids only (no vessels, except Gnetum)",
            "Angiosperm: seeds enclosed in fruit, flowers present, double fertilization, vessels + tracheids in xylem",
            "Dicot vs Monocot comparison: cotyledons (2 vs 1), root (tap vs fibrous), venation (reticulate vs parallel), flower parts (4/5 vs 3), vascular bundles (ring/open vs scattered/closed), secondary growth (present vs absent)",
            "Double fertilization: one sperm + egg -> zygote (2n); other sperm + two polar nuclei -> primary endosperm nucleus (3n) -> endosperm",
            "Angiosperm = Dicotyledonae (Magnoliopsida) + Monocotyledonae (Liliopsida)",
        ],
        "common_mistakes": [
            "Thinking coconut is a dicot because it is a large tree with a thick trunk — coconut (Cocos nucifera) is a MONOCOT. Verify: fibrous roots, parallel venation in leaves, flower parts in 3s, scattered vascular bundles.",
            "Confusing gymnosperms with angiosperms — students sometimes call pine cones \'fruits\'. Pine cones are NOT fruits; they are strobili. Fruits develop only from ovaries, which gymnosperms lack.",
            "Saying monocots never show secondary growth — while true that monocots lack vascular cambium for typical secondary growth, palms (coconut, taal) show anomalous secondary growth or primary thickening that increases trunk girth.",
            "Forgetting that banana has no seeds in cultivated varieties (parthenocarpy) but is still classified as a monocot angiosperm — classification is based on structural features, not just seed presence.",
        ],
        "practice_prompts": [
            "A farmer brings you two seedlings. One has a single cotyledon, fibrous roots, and parallel-veined leaves. The other has two cotyledons, a taproot, and net-veined leaves. Identify which is the monocot and which is the dicot. Give 3 examples of crop plants for each from Bangladesh.",
            "Compare a pine cone (gymnosperm) with a mango fruit (angiosperm). Where are the seeds located in each? Which provides better protection for the developing embryo and why?",
            "Explain how double fertilization works in angiosperms. What is the biological significance of endosperm formation? Why is the endosperm triploid (3n)?",
        ],
        "real_world_example": "Almost every food crop in Bangladesh is an angiosperm — dhan (rice, monocot) feeds 160 million Bangladeshis, paat (jute, dicot) was once the golden fiber earning foreign exchange, cha (tea, dicot) grows in the hills of Sylhet, and aam (mango, dicot) from Rajshahi is famous nationwide. Narikel (coconut, monocot) lines the coast of Cox\'s Bazar and Sundarbans. Bash (bamboo, monocot) is used for construction and furniture across rural Bangladesh. Understanding the monocot-dicot distinction helps agricultural scientists develop specific farming techniques — for example, many selective herbicides kill dicot weeds in monocot rice paddies by exploiting their structural and biochemical differences.",
    },

    # ══════════════════════════════════════════════════════════════
    # ══ BIOLOGY — Chapter 8: উদ্ভিদ টিস্যু (Plant Tissues) ══
    # ══════════════════════════════════════════════════════════════

    "bio1-08-01": {
        "title": "Plant Tissues — Meristematic, Simple, Complex (Xylem & Phloem)",
        "learning_objectives": [
            "Classify plant tissues into meristematic (apical, lateral, intercalary) and permanent (simple and complex) tissues",
            "Describe the structure and function of simple permanent tissues: parenchyma, collenchyma, and sclerenchyma",
            "Describe the structure, components, and function of xylem (tracheids, vessels, xylem fibers, xylem parenchyma) for water and mineral transport",
            "Describe the structure, components, and function of phloem (sieve tubes, companion cells, phloem fibers, phloem parenchyma) for food translocation",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: how does water travel from the roots of a tall coconut tree (30 meters!) all the way to the topmost leaf? And how does the sugar made in the leaves during photosynthesis travel DOWN to the roots? The answer lies in two specialized transport tissues — xylem and phloem. Just like blood vessels carry blood in your body, these tissues form the \'circulatory system\' of plants.",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Teach meristematic tissues first: undifferentiated, actively dividing cells with thin walls, dense cytoplasm, large nucleus, no vacuole. Types by position: apical meristem (root/shoot tips — primary growth, elongation), lateral meristem (vascular cambium, cork cambium — secondary growth, thickening), intercalary meristem (base of internodes — found in grasses/bamboo, that is why grass grows back after cutting!). Then teach simple permanent tissues: (1) Parenchyma — thin-walled, living, stores food, performs photosynthesis in mesophyll (chlorenchyma), stores air in aquatic plants (aerenchyma in water hyacinth/kochuripana). (2) Collenchyma — thickened at corners (angular) or surfaces, living, provides flexible support in young stems and petioles. (3) Sclerenchyma — thick-walled with lignin, dead at maturity, provides rigid mechanical support — two types: fibers (long, narrow — jute/paat fiber is sclerenchyma!) and sclereids/stone cells (short, isodiametric — hardness of narikel/coconut shell, pear fruit grit). Ask: why is jute fiber so strong? (Sclerenchyma fibers with heavy lignin deposition).",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Teach complex tissues in detail. XYLEM (water-conducting tissue, also called wood): (1) Tracheids — long, narrow, tapered ends, dead, lignified walls with pits — primitive (found in all vascular plants including gymnosperms). (2) Vessels (trachea) — shorter, wider, open ends (perforation plates), dead, more efficient — advanced (mainly in angiosperms). (3) Xylem fibers — dead, sclerenchyma type, mechanical support. (4) Xylem parenchyma — living, stores food and water. Xylem transport: water moves UP from roots to leaves by transpiration pull (cohesion-tension theory). Xylem is unidirectional. PHLOEM (food-conducting tissue): (1) Sieve tubes — living but no nucleus at maturity, end walls have sieve plates with pores. (2) Companion cells — living, have nucleus, connected to sieve tubes by plasmodesmata, provide metabolic support (companion cells are ABSENT in gymnosperms — they have albuminous cells instead). (3) Phloem fibers (bast fibers) — dead, mechanical support. (4) Phloem parenchyma — living, stores food. Phloem transport: food (mainly sucrose) moves from source (leaves) to sink (roots, fruits, growing tips) — bidirectional. Ask: which xylem element is more efficient at water transport — tracheids or vessels? Why? (Vessels — wider, open ends, less resistance).",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Comparison exercise: make a detailed table comparing xylem and phloem on: function, direction of transport, main conducting element, living/dead status of conducting elements, cell wall composition, associated cells, presence in gymnosperms vs angiosperms. Then classify: \'I am dead, lignified, and transport water upward\' — vessel/tracheid (xylem). \'I am alive, lack a nucleus, and have sieve plates\' — sieve tube (phloem). \'I am living, have a nucleus, and support the sieve tube\' — companion cell (phloem). Ask: a ring of xylem and phloem is visible in a dicot stem cross-section. Which is on the inner side and which on the outer side? (Xylem inner, phloem outer, with cambium between them).",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "Medical admission MCQ: \'Which of the following is a living component of xylem? (a) Tracheids (b) Vessels (c) Xylem fibers (d) Xylem parenchyma.\' Follow up: \'If the phloem of a tree is stripped in a ring around the trunk (girdling), predict what will happen. Where will sugars accumulate? What happens to the roots? Will the tree die immediately or slowly?\' (Sugars accumulate above the ring as phloem transport is blocked; roots starve and die; tree eventually dies — this is the classical Malpighi girdling experiment). Then: \'Explain the cohesion-tension theory of water transport in xylem. What role does transpiration, cohesion of water molecules (H-bonding), and adhesion to vessel walls play?\'",
            },
        ],
        "key_formulas": [
            "Meristematic tissue types: apical (primary growth — length), lateral (secondary growth — girth), intercalary (elongation at nodes — grasses)",
            "Simple tissues: parenchyma (storage, thin walls), collenchyma (flexible support, corner thickening), sclerenchyma (rigid support, lignified, dead — fibers and sclereids)",
            "Xylem components: tracheids (dead, primitive) + vessels (dead, advanced, open ends) + xylem fibers (dead) + xylem parenchyma (living)",
            "Phloem components: sieve tubes (living, no nucleus) + companion cells (living, has nucleus, absent in gymnosperms) + phloem fibers (dead) + phloem parenchyma (living)",
            "Xylem transport: unidirectional (root -> leaf), by transpiration pull/cohesion-tension; transports water + minerals",
            "Phloem transport: bidirectional (source -> sink), by pressure flow/Munch hypothesis; transports sucrose (organic food)",
        ],
        "common_mistakes": [
            "Saying all xylem cells are dead — xylem PARENCHYMA is living! Similarly, not all phloem cells are living — phloem FIBERS are dead. Students must know which specific cells in each tissue are living vs dead.",
            "Confusing tracheids and vessels — tracheids are long, narrow with tapered closed ends and pits (found in ALL vascular plants); vessels are shorter, wider with open perforation plates (mainly in angiosperms). Gymnosperms have tracheids but generally lack vessels (except Gnetum).",
            "Thinking phloem transport is unidirectional like xylem — phloem is BIDIRECTIONAL (source to sink), so sugars can move upward to growing buds or downward to roots depending on where the sink is.",
            "Forgetting companion cells are absent in gymnosperms — gymnosperms have albuminous cells instead, which perform a similar function. This is a frequently tested distinction.",
        ],
        "practice_prompts": [
            "A farmer cuts a ring of bark (which includes phloem) from around a mango tree trunk. Predict what happens above and below the ring over the next few weeks. Explain using your knowledge of phloem function. (Malpighi\'s girdling experiment).",
            "Compare tracheids and vessels in a table with at least 5 differences. Why are vessels considered more efficient? In which plant group are vessels generally absent?",
            "Explain how water reaches the top of a 30-meter-tall coconut tree against gravity without any pump. Describe the cohesion-tension theory, mentioning the roles of transpiration, root pressure, cohesion, and adhesion.",
        ],
        "real_world_example": "The jute fiber (paat) that made Bangladesh the \'Golden Fiber country\' is actually sclerenchyma fiber from the phloem region of the jute stem (bast fiber). When jute stems are retted (soaked in water for weeks), the softer tissues rot away, leaving behind the tough sclerenchyma fibers used for making rope, sacks, and now biodegradable bags. The wood of a mahogany or teak tree used in Bangladeshi furniture is actually secondary xylem — layers of dead xylem cells accumulated over years of secondary growth. The harder the wood (more lignin), the more valuable it is. When rubber tappers in Chittagong Hill Tracts cut into a rubber tree, they cut just deep enough to sever the phloem (where latex flows in specialized laticiferous tubes) without damaging the xylem — a practical application of plant tissue anatomy.",
    },

    # ══════════════════════════════════════════════════════════════
    # ══ BIOLOGY — Chapter 9: উদ্ভিদ শরীরতত্ত্ব (Plant Physiology) ══
    # ══════════════════════════════════════════════════════════════

    "bio1-09-01": {
        "title": "Photosynthesis — Light Reactions, Calvin Cycle & Factors",
        "learning_objectives": [
            "Write and explain the overall equation of photosynthesis: 6CO2 + 6H2O -> C6H12O6 + 6O2 (in presence of light and chlorophyll)",
            "Describe the light-dependent reactions (in thylakoid membranes): photolysis of water, electron transport chain, photophosphorylation (cyclic and non-cyclic), NADPH and ATP production",
            "Describe the light-independent reactions / Calvin cycle (in stroma): carbon fixation by RuBisCO, reduction of 3-PGA to G3P, regeneration of RuBP",
            "Explain factors affecting photosynthesis (light intensity, CO2 concentration, temperature) and Blackman\'s law of limiting factors",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: where does the food you eat ultimately come from? Even the mach (fish) you eat — it ate smaller organisms that ate algae. All food energy traces back to photosynthesis. Plants are the ultimate food factories. The equation 6CO2 + 6H2O -> C6H12O6 + 6O2 is arguably the most important chemical reaction on Earth. Why? (It produces ALL our food AND the oxygen we breathe!)",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Teach the light reactions (thylakoid membranes): (1) Photosystem II (P680) absorbs light -> water is split (photolysis: 2H2O -> 4H+ + 4e- + O2) — this is where O2 comes from. (2) Electrons pass through the electron transport chain (Plastoquinone -> Cytochrome b6f -> Plastocyanin). (3) At Cytochrome b6f, H+ ions are pumped into the thylakoid lumen, creating a proton gradient for ATP synthesis by ATP synthase (chemiosmosis/photophosphorylation). (4) Photosystem I (P700) re-energizes electrons -> passed via Ferredoxin to NADP+ reductase -> NADPH formed. This is NON-CYCLIC photophosphorylation (produces ATP + NADPH + O2). In CYCLIC photophosphorylation: only PSI involved, electrons cycle back, only ATP produced (no NADPH, no O2). Ask: why would a plant need cyclic photophosphorylation? (Calvin cycle needs more ATP than NADPH — 3ATP:2NADPH ratio).",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Teach the Calvin cycle (dark reactions/light-independent reactions, in stroma): (1) Carbon fixation: CO2 + RuBP (5C) --RuBisCO enzyme--> 2 molecules of 3-PGA (3C). RuBisCO is the most abundant protein on Earth! (2) Reduction: 3-PGA is reduced to G3P (glyceraldehyde-3-phosphate) using ATP and NADPH from light reactions. (3) Regeneration: 5 out of 6 G3P molecules are used to regenerate 3 RuBP (requires ATP). 1 G3P (out of 6) is the net product -> used to make glucose. To make 1 glucose: 6 turns of Calvin cycle, fixing 6 CO2, using 18 ATP and 12 NADPH. Then teach limiting factors: light intensity (increases rate until light saturation), CO2 concentration (normal 0.03%, increasing to 0.05% boosts rate), temperature (enzyme-dependent, optimum ~25-35 degrees C). Blackman\'s law: the rate of photosynthesis is limited by the factor that is nearest to its minimum value.",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Calculation problem: For the production of ONE molecule of glucose via the Calvin cycle, calculate: (a) How many CO2 molecules are fixed? (6) (b) How many turns of the Calvin cycle? (6) (c) How many ATP molecules used? (18) (d) How many NADPH molecules used? (12) (e) How many G3P molecules formed in total? (12) (f) How many G3P molecules used for RuBP regeneration? (10) (g) Net G3P output? (2, which combine to form 1 glucose). Then conceptual question: a student covers a geranium leaf with black paper for 48 hours, then tests for starch with iodine. Predict and explain the result. (No starch — no photosynthesis without light; existing starch was used up in respiration).",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "Medical admission MCQ: \'The oxygen released during photosynthesis comes from: (a) CO2 (b) H2O (c) C6H12O6 (d) Both CO2 and H2O.\' (Answer: H2O — proven by Hill\'s experiment using isotopic oxygen O-18). Follow up: \'Draw and explain the Z-scheme of electron transport in the light reactions, showing both PSI and PSII, the electron carriers, and where ATP and NADPH are produced.\' Then: \'A rice field in Bangladesh has adequate water and sunlight. The farmer adds extra CO2 by burning husk at the field edge. Explain using the law of limiting factors whether this would increase rice yield and under what conditions CO2 would no longer be the limiting factor.\'",
            },
        ],
        "key_formulas": [
            "Overall equation: 6CO2 + 6H2O --light, chlorophyll--> C6H12O6 + 6O2",
            "Photolysis of water (Hill reaction): 2H2O -> 4H+ + 4e- + O2 (occurs at PSII, O2 comes from water)",
            "Non-cyclic photophosphorylation: H2O -> PSII -> PQ -> Cyt b6f -> PC -> PSI -> Fd -> NADP+ reductase -> NADPH (produces ATP + NADPH + O2)",
            "Cyclic photophosphorylation: PSI -> Fd -> Cyt b6f -> PC -> PSI (produces only ATP, no NADPH, no O2)",
            "Calvin cycle per 1 glucose: 6CO2 + 18ATP + 12NADPH -> C6H12O6 + 18ADP + 12NADP+ + 6H2O",
            "RuBisCO reaction: CO2 + RuBP (5C) -> 2 x 3-PGA (3C) — carbon fixation step",
            "Blackman\'s law of limiting factors: rate limited by the factor at its minimum",
        ],
        "common_mistakes": [
            "Saying O2 comes from CO2 — the oxygen released in photosynthesis comes from WATER (H2O), not CO2. This was proven by Hill\'s experiment and later by Ruben and Kamen using O-18 isotope.",
            "Calling the Calvin cycle \'dark reactions\' and thinking it occurs in the dark — it does NOT require darkness; it simply does not directly need light. It needs ATP and NADPH which come from light reactions, so it occurs simultaneously with light reactions during the day.",
            "Confusing the Calvin cycle stoichiometry — it takes 6 turns (fixing 6 CO2) to produce 1 net glucose. Students often say 1 turn = 1 glucose. Each turn produces 2 G3P, but 10 out of 12 G3P are recycled to regenerate RuBP.",
            "Confusing cyclic and non-cyclic photophosphorylation — non-cyclic involves both PSI and PSII, produces ATP + NADPH + O2; cyclic involves only PSI, produces only ATP. Students must know when and why the plant uses each.",
        ],
        "practice_prompts": [
            "Trace the path of a carbon atom from atmospheric CO2 to glucose, naming each intermediate in the Calvin cycle. At which step is ATP used? At which step is NADPH used?",
            "Explain the Z-scheme of photosynthetic electron transport. Why is it called a Z-scheme? Include the roles of PSII (P680), PSI (P700), and all electron carriers.",
            "A greenhouse farmer in Jessore wants to maximize tomato yield. Currently light and water are abundant. Explain how increasing CO2 concentration from 0.03% to 0.1% would affect photosynthesis rate. At what point would CO2 no longer be the limiting factor?",
        ],
        "real_world_example": "Bangladesh\'s entire rice agriculture depends on photosynthesis. The IRRI and BRRI are researching C4 rice — engineering the more efficient C4 photosynthesis pathway (used by sugarcane and maize) into rice (which is a C3 plant) to boost yields by 50%. Currently, rice loses up to 30% efficiency due to photorespiration (RuBisCO fixing O2 instead of CO2 in hot conditions). In Bangladeshi tea gardens of Sylhet, tea bushes are often planted under shade trees because tea performs better at moderate light intensity — too much direct sunlight can cause photoinhibition and damage the photosynthetic machinery.",
    },

    "bio1-09-02": {
        "title": "Respiration and Transpiration",
        "learning_objectives": [
            "Describe the complete process of aerobic cellular respiration: glycolysis (cytoplasm), pyruvate oxidation (mitochondrial matrix), Krebs cycle (matrix), and oxidative phosphorylation/ETC (inner mitochondrial membrane)",
            "Calculate the net ATP yield from one glucose molecule (theoretical maximum 36-38 ATP) and explain the role of NADH and FADH2 as electron carriers",
            "Compare aerobic and anaerobic respiration (fermentation) — alcoholic fermentation in yeast (ethanol + CO2) and lactic acid fermentation in muscle",
            "Explain transpiration (types, mechanism, significance), stomatal opening/closing mechanism (K+ ion theory), and factors affecting transpiration rate",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: you eat bhat (rice) for energy, but how does your body actually extract energy from glucose? You cannot burn rice inside your body like burning wood! The process of cellular respiration breaks glucose down step by step, capturing energy in ATP — the energy currency of the cell. Meanwhile, plants lose over 90% of absorbed water through transpiration from leaves. Why would they \'waste\' so much water?",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Teach glycolysis (Embden-Meyerhof pathway, in cytoplasm): Glucose (6C) -> 2 Pyruvate (3C). Net gain: 2 ATP (substrate-level phosphorylation) + 2 NADH. Key steps: glucose is phosphorylated (uses 2 ATP), split into two 3C molecules, oxidized to pyruvate (produces 4 ATP and 2 NADH). Net: 2 ATP. Glycolysis is ANAEROBIC (does not need oxygen) and is common to both aerobic and anaerobic respiration. Then: if O2 is available -> pyruvate enters mitochondria. Pyruvate decarboxylation (link reaction): pyruvate (3C) -> acetyl CoA (2C) + CO2 + NADH (occurs in mitochondrial matrix). Then teach the Krebs cycle (citric acid cycle, in matrix): Acetyl CoA (2C) + OAA (4C) -> Citrate (6C) -> through a series of reactions, 2 CO2 are released, regenerating OAA. Per turn: 3 NADH + 1 FADH2 + 1 GTP (=1 ATP). Since 1 glucose gives 2 acetyl CoA, the Krebs cycle turns TWICE per glucose. Ask: where is CO2 produced in respiration? (Pyruvate decarboxylation and Krebs cycle — NOT in ETC!)",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Teach ETC and oxidative phosphorylation (inner mitochondrial membrane): NADH and FADH2 donate electrons to the electron transport chain (Complex I -> Ubiquinone -> Complex III -> Cytochrome c -> Complex IV -> O2). As electrons flow, protons (H+) are pumped into the intermembrane space, creating a proton gradient. H+ flows back through ATP synthase (chemiosmosis) -> ATP is produced. O2 is the final electron acceptor -> combines with H+ and electrons to form H2O. This is WHY we breathe oxygen! ATP yield: each NADH -> ~2.5 ATP, each FADH2 -> ~1.5 ATP. Total per glucose: Glycolysis (2 ATP + 2 NADH), Link reaction (2 NADH), Krebs (2 ATP + 6 NADH + 2 FADH2). Total NADH = 10 x 2.5 = 25 ATP; FADH2 = 2 x 1.5 = 3 ATP; direct ATP/GTP = 4. Grand total ~ 30-32 ATP (or 36-38 by older counting). Then teach anaerobic respiration: in absence of O2, pyruvate is not sent to mitochondria. Alcoholic fermentation (yeast): pyruvate -> ethanol + CO2 (used in bread, beer). Lactic acid fermentation (muscles): pyruvate -> lactate (causes muscle cramp during intense exercise). Only 2 ATP per glucose in anaerobic — much less efficient. Then teach transpiration: loss of water vapor from aerial parts (mainly leaves via stomata). Types: stomatal (90%), cuticular, lenticular. Stomatal mechanism: K+ ion theory — light triggers K+ influx into guard cells -> water enters by osmosis -> guard cells swell and open stomatal pore. In dark, K+ leaves -> water exits -> stomata close. Significance of transpiration: cooling effect (evaporative cooling), creates transpiration pull for water transport in xylem (cohesion-tension), helps mineral absorption and distribution. Factors: light, temperature, humidity, wind, CO2 concentration.",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "ATP accounting exercise: for the complete aerobic oxidation of 1 glucose molecule, make a table showing ATP production at each stage. Stage: Glycolysis — 2 ATP + 2 NADH (= 2 + 5 = 7). Link reaction — 2 NADH (= 5). Krebs cycle (x2 turns) — 2 GTP + 6 NADH + 2 FADH2 (= 2 + 15 + 3 = 20). Grand total: ~30-32 ATP. Then comparison: aerobic (glucose -> CO2 + H2O + 30-32 ATP) vs anaerobic alcoholic (glucose -> ethanol + CO2 + 2 ATP) vs lactic acid (glucose -> lactate + 2 ATP). Ask: why is aerobic respiration so much more efficient? (ETC extracts energy from NADH and FADH2 that is wasted in fermentation). For transpiration: draw and label a stomatal apparatus showing guard cells, subsidiary cells, and stomatal pore. Explain the K+ ion mechanism of stomatal opening.",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "Medical admission MCQ: \'The net gain of ATP from glycolysis is: (a) 4 (b) 2 (c) 8 (d) 38.\' Follow up: \'Cyanide is a deadly poison that blocks Complex IV (cytochrome oxidase) of the ETC. Explain step by step what happens when cyanide enters a cell: why does ATP production stop? Why does the cell die? Can glycolysis still occur?\' (Yes, but only 2 ATP — not enough to sustain life). Then: \'A farmer notices that his rice plants wilt at midday even though the soil is moist. Explain this using the concept of transpiration exceeding absorption. What is the role of root pressure vs transpiration pull? Why does temporary wilting recover by evening?\'",
            },
        ],
        "key_formulas": [
            "Aerobic respiration overall: C6H12O6 + 6O2 -> 6CO2 + 6H2O + ~30-32 ATP (energy)",
            "Glycolysis: Glucose (6C) -> 2 Pyruvate (3C) + 2 ATP + 2 NADH (cytoplasm, anaerobic)",
            "Pyruvate decarboxylation: Pyruvate (3C) -> Acetyl CoA (2C) + CO2 + NADH (mitochondrial matrix)",
            "Krebs cycle (per turn): Acetyl CoA + OAA -> Citrate -> ... -> OAA + 2CO2 + 3 NADH + 1 FADH2 + 1 GTP (x2 turns per glucose)",
            "ETC: NADH -> 2.5 ATP; FADH2 -> 1.5 ATP; O2 = final electron acceptor -> H2O",
            "Alcoholic fermentation: Pyruvate -> Ethanol + CO2 (by yeast/Saccharomyces; used in baking/brewing)",
            "Lactic acid fermentation: Pyruvate -> Lactate (in muscles during intense exercise; by Lactobacillus in doi/yogurt)",
            "Transpiration pull: cohesion-tension theory — transpiration from leaves pulls water column up xylem",
            "Stomatal opening: light -> K+ into guard cells -> osmotic water entry -> guard cells swell -> pore opens",
        ],
        "common_mistakes": [
            "Saying glycolysis produces 4 ATP — it PRODUCES 4 ATP but USES 2 ATP, so NET gain is only 2 ATP. Students must distinguish gross from net ATP production.",
            "Thinking O2 is needed for glycolysis — glycolysis is ANAEROBIC and occurs in the cytoplasm. O2 is only needed for the ETC (oxidative phosphorylation) in mitochondria.",
            "Confusing where each stage occurs — Glycolysis: cytoplasm; Pyruvate decarboxylation and Krebs cycle: mitochondrial matrix; ETC: inner mitochondrial membrane. Students often say Krebs cycle occurs in the cristae (it occurs in the matrix).",
            "Thinking transpiration is a waste of water — transpiration is essential for creating the pulling force (transpiration pull) for water transport, for evaporative cooling of leaves, and for mineral transport. Without transpiration, water and minerals could not reach tall tree canopies.",
        ],
        "practice_prompts": [
            "Trace the complete oxidation of one glucose molecule through all stages of aerobic respiration, showing ATP, NADH, FADH2, and CO2 produced at each stage. Where is the most ATP generated?",
            "A yeast culture is placed in a sugar solution in a sealed flask. Initially it respires aerobically. As oxygen is used up, what switch occurs? Write the equation for alcoholic fermentation. Why does bread dough rise? Why does the yeast eventually stop fermenting?",
            "Explain why plants transpire mostly during the day but respire 24 hours a day. Draw a graph showing how net CO2 exchange changes over a 24-hour cycle. At what point is the compensation point reached (photosynthesis = respiration)?",
        ],
        "real_world_example": "In Bangladesh, alcoholic fermentation by yeast is used to make tari (palm wine) from the sap of tal/taal (palmyra palm) and khejur (date palm) — the CO2 makes it fizzy and the ethanol gives the kick. Lactic acid fermentation by Lactobacillus converts milk to doi (yogurt) and mishti doi (sweetened yogurt, a Bengali specialty). In rice paddies, waterlogged soil has no oxygen, so rice roots perform anaerobic respiration, and the soil bacteria produce methane (CH4) — this is why rice paddies are a significant source of greenhouse gas globally. Bangladesh\'s millions of hectares of rice paddies contribute to methane emissions. Tea garden workers in Sylhet time plucking for early morning when stomata are just opening and transpiration is low — leaves retain more moisture and weigh more, which means better pay per kilogram!",
    },

    # ══════════════════════════════════════════════════════════════
    # ══ BIOLOGY — Chapter 10: উদ্ভিদের জনন (Plant Reproduction) ══
    # ══════════════════════════════════════════════════════════════

    "bio1-10-01": {
        "title": "Plant Reproduction — Pollination, Double Fertilization & Fruit Formation",
        "learning_objectives": [
            "Describe the structure of a typical flower (calyx, corolla, androecium, gynoecium) and distinguish between complete and incomplete flowers",
            "Explain pollination types (self-pollination vs cross-pollination) and adaptations for each (wind, insect, water pollination with examples)",
            "Describe the process of double fertilization unique to angiosperms: one sperm + egg -> zygote (2n), other sperm + polar nuclei -> endosperm (3n)",
            "Explain post-fertilization changes: ovule -> seed, ovary -> fruit, and types of fruits (simple, aggregate, composite) with Bangladeshi examples",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: have you seen bees buzzing around jaba (hibiscus) or shiuli flowers? Or noticed the fine powder (pollen) that falls from a shimul tree flower? Why do flowers exist — just to look beautiful? No! Flowers are the reproductive organs of angiosperms. The bright colors, sweet nectar, and fragrance all serve one purpose: getting pollen from one flower to another. Let us learn how plants reproduce and how every aam (mango), litchi, and kathal (jackfruit) you eat is actually a fertilized ovary!",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Teach flower structure: (1) Calyx (sepals — protect bud), (2) Corolla (petals — attract pollinators), (3) Androecium (stamens = filament + anther; anther contains pollen sacs that produce pollen grains/microspores), (4) Gynoecium (pistil = stigma + style + ovary; ovary contains ovules with embryo sac/megaspore). If a flower has all 4 whorls, it is complete. If it has both stamens and pistil, it is bisexual/perfect (e.g., jaba/hibiscus, rose). If only stamens = staminate/male; if only pistil = pistillate/female (e.g., lau/gourd, kumra/pumpkin have separate male and female flowers on same plant — monoecious). Then teach pollination: transfer of pollen from anther to stigma. Self-pollination: same flower or same plant (ensures reproduction but no genetic variation). Cross-pollination: different plant of same species (produces genetic variation). Adaptations: insect pollination (entomophily) — bright colored, scented, nectar-producing (jaba, rose, mustard/shorishe); wind pollination (anemophily) — small, no color/scent, light/abundant pollen, feathery stigma (rice/dhan, wheat, corn/bhutta, grass); water pollination (hydrophily) — rare, in aquatic plants (Vallisneria, Hydrilla). Ask: is rice pollinated by insects or wind? (Wind — that is why rice flowers are small and inconspicuous).",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Teach double fertilization in detail — this is the MOST important topic in plant reproduction for medical admission. After pollination, pollen grain germinates on stigma -> pollen tube grows down through style to ovary -> enters ovule through micropyle. The pollen tube has 2 male gametes (sperm cells) and 1 tube nucleus. Inside the ovule, the embryo sac has: egg cell (n) + 2 synergids (at micropylar end), 3 antipodal cells (at chalazal end), and 2 polar nuclei in central cell. DOUBLE FERTILIZATION: First sperm (n) + Egg (n) -> Zygote (2n) -> develops into embryo. Second sperm (n) + 2 polar nuclei (n + n) -> Primary endosperm nucleus (3n) -> develops into endosperm (nutrition for embryo). This is UNIQUE to angiosperms — does not occur in gymnosperms! Discovered by Nawaschin (1898). Post-fertilization: ovule -> seed (seed coat from integuments, embryo from zygote, endosperm from PEN). Ovary -> fruit (ovary wall becomes pericarp — epicarp, mesocarp, endocarp). Ask: in a mango, which part is the seed? Which part is the fruit? (The hard stone/athi is the endocarp, the fleshy part is mesocarp, the skin is epicarp; the seed is inside the stone).",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Identification exercise using Bangladeshi fruits: (1) Aam (mango) — drupe (single seed with stony endocarp). (2) Kathal (jackfruit) — composite/multiple fruit (from entire inflorescence). (3) Kola (banana) — berry (seedless in cultivated varieties — parthenocarpy). (4) Litchi — nut-like drupe with fleshy aril. (5) Narikel (coconut) — drupe (coir = mesocarp, shell = endocarp, white flesh = endosperm, coconut water = liquid endosperm). (6) Dhan (rice grain) — caryopsis (pericarp fused with seed coat). Ask students to identify the edible part in each: mango — mesocarp; coconut — endosperm; rice — endosperm (the white rice we eat is starchy endosperm!); jackfruit — perianth and seeds. Then: explain why the banana is seedless. (Parthenocarpy — fruit develops without fertilization; cultivated banana is triploid 3n, so meiosis fails and seeds do not develop).",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "Medical admission MCQ: \'Double fertilization involves: (a) Fusion of two eggs with two sperms (b) Fusion of one sperm with egg and another sperm with secondary nucleus (c) Fusion of two polar nuclei (d) Fusion of egg with polar nuclei.\' Follow up: \'Explain what happens if pollination occurs but one of the two sperms fails to fuse. Can a seed still develop without endosperm formation? (Generally no — endosperm provides nutrition for embryo development; without it, the seed usually aborts).\' Then: \'A mango farmer in Rajshahi wants to ensure good mango production. Explain the role of pollinators. What happens if the mango orchard is treated with pesticides that kill bees and flies? Suggest alternatives (integrated pest management, maintaining pollinator habitats).\' Finally: \'Explain why coconut water is considered liquid endosperm. What is the ploidy of coconut water? (3n — triploid, like all endosperm in angiosperms).\'",
            },
        ],
        "key_formulas": [
            "Flower structure: Calyx (sepals) + Corolla (petals) + Androecium (stamens: filament + anther) + Gynoecium (pistil: stigma + style + ovary with ovules)",
            "Pollination types: self (autogamy) vs cross (allogamy/xenogamy); agents — wind (anemophily), insect (entomophily), water (hydrophily), bird (ornithophily)",
            "Double fertilization: 1st sperm (n) + egg (n) -> zygote (2n) -> embryo; 2nd sperm (n) + 2 polar nuclei (n+n) -> PEN (3n) -> endosperm",
            "Post-fertilization: ovule -> seed (integuments -> seed coat, zygote -> embryo, PEN -> endosperm); ovary -> fruit (ovary wall -> pericarp)",
            "Endosperm is triploid (3n) — formed from fusion of one sperm nucleus with two polar nuclei",
            "Parthenocarpy: fruit development without fertilization (seedless fruits — banana, seedless watermelon)",
            "Types of fruits: simple (from single ovary — mango/drupe, tomato/berry), aggregate (from multiple carpels of one flower — custard apple/ata), composite/multiple (from inflorescence — jackfruit/kathal, pineapple/anaros)",
        ],
        "common_mistakes": [
            "Confusing pollination with fertilization — pollination is merely the transfer of pollen to stigma (an external event). Fertilization is the fusion of gametes inside the ovule (internal event). Pollination can occur without fertilization (incompatible pollen, for example).",
            "Forgetting that endosperm is 3n (triploid) — one sperm nucleus (n) fuses with TWO polar nuclei (n + n) to give 3n. Students often say 2n. The 3n endosperm is a key distinguishing feature of angiosperms.",
            "Thinking the fruit is the seed — in a mango, the stone/athi is NOT the seed; it is the endocarp (inner layer of the fruit). The actual seed is inside the stone. Similarly, the rice grain\'s white part we eat is endosperm, not the whole seed.",
            "Confusing wind-pollinated and insect-pollinated flowers — wind-pollinated flowers (rice, wheat, corn) are small, dull, unscented with abundant light pollen and feathery stigmas. Insect-pollinated flowers (mustard, rose, hibiscus) are large, colorful, scented with sticky pollen and nectar. Students mix up these adaptations.",
        ],
        "practice_prompts": [
            "Draw a labeled diagram of the embryo sac (female gametophyte) of an angiosperm showing all 7 cells and 8 nuclei. Describe the role of each cell type (egg, synergids, antipodals, central cell) during fertilization.",
            "Trace the path of a pollen grain from the time it lands on the stigma to the completion of double fertilization inside the ovule. Name all structures encountered along the way.",
            "A Rajshahi mango farmer and a Dinajpur rice farmer both need successful pollination for their crops. Compare the pollination mechanisms in mango (insect-pollinated) and rice (wind-pollinated). What adaptations does each flower have for its pollination method?",
        ],
        "real_world_example": "Every grain of rice you eat is a product of double fertilization — the starchy white part (endosperm, 3n) nourished the rice embryo, and now it nourishes you. The Rajshahi mango is famous because the warm, dry pre-monsoon climate is perfect for insect pollinators like flies and bees to visit mango flowers. Kathal (jackfruit), the national fruit of Bangladesh, is a composite fruit formed from an entire female inflorescence — hundreds of individual fruits fused together. The narikel (coconut) of coastal Bangladesh is a drupe where we eat the endosperm (white flesh and water). Bangladeshi mustard fields (shorishe khet) turn bright yellow to attract bees for cross-pollination — and beekeepers place hives near these fields to produce mustard honey, a dual agricultural benefit. Seedless kola (banana) is triploid and parthenocarpic — the fruit develops without fertilization, which is why cultivated bananas have no seeds.",
    },

    # ══ CHEMISTRY, MATH — Additional Chapters ══
    "chem1-03-02": {
        "title": "Periodic Trends: Radius, IE, EA & Electronegativity",
        "learning_objectives": [
            "Explain trends in atomic radius, ionic radius across periods and down groups",
            "Compare ionization energies and identify anomalies (Be>B, N>O)",
            "Distinguish electron affinity and electronegativity",
            "Use periodic trends to predict chemical behavior and bond type",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: which atom is bigger — Na or Cl? They are in the same period. What about Na or K? Why does size change across and down the table?",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Teach atomic radius trend: decreases across a period (more protons, same shell), increases down a group (more shells). Ask: why is Na+ much smaller than Na, but Cl^- is larger than Cl?",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Teach ionization energy trends and anomalies. IE increases across a period but B < Be (2p1 easier to remove than 2s2) and O < N (paired 2p4 electron easier than half-filled 2p3). Explain with orbital diagrams.",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Arrange in order of increasing first ionization energy: Na, Mg, Al, Si, P. Explain any anomalies. Then arrange O, S, Se in order of increasing electron affinity.",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "BUET-level: The first ionization energies (kJ/mol) of four consecutive elements are: 786, 1086, 1402, 1314. Identify the elements and explain why the 4th value is lower than the 3rd. Also predict which of these elements forms the most stable +2 ion.",
            },
        ],
        "key_formulas": [
            "Atomic radius: decreases L->R across period, increases top->bottom in group",
            "Ionic radius: cation < atom < anion (for same element)",
            "Isoelectronic species: more protons = smaller radius (O^2- > F^- > Na+ > Mg^2+)",
            "IE1 < IE2 < IE3 ... (successive IEs always increase)",
            "Electronegativity (Pauling): F(4.0) > O(3.5) > N(3.0) > Cl(3.0)",
            "Electron affinity: most negative (exothermic) for halogens; noble gases ~0",
        ],
        "common_mistakes": [
            "Thinking atomic radius always decreases across a period without exception — actually d-block elements show very small changes due to poor shielding by d electrons",
            "Confusing electron affinity with electronegativity — EA is energy released when an atom gains one electron (measurable), electronegativity is the tendency to attract shared electrons in a bond (relative scale)",
            "Not recognizing IE anomalies: Be > B and N > O due to subshell stability — this is a very common BUET/DU admission question",
        ],
        "practice_prompts": [
            "Arrange the following isoelectronic species in order of increasing ionic radius: Na+, F^-, O^2-, Mg^2+, N^3-. Explain your reasoning.",
            "The second ionization energy of Na is dramatically higher than its first IE, but for Mg the jump is less dramatic. Explain using electron configuration.",
            "Which has a more negative electron affinity: Cl or F? Explain why, despite F being more electronegative. (Hint: consider the small size of the 2p orbital)",
        ],
        "real_world_example": "The reason table salt (NaCl) forms so readily is explained by periodic trends. Na has very low ionization energy (easy to lose its electron) and Cl has very high electron affinity (eager to gain one). This huge difference in electronegativity across period 3 drives the formation of ionic bonds — the same chemistry that preserves fish (shutki) in Cox's Bazar.",
    },

    # ══ HIGHER MATHEMATICS — Chapter 1: সেট ও ফাংশন (Sets & Functions) ══
    "hm1-01-01": {
        "title": "Sets, Subsets & Set Operations",
        "learning_objectives": [
            "Define sets using roster and set-builder notation and identify types (finite, infinite, empty, universal)",
            "Determine subsets, proper subsets, and power sets of a given set",
            "Perform union, intersection, difference, and complement operations",
            "Apply De Morgan's laws and verify results using Venn diagrams",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: if I say 'the set of all rivers in Bangladesh', how would you list its elements? What if I say 'the set of all even numbers' — can you list them all?",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Explain roster vs set-builder notation. Ask student to write {x ∈ ℕ : x < 6} in roster form and vice versa. Introduce empty set ∅ and universal set U.",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Teach subset (⊆), proper subset (⊂), and power set P(A). Ask: if A = {1, 2, 3}, how many elements does P(A) have? Then introduce A ∪ B, A ∩ B, A − B, and A' with Venn diagrams.",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Problem: Let U = {1,2,3,...,10}, A = {1,2,3,4,5}, B = {3,4,5,6,7}. Find A ∪ B, A ∩ B, A − B, A', and verify (A ∪ B)' = A' ∩ B' (De Morgan's law).",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "BUET-level: If n(A) = 40, n(B) = 35, n(A ∪ B) = 60, n(U) = 80, find n(A ∩ B), n(A' ∩ B'), and n(A − B). Ask student to draw the Venn diagram with cardinalities in each region.",
            },
        ],
        "key_formulas": [
            "|P(A)| = 2ⁿ where n = |A|",
            "n(A ∪ B) = n(A) + n(B) − n(A ∩ B)",
            "(A ∪ B)' = A' ∩ B' and (A ∩ B)' = A' ∪ B' — De Morgan's laws",
            "n(A ∪ B ∪ C) = n(A) + n(B) + n(C) − n(A∩B) − n(B∩C) − n(A∩C) + n(A∩B∩C)",
        ],
        "common_mistakes": [
            "Confusing ∈ (element of) with ⊆ (subset of) — e.g., writing {1} ∈ {1,2} instead of {1} ⊆ {1,2}",
            "Forgetting that ∅ is a subset of every set, and every set is a subset of itself",
            "Errors in De Morgan's law — swapping union and intersection without also taking complements",
        ],
        "practice_prompts": [
            "If A = {a, b, c}, list all subsets of A. How many are proper subsets?",
            "In a class of 100 students, 60 take Physics, 50 take Math, 20 take both. How many take neither?",
            "Prove using set algebra that A − (B ∩ C) = (A − B) ∪ (A − C).",
        ],
        "real_world_example": "Think of mobile phone plans in Bangladesh — Grameenphone's 4G coverage area is set A, Robi's is set B. The intersection A ∩ B is where both have 4G. The union A ∪ B is total 4G coverage. Areas with no coverage at all are (A ∪ B)'.",
    },

    "hm1-01-02": {
        "title": "Functions, Domain & Range",
        "learning_objectives": [
            "Define a function as a special relation and distinguish from general relations",
            "Determine domain, co-domain, and range of a function",
            "Classify functions as one-one (injective), onto (surjective), and bijective",
            "Compute composite functions (f∘g) and inverse functions (f⁻¹)",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: if every student in your class is assigned exactly one roll number, is this a function? What if two students share the same roll number — is it still a function from students to roll numbers?",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Define function f: A → B as a relation where every element of A maps to exactly one element of B. Explain domain, co-domain, range. Ask: if f(x) = √(x−2), what is the domain?",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Teach one-one, onto, bijective with arrow diagrams. Then introduce composite function: if f(x) = 2x+1 and g(x) = x², find (f∘g)(x) and (g∘f)(x). Ask: are they equal?",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Problem: f(x) = (3x−2)/(x+1). Find domain of f, then find f⁻¹(x). Verify that f(f⁻¹(x)) = x.",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "BUET-level: Let f: ℝ→ℝ, f(x) = x² − 4x + 3. Find the range of f. Is f one-one? If we restrict domain to [2, ∞), find f⁻¹(x) and state its domain.",
            },
        ],
        "key_formulas": [
            "Domain of f(x) = √(g(x)) requires g(x) ≥ 0",
            "Domain of f(x) = 1/g(x) requires g(x) ≠ 0",
            "(f∘g)(x) = f(g(x))",
            "f⁻¹ exists iff f is bijective; solve y = f(x) for x to get f⁻¹(y)",
        ],
        "common_mistakes": [
            "Confusing co-domain with range — range is the actual output set, co-domain is the declared target set",
            "Assuming f∘g = g∘f — composite functions are generally not commutative",
            "Forgetting to check domain restrictions when finding inverse (e.g., for quadratics, must restrict domain first)",
        ],
        "practice_prompts": [
            "Find the domain and range of f(x) = 1/(x² − 9).",
            "If f(x) = 2x + 3 and g(x) = (x − 3)/2, show that f and g are inverses of each other.",
            "Is f(x) = |x| one-one? Is it onto when f: ℝ → ℝ? What about f: ℝ → [0, ∞)?",
        ],
        "real_world_example": "Think of your National ID card system — each citizen maps to exactly one NID number (function). If no two people share an NID, it is one-one. If every possible NID is assigned, it is onto. Bangladesh's NID is designed to be bijective — a perfect one-to-one correspondence.",
    },

    # ══ HIGHER MATHEMATICS — Chapter 2: বীজগাণিতিক রাশি (Algebraic Expressions) ══
    "hm1-02-01": {
        "title": "Polynomials & Factoring",
        "learning_objectives": [
            "Classify polynomials by degree and number of terms",
            "Apply Factor Theorem and Remainder Theorem to find factors and remainders",
            "Factor polynomials using grouping, identities, and synthetic division",
            "Solve polynomial equations and find relationships between roots and coefficients",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: what is the remainder when you divide x³ − 3x² + 2x − 5 by (x − 1)? Can you guess without doing long division?",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Teach Remainder Theorem: f(a) = remainder when f(x) ÷ (x−a). Then Factor Theorem: (x−a) is a factor iff f(a) = 0. Ask student to check if (x−2) is a factor of x³ − 6x² + 11x − 6.",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Demonstrate synthetic division to factor x³ − 6x² + 11x − 6 completely. Teach sum/product of roots: for ax² + bx + c = 0, α+β = −b/a, αβ = c/a. Extend to cubic equations.",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Problem: Factor 2x³ + x² − 13x + 6 completely. Then find all roots. Verify using sum and product of roots.",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "BUET-level: If α, β are roots of x² − 5x + 3 = 0, find the value of α³ + β³ and form the equation whose roots are α² and β². No calculator — use identities only.",
            },
        ],
        "key_formulas": [
            "Remainder Theorem: f(x) ÷ (x−a) gives remainder f(a)",
            "Factor Theorem: (x−a) | f(x) ⟺ f(a) = 0",
            "For ax² + bx + c = 0: α+β = −b/a, αβ = c/a",
            "α³ + β³ = (α+β)³ − 3αβ(α+β)",
            "For ax³ + bx² + cx + d = 0: α+β+γ = −b/a, αβ+βγ+γα = c/a, αβγ = −d/a",
        ],
        "common_mistakes": [
            "Sign error in Remainder Theorem — evaluating f(a) when divisor is (x−a), not (x+a)",
            "Forgetting the negative sign in sum of roots: α+β = −b/a (not +b/a)",
            "Incomplete factoring — stopping at one factor instead of factoring the remaining quadratic",
        ],
        "practice_prompts": [
            "Use the Factor Theorem to show (x + 3) is a factor of x³ + 27. Then factor completely.",
            "If α, β are roots of 2x² − 7x + 5 = 0, find 1/α + 1/β without solving for α, β.",
            "Find k if (x − 2) is a factor of x³ − kx² + 5x + 2.",
        ],
        "real_world_example": "When engineers at Padma Bridge calculated load distribution across supports, they used polynomial equations where the roots represent critical stress points. Factoring tells them exactly where the structure needs reinforcement.",
    },

    "hm1-02-02": {
        "title": "Partial Fractions",
        "learning_objectives": [
            "Decompose proper rational expressions into partial fractions with linear factors",
            "Handle repeated linear factors in partial fraction decomposition",
            "Decompose expressions with irreducible quadratic factors",
            "Convert improper fractions to proper form before decomposition",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: you know how to add 1/(x+1) + 2/(x−1) into a single fraction. Can you reverse the process? Given (3x−1)/((x+1)(x−1)), can you break it back into simpler fractions?",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Teach the general rule: P(x)/((x−a)(x−b)) = A/(x−a) + B/(x−b). Show the cover-up method and the method of equating coefficients. Ask student to decompose (5x+3)/((x+1)(x+2)).",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Handle repeated factors: P(x)/(x−a)² = A/(x−a) + B/(x−a)². Then irreducible quadratic: P(x)/((x−a)(x²+bx+c)) = A/(x−a) + (Bx+C)/(x²+bx+c). Solve an example of each type.",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Problem: Decompose (3x² + 5x + 2)/((x+1)²(x+2)) into partial fractions. Verify by recombining.",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "BUET-level: Decompose (x⁴ + 1)/(x(x² + 1)²) into partial fractions. Note: check if it is proper first. Then decompose handling the repeated irreducible quadratic factor.",
            },
        ],
        "key_formulas": [
            "P(x)/((x−a)(x−b)) = A/(x−a) + B/(x−b)",
            "P(x)/(x−a)ⁿ = A₁/(x−a) + A₂/(x−a)² + ... + Aₙ/(x−a)ⁿ",
            "For irreducible (ax²+bx+c): numerator is (Ax+B), not just A",
            "If degree(numerator) ≥ degree(denominator), do polynomial long division first",
        ],
        "common_mistakes": [
            "Using A/(x²+1) instead of (Ax+B)/(x²+1) for irreducible quadratic factors",
            "Forgetting to do long division when the fraction is improper (degree of numerator ≥ denominator)",
            "Arithmetic errors when equating coefficients — not checking the answer by recombining fractions",
        ],
        "practice_prompts": [
            "Decompose (2x + 3)/((x − 1)(x + 2)) into partial fractions.",
            "Find the partial fraction form of (x² + 1)/((x − 1)²(x + 1)).",
            "Decompose (x³ + x + 1)/(x²(x² + 1)). Is this proper or improper?",
        ],
        "real_world_example": "Partial fractions are like breaking a mixed curry into its individual spices — you can taste the whole dish, but to understand (or integrate) it, you need to separate each component. This technique is essential for solving differential equations used in circuit analysis at BUET EEE.",
    },

    # ══ HIGHER MATHEMATICS — Chapter 3: জ্যামিতি (Geometry / Coordinate Geometry) ══
    "hm1-03-01": {
        "title": "Straight Lines: Distance & Section Formulas",
        "learning_objectives": [
            "Apply the distance formula between two points in 2D",
            "Use section formula to find internal and external division points",
            "Calculate area of a triangle given three vertices",
            "Determine collinearity of three points using the area method",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: if you are at Motijheel (point A) and your friend is at Uttara (point B), and you know both locations on a grid map, how would you calculate the straight-line distance?",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Derive distance formula d = √((x₂−x₁)² + (y₂−y₁)²) from Pythagoras. Ask: find distance between (3, 4) and (−1, 1). Then teach the section formula for internal division: ((mx₂+nx₁)/(m+n), (my₂+ny₁)/(m+n)).",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Teach external division formula (change + to − in denominator). Then area of triangle with vertices: ½|x₁(y₂−y₃) + x₂(y₃−y₁) + x₃(y₁−y₂)|. Ask: what does area = 0 mean geometrically?",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Problem: A(2, 3), B(8, 11). Find the point dividing AB in ratio 3:1 internally and externally. Then find the midpoint and verify it equals the 1:1 division.",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "BUET-level: Show that points (1, 1), (3, 5), (5, 9) are collinear. Then find the ratio in which (3, 5) divides the line joining (1, 1) and (5, 9). Also find the area of triangle formed by (0, 0), (4, 0), (0, 3).",
            },
        ],
        "key_formulas": [
            "Distance: d = √((x₂−x₁)² + (y₂−y₁)²)",
            "Internal division: P = ((mx₂+nx₁)/(m+n), (my₂+ny₁)/(m+n))",
            "External division: P = ((mx₂−nx₁)/(m−n), (my₂−ny₁)/(m−n))",
            "Area of △ = ½|x₁(y₂−y₃) + x₂(y₃−y₁) + x₃(y₁−y₂)|",
            "Midpoint: M = ((x₁+x₂)/2, (y₁+y₂)/2)",
        ],
        "common_mistakes": [
            "Sign errors in the distance formula — forgetting that squaring eliminates negatives, so order of subtraction does not matter",
            "Mixing up internal and external division — using + in denominator for external division instead of −",
            "Forgetting the absolute value in the area formula, leading to negative area values",
        ],
        "practice_prompts": [
            "Find the distance between (−2, 5) and (4, −3).",
            "The point P(4, m) divides the line joining A(2, 3) and B(6, 7) in the ratio 1:1. Find m.",
            "Prove that the points (2, −2), (8, 4), (5, 7), (−1, 1) form a rhombus by showing all sides are equal.",
        ],
        "real_world_example": "When Bangladesh Survey maps land boundaries, they use coordinate geometry. If a piece of land has corners at known GPS coordinates, the area formula gives the exact plot area — crucial for land registration and disputes that are so common in Bangladesh.",
    },

    "hm1-03-02": {
        "title": "Equations of Straight Lines & Line Properties",
        "learning_objectives": [
            "Write equations of lines in slope-intercept, point-slope, and two-point forms",
            "Find slope, intercepts, and angle between two lines",
            "Calculate perpendicular distance from a point to a line",
            "Determine conditions for parallel and perpendicular lines",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: if a road goes uphill — for every 10 meters horizontally, it rises 3 meters. What is the slope? How would you describe the road's equation if it starts at height 5 meters?",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Teach slope m = (y₂−y₁)/(x₂−x₁). Then three forms: y = mx + c (slope-intercept), y − y₁ = m(x − x₁) (point-slope), (y−y₁)/(y₂−y₁) = (x−x₁)/(x₂−x₁) (two-point). Ask student to convert between forms.",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Teach general form ax + by + c = 0. Conditions: parallel lines have equal slopes (m₁ = m₂), perpendicular lines have m₁ × m₂ = −1. Angle between lines: tan θ = |(m₁−m₂)/(1+m₁m₂)|. Perpendicular distance: d = |ax₁+by₁+c|/√(a²+b²).",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Problem: Find the equation of the line through (3, −2) perpendicular to 2x − 3y + 5 = 0. Then find the distance from origin to this new line.",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "BUET-level: Two lines are 3x + 4y = 12 and 4x − 3y = 6. Find: (a) angle between them, (b) point of intersection, (c) equation of the line through their intersection parallel to x − 2y = 5. Use the family of lines concept: L₁ + λL₂ = 0.",
            },
        ],
        "key_formulas": [
            "Slope: m = (y₂−y₁)/(x₂−x₁) = −a/b (for ax+by+c=0)",
            "Slope-intercept: y = mx + c",
            "Point-slope: y − y₁ = m(x − x₁)",
            "Perpendicular distance: d = |ax₁ + by₁ + c| / √(a² + b²)",
            "Angle between lines: tan θ = |(m₁ − m₂)/(1 + m₁m₂)|",
            "Parallel: m₁ = m₂ | Perpendicular: m₁ × m₂ = −1",
        ],
        "common_mistakes": [
            "Computing slope as (x₂−x₁)/(y₂−y₁) instead of (y₂−y₁)/(x₂−x₁) — swapping numerator and denominator",
            "Forgetting the absolute value in perpendicular distance formula, getting negative distances",
            "For perpendicular lines, using m₁ × m₂ = 1 instead of m₁ × m₂ = −1 (missing the negative sign)",
        ],
        "practice_prompts": [
            "Find the equation of the line passing through (1, 2) and (4, 8) in all three forms.",
            "Find the perpendicular distance from the point (3, 4) to the line 3x + 4y − 5 = 0.",
            "Lines 2x + 3y = 6 and 4x + 6y = k are parallel. For what value of k is the distance between them equal to 1?",
        ],
        "real_world_example": "When BUET civil engineers design roads in Dhaka, they calculate slopes for drainage — water must flow at a minimum gradient. The perpendicular distance formula helps determine how far a building is from the road centerline, essential for setback rules in RAJUK building codes.",
    },

    # ══════════════════════════════════════════════════════════════
    # ══ BIOLOGY — Chapter 1: কোষ ও এর গঠন (Cell & Its Structure) ══
    # ══════════════════════════════════════════════════════════════

    "bio1-01-01": {
        "title": "Prokaryotic vs Eukaryotic Cells & Cell Theory",
        "learning_objectives": [
            "Compare structural differences between prokaryotic and eukaryotic cells",
            "Explain the cell theory and contributions of Schleiden, Schwann, and Virchow",
            "Identify membrane-bound organelles present only in eukaryotes",
            "Classify organisms (bacteria, cyanobacteria, fungi, protists, plants, animals) as prokaryotic or eukaryotic",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Start by asking: what do you think is the smallest living unit? Can something alive exist without a cell? Relate to bacteria in curd (doi) we eat every day.",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Explain the 3 postulates of cell theory. Ask: which scientist said 'Omnis cellula e cellula'? Then introduce the key differences — prokaryotes lack a true nucleus and membrane-bound organelles. Ask student to name 2 examples of prokaryotes.",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Compare prokaryotic and eukaryotic cells systematically: nucleus (nucleoid vs true nucleus), ribosomes (70S vs 80S), DNA (circular vs linear), cell wall composition (peptidoglycan vs cellulose/chitin), membrane-bound organelles. Draw a comparison table with the student.",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Give a classification exercise: classify these as prokaryotic or eukaryotic — E. coli, Amoeba, Nostoc (cyanobacteria), mushroom, rice plant cell, Plasmodium (malaria parasite). Ask which of these are relevant to Bangladesh (Nostoc in rice paddies, Plasmodium causing malaria).",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "Medical admission level MCQ: 'Which of the following is found in both prokaryotic and eukaryotic cells? (a) Mitochondria (b) Endoplasmic reticulum (c) Ribosome (d) Golgi body.' Follow up with: why do prokaryotes have 70S ribosomes while eukaryotes have 80S? What is the medical significance of this difference (hint: antibiotics)?",
            },
        ],
        "key_formulas": [
            "Prokaryotic ribosome: 70S (50S + 30S subunits)",
            "Eukaryotic ribosome: 80S (60S + 40S subunits)",
            "Prokaryotic DNA: single circular chromosome + plasmids",
            "Eukaryotic DNA: multiple linear chromosomes with histones",
            "Cell theory: all living things are made of cells; cell is the basic unit of life; cells arise from pre-existing cells",
        ],
        "common_mistakes": [
            "Thinking all bacteria are harmful — many are beneficial (e.g., Lactobacillus in doi/yogurt, nitrogen-fixing bacteria in rice paddies)",
            "Confusing 70S and 80S ribosome subunit values — students add 50+30=80 and think prokaryotes have 80S (Svedberg units are not additive)",
            "Forgetting that prokaryotes CAN have cell walls (peptidoglycan) — students wrongly think only plant cells have walls",
        ],
        "practice_prompts": [
            "A cell has no nuclear membrane, has 70S ribosomes, and a circular DNA. Identify the cell type and give two examples of organisms with this cell type.",
            "Explain why antibiotics like streptomycin target 70S ribosomes but do not harm human cells. What is the clinical significance?",
            "Compare the genetic material organization in E. coli and a human cheek cell. Include at least 4 differences.",
        ],
        "real_world_example": "The doi (yogurt) you eat with rice is made by Lactobacillus — a prokaryote! It converts lactose in milk to lactic acid. Meanwhile, the rice grain itself came from a eukaryotic plant cell. So in one meal of bhat-doi, you are eating products of both prokaryotic and eukaryotic life.",
    },

    "bio1-01-02": {
        "title": "Cell Organelles & Plant vs Animal Cells",
        "learning_objectives": [
            "Describe the structure and function of each major cell organelle (nucleus, mitochondria, ER, Golgi, ribosome, lysosome, chloroplast, vacuole)",
            "Explain the fluid mosaic model of cell membrane (Singer-Nicolson model)",
            "Compare plant and animal cells with at least 5 structural differences",
            "Relate organelle dysfunction to diseases (e.g., lysosomal storage diseases, mitochondrial disorders)",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: if a cell is like a factory, what would be the manager's office? The power plant? The packaging department? The waste disposal unit? Let the student guess before revealing organelle functions.",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Teach the fluid mosaic model of cell membrane — phospholipid bilayer with embedded proteins, cholesterol for fluidity, glycoproteins for recognition. Ask: why is it called 'fluid' mosaic? What makes the membrane selectively permeable?",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Go through each organelle systematically: Nucleus (double membrane, nucleolus, chromatin), Mitochondria (powerhouse, double membrane, own DNA — endosymbiotic theory), ER (rough with ribosomes for protein synthesis, smooth for lipid synthesis), Golgi (packaging & secretion, cis and trans face), Lysosome (digestive enzymes, pH 4.5-5), Chloroplast (photosynthesis, thylakoid grana, stroma). Ask after each: what happens to the cell if this organelle stops working?",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Create a comparison table: Plant cell vs Animal cell. Key differences — cell wall (present/absent), chloroplast, central vacuole (large in plant), centrioles (present in animal), lysosomes (prominent in animal), shape (fixed rectangular vs irregular). Ask: why do plant cells not need lysosomes as much as animal cells?",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "Medical admission MCQ: 'Which organelle is called the suicide bag of the cell? (a) Ribosome (b) Lysosome (c) Peroxisome (d) Glyoxysome.' Follow up: 'A cell is actively secreting proteins. Which organelles would show increased activity? List them in order of the secretory pathway.' (Answer: Nucleus -> Rough ER -> Golgi -> Cell membrane)",
            },
        ],
        "key_formulas": [
            "Cell membrane: phospholipid bilayer + integral/peripheral proteins + cholesterol + glycocalyx",
            "Mitochondria: outer membrane + inner membrane (cristae) + matrix — site of ATP synthesis via oxidative phosphorylation",
            "Chloroplast: outer membrane + inner membrane + thylakoid (grana + stroma lamellae) + stroma — site of photosynthesis",
            "Protein secretory pathway: Ribosome -> Rough ER -> Transport vesicle -> Golgi (cis to trans) -> Secretory vesicle -> Cell membrane",
            "Endosymbiotic theory: mitochondria and chloroplasts were once free-living prokaryotes (have own 70S ribosomes and circular DNA)",
        ],
        "common_mistakes": [
            "Confusing rough ER and smooth ER functions — rough ER has ribosomes for protein synthesis, smooth ER synthesizes lipids and detoxifies drugs (students mix these up)",
            "Thinking mitochondria are only in animal cells — both plant AND animal cells have mitochondria (plants need cellular respiration too!)",
            "Confusing centrioles with centromeres — centrioles are organelles for spindle formation (absent in most plant cells), centromeres are regions on chromosomes",
        ],
        "practice_prompts": [
            "Trace the path of a secretory protein from its synthesis to its release outside the cell. Name every organelle involved in order.",
            "A plant cell and an animal cell are both placed in a hypotonic solution. Predict what happens to each and explain why their fates differ.",
            "Explain the endosymbiotic theory of mitochondrial origin. Give 3 pieces of evidence that support this theory.",
        ],
        "real_world_example": "Think of a paat (jute) fiber cell — it has an extremely thick cell wall made of cellulose, which gives jute its strength for making rope and bags. The cell wall is why plants can stand upright without bones. A mango leaf cell has abundant chloroplasts for photosynthesis, while root cells of the same mango tree have no chloroplasts but many mitochondria for energy to absorb water and minerals.",
    },

    # ══════════════════════════════════════════════════════════════
    # ══ BIOLOGY — Chapter 2: কোষ বিভাজন (Cell Division) ══
    # ══════════════════════════════════════════════════════════════

    "bio1-02-01": {
        "title": "Mitosis — Stages and Significance",
        "learning_objectives": [
            "Describe each phase of the cell cycle (G1, S, G2, M) with duration and events",
            "Explain the 4 stages of mitosis (prophase, metaphase, anaphase, telophase) with key events in each",
            "Differentiate cytokinesis in plant cells (cell plate) vs animal cells (cleavage furrow)",
            "Explain the significance of mitosis in growth, repair, and asexual reproduction",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: when you cut your finger, how does the wound heal? Where do new skin cells come from? When a rice seedling grows from a small shoot to a full plant, where are the new cells coming from?",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Teach the cell cycle: Interphase (G1 — cell growth, protein synthesis; S — DNA replication, chromosome number unchanged but DNA doubles; G2 — preparation for division) and M phase (mitosis + cytokinesis). Ask: a human cell has 46 chromosomes. After S phase, how many chromosomes does it have? (Still 46, but each has 2 chromatids — students often say 92 here!)",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Walk through mitosis step by step: Prophase (chromatin condenses, nucleolus disappears, spindle forms), Metaphase (chromosomes align at metaphase plate, spindle fibers attach to kinetochore), Anaphase (centromeres split, sister chromatids pulled to poles — shortest phase), Telophase (nuclear envelope reforms, chromosomes decondense). Use mnemonic PMAT. Ask student to identify the phase from descriptions.",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Ask: what is different about cytokinesis in plant cells vs animal cells? (Cell plate vs cleavage furrow). Then: a cell with 2n=14 undergoes mitosis. How many chromosomes in each daughter cell? How many daughter cells are produced? Are they genetically identical to the parent?",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "Medical admission MCQ: 'During which phase of mitosis do chromosomes first become visible under a light microscope? (a) Interphase (b) Prophase (c) Metaphase (d) Anaphase.' Follow up: 'Why is uncontrolled mitosis dangerous? How does this relate to cancer?' Ask about the role of checkpoints (G1, G2, M checkpoints) in preventing cancer.",
            },
        ],
        "key_formulas": [
            "Cell cycle: G1 -> S -> G2 -> M (Prophase -> Metaphase -> Anaphase -> Telophase -> Cytokinesis)",
            "Mitosis: 1 parent cell (2n) -> 2 daughter cells (2n) — genetically identical",
            "After S phase: chromosome count unchanged, but each chromosome has 2 sister chromatids (DNA content doubles: 2C -> 4C)",
            "Shortest phase: Anaphase; Longest phase of mitosis: Prophase; Longest phase of cell cycle: Interphase (especially S phase)",
            "Cytokinesis: animal cells — cleavage furrow (actin-myosin ring); plant cells — cell plate (vesicles from Golgi)",
        ],
        "common_mistakes": [
            "Saying chromosome number doubles after S phase — it does NOT; each chromosome becomes 2 sister chromatids joined at centromere, but chromosome count stays the same (2n). DNA content doubles, not chromosome number.",
            "Confusing the order of mitosis phases or mixing up events — e.g., thinking chromosomes align at metaphase plate during prophase, or thinking nuclear envelope breaks in metaphase (it breaks in late prophase/prometaphase)",
            "Forgetting that cytokinesis is NOT part of mitosis itself — mitosis is nuclear division only; cytokinesis is cytoplasmic division and can be separated",
        ],
        "practice_prompts": [
            "A cell with 2n=24 is undergoing mitosis. State the chromosome number and DNA content (in terms of C) at: (i) G1 phase, (ii) after S phase, (iii) metaphase, (iv) each daughter cell after division.",
            "A student observing onion root tip cells under a microscope sees most cells in interphase and very few in anaphase. Explain why.",
            "How is cancer related to failure of cell cycle regulation? Name the phases where checkpoints occur and what each checkpoint monitors.",
        ],
        "real_world_example": "When you plant a dhan (rice) seed, it germinates and grows into a full plant with thousands of cells — all produced by mitosis from that one original seed cell. The meristematic tissue at the root tip and shoot tip is where mitosis is most active. That is why when you look at onion root tip slides in your HSC practical, you see so many dividing cells!",
    },

    "bio1-02-02": {
        "title": "Meiosis — Stages, Crossing Over & Significance",
        "learning_objectives": [
            "Describe the stages of meiosis I (especially prophase I sub-stages) and meiosis II",
            "Explain crossing over, synapsis, and chiasmata formation during prophase I",
            "Compare mitosis and meiosis with at least 6 key differences",
            "Explain the biological significance of meiosis — genetic variation, maintaining chromosome number across generations",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: why don't you look exactly like your siblings even though you have the same parents? If gametes were produced by mitosis, what would happen to chromosome number each generation? (It would double! 46 -> 92 -> 184...) This is why meiosis is essential.",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Explain meiosis I as the reductional division: homologous chromosomes pair (synapsis), form bivalents/tetrads, crossing over occurs at chiasmata. Teach prophase I sub-stages using mnemonic LZPDD: Leptotene (thin threads), Zygotene (synapsis begins), Pachytene (crossing over — thickest chromosomes), Diplotene (chiasmata visible, separation begins), Diakinesis (terminalization of chiasmata). Ask: at which sub-stage does genetic recombination actually occur?",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Complete meiosis I (metaphase I — bivalents align, independent assortment; anaphase I — homologous chromosomes separate; telophase I — two haploid cells). Then teach meiosis II — similar to mitosis but starts with haploid cells. End result: 4 haploid cells. Compare: in males all 4 become sperm; in females only 1 becomes ovum (other 3 are polar bodies). Ask: why is meiosis I called reductional and meiosis II called equational?",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Comparison exercise: make a table comparing mitosis vs meiosis on: number of divisions, number of daughter cells, chromosome number in daughters, genetic variation, where it occurs, crossing over (yes/no), synapsis (yes/no). Then ask: a cell with 2n=46 undergoes meiosis. What is the chromosome number after meiosis I? After meiosis II?",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "Medical admission MCQ: 'Crossing over occurs between: (a) sister chromatids (b) non-sister chromatids of homologous chromosomes (c) non-homologous chromosomes (d) any two chromatids.' Follow up: 'Explain how both crossing over AND independent assortment contribute to genetic variation. Calculate: with n=23 chromosomes, how many possible gamete combinations from independent assortment alone?' (2^23 = 8,388,608)",
            },
        ],
        "key_formulas": [
            "Meiosis: 1 parent cell (2n) -> 4 daughter cells (n) — genetically different",
            "Prophase I sub-stages: Leptotene -> Zygotene -> Pachytene -> Diplotene -> Diakinesis (LZPDD)",
            "Crossing over: exchange of genetic material between non-sister chromatids of homologous chromosomes at chiasmata",
            "Independent assortment: possible combinations = 2^n (where n = haploid chromosome number)",
            "Human: 2n=46, so n=23; after meiosis I: 23 chromosomes per cell; after meiosis II: 23 chromosomes per cell (but single chromatids)",
        ],
        "common_mistakes": [
            "Confusing crossing over between sister chromatids (does not produce variation) with crossing over between non-sister chromatids of homologous chromosomes (produces genetic recombination)",
            "Mixing up meiosis I and meiosis II — students forget that homologous chromosomes separate in meiosis I (reductional) while sister chromatids separate in meiosis II (equational, like mitosis)",
            "Forgetting the sub-stages of prophase I — this is a very common Medical admission question; LZPDD mnemonic is essential and students often mix up the order or events of Pachytene vs Diplotene",
        ],
        "practice_prompts": [
            "A cell with 2n=8 undergoes meiosis. Draw or describe the chromosome arrangement at: (i) metaphase I, (ii) anaphase I, (iii) metaphase II, (iv) anaphase II. State chromosome count at each stage.",
            "Explain why meiosis is called the basis of sexual reproduction. What would happen to a species if meiosis did not occur but sexual reproduction continued?",
            "During oogenesis in a human female, one primary oocyte produces how many functional ova? Explain the formation of polar bodies and their fate.",
        ],
        "real_world_example": "Think about Bangladeshi rice varieties — BRRI has developed over 100 dhan varieties (BRRI dhan28, BRRI dhan29, etc.) by cross-breeding. This works because meiosis creates genetic variation through crossing over and independent assortment. Each rice grain from a cross is genetically unique, letting breeders select for flood resistance, salt tolerance, or higher yield — all crucial for Bangladesh's food security.",
    },

    # ══════════════════════════════════════════════════════════════
    # ══ BIOLOGY — Chapter 3: কোষ রসায়ন (Cell Chemistry / Biochemistry) ══
    # ══════════════════════════════════════════════════════════════

    "bio1-03-01": {
        "title": "Carbohydrates, Lipids & Proteins — Structure and Function",
        "learning_objectives": [
            "Classify carbohydrates into monosaccharides, disaccharides, and polysaccharides with examples and bonding",
            "Describe the structure of lipids — triglycerides, phospholipids, and steroids — and distinguish saturated from unsaturated fatty acids",
            "Explain protein structure at all 4 levels (primary, secondary, tertiary, quaternary) and the role of peptide bonds",
            "Relate the structure of each biomolecule to its biological function",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: what did you eat for breakfast? Probably bhat (rice), dal (lentils), and maybe an egg or fish. Which one gives you energy quickly? Which builds your muscles? Which is stored as fat? Connect food to biomolecules — carbohydrates, proteins, lipids.",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Teach carbohydrates: general formula Cn(H2O)n. Monosaccharides (glucose, fructose, galactose — all C6H12O6 but different structures), Disaccharides (sucrose = glucose + fructose via glycosidic bond; maltose = glucose + glucose; lactose = glucose + galactose), Polysaccharides (starch — plant storage in rice/potato; glycogen — animal storage in liver/muscle; cellulose — structural in plant cell wall; chitin — in insect exoskeleton/fungal wall). Ask: why can humans digest starch but not cellulose, even though both are made of glucose?",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Teach lipids: triglyceride = glycerol + 3 fatty acids via ester bonds. Saturated (no double bonds, solid at room temperature — ghee, butter) vs unsaturated (double bonds, liquid — soyabean oil, mustard oil/sorsher tel). Phospholipids: glycerol + 2 fatty acids + phosphate group — amphipathic, forms cell membrane bilayer. Then teach proteins: amino acids joined by peptide bonds (CO-NH). 4 levels of structure: primary (sequence), secondary (alpha-helix, beta-sheet via H-bonds), tertiary (3D folding via disulfide bonds, hydrophobic interactions), quaternary (multiple polypeptides, e.g., hemoglobin has 4 subunits). Ask: what level of protein structure is disrupted when you boil an egg?",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Identification exercise: classify these as carbohydrate, lipid, or protein — hemoglobin, cellulose, cholesterol, insulin, starch, phospholipid, glycogen, keratin, chitin, triglyceride. Then ask: which bond links (a) two amino acids, (b) two monosaccharides, (c) glycerol and fatty acid? (peptide bond, glycosidic bond, ester bond)",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "Medical admission MCQ: 'Which of the following is a reducing sugar? (a) Sucrose (b) Starch (c) Maltose (d) Cellulose.' Follow up: 'Sickle cell anemia is caused by a change in which level of protein structure? Explain how a single amino acid substitution (Glu -> Val) in hemoglobin leads to the disease.' This tests understanding of how primary structure determines all higher levels.",
            },
        ],
        "key_formulas": [
            "General formula of carbohydrates: Cn(H2O)n — e.g., glucose C6H12O6",
            "Sucrose = glucose + fructose (non-reducing sugar, 1-2 glycosidic bond)",
            "Maltose = glucose + glucose (reducing sugar, 1-4 glycosidic bond)",
            "Starch: amylose (unbranched, 1-4 bonds) + amylopectin (branched, 1-4 and 1-6 bonds)",
            "Triglyceride = glycerol + 3 fatty acids (ester bonds, via condensation/dehydration reaction)",
            "Peptide bond: -CO-NH- bond between carboxyl of one amino acid and amino group of another (with release of H2O)",
            "Protein levels: primary (peptide bonds) -> secondary (H-bonds) -> tertiary (disulfide, ionic, hydrophobic) -> quaternary (multiple polypeptides)",
        ],
        "common_mistakes": [
            "Thinking sucrose is a reducing sugar — it is NOT because the glycosidic bond involves the anomeric carbons of BOTH glucose and fructose, leaving no free aldehyde/ketone group. Maltose and lactose ARE reducing sugars.",
            "Confusing starch and cellulose — both are polymers of glucose but starch has alpha-1,4 glycosidic bonds (digestible by humans) while cellulose has beta-1,4 bonds (indigestible by humans, requires cellulase enzyme found in ruminants and termites)",
            "Mixing up the 4 levels of protein structure — especially confusing secondary (local H-bonding: alpha-helix, beta-sheet) with tertiary (overall 3D shape from R-group interactions: disulfide bonds, hydrophobic interactions, ionic bonds)",
        ],
        "practice_prompts": [
            "Compare starch, glycogen, and cellulose in terms of: monomer, type of glycosidic bond, branching, biological function, and which organisms use them for what purpose.",
            "Explain why phospholipids spontaneously form bilayers in water. How does this property relate to cell membrane formation? What role does cholesterol play in the membrane?",
            "A patient has sickle cell disease. Explain the molecular basis at each level of hemoglobin structure — from the DNA mutation to the final effect on red blood cell shape and oxygen transport.",
        ],
        "real_world_example": "Your bhat (rice) is mostly starch — a polysaccharide that your amylase enzyme breaks into glucose for energy. The mach (fish) you eat with rice provides protein — amino acids for building muscle. The sorsher tel (mustard oil) your mother cooks with is a lipid — triglycerides with unsaturated fatty acids. Even the paan (betel leaf) you might see elders chewing has cellulose cell walls your body cannot digest. Every Bangladeshi meal is a biochemistry lesson!",
    },

    "bio1-03-02": {
        "title": "Nucleic Acids (DNA & RNA) and Enzymes",
        "learning_objectives": [
            "Describe the structure of DNA (double helix model of Watson & Crick) and RNA with their chemical components",
            "Explain base pairing rules (A-T with 2 H-bonds, G-C with 3 H-bonds) and Chargaff's rules",
            "Compare DNA and RNA in terms of sugar, bases, structure, location, and function",
            "Explain enzyme action using lock-and-key and induced fit models, including factors affecting enzyme activity",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: what carries the instructions to build your entire body? How does a single fertilized egg know how to become a complete human with eyes, heart, and brain? This is the role of DNA — the blueprint of life. Then ask: have you heard of DNA testing in crime investigation or paternity tests?",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Teach nucleotide structure: phosphate + sugar (deoxyribose in DNA, ribose in RNA) + nitrogenous base. Purines: Adenine (A) and Guanine (G) — double ring. Pyrimidines: Cytosine (C), Thymine (T in DNA), Uracil (U in RNA) — single ring. Mnemonic: PURe As Gold (purines = A, G). Teach Chargaff's rules: A=T, G=C, so A+G = T+C (purines = pyrimidines). Ask: if a DNA strand has 30% adenine, what percentage of guanine does it have?",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Describe the Watson-Crick double helix model: two antiparallel polynucleotide strands (5'->3' and 3'->5'), sugar-phosphate backbone on outside, bases inside paired by H-bonds (A=T with 2 H-bonds, G-C with 3 H-bonds), one complete turn = 3.4 nm with 10 base pairs, distance between base pairs = 0.34 nm, diameter = 2 nm. Then compare DNA vs RNA in a table (5 differences minimum). Then teach enzymes: biological catalysts (mostly proteins), lock-and-key model vs induced fit model, active site, substrate specificity. Factors: temperature, pH, substrate concentration, enzyme concentration, inhibitors (competitive vs non-competitive).",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Problem: A DNA sample has 20% cytosine. Calculate the percentages of all 4 bases. (C=20%, G=20%, A=30%, T=30%). Then: if one strand of DNA has the sequence 5'-ATGCCGTA-3', write the complementary strand with correct polarity. For enzymes: explain why pepsin works in the stomach (pH 2) but trypsin works in the intestine (pH 8). What happens to pepsin at pH 8?",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "Medical admission MCQ: 'Which of the following is TRUE about DNA? (a) It contains ribose sugar (b) A-T base pair has 3 hydrogen bonds (c) The two strands run in the same direction (d) One complete turn has 10 base pairs.' Follow up: 'A DNA molecule has 1000 base pairs. If 200 of them are adenine-thymine pairs, how many hydrogen bonds are in this DNA? (200 A-T pairs x 2 = 400, plus 800 G-C pairs x 3 = 2400, total = 2800 H-bonds).' For enzymes: 'Explain competitive inhibition with a medical example — how do sulfa drugs work as antibiotics?'",
            },
        ],
        "key_formulas": [
            "Nucleotide = phosphate group + pentose sugar + nitrogenous base",
            "Chargaff's rule: A = T, G = C; therefore %A + %G = %T + %C = 50%",
            "DNA double helix: 1 turn = 3.4 nm = 10 base pairs; distance between base pairs = 0.34 nm; diameter = 2 nm",
            "H-bonds: A=T (2 hydrogen bonds), G-C (3 hydrogen bonds) — GC-rich DNA is more thermally stable",
            "Total H-bonds in DNA = (2 x number of A-T pairs) + (3 x number of G-C pairs)",
            "Types of RNA: mRNA (carries genetic message), tRNA (carries amino acids, has anticodon), rRNA (structural component of ribosomes)",
            "Enzyme kinetics: Vmax = maximum rate at substrate saturation; Km = substrate concentration at half Vmax (Michaelis-Menten)",
        ],
        "common_mistakes": [
            "Applying Chargaff's rule to single-stranded RNA — Chargaff's rule (A=T, G=C) applies ONLY to double-stranded DNA, NOT to single-stranded RNA where A does not necessarily equal U",
            "Confusing the number of hydrogen bonds — A-T has 2 H-bonds (not 3) and G-C has 3 H-bonds (not 2); students frequently reverse these. Remember: C and G are 'stronger' (3 bonds) so GC-rich DNA needs higher temperature to denature",
            "Thinking enzymes are consumed in reactions — enzymes are catalysts that are NOT used up; they lower activation energy and are recycled. Also confusing competitive inhibition (blocks active site, overcome by more substrate) with non-competitive inhibition (binds allosteric site, cannot be overcome by more substrate)",
        ],
        "practice_prompts": [
            "A double-stranded DNA molecule has 1500 base pairs. If adenine constitutes 35% of total bases, calculate: (i) percentage of each base, (ii) number of each type of base pair, (iii) total number of hydrogen bonds in this DNA molecule.",
            "Compare DNA and RNA in a table with at least 6 differences covering: sugar type, bases, number of strands, location in cell, stability, and function.",
            "Explain with a diagram how a competitive inhibitor differs from a non-competitive inhibitor. Give a medical/pharmacological example of each type. Why can competitive inhibition be reversed by increasing substrate concentration but non-competitive cannot?",
        ],
        "real_world_example": "Forensic DNA testing is now used in Bangladeshi courts for paternity disputes and criminal cases. The technique works because everyone's DNA base sequence is unique (except identical twins). Enzymes are everywhere in daily life too — the papain enzyme in raw kacha papaya (pepe) tenderizes meat, which is why Bangladeshi cooks add papaya paste to tough beef before cooking. Your saliva contains amylase enzyme that starts digesting the starch in bhat right in your mouth — try chewing plain rice for 30 seconds and it starts tasting sweet as starch breaks into maltose!",
    },

    # ══ PHYSICS — Chapters 4-10 ══
    "phy1-02-02": {
        "title": "Scalar & Vector Products",
        "learning_objectives": [
                "Calculate dot product and find angle between vectors",
                "Calculate cross product and find area of parallelogram",
                "Apply scalar product in work calculations",
                "Apply vector product in torque calculations"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: when you push a box at an angle, not all your force moves it forward. How do we calculate the useful part of the force?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Teach dot product: A·B = AB cos θ (scalar result). Ask: what is the dot product when vectors are perpendicular?"
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Teach cross product: A×B = AB sin θ n̂ (vector result). Explain right-hand rule. Ask: what is cross product when vectors are parallel?"
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "Find dot product of A=(3,4) and B=(2,-1). Then find the angle between them."
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ: if A×B = 0 and A·B = AB, what is the angle between A and B?"
                }
        ],
        "key_formulas": [
                "A·B = AB cos θ = a₁b₁ + a₂b₂ + a₃b₃",
                "A×B = AB sin θ n̂",
                "|A×B| = area of parallelogram"
        ],
        "common_mistakes": [
                "Confusing dot product (scalar) with cross product (vector)",
                "Wrong sign in cross product (not commutative: A×B = -B×A)",
                "Forgetting that perpendicular vectors have zero dot product"
        ],
        "practice_prompts": [
                "If A=(1,2,3) and B=(4,-1,2), find A·B",
                "Two forces 5N and 8N act at 60°. Find A×B magnitude."
        ],
        "real_world_example": "When you pull a rickshaw with a rope at an angle, only the horizontal component (F cos θ) moves it forward — that's the dot product of force and displacement giving you work done."
},

    "phy1-04-01": {
        "title": "Newton's Laws of Motion",
        "learning_objectives": [
                "State and apply all three Newton's laws",
                "Draw free body diagrams for complex systems",
                "Solve problems with connected bodies",
                "Apply Newton's laws to lift/elevator problems"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: why does your body jerk forward when a bus suddenly stops? Which Newton's law explains this?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Teach all 3 laws with examples. 1st: inertia (bus example). 2nd: F=ma (pushing cart). 3rd: action-reaction (walking). Ask student to identify which law applies in each scenario."
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Teach free body diagrams. Draw FBD for a block on an incline. Identify normal force, weight components, friction. Solve for acceleration."
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "Two blocks (3kg and 5kg) connected by string on frictionless surface. Force 40N applied on 5kg block. Find acceleration and tension."
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "Elevator problem: a 60kg person in a lift accelerating upward at 2 m/s². What does the scale read? BUET-level."
                }
        ],
        "key_formulas": [
                "F = ma",
                "Weight W = mg",
                "Apparent weight in lift: N = m(g ± a)",
                "Connected bodies: same acceleration, tension is internal force"
        ],
        "common_mistakes": [
                "Confusing mass and weight",
                "Forgetting that action-reaction forces act on DIFFERENT bodies",
                "Not resolving forces into components on inclined planes"
        ],
        "practice_prompts": [
                "A 10kg box on a smooth surface is pushed with 50N. Find acceleration.",
                "In a lift going up with acceleration 3 m/s², what is the apparent weight of a 50kg person?"
        ],
        "real_world_example": "When a CNG auto-rickshaw suddenly brakes, you slide forward — that's Newton's 1st law. The harder the driver brakes (more force), the faster you decelerate (2nd law). Your feet push backward on the floor, floor pushes you forward (3rd law)."
},

    "phy1-04-02": {
        "title": "Friction & Circular Motion",
        "learning_objectives": [
                "Calculate static and kinetic friction",
                "Solve problems on banked roads and circular motion",
                "Apply centripetal force concept",
                "Understand the role of friction in daily life"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: why is it easier to push a box once it starts moving than to start pushing it? What's the difference between static and kinetic friction?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Teach f = μN. Static friction ≤ μₛN, kinetic friction = μₖN. Ask: why is μₛ > μₖ always?"
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Circular motion: centripetal force F = mv²/r. For car on banked road: tan θ = v²/rg. Derive step by step."
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "A car turns on a flat road (μ=0.4, r=50m). Find maximum safe speed. Then: what if the road is banked at 30°?"
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ about friction on incline or centripetal force in vertical circular motion."
                }
        ],
        "key_formulas": [
                "f = μN",
                "Centripetal force F = mv²/r",
                "Banked road: tan θ = v²/rg",
                "Min speed at top of loop: v = √(rg)"
        ],
        "common_mistakes": [
                "Using μmg for friction on incline (should be μN = μmg cos θ)",
                "Confusing centripetal (real) with centrifugal (pseudo) force",
                "Forgetting that static friction has a maximum value, not a fixed value"
        ],
        "practice_prompts": [
                "A 5kg block on a surface with μ=0.3. Find friction when 10N horizontal force applied.",
                "Find the banking angle for a road curve (r=100m) at speed 72 km/h."
        ],
        "real_world_example": "The flyover curves in Dhaka are slightly banked — the road tilts inward so cars don't need to rely only on tire friction. Same reason why cricket bowlers can make the ball curve — friction and circular motion!"
},

    "phy1-05-01": {
        "title": "Work & Energy",
        "learning_objectives": [
                "Calculate work done by constant and variable forces",
                "Apply work-energy theorem",
                "Understand potential and kinetic energy",
                "Apply conservation of energy to solve problems"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: if you carry a heavy bag horizontally across a room, have you done any work on it (in physics terms)? Why or why not?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Teach W = Fd cos θ. When θ=90°, W=0 (carrying bag horizontally). KE = ½mv², PE = mgh. Ask: what type of energy does a flying bird have?"
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Work-energy theorem: net work = change in KE. Solve: a 2kg ball falls from 10m. Find velocity just before hitting ground using energy conservation."
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "A 1000kg car accelerates from 10 m/s to 30 m/s. Find the work done by the engine."
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ: a pendulum released from height h. Find velocity at lowest point. Then: if string is cut at lowest point, what path does it follow?"
                }
        ],
        "key_formulas": [
                "W = Fd cos θ",
                "KE = ½mv²",
                "PE = mgh",
                "Conservation: KE₁ + PE₁ = KE₂ + PE₂"
        ],
        "common_mistakes": [
                "Saying you do work when carrying a bag horizontally (W=0 since F⊥d)",
                "Forgetting that work can be negative (friction does negative work)",
                "Not using energy conservation when it's simpler than force equations"
        ],
        "practice_prompts": [
                "A 50kg boy climbs 10m stairs. How much work against gravity?",
                "A spring (k=200 N/m) compressed 0.1m. Find stored PE."
        ],
        "real_world_example": "When water falls at Kaptai Dam from height h, its PE converts to KE, which spins turbines to generate electricity. The higher the dam, the more energy — that's why Kaptai was built in the hills of Rangamati."
},

    "phy1-05-02": {
        "title": "Power & Collisions",
        "learning_objectives": [
                "Calculate power as rate of work done",
                "Distinguish elastic and inelastic collisions",
                "Apply momentum conservation in collisions",
                "Solve problems involving coefficient of restitution"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: two people carry the same weight up stairs — one takes 1 minute, the other takes 5 minutes. Who does more work? Who has more power?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Power P = W/t = Fv. 1 HP = 746 W. Teach elastic (KE conserved) vs inelastic (KE not conserved) collisions."
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Collision formulas: m₁u₁ + m₂u₂ = m₁v₁ + m₂v₂. For perfectly inelastic: bodies stick together. Solve: 2kg ball at 3m/s hits stationary 1kg ball elastically."
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "A 1500kg car at 20 m/s collides with stationary 1000kg car. They stick together. Find final velocity and energy lost."
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ about collision or power calculation."
                }
        ],
        "key_formulas": [
                "P = W/t = Fv",
                "1 HP = 746 W",
                "Coefficient of restitution e = (v₂-v₁)/(u₁-u₂)",
                "Elastic: e=1, Perfectly inelastic: e=0"
        ],
        "common_mistakes": [
                "Confusing work (same for both) with power (different if time differs)",
                "Thinking momentum is not conserved in inelastic collisions (it IS, only KE isn't)",
                "Forgetting that in 2D collisions, momentum is conserved in each direction separately"
        ],
        "practice_prompts": [
                "A pump lifts 500kg water to 10m in 5 seconds. Find power in watts and HP.",
                "Two identical balls collide elastically head-on. What happens?"
        ],
        "real_world_example": "When a truck hits a small car, both have the same momentum change (Newton's 3rd law) — but the small car gets much more acceleration because F=ma and its mass is less. That's why trucks cause more damage in accidents on the Dhaka-Chittagong highway."
},

    "phy1-06-01": {
        "title": "Gravitation",
        "learning_objectives": [
                "Apply Newton's law of gravitation",
                "Calculate gravitational field strength at different altitudes",
                "Derive orbital velocity and escape velocity",
                "Apply Kepler's laws of planetary motion"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: why does the Moon orbit the Earth instead of flying away? What force keeps it in orbit?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Teach F = GMm/r². Surface gravity g = GM/R². Ask: what happens to g if you go to a mountain top? What about deep inside Earth?"
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Derive orbital velocity v = √(GM/r) and escape velocity vₑ = √(2GM/R) = √(2gR). Ask: why is escape velocity √2 times orbital velocity?"
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "Calculate g at height equal to Earth's radius. Then: find escape velocity from Earth (R=6400km, g=9.8)."
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ about satellite period or variation of g with altitude/depth."
                }
        ],
        "key_formulas": [
                "F = GMm/r²",
                "g = GM/R²",
                "Orbital velocity v₀ = √(GM/r)",
                "Escape velocity vₑ = √(2gR)",
                "Kepler's T² ∝ r³"
        ],
        "common_mistakes": [
                "Using r (distance from center) vs h (height above surface) — g at height h: g'=g(R/(R+h))²",
                "Forgetting that inside Earth, g decreases linearly with depth",
                "Confusing orbital velocity with escape velocity"
        ],
        "practice_prompts": [
                "At what height above Earth is g reduced to g/4?",
                "Find the time period of a satellite orbiting just above Earth's surface."
        ],
        "real_world_example": "Bangladesh's Bangabandhu-1 satellite orbits at 35,786 km (geostationary orbit) — at that height, it takes exactly 24 hours to orbit, so it stays over the same spot above Bangladesh. That's Kepler's third law in action!"
},

    "phy1-07-01": {
        "title": "Elasticity & Fluid Mechanics",
        "learning_objectives": [
                "Define stress, strain, and Young's modulus",
                "Apply Hooke's law within elastic limit",
                "Apply Pascal's law and Archimedes' principle",
                "Use Bernoulli's equation for fluid flow"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: why does a rubber band return to its original shape but clay doesn't? What's the difference?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Teach stress = F/A, strain = ΔL/L, Young's modulus Y = stress/strain. Hooke's law: F = kx. Ask: what happens beyond the elastic limit?"
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Fluid statics: Pascal's law (hydraulic press), Archimedes' principle (buoyancy). Bernoulli's: P + ½ρv² + ρgh = constant."
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "A steel wire (Y=2×10¹¹ Pa, L=2m, A=1mm²) stretched by 100N. Find extension."
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ about buoyancy or Bernoulli's application."
                }
        ],
        "key_formulas": [
                "Stress = F/A, Strain = ΔL/L",
                "Young's modulus Y = Stress/Strain",
                "Pascal's law: pressure transmitted equally",
                "Bernoulli: P + ½ρv² + ρgh = constant"
        ],
        "common_mistakes": [
                "Confusing stress (force per unit area) with pressure (same unit but different concept)",
                "Forgetting that Bernoulli's equation only applies to ideal (inviscid) fluids",
                "Using weight instead of mass in buoyancy calculations"
        ],
        "practice_prompts": [
                "A hydraulic press has pistons of area 10 cm² and 100 cm². Force on small piston is 50N. Find force on large piston.",
                "A block of wood (density 600 kg/m³) floats in water. What fraction is submerged?"
        ],
        "real_world_example": "The hydraulic brakes in buses work on Pascal's law — a small force on the brake pedal creates a large force on the brake pads. And country boats (নৌকা) float because of Archimedes' principle — the water pushes up with a force equal to the weight of water displaced."
},

    "phy1-08-01": {
        "title": "Simple Harmonic Motion",
        "learning_objectives": [
                "Define SHM and identify SHM systems",
                "Derive equations of SHM (displacement, velocity, acceleration)",
                "Calculate time period of simple pendulum and spring-mass system",
                "Understand energy in SHM"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: a swing in a playground goes back and forth. Is the motion uniform? What pattern does it follow?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Define SHM: acceleration proportional to displacement, directed toward mean position. a = -ω²x. Ask: is uniform circular motion related to SHM?"
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Equations: x = A sin(ωt), v = Aω cos(ωt), a = -Aω² sin(ωt). For pendulum: T = 2π√(l/g). For spring: T = 2π√(m/k)."
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "A spring (k=100 N/m) with 0.5kg mass. Find time period and maximum velocity if amplitude is 0.1m."
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ: energy variation in SHM — KE and PE as function of displacement."
                }
        ],
        "key_formulas": [
                "x = A sin(ωt + φ)",
                "T = 2π/ω",
                "Pendulum: T = 2π√(l/g)",
                "Spring: T = 2π√(m/k)",
                "Total energy E = ½kA² = ½mω²A²"
        ],
        "common_mistakes": [
                "Thinking pendulum period depends on mass (it doesn't for simple pendulum)",
                "Confusing amplitude with displacement at a given time",
                "Forgetting that at mean position KE=max and PE=0, at extreme PE=max and KE=0"
        ],
        "practice_prompts": [
                "A pendulum has T=2s. Find its length.",
                "In SHM, at what displacement is KE equal to PE?"
        ],
        "real_world_example": "The clock pendulums in old Bangladeshi homes (দেয়াল ঘড়ি) are SHM — the longer the pendulum, the slower it swings. That's why grandfather clocks are tall!"
},

    "phy1-09-01": {
        "title": "Wave Properties",
        "learning_objectives": [
                "Distinguish transverse and longitudinal waves",
                "Apply v = fλ relationship",
                "Understand superposition and standing waves",
                "Calculate frequency of vibrating strings and air columns"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: when you throw a stone in a pond, ripples spread out. Is the water actually moving outward, or is it something else?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Teach transverse (particle ⊥ wave direction) vs longitudinal (particle ∥ wave direction). v = fλ. Ask: is sound transverse or longitudinal?"
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Standing waves on string: harmonics. f_n = n(v/2L). For closed pipe: only odd harmonics. Open pipe: all harmonics."
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "A string (L=1m, μ=0.01 kg/m) under tension 40N. Find fundamental frequency and first three harmonics."
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ about standing waves in pipes or strings."
                }
        ],
        "key_formulas": [
                "v = fλ",
                "String: v = √(T/μ)",
                "String harmonics: fₙ = nv/2L",
                "Open pipe: fₙ = nv/2L (all n)",
                "Closed pipe: fₙ = nv/4L (odd n only)"
        ],
        "common_mistakes": [
                "Thinking wave speed depends on frequency (it depends on medium)",
                "Forgetting closed pipe has only odd harmonics",
                "Confusing nodes and antinodes in standing waves"
        ],
        "practice_prompts": [
                "Sound speed is 340 m/s. Find wavelength of 680 Hz sound.",
                "A closed pipe has fundamental 200 Hz. What is its 2nd overtone?"
        ],
        "real_world_example": "When a বাঁশি (bamboo flute) player covers different holes, they change the effective length of the air column — shorter column = higher frequency = higher pitch. That's standing waves in an open pipe!"
},

    "phy1-09-02": {
        "title": "Sound & Doppler Effect",
        "learning_objectives": [
                "Calculate beat frequency",
                "Apply Doppler effect formula for moving source/observer",
                "Understand resonance and its applications",
                "Solve problems on speed of sound in different media"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: why does an ambulance siren sound higher-pitched when approaching and lower when moving away?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Doppler effect: f' = f(v ± v₀)/(v ∓ vₛ). Convention: approaching = higher, receding = lower. Ask: what if both source and observer are moving?"
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Beats: when two frequencies are close, f_beat = |f₁ - f₂|. Resonance: when driving frequency = natural frequency, amplitude is maximum."
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "An ambulance (f=500Hz) moves at 30 m/s toward you. Speed of sound = 340 m/s. Find the frequency you hear."
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ about Doppler effect or beats."
                }
        ],
        "key_formulas": [
                "Doppler: f' = f(v + v₀)/(v - vₛ) (approaching)",
                "Beat frequency = |f₁ - f₂|",
                "Speed of sound in air ≈ 340 m/s at 20°C",
                "v_sound ∝ √T (temperature in Kelvin)"
        ],
        "common_mistakes": [
                "Getting signs wrong in Doppler formula (remember: approaching = higher frequency)",
                "Thinking beats frequency = average of two frequencies (it's the difference)",
                "Forgetting speed of sound changes with temperature"
        ],
        "practice_prompts": [
                "Two tuning forks of 256 Hz and 260 Hz are sounded together. How many beats per second?",
                "A train (speed 36 km/h) blows whistle at 500 Hz. Find frequency heard by stationary observer as train approaches."
        ],
        "real_world_example": "Next time you hear a motorcycle zooming past on the highway, notice how the pitch drops as it passes you — that's the Doppler effect. Astronomers use the same principle to tell if a star is moving toward or away from us (red shift/blue shift)."
},

    "phy1-10-01": {
        "title": "Gas Laws & Kinetic Theory",
        "learning_objectives": [
                "Apply ideal gas equation PV = nRT",
                "Derive kinetic energy from kinetic theory",
                "Understand Maxwell-Boltzmann distribution",
                "Apply gas laws to solve problems"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: why does a balloon expand when you heat it? What's happening to the gas molecules inside?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Teach PV = nRT. Gas laws: Boyle's (P∝1/V), Charles's (V∝T), Gay-Lussac's (P∝T). Ask: what is an ideal gas?"
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Kinetic theory: KE = (3/2)kT. RMS speed v_rms = √(3RT/M). Ask: which gas molecules move faster at same temperature — hydrogen or oxygen?"
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "2 moles of ideal gas at 300K in 10L container. Find pressure. Then: if temperature doubles at constant volume, new pressure?"
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ about KE of gas molecules or gas law application."
                }
        ],
        "key_formulas": [
                "PV = nRT (R = 8.314 J/mol·K)",
                "KE_avg = (3/2)kT",
                "v_rms = √(3RT/M)",
                "Boyle: P₁V₁ = P₂V₂",
                "Charles: V₁/T₁ = V₂/T₂"
        ],
        "common_mistakes": [
                "Using Celsius instead of Kelvin in gas law calculations",
                "Confusing R (gas constant) with k (Boltzmann constant) — k = R/Nₐ",
                "Thinking all gas molecules move at the same speed (they have a distribution)"
        ],
        "practice_prompts": [
                "Find the RMS speed of N₂ molecules at 27°C. (M=28 g/mol)",
                "A gas at 2 atm and 300K is heated to 600K at constant volume. Find new pressure."
        ],
        "real_world_example": "The pressure cooker in every Bangladeshi kitchen works on Gay-Lussac's law — as temperature increases at constant volume, pressure increases. That's why food cooks faster inside — higher pressure means higher boiling point of water!"
},


    # ══ PHYSICS — Chapters 4-10 ══
    "phy1-02-02": {
        "title": "Scalar & Vector Products",
        "learning_objectives": [
                "Calculate dot product and find angle between vectors",
                "Calculate cross product and find area of parallelogram",
                "Apply scalar product in work calculations",
                "Apply vector product in torque calculations"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: when you push a box at an angle, not all your force moves it forward. How do we calculate the useful part of the force?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Teach dot product: A·B = AB cos θ (scalar result). Ask: what is the dot product when vectors are perpendicular?"
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Teach cross product: A×B = AB sin θ n̂ (vector result). Explain right-hand rule. Ask: what is cross product when vectors are parallel?"
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "Find dot product of A=(3,4) and B=(2,-1). Then find the angle between them."
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ: if A×B = 0 and A·B = AB, what is the angle between A and B?"
                }
        ],
        "key_formulas": [
                "A·B = AB cos θ = a₁b₁ + a₂b₂ + a₃b₃",
                "A×B = AB sin θ n̂",
                "|A×B| = area of parallelogram"
        ],
        "common_mistakes": [
                "Confusing dot product (scalar) with cross product (vector)",
                "Wrong sign in cross product (not commutative: A×B = -B×A)",
                "Forgetting that perpendicular vectors have zero dot product"
        ],
        "practice_prompts": [
                "If A=(1,2,3) and B=(4,-1,2), find A·B",
                "Two forces 5N and 8N act at 60°. Find A×B magnitude."
        ],
        "real_world_example": "When you pull a rickshaw with a rope at an angle, only the horizontal component (F cos θ) moves it forward — that's the dot product of force and displacement giving you work done."
},

    "phy1-04-01": {
        "title": "Newton's Laws of Motion",
        "learning_objectives": [
                "State and apply all three Newton's laws",
                "Draw free body diagrams for complex systems",
                "Solve problems with connected bodies",
                "Apply Newton's laws to lift/elevator problems"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: why does your body jerk forward when a bus suddenly stops? Which Newton's law explains this?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Teach all 3 laws with examples. 1st: inertia (bus example). 2nd: F=ma (pushing cart). 3rd: action-reaction (walking). Ask student to identify which law applies in each scenario."
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Teach free body diagrams. Draw FBD for a block on an incline. Identify normal force, weight components, friction. Solve for acceleration."
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "Two blocks (3kg and 5kg) connected by string on frictionless surface. Force 40N applied on 5kg block. Find acceleration and tension."
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "Elevator problem: a 60kg person in a lift accelerating upward at 2 m/s². What does the scale read? BUET-level."
                }
        ],
        "key_formulas": [
                "F = ma",
                "Weight W = mg",
                "Apparent weight in lift: N = m(g ± a)",
                "Connected bodies: same acceleration, tension is internal force"
        ],
        "common_mistakes": [
                "Confusing mass and weight",
                "Forgetting that action-reaction forces act on DIFFERENT bodies",
                "Not resolving forces into components on inclined planes"
        ],
        "practice_prompts": [
                "A 10kg box on a smooth surface is pushed with 50N. Find acceleration.",
                "In a lift going up with acceleration 3 m/s², what is the apparent weight of a 50kg person?"
        ],
        "real_world_example": "When a CNG auto-rickshaw suddenly brakes, you slide forward — that's Newton's 1st law. The harder the driver brakes (more force), the faster you decelerate (2nd law). Your feet push backward on the floor, floor pushes you forward (3rd law)."
},

    "phy1-04-02": {
        "title": "Friction & Circular Motion",
        "learning_objectives": [
                "Calculate static and kinetic friction",
                "Solve problems on banked roads and circular motion",
                "Apply centripetal force concept",
                "Understand the role of friction in daily life"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: why is it easier to push a box once it starts moving than to start pushing it? What's the difference between static and kinetic friction?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Teach f = μN. Static friction ≤ μₛN, kinetic friction = μₖN. Ask: why is μₛ > μₖ always?"
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Circular motion: centripetal force F = mv²/r. For car on banked road: tan θ = v²/rg. Derive step by step."
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "A car turns on a flat road (μ=0.4, r=50m). Find maximum safe speed. Then: what if the road is banked at 30°?"
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ about friction on incline or centripetal force in vertical circular motion."
                }
        ],
        "key_formulas": [
                "f = μN",
                "Centripetal force F = mv²/r",
                "Banked road: tan θ = v²/rg",
                "Min speed at top of loop: v = √(rg)"
        ],
        "common_mistakes": [
                "Using μmg for friction on incline (should be μN = μmg cos θ)",
                "Confusing centripetal (real) with centrifugal (pseudo) force",
                "Forgetting that static friction has a maximum value, not a fixed value"
        ],
        "practice_prompts": [
                "A 5kg block on a surface with μ=0.3. Find friction when 10N horizontal force applied.",
                "Find the banking angle for a road curve (r=100m) at speed 72 km/h."
        ],
        "real_world_example": "The flyover curves in Dhaka are slightly banked — the road tilts inward so cars don't need to rely only on tire friction. Same reason why cricket bowlers can make the ball curve — friction and circular motion!"
},

    "phy1-05-01": {
        "title": "Work & Energy",
        "learning_objectives": [
                "Calculate work done by constant and variable forces",
                "Apply work-energy theorem",
                "Understand potential and kinetic energy",
                "Apply conservation of energy to solve problems"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: if you carry a heavy bag horizontally across a room, have you done any work on it (in physics terms)? Why or why not?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Teach W = Fd cos θ. When θ=90°, W=0 (carrying bag horizontally). KE = ½mv², PE = mgh. Ask: what type of energy does a flying bird have?"
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Work-energy theorem: net work = change in KE. Solve: a 2kg ball falls from 10m. Find velocity just before hitting ground using energy conservation."
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "A 1000kg car accelerates from 10 m/s to 30 m/s. Find the work done by the engine."
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ: a pendulum released from height h. Find velocity at lowest point. Then: if string is cut at lowest point, what path does it follow?"
                }
        ],
        "key_formulas": [
                "W = Fd cos θ",
                "KE = ½mv²",
                "PE = mgh",
                "Conservation: KE₁ + PE₁ = KE₂ + PE₂"
        ],
        "common_mistakes": [
                "Saying you do work when carrying a bag horizontally (W=0 since F⊥d)",
                "Forgetting that work can be negative (friction does negative work)",
                "Not using energy conservation when it's simpler than force equations"
        ],
        "practice_prompts": [
                "A 50kg boy climbs 10m stairs. How much work against gravity?",
                "A spring (k=200 N/m) compressed 0.1m. Find stored PE."
        ],
        "real_world_example": "When water falls at Kaptai Dam from height h, its PE converts to KE, which spins turbines to generate electricity. The higher the dam, the more energy — that's why Kaptai was built in the hills of Rangamati."
},

    "phy1-05-02": {
        "title": "Power & Collisions",
        "learning_objectives": [
                "Calculate power as rate of work done",
                "Distinguish elastic and inelastic collisions",
                "Apply momentum conservation in collisions",
                "Solve problems involving coefficient of restitution"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: two people carry the same weight up stairs — one takes 1 minute, the other takes 5 minutes. Who does more work? Who has more power?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Power P = W/t = Fv. 1 HP = 746 W. Teach elastic (KE conserved) vs inelastic (KE not conserved) collisions."
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Collision formulas: m₁u₁ + m₂u₂ = m₁v₁ + m₂v₂. For perfectly inelastic: bodies stick together. Solve: 2kg ball at 3m/s hits stationary 1kg ball elastically."
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "A 1500kg car at 20 m/s collides with stationary 1000kg car. They stick together. Find final velocity and energy lost."
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ about collision or power calculation."
                }
        ],
        "key_formulas": [
                "P = W/t = Fv",
                "1 HP = 746 W",
                "Coefficient of restitution e = (v₂-v₁)/(u₁-u₂)",
                "Elastic: e=1, Perfectly inelastic: e=0"
        ],
        "common_mistakes": [
                "Confusing work (same for both) with power (different if time differs)",
                "Thinking momentum is not conserved in inelastic collisions (it IS, only KE isn't)",
                "Forgetting that in 2D collisions, momentum is conserved in each direction separately"
        ],
        "practice_prompts": [
                "A pump lifts 500kg water to 10m in 5 seconds. Find power in watts and HP.",
                "Two identical balls collide elastically head-on. What happens?"
        ],
        "real_world_example": "When a truck hits a small car, both have the same momentum change (Newton's 3rd law) — but the small car gets much more acceleration because F=ma and its mass is less. That's why trucks cause more damage in accidents on the Dhaka-Chittagong highway."
},

    "phy1-06-01": {
        "title": "Gravitation",
        "learning_objectives": [
                "Apply Newton's law of gravitation",
                "Calculate gravitational field strength at different altitudes",
                "Derive orbital velocity and escape velocity",
                "Apply Kepler's laws of planetary motion"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: why does the Moon orbit the Earth instead of flying away? What force keeps it in orbit?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Teach F = GMm/r². Surface gravity g = GM/R². Ask: what happens to g if you go to a mountain top? What about deep inside Earth?"
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Derive orbital velocity v = √(GM/r) and escape velocity vₑ = √(2GM/R) = √(2gR). Ask: why is escape velocity √2 times orbital velocity?"
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "Calculate g at height equal to Earth's radius. Then: find escape velocity from Earth (R=6400km, g=9.8)."
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ about satellite period or variation of g with altitude/depth."
                }
        ],
        "key_formulas": [
                "F = GMm/r²",
                "g = GM/R²",
                "Orbital velocity v₀ = √(GM/r)",
                "Escape velocity vₑ = √(2gR)",
                "Kepler's T² ∝ r³"
        ],
        "common_mistakes": [
                "Using r (distance from center) vs h (height above surface) — g at height h: g'=g(R/(R+h))²",
                "Forgetting that inside Earth, g decreases linearly with depth",
                "Confusing orbital velocity with escape velocity"
        ],
        "practice_prompts": [
                "At what height above Earth is g reduced to g/4?",
                "Find the time period of a satellite orbiting just above Earth's surface."
        ],
        "real_world_example": "Bangladesh's Bangabandhu-1 satellite orbits at 35,786 km (geostationary orbit) — at that height, it takes exactly 24 hours to orbit, so it stays over the same spot above Bangladesh. That's Kepler's third law in action!"
},

    "phy1-07-01": {
        "title": "Elasticity & Fluid Mechanics",
        "learning_objectives": [
                "Define stress, strain, and Young's modulus",
                "Apply Hooke's law within elastic limit",
                "Apply Pascal's law and Archimedes' principle",
                "Use Bernoulli's equation for fluid flow"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: why does a rubber band return to its original shape but clay doesn't? What's the difference?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Teach stress = F/A, strain = ΔL/L, Young's modulus Y = stress/strain. Hooke's law: F = kx. Ask: what happens beyond the elastic limit?"
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Fluid statics: Pascal's law (hydraulic press), Archimedes' principle (buoyancy). Bernoulli's: P + ½ρv² + ρgh = constant."
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "A steel wire (Y=2×10¹¹ Pa, L=2m, A=1mm²) stretched by 100N. Find extension."
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ about buoyancy or Bernoulli's application."
                }
        ],
        "key_formulas": [
                "Stress = F/A, Strain = ΔL/L",
                "Young's modulus Y = Stress/Strain",
                "Pascal's law: pressure transmitted equally",
                "Bernoulli: P + ½ρv² + ρgh = constant"
        ],
        "common_mistakes": [
                "Confusing stress (force per unit area) with pressure (same unit but different concept)",
                "Forgetting that Bernoulli's equation only applies to ideal (inviscid) fluids",
                "Using weight instead of mass in buoyancy calculations"
        ],
        "practice_prompts": [
                "A hydraulic press has pistons of area 10 cm² and 100 cm². Force on small piston is 50N. Find force on large piston.",
                "A block of wood (density 600 kg/m³) floats in water. What fraction is submerged?"
        ],
        "real_world_example": "The hydraulic brakes in buses work on Pascal's law — a small force on the brake pedal creates a large force on the brake pads. And country boats (নৌকা) float because of Archimedes' principle — the water pushes up with a force equal to the weight of water displaced."
},

    "phy1-08-01": {
        "title": "Simple Harmonic Motion",
        "learning_objectives": [
                "Define SHM and identify SHM systems",
                "Derive equations of SHM (displacement, velocity, acceleration)",
                "Calculate time period of simple pendulum and spring-mass system",
                "Understand energy in SHM"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: a swing in a playground goes back and forth. Is the motion uniform? What pattern does it follow?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Define SHM: acceleration proportional to displacement, directed toward mean position. a = -ω²x. Ask: is uniform circular motion related to SHM?"
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Equations: x = A sin(ωt), v = Aω cos(ωt), a = -Aω² sin(ωt). For pendulum: T = 2π√(l/g). For spring: T = 2π√(m/k)."
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "A spring (k=100 N/m) with 0.5kg mass. Find time period and maximum velocity if amplitude is 0.1m."
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ: energy variation in SHM — KE and PE as function of displacement."
                }
        ],
        "key_formulas": [
                "x = A sin(ωt + φ)",
                "T = 2π/ω",
                "Pendulum: T = 2π√(l/g)",
                "Spring: T = 2π√(m/k)",
                "Total energy E = ½kA² = ½mω²A²"
        ],
        "common_mistakes": [
                "Thinking pendulum period depends on mass (it doesn't for simple pendulum)",
                "Confusing amplitude with displacement at a given time",
                "Forgetting that at mean position KE=max and PE=0, at extreme PE=max and KE=0"
        ],
        "practice_prompts": [
                "A pendulum has T=2s. Find its length.",
                "In SHM, at what displacement is KE equal to PE?"
        ],
        "real_world_example": "The clock pendulums in old Bangladeshi homes (দেয়াল ঘড়ি) are SHM — the longer the pendulum, the slower it swings. That's why grandfather clocks are tall!"
},

    "phy1-09-01": {
        "title": "Wave Properties",
        "learning_objectives": [
                "Distinguish transverse and longitudinal waves",
                "Apply v = fλ relationship",
                "Understand superposition and standing waves",
                "Calculate frequency of vibrating strings and air columns"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: when you throw a stone in a pond, ripples spread out. Is the water actually moving outward, or is it something else?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Teach transverse (particle ⊥ wave direction) vs longitudinal (particle ∥ wave direction). v = fλ. Ask: is sound transverse or longitudinal?"
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Standing waves on string: harmonics. f_n = n(v/2L). For closed pipe: only odd harmonics. Open pipe: all harmonics."
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "A string (L=1m, μ=0.01 kg/m) under tension 40N. Find fundamental frequency and first three harmonics."
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ about standing waves in pipes or strings."
                }
        ],
        "key_formulas": [
                "v = fλ",
                "String: v = √(T/μ)",
                "String harmonics: fₙ = nv/2L",
                "Open pipe: fₙ = nv/2L (all n)",
                "Closed pipe: fₙ = nv/4L (odd n only)"
        ],
        "common_mistakes": [
                "Thinking wave speed depends on frequency (it depends on medium)",
                "Forgetting closed pipe has only odd harmonics",
                "Confusing nodes and antinodes in standing waves"
        ],
        "practice_prompts": [
                "Sound speed is 340 m/s. Find wavelength of 680 Hz sound.",
                "A closed pipe has fundamental 200 Hz. What is its 2nd overtone?"
        ],
        "real_world_example": "When a বাঁশি (bamboo flute) player covers different holes, they change the effective length of the air column — shorter column = higher frequency = higher pitch. That's standing waves in an open pipe!"
},

    "phy1-09-02": {
        "title": "Sound & Doppler Effect",
        "learning_objectives": [
                "Calculate beat frequency",
                "Apply Doppler effect formula for moving source/observer",
                "Understand resonance and its applications",
                "Solve problems on speed of sound in different media"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: why does an ambulance siren sound higher-pitched when approaching and lower when moving away?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Doppler effect: f' = f(v ± v₀)/(v ∓ vₛ). Convention: approaching = higher, receding = lower. Ask: what if both source and observer are moving?"
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Beats: when two frequencies are close, f_beat = |f₁ - f₂|. Resonance: when driving frequency = natural frequency, amplitude is maximum."
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "An ambulance (f=500Hz) moves at 30 m/s toward you. Speed of sound = 340 m/s. Find the frequency you hear."
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ about Doppler effect or beats."
                }
        ],
        "key_formulas": [
                "Doppler: f' = f(v + v₀)/(v - vₛ) (approaching)",
                "Beat frequency = |f₁ - f₂|",
                "Speed of sound in air ≈ 340 m/s at 20°C",
                "v_sound ∝ √T (temperature in Kelvin)"
        ],
        "common_mistakes": [
                "Getting signs wrong in Doppler formula (remember: approaching = higher frequency)",
                "Thinking beats frequency = average of two frequencies (it's the difference)",
                "Forgetting speed of sound changes with temperature"
        ],
        "practice_prompts": [
                "Two tuning forks of 256 Hz and 260 Hz are sounded together. How many beats per second?",
                "A train (speed 36 km/h) blows whistle at 500 Hz. Find frequency heard by stationary observer as train approaches."
        ],
        "real_world_example": "Next time you hear a motorcycle zooming past on the highway, notice how the pitch drops as it passes you — that's the Doppler effect. Astronomers use the same principle to tell if a star is moving toward or away from us (red shift/blue shift)."
},

    "phy1-10-01": {
        "title": "Gas Laws & Kinetic Theory",
        "learning_objectives": [
                "Apply ideal gas equation PV = nRT",
                "Derive kinetic energy from kinetic theory",
                "Understand Maxwell-Boltzmann distribution",
                "Apply gas laws to solve problems"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: why does a balloon expand when you heat it? What's happening to the gas molecules inside?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Teach PV = nRT. Gas laws: Boyle's (P∝1/V), Charles's (V∝T), Gay-Lussac's (P∝T). Ask: what is an ideal gas?"
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Kinetic theory: KE = (3/2)kT. RMS speed v_rms = √(3RT/M). Ask: which gas molecules move faster at same temperature — hydrogen or oxygen?"
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "2 moles of ideal gas at 300K in 10L container. Find pressure. Then: if temperature doubles at constant volume, new pressure?"
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ about KE of gas molecules or gas law application."
                }
        ],
        "key_formulas": [
                "PV = nRT (R = 8.314 J/mol·K)",
                "KE_avg = (3/2)kT",
                "v_rms = √(3RT/M)",
                "Boyle: P₁V₁ = P₂V₂",
                "Charles: V₁/T₁ = V₂/T₂"
        ],
        "common_mistakes": [
                "Using Celsius instead of Kelvin in gas law calculations",
                "Confusing R (gas constant) with k (Boltzmann constant) — k = R/Nₐ",
                "Thinking all gas molecules move at the same speed (they have a distribution)"
        ],
        "practice_prompts": [
                "Find the RMS speed of N₂ molecules at 27°C. (M=28 g/mol)",
                "A gas at 2 atm and 300K is heated to 600K at constant volume. Find new pressure."
        ],
        "real_world_example": "The pressure cooker in every Bangladeshi kitchen works on Gay-Lussac's law — as temperature increases at constant volume, pressure increases. That's why food cooks faster inside — higher pressure means higher boiling point of water!"
},


    "chem1-03-02": {
        "title": "Chemical Bonding",
        "learning_objectives": [
                "Distinguish ionic, covalent, and metallic bonds",
                "Draw Lewis structures and apply VSEPR theory",
                "Explain hybridization (sp, sp², sp³)",
                "Predict molecular geometry and polarity"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: why do atoms bond? Why doesn't helium form bonds but sodium does?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Teach ionic (electron transfer) vs covalent (sharing). Draw NaCl and H₂O Lewis structures. Ask: which has higher melting point and why?"
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "VSEPR theory: electron pairs repel. sp³=tetrahedral, sp²=trigonal planar, sp=linear. Ask: what is the shape of CH₄? NH₃? H₂O?"
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "Draw Lewis structure of CO₂. What hybridization? What shape? Is it polar or nonpolar?"
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ: predict the bond angle in BF₃ vs NF₃. Why are they different?"
                }
        ],
        "key_formulas": [
                "Ionic bond: metal + nonmetal",
                "Covalent bond: nonmetal + nonmetal",
                "sp³: 109.5°, sp²: 120°, sp: 180°",
                "VSEPR: minimize electron pair repulsion"
        ],
        "common_mistakes": [
                "Thinking all covalent compounds are nonpolar (HCl is polar covalent)",
                "Forgetting lone pairs affect molecular geometry (NH₃ is pyramidal, not tetrahedral)",
                "Confusing electron geometry with molecular geometry"
        ],
        "practice_prompts": [
                "What is the hybridization of carbon in ethene (C₂H₄)?",
                "Why is water bent (104.5°) instead of linear?"
        ],
        "real_world_example": "Table salt (NaCl) dissolves in water because water molecules pull apart the ionic bond — the Na⁺ and Cl⁻ ions separate. But oil (covalent, nonpolar) doesn't dissolve because water is polar. That's why তেল (oil) and জল (water) don't mix in your kitchen!"
},

    "chem1-04-01": {
        "title": "Chemical Equilibrium",
        "learning_objectives": [
                "Write equilibrium expressions (Kc, Kp)",
                "Apply Le Chatelier's principle",
                "Calculate equilibrium concentrations",
                "Distinguish between Kc and Kp"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: if you open a bottle of Coca-Cola, bubbles come out. But in the sealed bottle, was the CO₂ not dissolving and undissolving at the same time?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Dynamic equilibrium: forward rate = reverse rate. Kc = [products]/[reactants]. Ask: what does a large Kc mean?"
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Le Chatelier: if you disturb equilibrium, it shifts to counteract. Add reactant → shifts right. Increase temperature for exothermic → shifts left."
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "N₂ + 3H₂ ⇌ 2NH₃ (exothermic). What happens if we: (a) add N₂, (b) increase pressure, (c) increase temperature?"
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "Calculate Kc: if [N₂]=0.1, [H₂]=0.3, [NH₃]=0.2 at equilibrium."
                }
        ],
        "key_formulas": [
                "Kc = [C]ᶜ[D]ᵈ / [A]ᵃ[B]ᵇ",
                "Kp = Kc(RT)^Δn",
                "Le Chatelier's principle",
                "Q vs K: Q<K→forward, Q>K→reverse"
        ],
        "common_mistakes": [
                "Including solids and pure liquids in the Kc expression",
                "Thinking a catalyst changes equilibrium position (it only speeds up reaching equilibrium)",
                "Confusing Kc (concentration) with Kp (pressure)"
        ],
        "practice_prompts": [
                "For 2SO₂ + O₂ ⇌ 2SO₃, write the Kc expression.",
                "If Kc = 4.0 and initial [A]=1M, [B]=1M for A ⇌ B, find equilibrium concentrations."
        ],
        "real_world_example": "The Haber process for making fertilizer (NH₃) at Chittagong's KAFCO factory uses Le Chatelier's principle: high pressure (200 atm) and moderate temperature (450°C) to push equilibrium toward NH₃ production. Bangladesh imports most fertilizer, but understanding equilibrium could help optimize local production."
},

    "chem1-04-02": {
        "title": "Acids, Bases & Redox",
        "learning_objectives": [
                "Calculate pH from H⁺ concentration",
                "Identify oxidation and reduction in reactions",
                "Balance redox equations",
                "Apply Brønsted-Lowry and Lewis acid-base theories"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: lemon juice is sour, soap is slippery. What makes them different chemically?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "pH = -log[H⁺]. pH<7 acidic, pH>7 basic. Brønsted acid = proton donor. Ask: is water an acid or base?"
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Redox: oxidation = loss of electrons, reduction = gain. OIL RIG mnemonic. Assign oxidation numbers in Fe₂O₃ + CO → Fe + CO₂."
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "Find pH of 0.01M HCl. Then: find pH of 0.1M NaOH."
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "Balance this redox reaction in acidic medium: MnO₄⁻ + Fe²⁺ → Mn²⁺ + Fe³⁺"
                }
        ],
        "key_formulas": [
                "pH = -log[H⁺]",
                "pOH = -log[OH⁻]",
                "pH + pOH = 14",
                "OIL RIG: Oxidation Is Loss, Reduction Is Gain"
        ],
        "common_mistakes": [
                "Forgetting that pH is a LOG scale (pH 3 is 10x more acidic than pH 4)",
                "Confusing oxidation number with charge",
                "Not balancing atoms AND charges in redox equations"
        ],
        "practice_prompts": [
                "What is the pH of pure water?",
                "In 2Mg + O₂ → 2MgO, which is oxidized and which is reduced?"
        ],
        "real_world_example": "When you add তেঁতুল (tamarind, acidic) to your tarkari, the sour taste is from H⁺ ions. Adding baking soda (basic) neutralizes it. The pH of the Padma river water matters for fish survival — too acidic or basic and fish die."
},

    "chem2-02-01": {
        "title": "IUPAC Naming & Functional Groups",
        "learning_objectives": [
                "Name organic compounds using IUPAC rules",
                "Identify functional groups in organic molecules",
                "Classify organic compounds by functional group",
                "Draw structural formulas from IUPAC names"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: methane, ethane, propane — do you see a pattern in the names? What do you think butane has?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "IUPAC naming: find longest chain, number carbons, name substituents. Meth=1, Eth=2, Prop=3, But=4. Suffixes: -ane, -ene, -yne, -ol, -al, -one, -oic acid."
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Functional groups: -OH (alcohol), -CHO (aldehyde), -COOH (carboxylic acid), -NH₂ (amine). Ask: name CH₃CH₂OH using IUPAC rules."
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "Name: CH₃CH(CH₃)CH₂CH₃. Then: draw the structure of 2-methylpropan-1-ol."
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ: name a branched compound with a functional group."
                }
        ],
        "key_formulas": [
                "Alkane: CₙH₂ₙ₊₂",
                "Alkene: CₙH₂ₙ",
                "Alkyne: CₙH₂ₙ₋₂",
                "Alcohol: R-OH, Aldehyde: R-CHO, Ketone: R-CO-R'"
        ],
        "common_mistakes": [
                "Not choosing the longest carbon chain as the parent chain",
                "Numbering from the wrong end (should give lowest locants to substituents)",
                "Confusing -al (aldehyde) with -ol (alcohol)"
        ],
        "practice_prompts": [
                "Name CH₃CH₂CH₂OH",
                "Draw 3-ethyl-2-methylpentane"
        ],
        "real_world_example": "The smell of পাকা আম (ripe mango) comes from organic compounds called esters. Vinegar is acetic acid (ethanoic acid). The natural gas used in Bangladeshi kitchens is mainly methane (CH₄) — the simplest organic compound!"
},

    "chem2-02-02": {
        "title": "Hydrocarbons & Organic Reactions",
        "learning_objectives": [
                "Classify hydrocarbons as saturated/unsaturated",
                "Explain isomerism (structural and geometrical)",
                "Describe substitution, addition, and elimination reactions",
                "Predict products of organic reactions"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: petrol, diesel, kerosene are all hydrocarbons. What's the difference between them?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Saturated (single bonds only) vs unsaturated (double/triple bonds). Alkanes do substitution, alkenes do addition. Ask: why can't alkanes do addition reactions?"
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Isomerism: same formula, different structure. CH₃CH₂CH₂CH₃ vs CH₃CH(CH₃)CH₃ — both C₄H₁₀. Teach geometrical isomerism (cis-trans) in alkenes."
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "Write the products: CH₂=CH₂ + HBr → ? (addition). CH₄ + Cl₂ → ? (substitution with UV light)."
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "How many structural isomers does C₅H₁₂ have? Draw all of them."
                }
        ],
        "key_formulas": [
                "Substitution: CH₄ + Cl₂ → CH₃Cl + HCl (UV)",
                "Addition: CH₂=CH₂ + H₂ → CH₃CH₃",
                "Markovnikov's rule: H adds to C with more H's",
                "C₅H₁₂ has 3 isomers"
        ],
        "common_mistakes": [
                "Applying Markovnikov's rule incorrectly",
                "Forgetting UV light is needed for free radical substitution",
                "Not counting all possible structural isomers"
        ],
        "practice_prompts": [
                "What is the product of propene + HCl (Markovnikov)?",
                "Draw all isomers of C₄H₁₀."
        ],
        "real_world_example": "The Sylhet natural gas fields produce methane and ethane. At refineries, crude oil is separated into petrol (C₅-C₈), kerosene (C₁₂-C₁₅), and diesel (C₁₅-C₂₀) by fractional distillation — longer chains = higher boiling point."
},

    "chem2-03-01": {
        "title": "Mole Concept & Stoichiometry",
        "learning_objectives": [
                "Calculate moles from mass and vice versa",
                "Apply Avogadro's number in calculations",
                "Use mole ratios in stoichiometric calculations",
                "Find limiting reagent and percentage yield"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: a dozen eggs = 12 eggs. A mole of atoms = ? atoms. Why do chemists use such a huge number?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "1 mole = 6.022 × 10²³ particles. Molar mass of H₂O = 18 g/mol. Moles = mass/molar mass. Ask: how many moles in 36g of water?"
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Stoichiometry: balanced equation gives mole ratios. 2H₂ + O₂ → 2H₂O means 2 moles H₂ reacts with 1 mole O₂. Teach limiting reagent concept."
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "How many grams of CO₂ produced when 12g of C burns completely? (C + O₂ → CO₂)"
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "10g H₂ and 64g O₂ react. Find limiting reagent and mass of water produced."
                }
        ],
        "key_formulas": [
                "n = m/M",
                "Nₐ = 6.022 × 10²³",
                "At STP: 1 mole gas = 22.4 L",
                "% yield = (actual/theoretical) × 100"
        ],
        "common_mistakes": [
                "Confusing molar mass with atomic mass number",
                "Not balancing the equation before doing stoichiometry",
                "Forgetting to identify the limiting reagent in excess reagent problems"
        ],
        "practice_prompts": [
                "How many molecules in 9g of water?",
                "50g CaCO₃ heated: CaCO₃ → CaO + CO₂. Find mass of CO₂."
        ],
        "real_world_example": "When a ফার্মেসি (pharmacy) makes medicine, they need exact amounts — too little active ingredient won't work, too much is dangerous. Stoichiometry ensures the right mole ratios. Same principle applies when mixing cement for building construction in Bangladesh."
},

    "chem2-04-01": {
        "title": "Electrochemistry",
        "learning_objectives": [
                "Calculate cell potential using E° values",
                "Apply Nernst equation",
                "Explain Faraday's laws of electrolysis",
                "Distinguish galvanic from electrolytic cells"
        ],
        "teaching_steps": [
                {
                        "step": 1,
                        "type": "intro",
                        "prompt": "Ask: how does a battery produce electricity? What's happening inside at the atomic level?"
                },
                {
                        "step": 2,
                        "type": "concept",
                        "prompt": "Galvanic cell: spontaneous redox → electricity. E°cell = E°cathode - E°anode. If E°cell > 0, reaction is spontaneous."
                },
                {
                        "step": 3,
                        "type": "teach",
                        "prompt": "Faraday's law: mass deposited ∝ charge passed. m = (M × I × t)/(n × F). F = 96500 C/mol. Solve: how much copper deposited by 2A current for 1 hour?"
                },
                {
                        "step": 4,
                        "type": "practice",
                        "prompt": "Calculate E°cell for Zn-Cu cell. E°(Zn²⁺/Zn) = -0.76V, E°(Cu²⁺/Cu) = +0.34V."
                },
                {
                        "step": 5,
                        "type": "mastery",
                        "prompt": "BUET MCQ about Nernst equation or electrolysis calculation."
                }
        ],
        "key_formulas": [
                "E°cell = E°cathode - E°anode",
                "Nernst: E = E° - (RT/nF)ln Q",
                "Faraday: m = MIt/nF",
                "F = 96500 C/mol"
        ],
        "common_mistakes": [
                "Getting anode and cathode confused (anode = oxidation, cathode = reduction)",
                "Forgetting to convert time to seconds in Faraday's law",
                "Using wrong n (number of electrons transferred) in Nernst equation"
        ],
        "practice_prompts": [
                "Is a cell with E°cell = -0.5V spontaneous?",
                "How long to deposit 63.5g Cu from CuSO₄ using 5A current?"
        ],
        "real_world_example": "The battery rickshaws (ব্যাটারি চালিত রিকশা) in Dhaka use lead-acid batteries — a galvanic cell where lead reacts with sulfuric acid. When you charge your phone, that's an electrolytic cell — using electricity to reverse the chemical reaction."
    },

    # ══ HIGHER MATHEMATICS — Chapter 4: বৃত্ত (Circle) ══
    "hm1-04-01": {
        "title": "Circles (Equation, Tangent & Normal)",
        "learning_objectives": [
            "Derive and apply the standard equation of a circle x² + y² = r² and general form x² + y² + 2gx + 2fy + c = 0",
            "Find center and radius from the general equation (center = (−g, −f), radius = √(g²+f²−c))",
            "Determine the equation of a circle given different conditions (center-radius, diameter endpoints, three points)",
            "Find equations of tangent and normal to a circle at a given point and from an external point",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: think of the Shaheed Minar roundabout in Dhaka — every point on the circular road is the same distance from the center. If we place the center at the origin, how would you write the equation describing all points on that circle?",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Derive x² + y² = r² from the distance formula. Then shift center to (h, k): (x−h)² + (y−k)² = r². Expand to get the general form x² + y² + 2gx + 2fy + c = 0 where center = (−g, −f), radius = √(g²+f²−c). Ask: what condition must hold for this to represent a real circle? (g²+f²−c > 0)",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Teach how to find circle equations from conditions: (a) given center and radius — direct substitution, (b) given endpoints of diameter — use (x−x₁)(x−x₂) + (y−y₁)(y−y₂) = 0, (c) given three points on the circle — substitute into general form and solve 3 equations. Then teach tangent: at point (x₁, y₁) on x²+y²=r², tangent is xx₁+yy₁=r². For general form, replace x² by xx₁, y² by yy₁, 2x by (x+x₁), 2y by (y+y₁).",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Problem: Find the equation of the circle passing through (1, 2), (3, 4), and (5, 2). Then find the equation of the tangent to x² + y² = 25 at the point (3, 4). Verify that the tangent is perpendicular to the radius at that point.",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "BUET-level: Find the length of the tangent from the external point (7, 1) to the circle x² + y² − 4x − 6y + 9 = 0. Then find the equation of the pair of tangents from (7, 1) to this circle. Also: two circles x² + y² = 9 and x² + y² − 6x − 8y + 9 = 0 — do they intersect, touch, or are separate? Find the radical axis.",
            },
        ],
        "key_formulas": [
            "Standard form: (x−h)² + (y−k)² = r²",
            "General form: x² + y² + 2gx + 2fy + c = 0, center (−g, −f), radius √(g²+f²−c)",
            "Tangent at (x₁,y₁) on x²+y²=r²: xx₁ + yy₁ = r²",
            "Tangent with slope m to x²+y²=r²: y = mx ± r√(1+m²)",
            "Length of tangent from (x₁,y₁) to circle: √(x₁²+y₁²+2gx₁+2fy₁+c)",
            "Condition for tangency: distance from center to line = radius",
            "Radical axis of two circles S₁=0, S₂=0: S₁ − S₂ = 0",
        ],
        "common_mistakes": [
            "Forgetting the condition g²+f²−c > 0 for a real circle — if g²+f²−c = 0, it is a point circle; if negative, no real circle exists",
            "Sign error when reading center from general form — center is (−g, −f), not (g, f); students frequently forget the negative sign",
            "When finding tangent from an external point, confusing the tangent length formula with the distance formula — tangent length uses √(S₁) where S₁ is the value obtained by substituting the point in the circle equation",
        ],
        "practice_prompts": [
            "Find center and radius of x² + y² − 6x + 8y − 11 = 0. Sketch the circle showing center, radius, and intercepts.",
            "Find the equation of the circle with center (2, −3) that touches the x-axis. What is its radius?",
            "The line y = mx + c is tangent to x² + y² = 16. Find the relationship between m and c. Hence find the tangent lines with slope 3/4.",
        ],
        "real_world_example": "The Bangabandhu Satellite ground station antenna has a circular dish. Engineers use circle equations to design the parabolic reflector cross-section. When planning circular roundabouts like the Farmgate or Mohakhali flyover loops in Dhaka, RAJUK engineers use tangent and normal calculations to ensure smooth road entry and exit at the correct angle.",
    },

    # ══ HIGHER MATHEMATICS — Chapter 5: বিন্যাস ও সমাবেশ (Permutations & Combinations) ══
    "hm1-05-01": {
        "title": "Permutations & Combinations",
        "learning_objectives": [
            "Apply the fundamental counting principle (multiplication and addition rules)",
            "Calculate permutations nPr = n!/(n−r)! for arrangements where order matters",
            "Calculate combinations nCr = n!/(r!(n−r)!) for selections where order does not matter",
            "Solve problems involving repeated objects, circular permutations, and restricted arrangements",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: you have 5 friends and want to select 3 to form a cricket team's opening trio. Does the order matter? What if you need to assign them as batsman 1, 2, and 3 — does order matter now? This is the difference between combinations and permutations.",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Teach the fundamental counting principle: if task 1 can be done in m ways and task 2 in n ways, together they can be done in m × n ways. Then factorials: n! = n × (n−1) × ... × 1, with 0! = 1. Permutations: nPr = n!/(n−r)! — order matters. Ask: how many 3-digit numbers can be formed from digits 1-5 without repetition?",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Teach combinations: nCr = n!/(r!(n−r)!). Key property: nCr = nC(n−r). Then special cases: permutations with repeated objects: n!/(p!q!r!...) where p, q, r are frequencies. Circular permutations: (n−1)! for n objects in a circle. Ask: how many ways can 5 people sit around a round table? How many distinct arrangements of the letters in MISSISSIPPI?",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Problem: From a group of 7 boys and 5 girls, a committee of 5 is to be formed. How many committees can be formed if: (a) there are no restrictions, (b) exactly 2 girls must be included, (c) at least 1 girl must be included? Use complementary counting for part (c).",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "BUET-level: How many 4-letter words (with or without meaning) can be formed from the letters of EQUATION such that each word starts with a vowel and ends with a consonant? Then: find the number of ways to distribute 10 identical sweets among 4 children such that each child gets at least 1 sweet. (Stars and bars: C(n−1, r−1) = C(9,3))",
            },
        ],
        "key_formulas": [
            "nPr = n! / (n−r)!  — permutations (order matters)",
            "nCr = n! / (r!(n−r)!)  — combinations (order does not matter)",
            "nCr = nC(n−r)  — symmetry property",
            "Permutations of n objects with repetition: n! / (p₁! × p₂! × ... × pₖ!)",
            "Circular permutations of n objects: (n−1)!",
            "Stars and bars: distributing n identical items into r distinct bins = C(n+r−1, r−1)",
            "With 'at least one' condition: total − none = C(n,r) − C(n−k, r) or use complementary counting",
        ],
        "common_mistakes": [
            "Confusing permutation with combination — ask yourself 'does the order of selection matter?' If choosing a committee, order does not matter (combination). If assigning positions/ranks, order matters (permutation)",
            "Forgetting 0! = 1 — this is used in nCn = n!/n!0! = 1 and nC0 = 1",
            "In problems with restrictions (e.g., certain people must be included or excluded), not separating the restricted elements first before counting the remaining selections",
        ],
        "practice_prompts": [
            "How many ways can the letters of the word ARRANGE be arranged? How many of these have the two R's together?",
            "A cricket team of 11 must be chosen from 15 players. If 2 particular players are always included and 3 are always excluded, how many selections are possible?",
            "In how many ways can 8 people be seated around a circular table if 2 particular people must sit next to each other?",
        ],
        "real_world_example": "In the Bangladesh national cricket team selection, the selectors choose 11 from about 30 players — that is C(30,11). But when the coach decides the batting order, that becomes a permutation problem. For the BUET admission test with 12,000+ seats and 100,000+ applicants, the number of possible admit lists is astronomically large — combinatorics tells us exactly how large.",
    },

    # ══ HIGHER MATHEMATICS — Chapter 6: ত্রিকোণমিতিক অনুপাত ও অভেদাবলি (Trigonometric Ratios & Identities) ══
    "hm1-06-01": {
        "title": "Trigonometric Ratios & Fundamental Identities",
        "learning_objectives": [
            "Define the six trigonometric ratios (sin, cos, tan, csc, sec, cot) for any angle using the unit circle",
            "Prove and apply the Pythagorean identities: sin²θ + cos²θ = 1, 1 + tan²θ = sec²θ, 1 + cot²θ = csc²θ",
            "Determine signs of trigonometric functions in all four quadrants (ASTC rule)",
            "Evaluate trigonometric functions for standard angles and prove trigonometric identities",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: if you stand at the base of the National Parliament Building (Jatiyo Sangsad Bhaban) and look up at the top, the angle your line of sight makes with the ground is the angle of elevation. How would you calculate the building's height knowing only this angle and your distance from the base? This is where trigonometric ratios come in.",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Define sin, cos, tan from a right triangle (SOH CAH TOA). Extend to the unit circle: for angle θ, the point on the unit circle is (cos θ, sin θ). Derive the Pythagorean identity sin²θ + cos²θ = 1 from x² + y² = 1. Divide by cos²θ to get 1 + tan²θ = sec²θ, by sin²θ to get 1 + cot²θ = csc²θ. Ask student to verify for θ = 30°.",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Teach the ASTC rule (All Sin Tan Cos) for signs in quadrants — mnemonic: 'After School To College'. Standard angle values: construct the table for 0°, 30°, 45°, 60°, 90° using sin θ = √0/2, √1/2, √2/2, √3/2, √4/2. Then teach allied angles: sin(180°−θ) = sin θ, cos(180°−θ) = −cos θ, sin(90°−θ) = cos θ, etc. Give techniques for proving identities: start from more complex side, convert everything to sin and cos.",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Prove: (1 + tan²θ)/(1 + cot²θ) = tan²θ. Then prove: (sec θ − tan θ)² = (1 − sin θ)/(1 + sin θ). Ask student to verify each identity numerically with θ = 45° as a check.",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "BUET-level: If sin θ + cos θ = √2, find the value of sin⁶θ + cos⁶θ. (Hint: first find sin θ cos θ from squaring the given equation, then use the factorization a³+b³ = (a+b)(a²−ab+b²) with a = sin²θ, b = cos²θ). Also prove: tan A + tan B + tan C = tan A · tan B · tan C for any triangle ABC.",
            },
        ],
        "key_formulas": [
            "sin²θ + cos²θ = 1",
            "1 + tan²θ = sec²θ",
            "1 + cot²θ = csc²θ",
            "ASTC: Q1 all +, Q2 sin +, Q3 tan +, Q4 cos +",
            "sin(90°−θ) = cos θ, cos(90°−θ) = sin θ",
            "sin(180°−θ) = sin θ, cos(180°−θ) = −cos θ",
            "a³+b³ = (a+b)(a²−ab+b²) — useful for sin⁶+cos⁶ type problems",
            "In triangle ABC: A+B+C = π, so tan A + tan B + tan C = tan A · tan B · tan C",
        ],
        "common_mistakes": [
            "Writing sin²θ + cos²θ = 1 but then incorrectly simplifying sin²θ = 1 − cos θ (forgetting the square on cos θ)",
            "Confusing allied angle formulas — when the angle changes from 90°±θ, the function changes (sin<->cos, tan<->cot, sec<->csc); for 180°±θ or 360°±θ, the function stays the same but sign may change",
            "Trying to prove an identity by cross-multiplying or moving terms from one side to the other — an identity proof should manipulate only one side (or both sides independently) to show they equal the same expression",
        ],
        "practice_prompts": [
            "Without using a calculator, find: sin 150° + cos 240° + tan 315° + cot 210°.",
            "Prove: (sin A + csc A)² + (cos A + sec A)² = 7 + tan²A + cot²A.",
            "If 3 sin θ + 4 cos θ = 5, find the value of 3 cos θ − 4 sin θ. (Hint: square both equations and add.)",
        ],
        "real_world_example": "Surveyors from the Bangladesh Survey Department use trigonometric ratios to measure the heights of buildings and the widths of rivers like the Padma without crossing them. By measuring one distance and one angle, they calculate everything else. The entire GPS system that your Pathao or Uber ride uses relies on trigonometry to calculate your position from satellite signals.",
    },

    # ══ HIGHER MATHEMATICS — Chapter 7: যৌগিক ও গুণিতক কোণের ত্রিকোণমিতি (Compound & Multiple Angles) ══
    "hm1-07-01": {
        "title": "Compound & Multiple Angle Formulas",
        "learning_objectives": [
            "Apply compound angle formulas: sin(A±B), cos(A±B), tan(A±B)",
            "Derive and use double angle formulas: sin 2A, cos 2A (three forms), tan 2A",
            "Derive and use half angle formulas: sin(A/2), cos(A/2), tan(A/2)",
            "Transform products to sums and sums to products (prosthaphaeresis formulas)",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: can you find sin 75° without a calculator? If you know sin 45° and sin 30°, is sin 75° = sin 45° + sin 30°? (No! sin is not linear.) Then: sin 75° = sin(45° + 30°). This is where compound angle formulas shine.",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Derive sin(A+B) = sin A cos B + cos A sin B geometrically or from the rotation matrix approach. From this derive: sin(A−B), cos(A+B) = cos A cos B − sin A sin B, cos(A−B), tan(A+B) = (tan A + tan B)/(1 − tan A tan B). Ask student to find the exact value of sin 75°, cos 15°, and tan 105° using these formulas.",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Set B = A in compound formulas to get double angle: sin 2A = 2 sin A cos A, cos 2A = cos²A − sin²A = 2cos²A − 1 = 1 − 2sin²A, tan 2A = 2tan A/(1 − tan²A). From cos 2A forms, derive half-angle formulas. Then teach product-to-sum: 2 sin A cos B = sin(A+B) + sin(A−B), and sum-to-product: sin C + sin D = 2 sin((C+D)/2) cos((C−D)/2). Ask: express sin 5x + sin 3x as a product.",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Problem: Prove that cos 20° cos 40° cos 60° cos 80° = 1/16. (Hint: use cos 60° = 1/2, then apply product-to-sum formulas repeatedly). Then: if tan A = 1/2 and tan B = 1/3, find A + B. (Answer: π/4, since tan(A+B) = (1/2+1/3)/(1−1/6) = 1)",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "BUET-level: Prove that sin 20° sin 40° sin 80° = √3/8. Also: solve the equation sin x + sin 3x + sin 5x = 0 for 0 ≤ x ≤ π using the sum-to-product formula. Then: if sin A + sin B = 1/2 and cos A + cos B = √3/2, find A − B and A + B.",
            },
        ],
        "key_formulas": [
            "sin(A±B) = sin A cos B ± cos A sin B",
            "cos(A±B) = cos A cos B ∓ sin A sin B",
            "tan(A±B) = (tan A ± tan B) / (1 ∓ tan A tan B)",
            "sin 2A = 2 sin A cos A",
            "cos 2A = cos²A − sin²A = 2cos²A − 1 = 1 − 2sin²A",
            "tan 2A = 2tan A / (1 − tan²A)",
            "sin C + sin D = 2 sin((C+D)/2) cos((C−D)/2)",
            "cos C + cos D = 2 cos((C+D)/2) cos((C−D)/2)",
            "2 sin A cos B = sin(A+B) + sin(A−B)",
            "2 cos A cos B = cos(A−B) + cos(A+B)",
        ],
        "common_mistakes": [
            "Writing sin(A+B) = sin A + sin B — this is WRONG; sin is NOT a linear function. The correct expansion involves products of sin and cos",
            "Confusing the sign in cos(A+B) vs sin(A+B) — in cos(A+B) the middle sign is MINUS (cos A cos B − sin A sin B), opposite to the + in the argument",
            "Forgetting there are THREE forms of cos 2A — different forms are useful in different contexts: use 1−2sin²A when you want to eliminate cos, use 2cos²A−1 when you want to eliminate sin",
        ],
        "practice_prompts": [
            "Find the exact values of sin 15°, cos 75°, and tan 22.5° without a calculator.",
            "Prove: (cos A − cos B)/(sin A + sin B) = −tan((A−B)/2). Which sum-to-product formula do you use?",
            "If cos 2A = −1/2 and 0 < A < π, find all possible values of sin A and cos A.",
        ],
        "real_world_example": "Signal processing in Bangladeshi mobile networks (Grameenphone, Robi, Banglalink) uses these exact formulas. When two radio waves combine, the resulting signal is modeled by sin A + sin B = 2 sin((A+B)/2) cos((A−B)/2) — the product-to-sum conversion. This is how your phone separates your call from millions of others on the same tower.",
    },

    # ══ HIGHER MATHEMATICS — Chapter 8: ফাংশন ও গ্রাফ (Functions & Graphs) ══
    "hm1-08-01": {
        "title": "Functions & Graphs (Domain, Range, Inverse & Transformations)",
        "learning_objectives": [
            "Determine domain and range of polynomial, rational, radical, exponential, logarithmic, and trigonometric functions",
            "Sketch graphs of standard functions and apply transformations (shift, stretch, reflection)",
            "Identify and apply properties of even/odd functions and periodic functions",
            "Find and verify inverse functions graphically and algebraically, including domain restriction for non-injective functions",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: the temperature in Dhaka varies throughout the year — it is a function of time. Can you think of its domain (all days of the year) and range (roughly 10°C to 40°C)? Is this function one-to-one? (No — different months can have the same temperature.) Can you find an inverse?",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Review domain restrictions systematically: denominator ≠ 0, expression under √ ≥ 0, log argument > 0. Find domain and range of f(x) = √(4−x²) (domain: [−2,2], range: [0,2] — it is a semicircle!). Then classify: even function f(−x) = f(x) (symmetric about y-axis), odd function f(−x) = −f(x) (symmetric about origin). Ask: is f(x) = x³ − x even, odd, or neither?",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Teach graph transformations: y = f(x) + k (vertical shift), y = f(x−h) (horizontal shift), y = af(x) (vertical stretch), y = f(bx) (horizontal compression), y = −f(x) (reflection in x-axis), y = f(−x) (reflection in y-axis). Apply to sketch y = |x−2| + 1 from y = |x|. Then teach inverse functions: reflect graph in y = x line. Condition: f must be one-to-one (use horizontal line test). For f(x) = x², restrict to x ≥ 0 to get f⁻¹(x) = √x.",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Problem: Sketch the graph of f(x) = 2^(x−1) + 3, identifying domain, range, asymptote, and key points. Then find f⁻¹(x) and sketch it on the same axes. Verify f(f⁻¹(x)) = x. Also: find domain and range of g(x) = ln(x² − 4).",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "BUET-level: Let f(x) = (2x + 3)/(x − 1). Find f⁻¹(x). Show that f(f(x)) = x — this means f is its own inverse (involution). Explain graphically what this means. Then: the function g(x) = x − [x] where [x] is the floor function — sketch its graph, find its domain, range, and period. Is it continuous?",
            },
        ],
        "key_formulas": [
            "Domain of √(f(x)): solve f(x) ≥ 0",
            "Domain of 1/f(x): solve f(x) ≠ 0",
            "Domain of log(f(x)): solve f(x) > 0",
            "Even function: f(−x) = f(x); Odd function: f(−x) = −f(x)",
            "Transformations: y = af(b(x−h)) + k — vertical stretch a, horizontal compress b, shift right h, shift up k",
            "Inverse: swap x and y, solve for y; domain of f⁻¹ = range of f, range of f⁻¹ = domain of f",
            "Horizontal line test: f is one-to-one iff no horizontal line intersects the graph more than once",
        ],
        "common_mistakes": [
            "Confusing horizontal and vertical shifts — y = f(x−2) shifts RIGHT by 2 (not left), because x must be 2 more to get the same y-value. Students intuitively expect the opposite",
            "Finding the inverse of a non-injective function without restricting the domain first — e.g., f(x) = x² does not have an inverse on all of ℝ; must restrict to x ≥ 0 or x ≤ 0",
            "Confusing the graph of y = f(−x) (reflection in y-axis) with y = −f(x) (reflection in x-axis) — students frequently swap these two transformations",
        ],
        "practice_prompts": [
            "Find domain and range of f(x) = (x + 1)/(x² − 4). Identify all asymptotes.",
            "Starting from y = sin x, describe the transformations to obtain y = 3 sin(2x − π/3) + 1. State the amplitude, period, and phase shift.",
            "Prove that f(x) = x³ + x is an odd function. Then show it is one-to-one on ℝ and find a formula for f⁻¹(x) at specific points (or explain why a closed-form inverse is difficult).",
        ],
        "real_world_example": "The water level of the Padma river at Mawa ferry ghat is a periodic function of time — it rises and falls with the tides and seasons. Meteorologists model it as a transformed sine function: h(t) = A sin(Bt + C) + D where A is the amplitude (flood vs dry season difference), B determines the period, C the phase shift, and D the average level. Understanding function transformations lets BWDB engineers predict flood levels and plan evacuations.",
    },

    # ══ HIGHER MATHEMATICS — Chapter 9: সীমা ও অন্তরীকরণ (Limits & Differentiation) ══
    "hm1-09-01": {
        "title": "Limits & Differentiation (Rules & Techniques)",
        "learning_objectives": [
            "Evaluate limits using direct substitution, factoring, rationalization, and L'Hopital's rule",
            "Apply standard limits: lim(x→0) sin x/x = 1, lim(x→0) (eˣ−1)/x = 1, lim(x→∞) (1+1/n)ⁿ = e",
            "Differentiate using first principles (definition) and apply power rule, product rule, quotient rule, and chain rule",
            "Find derivatives of polynomial, trigonometric, exponential, and logarithmic functions",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: if a rickshaw in Dhaka travels 100 meters in 20 seconds, its average speed is 5 m/s. But what is its speed at exactly the 10th second? To find instantaneous speed, you need limits — as the time interval shrinks to zero, the average speed approaches the instantaneous speed. This is the fundamental idea of calculus.",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Define limit: lim(x→a) f(x) = L means f(x) gets arbitrarily close to L as x approaches a. Teach evaluation techniques: (1) direct substitution, (2) if 0/0, factorize and cancel, (3) rationalize for expressions with surds, (4) standard limits: lim(x→0) sin x/x = 1, lim(x→0) tan x/x = 1, lim(x→0) (eˣ−1)/x = 1, lim(x→∞)(1+1/n)ⁿ = e. Ask: find lim(x→2) (x²−4)/(x−2).",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Define derivative from first principles: f'(x) = lim(h→0) [f(x+h)−f(x)]/h. Derive d/dx(xⁿ) = nxⁿ⁻¹ using the binomial theorem. Then teach the rules: (1) Power rule: d/dx(xⁿ) = nxⁿ⁻¹, (2) Product rule: (uv)' = u'v + uv', (3) Quotient rule: (u/v)' = (u'v−uv')/v², (4) Chain rule: d/dx[f(g(x))] = f'(g(x))·g'(x). Teach standard derivatives: d/dx(sin x) = cos x, d/dx(cos x) = −sin x, d/dx(eˣ) = eˣ, d/dx(ln x) = 1/x.",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Problem set: (a) Find lim(x→0) (1−cos x)/x² using the identity 1−cos x = 2sin²(x/2). (b) Differentiate f(x) = x² sin x using product rule. (c) Differentiate g(x) = (3x+1)⁵ using chain rule. (d) Differentiate h(x) = ln(sin x) using chain rule. (e) Find dy/dx if y = e^(x²+3x).",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "BUET-level: Find dy/dx by implicit differentiation if x² + y² + 2xy = 1. Then find the derivative of y = xˣ (hint: take ln of both sides first — logarithmic differentiation). Also evaluate: lim(x→0) (tan x − sin x)/x³ — this is a classic admission MCQ. (Answer: 1/2)",
            },
        ],
        "key_formulas": [
            "f'(x) = lim(h→0) [f(x+h) − f(x)] / h — definition of derivative",
            "d/dx(xⁿ) = nxⁿ⁻¹ (power rule)",
            "d/dx(uv) = u'v + uv' (product rule)",
            "d/dx(u/v) = (u'v − uv') / v² (quotient rule)",
            "d/dx[f(g(x))] = f'(g(x)) · g'(x) (chain rule)",
            "d/dx(sin x) = cos x, d/dx(cos x) = −sin x, d/dx(tan x) = sec²x",
            "d/dx(eˣ) = eˣ, d/dx(aˣ) = aˣ ln a, d/dx(ln x) = 1/x",
            "lim(x→0) sin x/x = 1, lim(x→0) (eˣ−1)/x = 1, lim(x→∞)(1+1/n)ⁿ = e",
        ],
        "common_mistakes": [
            "Applying the power rule to eˣ — d/dx(eˣ) is NOT xeˣ⁻¹; the power rule works for xⁿ (variable base, constant exponent), not aˣ (constant base, variable exponent)",
            "Forgetting the chain rule when differentiating composite functions — d/dx(sin(3x)) = cos(3x) × 3, not just cos(3x). The inner derivative must be multiplied",
            "In the quotient rule, getting the numerator order wrong — it is u'v − uv', not uv' − u'v (the derivative of the numerator comes first)",
        ],
        "practice_prompts": [
            "Differentiate from first principles: f(x) = 1/x. Verify your answer using the power rule with x⁻¹.",
            "Find dy/dx if y = sin²(3x + 1). Identify how many times you apply the chain rule.",
            "Evaluate lim(x→0) [√(1+x) − √(1−x)] / x using rationalization.",
        ],
        "real_world_example": "When a BUET engineering student designs a bridge over the Meghna river, they calculate how stress changes with load — that is a derivative. The rate of water flow in the Padma at any instant is the derivative of the total volume with respect to time. Even the speedometer in your bus from Dhaka to Chittagong shows the derivative of distance with respect to time — instantaneous speed, the very concept Newton invented calculus to understand.",
    },

    "hm1-09-02": {
        "title": "Applications of Derivatives (Maxima, Minima, Tangent & Normal)",
        "learning_objectives": [
            "Find equations of tangent and normal lines to a curve at a given point using derivatives",
            "Determine increasing and decreasing intervals of a function using the first derivative",
            "Find local maxima and minima using first derivative test and second derivative test",
            "Solve optimization problems involving maxima and minima in real-world contexts",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: a farmer near Rajshahi has 100 meters of fencing to enclose a rectangular mango orchard. What dimensions should he choose to maximize the area? This is an optimization problem that derivatives solve beautifully.",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Teach: the derivative f'(a) gives the slope of the tangent to y = f(x) at x = a. Tangent line: y − f(a) = f'(a)(x − a). Normal line (perpendicular to tangent): y − f(a) = −1/f'(a) · (x − a). Ask: find the tangent and normal to y = x³ − 3x at x = 1.",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Teach monotonicity: f'(x) > 0 means f is increasing, f'(x) < 0 means f is decreasing. Critical points where f'(x) = 0 or undefined. First derivative test: if f' changes from + to −, local max; from − to +, local min. Second derivative test: if f'(c) = 0 and f''(c) < 0, local max; f''(c) > 0, local min; f''(c) = 0, inconclusive. Solve: find all local extrema of f(x) = x³ − 12x + 5.",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Problem: A rectangular box with square base and no top is to be made from 48 cm² of cardboard. Find the dimensions that maximize the volume. (Let base = x, height = h. Surface area: x² + 4xh = 48. Express V = x²h in terms of x, differentiate, set to 0.) Then: find the points on y = x² − 4x + 5 where the tangent is parallel to the line y = 2x + 7.",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "BUET-level: A cylindrical tin can must hold 500 cm³ of condensed milk. Find the radius and height that minimize the total surface area (top + bottom + curved side). Express SA = 2πr² + 2πrh, use V = πr²h = 500 to eliminate h. Also: find the maximum and minimum values of f(x) = sin x + cos x on [0, 2π]. What is the absolute maximum of f(x) = x/(1+x²) for x > 0?",
            },
        ],
        "key_formulas": [
            "Tangent at (a, f(a)): y − f(a) = f'(a)(x − a)",
            "Normal at (a, f(a)): y − f(a) = −(1/f'(a))(x − a)",
            "f increasing when f'(x) > 0; f decreasing when f'(x) < 0",
            "Critical points: f'(x) = 0 or f'(x) undefined",
            "Second derivative test: f''(c) > 0 → local min; f''(c) < 0 → local max",
            "Optimization: set up the objective function, use constraint to reduce to one variable, differentiate and set to zero",
        ],
        "common_mistakes": [
            "Forgetting to check endpoints when finding absolute max/min on a closed interval — the extreme values may occur at the endpoints, not at critical points",
            "Using the second derivative test when f''(c) = 0 — the test is inconclusive in this case, and you must fall back to the first derivative test or higher derivative test",
            "In optimization problems, forgetting to verify that the critical point is indeed a maximum (or minimum) as required — students find the critical point but do not confirm it is the desired type of extremum",
        ],
        "practice_prompts": [
            "Find the local maxima and minima of f(x) = 2x³ − 9x² + 12x − 4. Sketch the curve showing the turning points.",
            "A ball is thrown upward with velocity v₀ = 20 m/s. Its height is h(t) = 20t − 5t². Find the maximum height and the time to reach it.",
            "Among all rectangles with perimeter 20 cm, find the one with the largest area. Prove it is a square.",
        ],
        "real_world_example": "Bangladesh Krishi Bank optimizes fertilizer distribution — too little urea means low yield, too much wastes money and pollutes water. The yield Y as a function of fertilizer amount x follows a curve with a clear maximum. Derivatives find that optimal point. Similarly, BRTC bus operators want to find the speed that minimizes fuel cost per kilometer — calculus tells them the exact optimal speed for their Dhaka-Chittagong route.",
    },

    # ══ HIGHER MATHEMATICS — Chapter 10: যোগজীকরণ (Integration) ══
    "hm1-10-01": {
        "title": "Integration Basics (Indefinite Integrals & Techniques)",
        "learning_objectives": [
            "Understand integration as the reverse process of differentiation (antiderivative)",
            "Apply the power rule for integration: ∫xⁿ dx = xⁿ⁺¹/(n+1) + C (n ≠ −1)",
            "Integrate standard functions: polynomial, trigonometric, exponential, and logarithmic",
            "Apply substitution method (u-substitution) to evaluate integrals of composite functions",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: if the derivative of x² is 2x, what function has derivative 2x? What about 2x + any constant — does its derivative also equal 2x? This reverse process is integration, and the '+C' (constant of integration) is why indefinite integrals have infinitely many answers.",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "Define: ∫f(x) dx = F(x) + C where F'(x) = f(x). Teach the power rule: ∫xⁿ dx = xⁿ⁺¹/(n+1) + C for n ≠ −1. For n = −1: ∫(1/x) dx = ln|x| + C. Standard integrals: ∫sin x dx = −cos x + C, ∫cos x dx = sin x + C, ∫eˣ dx = eˣ + C, ∫sec²x dx = tan x + C. Ask: find ∫(3x² + 2x − 5) dx. Why is +C essential?",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Teach substitution: if the integral has the form ∫f(g(x))·g'(x) dx, let u = g(x), then du = g'(x) dx, and the integral becomes ∫f(u) du. Example: ∫2x·cos(x²) dx — let u = x², du = 2x dx, integral = ∫cos u du = sin u + C = sin(x²) + C. Work through: ∫(3x+1)⁵ dx, ∫sin³x cos x dx, ∫eˢⁱⁿˣ cos x dx. Emphasize: choosing the right u is the key skill.",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Problem set: (a) ∫(x³ + 1/x² − √x) dx, (b) ∫tan x dx (hint: write as sin x/cos x and substitute u = cos x), (c) ∫x/√(1+x²) dx using substitution u = 1+x², (d) ∫e^(3x+2) dx, (e) ∫dx/(x ln x) using substitution u = ln x.",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "BUET-level: Evaluate ∫sin³x dx by writing sin³x = sin x(1−cos²x) and substituting u = cos x. Then evaluate ∫dx/(x² + 4x + 13) by completing the square and using the arctan formula. Also: ∫x·eˣ dx using integration by parts (∫u dv = uv − ∫v du) — this previews an advanced technique.",
            },
        ],
        "key_formulas": [
            "∫xⁿ dx = xⁿ⁺¹/(n+1) + C, n ≠ −1",
            "∫(1/x) dx = ln|x| + C",
            "∫sin x dx = −cos x + C, ∫cos x dx = sin x + C",
            "∫sec²x dx = tan x + C, ∫csc²x dx = −cot x + C",
            "∫eˣ dx = eˣ + C, ∫aˣ dx = aˣ/ln a + C",
            "Substitution: ∫f(g(x))·g'(x) dx = ∫f(u) du where u = g(x)",
            "∫dx/(x²+a²) = (1/a)tan⁻¹(x/a) + C",
            "Integration by parts: ∫u dv = uv − ∫v du",
        ],
        "common_mistakes": [
            "Forgetting the constant of integration +C in indefinite integrals — every antiderivative has a family of solutions differing by a constant",
            "Applying the power rule to ∫(1/x) dx as x⁰/0 — this is undefined! The integral of 1/x is ln|x| + C, not x⁰/0",
            "In substitution, forgetting to change dx to du completely — if u = x², then du = 2x dx, so dx = du/(2x). All x-terms must be expressed in terms of u before integrating",
        ],
        "practice_prompts": [
            "Evaluate ∫(4x³ − 6x² + 2x − 7) dx and verify by differentiating your answer.",
            "Use substitution to evaluate ∫cos(5x + 3) dx. What is your choice of u?",
            "Evaluate ∫x²/(x³ + 1) dx. (Hint: the numerator is almost the derivative of the denominator.)",
        ],
        "real_world_example": "When BWDB (Bangladesh Water Development Board) engineers measure the flow rate of the Jamuna river at different depths, they get a velocity function v(y). To find the total volume of water flowing per second, they integrate v(y) across the river's cross-section. The total water discharge Q = ∫v·dA is a direct application of integration — this calculation determines flood warnings for millions of Bangladeshis living on the char lands.",
    },

    "hm1-10-02": {
        "title": "Definite Integrals & Area Under Curves",
        "learning_objectives": [
            "Evaluate definite integrals using the Fundamental Theorem of Calculus: ∫ₐᵇ f(x) dx = F(b) − F(a)",
            "Apply properties of definite integrals (linearity, interval splitting, symmetry for even/odd functions)",
            "Calculate the area bounded by curves, the x-axis, and given vertical lines",
            "Find the area between two curves by integrating the difference of the upper and lower functions",
        ],
        "teaching_steps": [
            {
                "step": 1,
                "type": "intro",
                "prompt": "Ask: if you know the speed of a bus on the Dhaka-Mymensingh highway at every moment, how do you find the total distance traveled in 2 hours? You add up speed × small time intervals — this is exactly what a definite integral does. The area under the speed-time graph equals the distance.",
            },
            {
                "step": 2,
                "type": "concept",
                "prompt": "State the Fundamental Theorem of Calculus: if F'(x) = f(x), then ∫ₐᵇ f(x) dx = F(b) − F(a). No +C needed for definite integrals! Evaluate: ∫₀² (3x² + 2x) dx = [x³ + x²]₀² = (8+4) − (0+0) = 12. Teach properties: ∫ₐᵇ kf(x) dx = k∫ₐᵇ f(x) dx, ∫ₐᵇ = ∫ₐᶜ + ∫ᶜᵇ, ∫ₐᵇ f(x) dx = −∫ᵇₐ f(x) dx. For even functions: ∫₋ₐᵃ f(x) dx = 2∫₀ᵃ f(x) dx. For odd functions: ∫₋ₐᵃ f(x) dx = 0.",
            },
            {
                "step": 3,
                "type": "teach",
                "prompt": "Teach area under curve: Area = ∫ₐᵇ f(x) dx when f(x) ≥ 0. If f(x) < 0 on some interval, take absolute value: Area = ∫|f(x)| dx. For area between two curves: Area = ∫ₐᵇ [f(x) − g(x)] dx where f(x) ≥ g(x). Example: find area enclosed between y = x² and y = x. First find intersection: x² = x → x = 0, 1. Area = ∫₀¹ (x − x²) dx = [x²/2 − x³/3]₀¹ = 1/2 − 1/3 = 1/6.",
            },
            {
                "step": 4,
                "type": "practice",
                "prompt": "Problem: (a) Evaluate ∫₀^π sin x dx and interpret it as area. (b) Evaluate ∫₀^(2π) sin x dx — why is it 0? What is the actual area bounded by sin x and the x-axis from 0 to 2π? (c) Find the area enclosed between y = x² − 2x and the x-axis. (d) Find the area between y = x² and y = 2x − x² in the first quadrant.",
            },
            {
                "step": 5,
                "type": "mastery",
                "prompt": "BUET-level: Find the area enclosed by the circle x² + y² = 4 using integration (express y = √(4−x²) and integrate from −2 to 2; use the substitution x = 2 sin θ). Verify the answer equals πr² = 4π. Then: find the area bounded by the parabola y² = 4x and the line y = 2x − 4. Sketch the region first, find intersection points, and decide whether to integrate with respect to x or y.",
            },
        ],
        "key_formulas": [
            "Fundamental Theorem: ∫ₐᵇ f(x) dx = F(b) − F(a) where F'(x) = f(x)",
            "∫ₐᵇ f(x) dx = −∫ᵇₐ f(x) dx",
            "∫ₐᵇ [f(x) + g(x)] dx = ∫ₐᵇ f(x) dx + ∫ₐᵇ g(x) dx",
            "Even function: ∫₋ₐᵃ f(x) dx = 2∫₀ᵃ f(x) dx",
            "Odd function: ∫₋ₐᵃ f(x) dx = 0",
            "Area between curves: A = ∫ₐᵇ |f(x) − g(x)| dx",
            "Area under y = f(x) from a to b: A = ∫ₐᵇ |f(x)| dx (take absolute value if curve crosses x-axis)",
        ],
        "common_mistakes": [
            "Confusing the definite integral value with the area — ∫₀^(2π) sin x dx = 0, but the actual area is 4 because the integral counts area below x-axis as negative. For area, always use |f(x)|",
            "Forgetting to find intersection points before computing area between two curves — you must determine where the curves meet to set the correct limits of integration",
            "When the upper and lower curves switch (one curve is above for part of the interval and below for the rest), not splitting the integral at the crossing point — this leads to cancellation errors",
        ],
        "practice_prompts": [
            "Evaluate ∫₁³ (x² − 2x + 1) dx. What does this value represent geometrically?",
            "Find the total area enclosed between y = x³ − x and the x-axis between x = −1 and x = 1. (Hint: the curve crosses the x-axis at x = −1, 0, and 1.)",
            "The region bounded by y = √x, the x-axis, and the line x = 4 is rotated about the x-axis. Find the volume using the disk method: V = π∫₀⁴ (√x)² dx. (Bonus: this is a preview of volume of revolution.)",
        ],
        "real_world_example": "When Bangladesh designs flood embankments along the Brahmaputra, engineers calculate the cross-sectional area of the river channel using definite integrals — the riverbed profile is an irregular curve, and the area of water flow determines how much the river can carry before it overflows. During the 2022 Sylhet floods, these calculations were used to predict which areas would be inundated. Every square meter of cross-sectional area matters when millions of lives depend on accurate flood modeling.",
    },
}


import json
import os

_OVERRIDE_DIR = os.path.join(os.path.dirname(__file__), "lesson_overrides")


def _load_overrides() -> dict[str, dict]:
    """Load educator-created lesson content from JSON files."""
    if not os.path.isdir(_OVERRIDE_DIR):
        return {}
    overrides: dict[str, dict] = {}
    for fname in os.listdir(_OVERRIDE_DIR):
        if fname.endswith(".json"):
            lesson_id = fname[:-5]
            try:
                with open(os.path.join(_OVERRIDE_DIR, fname)) as f:
                    overrides[lesson_id] = json.load(f)
            except Exception:
                pass
    return overrides


_overrides_cache: dict[str, dict] | None = None


def _get_overrides() -> dict[str, dict]:
    global _overrides_cache
    if _overrides_cache is None:
        _overrides_cache = _load_overrides()
    return _overrides_cache


def save_lesson_content(lesson_id: str, content: dict) -> None:
    """Save lesson content to a JSON file (persists across restarts)."""
    os.makedirs(_OVERRIDE_DIR, exist_ok=True)
    path = os.path.join(_OVERRIDE_DIR, f"{lesson_id}.json")
    with open(path, "w") as f:
        json.dump(content, f, ensure_ascii=False, indent=2)
    LESSON_CONTENT[lesson_id] = content
    _get_overrides()[lesson_id] = content


def get_lesson_content(lesson_id: str) -> dict | None:
    overrides = _get_overrides()
    return overrides.get(lesson_id) or LESSON_CONTENT.get(lesson_id)


def get_teaching_prompt(lesson_id: str, step: int = 1) -> str | None:
    content = get_lesson_content(lesson_id)
    if not content:
        return None
    steps = content.get("teaching_steps", [])
    for s in steps:
        if s["step"] == step:
            return s["prompt"]
    return None
