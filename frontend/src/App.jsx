import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [isLogin, setIsLogin] = useState(true);

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
  });

  const [currentUser, setCurrentUser] = useState(null);
  const [dashboard, setDashboard] = useState(null);
  const [applicants, setApplicants] = useState([]);
  const [jobs, setJobs] = useState([]);
  const [myApplications, setMyApplications] = useState([]);

  const [showPostJob, setShowPostJob] = useState(false);
  const [currentInterview, setCurrentInterview] = useState(null);
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [answer, setAnswer] = useState("");
  const [showInterview, setShowInterview] = useState(false);

  const [jobData, setJobData] = useState({
    title: "",
    description: "",
  });

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  // Check saved login
  useEffect(() => {
    const token = localStorage.getItem("access_token");
    const savedUser = localStorage.getItem("current_user");

    if (token && savedUser) {
      const user = JSON.parse(savedUser);

      setCurrentUser(user);

      if (user.role === "recruiter") {
        loadRecruiterDashboard(token);
        loadApplicants(token);
}     else {
        loadUserDashboard(token);
        loadJobs(token);
        loadMyApplications(token);
}
    }
  }, []);

  // Input change
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  // User Dashboard
  const loadUserDashboard = async (token) => {
    try {
      setLoading(true);
      setError("");

      const response = await fetch(
        `${API_URL}/auth/user-dashboard`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          typeof data.detail === "string"
            ? data.detail
            : "Unable to load dashboard."
        );
      }

      setDashboard(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Recruiter Dashboard
  const loadRecruiterDashboard = async (token) => {
    try {
      setLoading(true);
      setError("");

      console.log("Recruiter token exists:", !!token);

      const response = await fetch(
        `${API_URL}/auth/recruiter-dashboard`,
        {
          method: "GET",
          headers: {
            Accept: "application/json",
            Authorization: `Bearer ${token}`,
          },
        }
      );

      console.log("Recruiter dashboard status:", response.status);

      const data = await response.json();

      console.log("Recruiter dashboard response:", data);

      if (!response.ok) {
        throw new Error(
          typeof data.detail === "string"
            ? data.detail
            : JSON.stringify(data.detail)
        );
      }

      setDashboard(data);
    } catch (err) {
      console.error("Recruiter dashboard error:", err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Load applicants
  const loadApplicants = async (token) => {
    try {
      const response = await fetch(
        `${API_URL}/applications/recruiter-applicants`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          typeof data.detail === "string"
            ? data.detail
            : "Unable to load applicants."
        );
      }

      setApplicants(data.applications || []);
    } catch (err) {
      console.error("Applicants error:", err);
      setError(err.message);
    }
  };
  // =====================================
// LOAD AVAILABLE JOBS
// =====================================

const loadJobs = async (token) => {
  try {
    console.log("Loading jobs with token:", token);
    const response = await fetch(
      `${API_URL}/jobs/`,
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        typeof data.detail === "string"
          ? data.detail
          : "Unable to load jobs."
      );
    }

    setJobs(data.jobs || []);

  } catch (err) {
    console.error("Jobs error:", err);
    setError(err.message);
  }
};


// =====================================
// LOAD MY APPLICATIONS
// =====================================

const loadMyApplications = async (token) => {
  try {
    console.log("Loading applications with token:", token);
    const response = await fetch(
      `${API_URL}/applications/my-applications`,
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        typeof data.detail === "string"
          ? data.detail
          : "Unable to load applications."
      );
    }

    setMyApplications(data.applications || []);

  } catch (err) {
    console.error(
      "My applications error:",
      err
    );

    setError(err.message);
  }
};
// =====================================
// APPLY FOR JOB
// =====================================

const handleApply = async (jobId) => {
  try {
    setMessage("");
    setError("");

    const token = localStorage.getItem("access_token");

    const response = await fetch(
      `${API_URL}/applications/`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          job_id: jobId,
        }),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        typeof data.detail === "string"
          ? data.detail
          : "Unable to apply for this job."
      );
    }

    setMessage("Application submitted successfully! ✅");

    // Refresh applications
    await loadMyApplications(token);

  } catch (err) {
    console.error("Apply error:", err);
    setError(err.message);
  }
};
const handleStartInterview = async () => {
  try {
    setMessage("");
    setError("");

    const token = localStorage.getItem("access_token");

    if (!jobs || jobs.length === 0) {
      setError("No job available to start interview.");
      return;
    }

    const response = await fetch(
      `${API_URL}/interviews/start`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          job_id: jobs[0].id,
        }),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        typeof data.detail === "string"
          ? data.detail
          : JSON.stringify(data.detail)
      );
    }

    console.log("Interview created:", data);

    setCurrentInterview(data.interview);
    setShowInterview(true);
    setMessage("AI Interview started successfully! 🎤");

  } catch (err) {
    console.error("Start interview error:", err);
    setError(err.message);
  }
};
const handleGenerateQuestion = async () => {
  try {
    setMessage("");
    setError("");

    const token = localStorage.getItem("access_token");

    const interviewId =
      currentInterview?.interview_id || currentInterview?.id;

    const response = await fetch(
      `${API_URL}/interviews/${interviewId}/generate-question`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        typeof data.detail === "string"
          ? data.detail
          : JSON.stringify(data.detail)
      );
    }

    console.log(
  "Generated question:",
  JSON.stringify(data, null, 2)
);
    setCurrentQuestion(data.question);
    setMessage("Question generated successfully! 🎯");

  } catch (err) {
    console.error("Generate question error:", err);
    setError(err.message);
  }
};
const handleSubmitAnswer = async () => {
  try {
    setMessage("");
    setError("");

    const token = localStorage.getItem("access_token");

    if (!currentQuestion) {
      setError("Please generate a question first.");
      return;
    }

    if (!answer.trim()) {
      setError("Please write your answer first.");
      return;
    }

    const questionId =
      currentQuestion?.question_id || currentQuestion?.id;

    const response = await fetch(
      `${API_URL}/interviews/questions/${questionId}/answer`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          answer: answer,
        }),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        typeof data.detail === "string"
          ? data.detail
          : JSON.stringify(data.detail)
      );
    }

    console.log(
      "Answer submitted:",
      JSON.stringify(data, null, 2)
    );

    // Save evaluated question
    setCurrentQuestion(data.question);

    // Clear answer box
    setAnswer("");

    setMessage(
      data.message || "Answer submitted successfully! ✅"
    );

  } catch (err) {
    console.error("Submit answer error:", err);
    setError(err.message);
  }
};
// =====================================
// UPDATE APPLICATION STATUS
// =====================================

const handleApplicationStatus = async (
  applicationId,
  status
) => {
  try {
    setMessage("");
    setError("");

    const token =
      localStorage.getItem("access_token");

    const response = await fetch(
      `${API_URL}/applications/${applicationId}/status`,
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          status: status,
        }),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        typeof data.detail === "string"
          ? data.detail
          : "Unable to update application status."
      );
    }

    setMessage(
      `Application ${status} successfully!`
    );

    // Refresh applicants
    await loadApplicants(token);

  } catch (err) {
    console.error(
      "Application status error:",
      err
    );

    setError(err.message);
  }
};

  // =====================================
// LOGIN / REGISTER
// =====================================

const handleSubmit = async (e) => {
  e.preventDefault();

  setMessage("");
  setError("");
  setLoading(true);

  try {
    // REGISTER
    if (!isLogin) {
      const response = await fetch(
        `${API_URL}/auth/register`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            name: formData.name,
            email: formData.email,
            password: formData.password,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        const errorMessage =
          typeof data.detail === "string"
            ? data.detail
            : JSON.stringify(data.detail);

        throw new Error(
          errorMessage || "Registration failed."
        );
      }

      setMessage(
        "Registration successful! You can now login."
      );

      setIsLogin(true);

      setFormData({
        name: "",
        email: formData.email,
        password: "",
      });

      return;
    }

    // LOGIN
    const response = await fetch(
      `${API_URL}/auth/login`,
      {
        method: "POST",
        headers: {
          "Content-Type":
            "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
          username: formData.email,
          password: formData.password,
        }),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      const errorMessage =
        typeof data.detail === "string"
          ? data.detail
          : JSON.stringify(data.detail);

      throw new Error(
        errorMessage || "Login failed."
      );
    }

    // Save JWT
    localStorage.setItem(
      "access_token",
      data.access_token
    );

    // Save user
    localStorage.setItem(
      "current_user",
      JSON.stringify(data.user)
    );

    setCurrentUser(data.user);
    setMessage("Login successful!");

    // Correct dashboard
    if (data.user.role === "recruiter") {
      await loadRecruiterDashboard(
        data.access_token
      );

      await loadApplicants(data.access_token);
    } else {
  await loadUserDashboard(
    data.access_token
  );

  await loadJobs(
    data.access_token
  );

  await loadMyApplications(
    data.access_token
  );
}
  } catch (err) {
    setError(err.message);
  } finally {
    setLoading(false);
  }
};

// =====================================
// JOB INPUT
// =====================================

const handleJobChange = (e) => {
  setJobData({
    ...jobData,
    [e.target.name]: e.target.value,
  });
};

// =====================================
// POST JOB
// =====================================

const handlePostJob = async (e) => {
  e.preventDefault();

  setMessage("");
  setError("");
  setLoading(true);

  try {
    const token =
      localStorage.getItem("access_token");

    const response = await fetch(
      `${API_URL}/jobs/`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          title: jobData.title,
          description: jobData.description,
        }),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      const errorMessage =
        typeof data.detail === "string"
          ? data.detail
          : JSON.stringify(data.detail);

      throw new Error(
        errorMessage || "Job posting failed."
      );
    }

    setMessage(
      "Job posted successfully!"
    );

    setJobData({
      title: "",
      description: "",
    });

    setShowPostJob(false);

    // Refresh dashboard
    await loadRecruiterDashboard(token);
  } catch (err) {
    setError(err.message);
  } finally {
    setLoading(false);
  }
};

// =====================================
// LOGOUT
// =====================================

const handleLogout = () => {
  localStorage.removeItem("access_token");
  localStorage.removeItem("current_user");

  setCurrentUser(null);
  setDashboard(null);
  setApplicants([]);

  setFormData({
    name: "",
    email: "",
    password: "",
  });

  setMessage("");
  setError("");
  setIsLogin(true);
};
// =====================================
// RECRUITER DASHBOARD
// =====================================

if (
  currentUser &&
  currentUser.role === "recruiter"
) {
  return (
    <div className="dashboard-container">

      {/* NAVBAR */}
      <nav className="dashboard-navbar">

        <div className="dashboard-logo">
          Intelli<span>Hire</span>
        </div>

        <div className="navbar-right">

          <span className="role-badge">
            Recruiter
          </span>

          <button
            className="logout-button"
            onClick={handleLogout}
          >
            Logout
          </button>

        </div>

      </nav>

      {/* MAIN */}
      <main className="dashboard-main">

        {/* WELCOME */}
        <div className="welcome-section">

          <h1>
            Welcome, {currentUser.name}! 👋
          </h1>

          <p>
            Manage your jobs and applicants
            from your recruiter dashboard.
          </p>

        </div>

        {/* MESSAGES */}

        {message && (
          <div className="success-message">
            {message}
          </div>
        )}

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {/* PROFILE */}

        <div className="user-info-card">

          <h2>Recruiter Profile</h2>

          <div className="profile-details">

            <p>
              <strong>Name:</strong>{" "}
              {currentUser.name}
            </p>

            <p>
              <strong>Email:</strong>{" "}
              {currentUser.email}
            </p>

            <p>
              <strong>Role:</strong>{" "}
              {currentUser.role}
            </p>

          </div>

        </div>

        {/* STATS */}

        <h2 className="section-title">
          Recruitment Overview
        </h2>

        <div className="stats-grid">

          <div className="stat-card">

            <div className="stat-icon">
              💼
            </div>

            <h3>
              {dashboard?.dashboard?.job_count ?? 0}
            </h3>

            <p>
              Jobs Posted
            </p>

          </div>

          <div className="stat-card">

            <div className="stat-icon">
              👥
            </div>

            <h3>
              {applicants.length}
            </h3>

            <p>
              Applicants
            </p>

          </div>

          <div className="stat-card">

            <div className="stat-icon">
              📋
            </div>

            <h3>
              {
                applicants.filter(
                  (app) =>
                    app.status === "applied"
                ).length
              }
            </h3>

            <p>
              Active Applications
            </p>

          </div>

        </div>

        {/* JOB MANAGEMENT */}

        <div className="dashboard-card">

          <div className="card-header">

            <div>

              <h2>
                Job Management
              </h2>

              <p>
                Create a new job opportunity
                for candidates.
              </p>

            </div>

            <button
              className="primary-button"
              onClick={() =>
                setShowPostJob(!showPostJob)
              }
            >
              {showPostJob
                ? "Close"
                : "+ Post Job"}
            </button>

          </div>

          {/* POST JOB FORM */}

          {showPostJob && (

            <form
              className="job-form"
              onSubmit={handlePostJob}
            >

              <div className="input-group">

                <label>
                  Job Title
                </label>

                <input
                  type="text"
                  name="title"
                  placeholder="e.g. AI Engineer"
                  value={jobData.title}
                  onChange={handleJobChange}
                  required
                />

              </div>

              <div className="input-group">

                <label>
                  Job Description
                </label>

                <textarea
                  name="description"
                  placeholder="Enter job description and requirements..."
                  value={jobData.description}
                  onChange={handleJobChange}
                  rows="6"
                  required
                />

              </div>

              <button
                type="submit"
                className="primary-button"
                disabled={loading}
              >
                {loading
                  ? "Posting..."
                  : "Post Job"}
              </button>

            </form>

          )}

        </div>

        {/* APPLICANTS */}

        <div className="dashboard-card">

          <h2>
            Recent Applicants
          </h2>

          {applicants.length === 0 ? (

            <div className="empty-state">

              <div className="empty-icon">
                👥
              </div>

              <h3>
                No applicants yet
              </h3>

              <p>
                Applicants will appear here
                when candidates apply to your
                jobs.
              </p>

            </div>

          ) : (

            <div className="applicant-list">

              {applicants.map(
                (applicant) => (

                  <div
                    className="applicant-card"
                    key={applicant.id}
                  >

                    <div className="applicant-info">

                      <h3>
                        {
                          applicant.applicant_name
                        }
                      </h3>

                      <p>
                        {
                          applicant.applicant_email
                        }
                      </p>

                      <p>
                        <strong>
                          Job:
                        </strong>{" "}
                        {applicant.job_title}
                      </p>

                    </div>
                    <div className="applicant-status">

  <span className="status-badge">
    {applicant.status}
  </span>

  {applicant.status === "applied" && (

    <div className="application-actions">

      <button
        className="primary-button"
        onClick={() =>
          handleApplicationStatus(
            applicant.id,
            "accepted"
          )
        }
      >
        Accept
      </button>

      <button
        className="logout-button"
        onClick={() =>
          handleApplicationStatus(
            applicant.id,
            "rejected"
          )
        }
      >
        Reject
      </button>

    </div>

  )}

</div>

                    

                      
                      
                      

                    

                  </div>

                )
              )}

            </div>

          )}

        </div>

      </main>

    </div>
  );
}
// =====================================
// USER DASHBOARD
// =====================================

if (
  currentUser &&
  currentUser.role === "user"
) {
  return (
    <div className="dashboard-container">

      {/* NAVBAR */}
      <nav className="dashboard-navbar">

        <div className="dashboard-logo">
          Intelli<span>Hire</span>
        </div>

        <button
          className="logout-button"
          onClick={handleLogout}
        >
          Logout
        </button>

      </nav>

      {/* MAIN */}
      <main className="dashboard-main">

        <div className="welcome-section">

          <h1>
            Welcome, {currentUser.name}! 👋
          </h1>

          <p>
            Welcome to your IntelliHire
            career dashboard.
          </p>

        </div>

        {/* PROFILE */}

        <div className="user-info-card">

          <h2>
            Profile Information
          </h2>

          <div className="profile-details">

            <p>
              <strong>Name:</strong>{" "}
              {currentUser.name}
            </p>

            <p>
              <strong>Email:</strong>{" "}
              {currentUser.email}
            </p>

            <p>
              <strong>Role:</strong>{" "}
              {currentUser.role}
            </p>

          </div>

        </div>

        {/* ACTIVITY */}

        <h2 className="section-title">
          Your Activity
        </h2>

        <div className="stats-grid">
  <div className="stat-card">
    <div className="stat-icon">📄</div>
    <h3>{dashboard?.dashboard?.resume_count ?? 0}</h3>
    <p>Resumes</p>
  </div>

  <div className="stat-card">
    <div className="stat-icon">📋</div>
    <h3>{dashboard?.dashboard?.application_count ?? 0}</h3>
    <p>Applications</p>
  </div>

  <div className="stat-card">
    <div className="stat-icon">🎤</div>
    <h3>{dashboard?.dashboard?.interview_count ?? 0}</h3>
    <p>Interviews</p>
  </div>
</div>
       {/* =====================================
    AVAILABLE JOBS
===================================== */}

<div className="dashboard-card">

  <div className="card-header">

    <div>
      <h2>
        Available Jobs
      </h2>

      <p>
        Explore jobs posted by recruiters
        and apply for suitable opportunities.
      </p>
    </div>

  </div>

  {jobs.length === 0 ? (

    <div className="empty-state">

      <div className="empty-icon">
        💼
      </div>

      <h3>
        No jobs available
      </h3>

      <p>
        New job opportunities will appear here.
      </p>

    </div>

  ) : (

    <div className="applicant-list">

      {jobs.map((job) => {

        const alreadyApplied =
          myApplications.some(
            (application) =>
              application.job_id === job.id
          );

        return (

          <div
            className="applicant-card"
            key={job.id}
          >

            <div className="applicant-info">

              <h3>
                {job.title}
              </h3>

              <p>
                {job.description}
              </p>

              <p>
                <strong>
                  Job ID:
                </strong>{" "}
                {job.id}
              </p>

            </div>

            <div className="applicant-status">

              {alreadyApplied ? (

                <span className="status-badge">
                  Applied ✓
                </span>

              ) : (

                <button
                  className="primary-button"
                  onClick={() =>
                    handleApply(job.id)
                  }
                >
                  Apply Now
                </button>

              )}

            </div>

          </div>

        );
      })}

    </div>

  )}

</div>
{/* =====================================
    MY APPLICATIONS
===================================== */}

<div className="dashboard-card">

  <h2>
    My Applications
  </h2>

  <p>
    Track the jobs you have applied for.
  </p>

  {myApplications.length === 0 ? (

    <div className="empty-state">

      <div className="empty-icon">
        📋
      </div>

      <h3>
        No applications yet
      </h3>

      <p>
        Apply for a job to see your application here.
      </p>

    </div>

  ) : (

    <div className="applicant-list">

      {myApplications.map((application) => {

        const job = jobs.find(
          (item) =>
            item.id === application.job_id
        );

        return (

          <div
            className="applicant-card"
            key={application.id}
          >

            <div className="applicant-info">

              <h3>
                {job
                  ? job.title
                  : `Job #${application.job_id}`}
              </h3>

              <p>
                <strong>
                  Application ID:
                </strong>{" "}
                {application.id}
              </p>

              <p>
                <strong>
                  Applied on:
                </strong>{" "}
                {application.created_at
                  ? new Date(
                      application.created_at
                    ).toLocaleDateString()
                  : "N/A"}
              </p>

            </div>

            <div className="applicant-status">

              <span className="status-badge">
                {application.status}
              </span>

            </div>

          </div>

        );
      })}

    </div>

  )}

</div>
<div className="dashboard-card">
  <div className="card-header">
    <div>
      <h2>🎤 AI Interview</h2>
      <p>
        Practice AI-powered interview questions and get instant feedback.
      </p>
    </div>
  </div>

  <div className="empty-state">
    <div className="empty-icon">🤖</div>

    {!showInterview ? (
      <>
        <h3>Ready for your AI Interview?</h3>

        <p>
          Test your technical and problem-solving skills with IntelliHire AI.
        </p>

        <button
          className="primary-button"
          onClick={handleStartInterview}
        >
          Start AI Interview
        </button>
      </>
    ) : (
      <>
        <h3>Interview Started Successfully! 🎉</h3>

        <p>
          Your AI interview is ready.
        </p>

        <p>
          <strong>Interview ID:</strong>{" "}
          {currentInterview?.interview_id || currentInterview?.id}
        </p>

       <button
  className="primary-button"
  onClick={handleGenerateQuestion}
>
  Generate First Question
</button>
{currentQuestion && (
  <div style={{ marginTop: "20px" }}>
    <h3>🤖 AI Question</h3>

    <p>
      {currentQuestion?.question}
    </p>
    <textarea
  value={answer}
  onChange={(e) => setAnswer(e.target.value)}
  placeholder="Write your answer here..."
  rows="6"
  style={{
    width: "100%",
    marginTop: "15px",
    padding: "12px",
    borderRadius: "10px",
    border: "1px solid #ccc",
    fontSize: "16px",
    resize: "vertical",
  }}
/>

<button
  className="primary-button"
  style={{ marginTop: "12px" }}
  onClick={handleSubmitAnswer}
>
  Submit Answer
</button>
{currentQuestion?.score !== null &&
  currentQuestion?.score !== undefined && (
    <div
      style={{
        marginTop: "20px",
        padding: "20px",
        borderRadius: "12px",
        background: "#f5f7fa",
        border: "1px solid #ddd",
        textAlign: "left",
      }}
    >
      <h3>📊 AI Evaluation</h3>

      <p>
        <strong>Score:</strong>{" "}
        {currentQuestion.score}/100
      </p>

      <p>
        <strong>Feedback:</strong>
        <br />
        {currentQuestion.feedback}
      </p>

      <button
        className="primary-button"
        style={{ marginTop: "12px" }}
        onClick={handleGenerateQuestion}
      >
        Generate Next Question 🎯
      </button>
    </div>
  )}
{message && (
  <p
    style={{
      marginTop: "15px",
      color: "green",
      fontWeight: "bold",
    }}
  >
    {message}
  </p>
)}

{error && (
  <p
    style={{
      marginTop: "15px",
      color: "red",
      fontWeight: "bold",
    }}
  >
    {error}
  </p>
)}
  </div>
)}
      </>
    )}
  </div>
</div>


        {/* CAREER INTELLIGENCE */}

        <div className="dashboard-card">

          <h2>
            Career Intelligence
          </h2>

          <p>
            IntelliHire helps you analyze
            your resume, match jobs, identify
            skill gaps and prepare for
            AI-powered interviews.
          </p>

        </div>

      </main>

    </div>
  );
}

// =====================================
// LOGIN / REGISTER PAGE
// =====================================

return (
  <div className="auth-container">

    <div className="auth-card">

      <div className="logo">
        Intelli<span>Hire</span>
      </div>

      <h1>
        {isLogin
          ? "Welcome Back!"
          : "Create Account"}
      </h1>

      <p className="subtitle">
        {isLogin
          ? "Login to continue to IntelliHire"
          : "Join IntelliHire and build your career"}
      </p>

      {/* SUCCESS MESSAGE */}

      {message && (
        <div className="success-message">
          {message}
        </div>
      )}

      {/* ERROR MESSAGE */}

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {/* FORM */}

      <form onSubmit={handleSubmit}>

        {!isLogin && (
          <div className="input-group">

            <label>
              Full Name
            </label>

            <input
              type="text"
              name="name"
              placeholder="Enter your name"
              value={formData.name}
              onChange={handleChange}
              required
            />

          </div>
        )}

        <div className="input-group">

          <label>
            Email
          </label>

          <input
            type="email"
            name="email"
            placeholder="Enter your email"
            value={formData.email}
            onChange={handleChange}
            required
          />

        </div>

        <div className="input-group">

          <label>
            Password
          </label>

          <input
            type="password"
            name="password"
            placeholder="Enter your password"
            value={formData.password}
            onChange={handleChange}
            required
          />

        </div>

        <button
          type="submit"
          className="auth-button"
          disabled={loading}
        >
          {loading
            ? "Please wait..."
            : isLogin
            ? "Login"
            : "Create Account"}
        </button>

      </form>

      {/* SWITCH LOGIN / REGISTER */}

      <div className="switch-auth">

        {isLogin
          ? "Don't have an account?"
          : "Already have an account?"}

        <button
          type="button"
          onClick={() => {
            setIsLogin(!isLogin);
            setMessage("");
            setError("");

            setFormData({
              name: "",
              email: "",
              password: "",
            });
          }}
        >
          {isLogin
            ? " Register"
            : " Login"}
        </button>

      </div>

    </div>

  </div>
);

}

export default App; 