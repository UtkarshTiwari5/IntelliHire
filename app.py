# ============================================================
# IntelliHire - V4 Dynamic Job Recommendation
# ============================================================

import tempfile
from pathlib import Path

import streamlit as st

from config.settings import (
    APP_NAME,
    APP_VERSION,
    APP_DESCRIPTION
)

from src.resume_parser import parse_resume
from src.skill_extractor import extract_skills
from src.job_matcher import match_resume_to_job
from src.job_recommender import recommend_jobs
from src.skill_gap import (
    generate_career_roadmap,
    generate_roadmap_from_job
)

# ============================================================
# V6 SEMANTIC AI
# ============================================================

from src.v6_pipeline import (
    run_v6_match_pipeline
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "resume_data" not in st.session_state:
    st.session_state["resume_data"] = None

if "skill_analysis" not in st.session_state:
    st.session_state["skill_analysis"] = None

if "match_result" not in st.session_state:
    st.session_state["match_result"] = None

if "recommendations" not in st.session_state:
    st.session_state["recommendations"] = None

if "roadmap_result" not in st.session_state:
    st.session_state["roadmap_result"] = None

if "analyzed_resume_name" not in st.session_state:
    st.session_state["analyzed_resume_name"] = None


# ============================================================
# HEADER
# ============================================================

st.title(
    "🤖 IntelliHire"
)

st.subheader(
    "AI-Powered Recruitment & Career Intelligence Platform"
)

st.caption(
    f"Version {APP_VERSION} | V4 Job Recommendation Engine"
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header(
        "🚀 IntelliHire"
    )

    st.markdown(
        """
        **STEP 1** ✓ Project Setup

        **STEP 2** ✓ V1 Resume Parser

        **STEP 3** ✓ V2 Intelligent Skill Extraction

        **STEP 4** ✓ V3 Resume ↔ Job Matching

        **STEP 5** ▶ V4 Job Recommendation

        **STEP 6** → V5 Skill Gap + Career Roadmap

        **STEP 7** → V6 NLP + Embeddings + Vector Search

        **STEP 8** → FastAPI Backend

        **STEP 9** → PostgreSQL Database

        **STEP 10** → Authentication

        **STEP 11** → AI Interview

        **STEP 12** → React Frontend

        **STEP 13** → Docker

        **STEP 14** → Testing

        **STEP 15** → Deployment
        """
    )


# ============================================================
# RESUME UPLOAD
# ============================================================

st.header(
    "📄 Resume Intelligence"
)

resume = st.file_uploader(
    "Upload Resume",
    type=[
        "pdf",
        "docx"
    ]
)


# ============================================================
# ANALYZE RESUME
# ============================================================

if resume is not None:

    st.success(
        f"Selected Resume: {resume.name}"
    )

    if st.button(
        "🚀 Analyze Resume",
        type="primary",
        key="analyze_resume_button"
    ):

        try:

            suffix = Path(
                resume.name
            ).suffix

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=suffix
            ) as temp_file:

                temp_file.write(
                    resume.getbuffer()
                )

                temp_path = temp_file.name


            # =================================================
            # V1 + V2
            # =================================================

            with st.spinner(
                "Running V1 + V2 analysis..."
            ):

                resume_data = parse_resume(
                    temp_path
                )

                skill_analysis = extract_skills(
                    resume_data.get(
                        "raw_text",
                        ""
                    )
                )


            # =================================================
            # SAVE DATA
            # =================================================

            st.session_state[
                "resume_data"
            ] = resume_data

            st.session_state[
                "skill_analysis"
            ] = skill_analysis

            st.session_state[
                "match_result"
            ] = None

            st.session_state[
                "recommendations"
            ] = None

            st.session_state[
                "roadmap_result"
            ] = None

            st.session_state[
                "analyzed_resume_name"
            ] = resume.name


            st.success(
                "✅ V1 + V2 analysis completed successfully."
            )


        except Exception as error:

            st.error(
                f"Resume analysis failed: {error}"
            )


# ============================================================
# LOAD SESSION DATA
# ============================================================

resume_data = st.session_state.get(
    "resume_data"
)

skill_analysis = st.session_state.get(
    "skill_analysis"
)

# ============================================================
# DISPLAY RESUME ANALYSIS
# ============================================================

if resume_data is not None and skill_analysis is not None:

    # ========================================================
    # CANDIDATE INFORMATION
    # ========================================================

    st.divider()

    st.header(
        "👤 Candidate Information"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            "**Name:**",
            resume_data.get(
                "name",
                "Not detected"
            )
        )

        st.write(
            "**Email:**",
            resume_data.get(
                "email",
                "Not detected"
            )
        )

        st.write(
            "**Phone:**",
            resume_data.get(
                "phone",
                "Not detected"
            )
        )

    with col2:

        st.write(
            "**LinkedIn:**",
            resume_data.get(
                "linkedin",
                "Not detected"
            )
        )

        st.write(
            "**GitHub:**",
            resume_data.get(
                "github",
                "Not detected"
            )
        )


    # ========================================================
    # RESUME SECTIONS
    # ========================================================

    st.divider()

    st.header(
        "📚 Resume Sections"
    )

    sections = resume_data.get(
        "sections",
        {}
    )

    for section_name, content in sections.items():

        with st.expander(
            section_name.title()
        ):

            st.write(
                content
            )


    # ========================================================
    # RAW TEXT
    # ========================================================

    st.divider()

    st.header(
        "🔍 Raw Resume Text"
    )

    st.text_area(
        "Extracted Text",
        resume_data.get(
            "raw_text",
            ""
        ),
        height=300,
        key="raw_resume_text"
    )


    # ========================================================
    # V2 SKILL INTELLIGENCE
    # ========================================================

    st.divider()

    st.header(
        "🧠 V2 Intelligent Skill Analysis"
    )

    known_skills = skill_analysis.get(
        "known_skills",
        []
    )

    unknown_candidates = skill_analysis.get(
        "unknown_candidates",
        []
    )

    total_skills = skill_analysis.get(
        "total_skills",
        len(known_skills)
        +
        len(unknown_candidates)
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Skills",
            total_skills
        )

    with col2:

        st.metric(
            "Known Skills",
            len(known_skills)
        )

    with col3:

        st.metric(
            "New Candidates",
            len(unknown_candidates)
        )


    # ========================================================
    # KNOWN SKILLS
    # ========================================================

    st.subheader(
        "✅ Detected Skills"
    )

    if known_skills:

        for skill in known_skills:

            if isinstance(
                skill,
                dict
            ):

                skill_name = skill.get(
                    "skill",
                    ""
                )

                category = skill.get(
                    "category",
                    "Unknown"
                )

                confidence = skill.get(
                    "confidence",
                    0
                )

                st.write(
                    f"**{skill_name}** "
                    f"— {category} "
                    f"— Confidence: "
                    f"{confidence:.0%}"
                )

            else:

                st.write(
                    f"**{skill}**"
                )

    else:

        st.info(
            "No known skills detected."
        )


    # ========================================================
    # UNKNOWN SKILLS
    # ========================================================

    st.subheader(
        "🔎 New / Unknown Skill Candidates"
    )

    if unknown_candidates:

        for skill in unknown_candidates:

            if isinstance(
                skill,
                dict
            ):

                skill_name = skill.get(
                    "skill",
                    ""
                )

                confidence = skill.get(
                    "confidence",
                    0
                )

                st.warning(
                    f"**{skill_name}** "
                    f"— Candidate technology/skill "
                    f"— Confidence: "
                    f"{confidence:.0%}"
                )

            else:

                st.warning(
                    f"**{skill}**"
                )

    else:

        st.info(
            "No new skill candidates detected."
        )


    # ========================================================
    # V3 RESUME ↔ JOB MATCHING
    # ========================================================

    st.divider()

    st.header(
        "💼 V3 Resume ↔ Job Matching"
    )

    st.write(
        "Enter a job role or paste a complete "
        "job description. IntelliHire will analyze "
        "the resume against it."
    )

    v3_job_description = st.text_area(
        "Paste Target Job Description",
        height=250,
        placeholder=(
            "Enter job role or job description...\n\n"
            "Examples:\n"
            "• Python Developer\n"
            "• Machine Learning Engineer\n"
            "• Data Scientist\n"
            "• AI Engineer\n"
            "• Backend Developer\n"
            "• Frontend Developer\n"
            "• Full Stack Developer\n\n"
            "You can also paste a complete job description."
        ),
        key="v3_job_description"
    )


    # ========================================================
    # V3 MATCH BUTTON
    # ========================================================

    if st.button(
        "🎯 Match Resume With Job",
        key="v3_match_button"
    ):

        if not v3_job_description.strip():

            st.warning(
                "Please enter a job description."
            )

        else:

            try:

                with st.spinner(
                    "Analyzing resume against job..."
                ):

                    match_result = match_resume_to_job(
                        resume_data.get(
                            "raw_text",
                            ""
                        ),
                        skill_analysis,
                        v3_job_description
                    )

                    # ========================================================
                    # V6 SEMANTIC MATCHING
                    # ========================================================

                    v3_keyword_score = match_result.get(
                        "match_score",
                        0
)

                    v6_result = run_v6_match_pipeline(
                        resume_data.get(
                             "raw_text",
                            ""
                        ),
                        v3_job_description,
                        v3_keyword_score
)

                match_result[
                "v6_semantic_score"
                ] = v6_result[
                "semantic_score"
]

                match_result[
                    "v6_hybrid_score"
                ] = v6_result[
                    "hybrid_score"
]



                st.session_state[
                    "match_result"
                ] = match_result

                st.session_state[
                    "v6_result"
                ] = v6_result

                st.session_state[
                    "recommendations"
                ] = None

                st.session_state[
                    "roadmap_result"
                ] = None

            except Exception as error:

                st.error(
                    f"Job matching failed: {error}"
                )


    # ========================================================
    # LOAD V3 RESULT
    # ========================================================

    match_result = st.session_state.get(
        "match_result"
    )


    # ========================================================
    # DISPLAY V3 RESULT
    # ========================================================

    if match_result is not None:

        st.divider()

        st.header(
            "📊 Job Match Result"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Overall Match",
                f"{match_result.get('overall_match_score', 0)}%"
            )

        with col2:

            st.metric(
                "Skill Coverage",
                f"{match_result.get('skill_coverage', 0)}%"
            )

        with col3:

            st.metric(
                "Experience Signal",
                f"{match_result.get('experience_score', 0)}%"
            )


        # ====================================================
        # MATCHED SKILLS
        # ====================================================

        st.subheader(
            "✅ Matched Skills"
        )

        matched_skills = match_result.get(
            "matched_skills",
            []
        )

        if matched_skills:

            for skill in matched_skills:

                st.success(
                    f"✓ {skill}"
                )

        else:

            st.info(
                "No direct skill matches found."
            )


        # ====================================================
        # MISSING SKILLS
        # ====================================================

        st.subheader(
            "❌ Missing / Required Skills"
        )

        missing_skills = match_result.get(
            "missing_skills",
            []
        )

        if missing_skills:

            for skill in missing_skills:

                st.error(
                    f"✗ {skill}"
                )

        else:

            st.success(
                "No directly missing skills detected."
            )


        # ====================================================
        # ADDITIONAL SKILLS
        # ====================================================

        st.subheader(
            "⭐ Additional Candidate Skills"
        )

        additional_skills = match_result.get(
            "additional_skills",
            []
        )

        if additional_skills:

            for skill in additional_skills:

                st.info(
                    f"• {skill}"
                )

        else:

            st.info(
                "No additional skills detected."
            )


        # ====================================================
        # UNKNOWN SKILL EVIDENCE
        # ====================================================

        st.subheader(
            "🔎 New / Unknown Skill Evidence"
        )

        unknown_evidence = match_result.get(
            "unknown_skill_evidence",
            []
        )

        if unknown_evidence:

            for item in unknown_evidence:

                skill_name = item.get(
                    "skill",
                    ""
                )

                if item.get(
                    "present_in_job",
                    False
                ):

                    st.warning(
                        f"**{skill_name}** "
                        "appears in both the resume "
                        "and job description."
                    )

                else:

                    st.caption(
                        f"{skill_name} "
                        "was detected in the resume "
                        "but was not explicitly found "
                        "in the job description."
                    )

        else:

            st.info(
                "No unknown skill candidates available."
            )


        # ====================================================
        # V3 DATA
        # ====================================================

        with st.expander(
            "🧩 V3 Matching Data"
        ):

            st.json(
                match_result
            )


        st.success(
            "✅ V1 + V2 + V3 analysis completed successfully."
        )

        # ====================================================
        # V6 SEMANTIC AI ANALYSIS
        # ====================================================

        v6_result = st.session_state.get(
            "v6_result"
        )

        if v6_result is not None:

            st.divider()

            st.header(
                "🧠 V6 Semantic AI Analysis"
            )

            st.write(
                "V6 uses NLP embeddings and semantic "
                "similarity to understand the relationship "
                "between the resume and target job."
            )

            v6_col1, v6_col2, v6_col3 = st.columns(3)

            with v6_col1:

                st.metric(
                    "V3 Keyword Score",
                    f"{v6_result.get('keyword_score', 0):.1f}%"
                )

            with v6_col2:

                st.metric(
                    "V6 Semantic Score",
                    f"{v6_result.get('semantic_score', 0):.1f}%"
                )

            with v6_col3:

                st.metric(
                    "V6 Hybrid Score",
                    f"{v6_result.get('hybrid_score', 0):.1f}%"
                )

            st.info(
                "💡 V3 performs skill/keyword matching, "
                "while V6 adds semantic understanding "
                "using NLP embeddings."
            )

            # ====================================================
            # V6 EXPLANATION
            # ====================================================

            st.info(
                "💡 V6 combines traditional keyword matching "
                "with semantic similarity. This helps IntelliHire "
                "understand related skills and job concepts even "
                "when the exact words are different."
            )

            





        # ============================================================
# V4 DYNAMIC JOB RECOMMENDATION
# ============================================================

    st.divider()

    st.header(
        "🚀 V4 AI Job Recommendation"
    )

    st.write(
        "IntelliHire dynamically recommends job roles "
        "based on the skills detected from your resume."
    )

    st.info(
        "💡 Recommendations are generated from your "
        "detected skills and do not require a fixed job dataset."
    )


    # ========================================================
    # USER RECOMMENDATION COUNT
    # ========================================================

    recommendation_count_input = st.text_input(
        "How many job recommendations do you want?",
        placeholder="Example: 5, 20, 100, 500, 5000...",
        key="v4_recommendation_count_input"
    )

    st.caption(
        "Enter any positive whole number."
    )


    # ========================================================
    # V4 RECOMMEND BUTTON
    # ========================================================

    if st.button(
        "🚀 Generate Job Recommendations",
        type="primary",
        key="v4_recommend_button"
    ):

        if not recommendation_count_input.strip():

            st.warning(
                "Please enter the number of recommendations."
            )

        elif not recommendation_count_input.strip().isdigit():

            st.error(
                "Please enter a valid positive whole number."
            )

        else:

            recommendation_count = int(
                recommendation_count_input.strip()
            )

            if recommendation_count <= 0:

                st.error(
                    "Recommendation count must be greater than 0."
                )

            else:

                try:

                    with st.spinner(
                        "Generating dynamic job recommendations..."
                    ):

                        recommendations = recommend_jobs(
                            skill_analysis,
                            top_n=recommendation_count
                        )


                    st.session_state[
                        "recommendations"
                    ] = recommendations

                    st.success(
                        "✅ Job recommendations generated successfully."
                    )


                except Exception as error:

                    st.error(
                        f"Job recommendation failed: {error}"
                    )


    # ========================================================
    # LOAD V4 RESULTS
    # ========================================================

    recommendations = st.session_state.get(
        "recommendations"
    )


    # ========================================================
    # DISPLAY V4 RESULTS
    # ========================================================

    if recommendations:

        st.divider()

        st.subheader(
            "🎯 Recommended Job Roles"
        )

        st.success(
            f"{len(recommendations)} "
            "job recommendations generated."
        )


        # ====================================================
        # RECOMMENDATION CARDS
        # ====================================================

        for job in recommendations:

            rank = job.get(
                "rank",
                "-"
            )

            job_title = job.get(
                "job_title",
                "Unknown Job"
            )

            match_score = job.get(
                "match_score",
                0
            )

            category = job.get(
                "category",
                "Technology"
            )

            description = job.get(
                "description",
                ""
            )

            matched = job.get(
                "matched_skills",
                []
            )

            missing = job.get(
                "missing_skills",
                []
            )

            required = job.get(
                "required_skills",
                []
            )


            with st.container():

                st.markdown(
                    f"### 🏆 #{rank} — {job_title}"
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "Match Score",
                        f"{match_score}%"
                    )

                with col2:

                    st.metric(
                        "Category",
                        category
                    )

                with col3:

                    st.metric(
                        "Matched Skills",
                        len(matched)
                    )


                st.write(
                    description
                )


                # --------------------------------------------
                # MATCHED SKILLS
                # --------------------------------------------

                if matched:

                    st.success(
                        "✅ Matched Skills: "
                        +
                        ", ".join(matched)
                    )


                # --------------------------------------------
                # MISSING SKILLS
                # --------------------------------------------

                if missing:

                    st.warning(
                        "⚠️ Missing Skills: "
                        +
                        ", ".join(missing)
                    )


                # --------------------------------------------
                # REQUIRED SKILLS
                # --------------------------------------------

                if required:

                    with st.expander(
                        "📚 Required Skills"
                    ):

                        st.write(
                            ", ".join(required)
                        )


                st.divider()


    else:

        st.info(
            "Enter the number of recommendations "
            "and click Generate Job Recommendations."
        )


    # ========================================================
    # STRUCTURED DATA
    # ========================================================

    with st.expander(
        "🧩 Structured Resume Data"
    ):

        st.json(
            resume_data
        )


    # ========================================================
    # V2 DATA
    # ========================================================

    with st.expander(
        "🧠 V2 Skill Analysis Data"
    ):

        st.json(
            skill_analysis
        )


    # ========================================================
    # V4 DATA
    # ========================================================

    if recommendations:

        with st.expander(
            "🚀 V4 Recommendation Data"
        ):

            st.json(
                recommendations
            )

            # ============================================================
# V5 SKILL GAP + CAREER ROADMAP
# ============================================================

    st.divider()

    st.header(
        "🎯 V5 Skill Gap + Career Roadmap"
    )

    st.write(
        "Analyze missing skills for a target job "
        "and generate a personalized learning roadmap."
    )


    # ========================================================
    # TARGET JOB
    # ========================================================

    st.subheader(
        "💼 V5 Target Job"
    )

    v5_target_job = st.text_input(
        "Enter Target Job Role",
        placeholder=(
            "Example: Machine Learning Engineer"
        ),
        key="v5_target_job"
    )


    # ========================================================
    # REQUIRED SKILLS
    # ========================================================

    v5_required_skills_text = st.text_area(
        "Required Skills",
        placeholder=(
            "Enter required skills separated by commas.\n\n"
            "Example:\n"
            "Python, Machine Learning, Docker, "
            "AWS, Kubernetes"
        ),
        height=150,
        key="v5_required_skills"
    )


    # ========================================================
    # USE V3 JOB DESCRIPTION
    # ========================================================

    if match_result is not None:

        st.info(
            "💡 V3 job matching data is available. "
            "You can enter a target role and skills above."
        )


    # ========================================================
    # V5 ANALYZE BUTTON
    # ========================================================

    if st.button(
        "🗺️ Generate Skill Gap & Career Roadmap",
        type="primary",
        key="v5_generate_button"
    ):

        if not v5_target_job.strip():

            st.warning(
                "Please enter a target job role."
            )

        elif not v5_required_skills_text.strip():

            st.warning(
                "Please enter the required skills."
            )

        else:

            try:

                required_skills = [

                    skill.strip()

                    for skill in
                    v5_required_skills_text.split(",")

                    if skill.strip()
                ]


                with st.spinner(
                    "Analyzing skill gap and building career roadmap..."
                ):

                    roadmap_result = (
                        generate_career_roadmap(
                            skill_analysis,
                            v5_target_job.strip(),
                            required_skills
                        )
                    )


                st.session_state[
                    "roadmap_result"
                ] = roadmap_result


                st.success(
                    "✅ Skill gap and career roadmap generated."
                )


            except Exception as error:

                st.error(
                    f"Career roadmap generation failed: {error}"
                )


    # ========================================================
    # LOAD V5 RESULT
    # ========================================================

    roadmap_result = st.session_state.get(
        "roadmap_result"
    )


    # ========================================================
    # DISPLAY V5 RESULT
    # ========================================================

    if roadmap_result:

        st.divider()

        st.subheader(
            "📊 Job Readiness"
        )


        # ====================================================
        # READINESS SCORE
        # ====================================================

        readiness_score = roadmap_result.get(
            "job_readiness_score",
            0
        )

        current_skills = roadmap_result.get(
            "current_skills",
            []
        )

        required_skills = roadmap_result.get(
            "required_skills",
            []
        )

        matched_skills = roadmap_result.get(
            "matched_skills",
            []
        )

        missing_skills = roadmap_result.get(
            "missing_skills",
            []
        )


        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Job Readiness",
                f"{readiness_score}%"
            )

        with col2:

            st.metric(
                "Current Skills",
                len(current_skills)
            )

        with col3:

            st.metric(
                "Matched Skills",
                len(matched_skills)
            )

        with col4:

            st.metric(
                "Skill Gap",
                len(missing_skills)
            )


        # ====================================================
        # TARGET ROLE
        # ====================================================

        st.subheader(
            "🎯 Target Role"
        )

        st.success(
            roadmap_result.get(
                "target_job",
                v5_target_job
            )
        )


        # ====================================================
        # CURRENT SKILLS
        # ====================================================

        st.subheader(
            "✅ Current Skills"
        )

        if current_skills:

            st.write(
                ", ".join(current_skills)
            )

        else:

            st.info(
                "No current skills detected."
            )


        # ====================================================
        # MATCHED SKILLS
        # ====================================================

        st.subheader(
            "🟢 Matched Skills"
        )

        if matched_skills:

            for skill in matched_skills:

                st.success(
                    f"✓ {skill}"
                )

        else:

            st.info(
                "No matched skills."
            )


        # ====================================================
        # MISSING SKILLS
        # ====================================================

        st.subheader(
            "🔴 Missing Skills"
        )

        if missing_skills:

            for skill in missing_skills:

                st.error(
                    f"✗ {skill}"
                )

        else:

            st.success(
                "🎉 No skill gap detected!"
            )


        # ====================================================
        # SKILL GAP DETAILS
        # ====================================================

        skill_gap_details = roadmap_result.get(
            "skill_gap_details",
            []
        )

        if skill_gap_details:

            st.subheader(
                "🔥 Skill Gap Priority"
            )

            for detail in skill_gap_details:

                skill = detail.get(
                    "skill",
                    "Unknown"
                )

                priority = detail.get(
                    "priority",
                    "Low"
                )

                topics = detail.get(
                    "topics",
                    []
                )

                projects = detail.get(
                    "projects",
                    []
                )


                with st.expander(
                    f"📌 {skill} — {priority} Priority"
                ):

                    st.write(
                        "**Priority:** "
                        + priority
                    )


                    if topics:

                        st.write(
                            "**Topics to Learn:**"
                        )

                        for topic in topics:

                            st.write(
                                f"• {topic}"
                            )


                    if projects:

                        st.write(
                            "**Projects to Build:**"
                        )

                        for project in projects:

                            st.write(
                                f"• {project}"
                            )


        # ====================================================
        # LEARNING ROADMAP
        # ====================================================

        learning_roadmap = roadmap_result.get(
            "learning_roadmap",
            []
        )

        st.subheader(
            "🗺️ Personalized Learning Roadmap"
        )

        if learning_roadmap:

            for phase in learning_roadmap:

                phase_number = phase.get(
                    "phase",
                    "-"
                )

                skill = phase.get(
                    "skill",
                    "Unknown Skill"
                )

                priority = phase.get(
                    "priority",
                    "Low"
                )

                topics = phase.get(
                    "topics",
                    []
                )

                projects = phase.get(
                    "projects",
                    []
                )


                with st.container():

                    st.markdown(
                        f"### 🚀 Phase {phase_number}: {skill}"
                    )

                    st.write(
                        f"**Priority:** {priority}"
                    )


                    if topics:

                        st.write(
                            "**📚 Learn:**"
                        )

                        for topic in topics:

                            st.write(
                                f"• {topic}"
                            )


                    if projects:

                        st.write(
                            "**💻 Build:**"
                        )

                        for project in projects:

                            st.write(
                                f"• {project}"
                            )


                    st.divider()

        else:

            st.info(
                "No learning roadmap required."
            )


        # ====================================================
        # COMPLETE V5 DATA
        # ====================================================

        with st.expander(
            "🧩 V5 Complete Roadmap Data"
        ):

            st.json(
                roadmap_result
            )


# ============================================================
# FINAL EXCEPTION / SAFETY
# ============================================================

try:

    pass

except Exception as error:

    st.error(
        f"Application error: {error}"
    )

        



