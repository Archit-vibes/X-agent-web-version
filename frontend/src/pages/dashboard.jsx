import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const Dashboard = () => {
  const [loading, setLoading] = useState(true);
  const [authenticated, setAuthenticated] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    fetch("http://localhost:5000/auth/check", {
      method: "GET",
      credentials: "include",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.authenticated) {
          setAuthenticated(true);
        } else {
          window.location.href = "/";
        }
      })
      .catch(() => {
        window.location.href = "/";
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div style={styles.center}>
        <p style={styles.text}>Checking authentication…</p>
      </div>
    );
  }

  if (!authenticated) return null;

  return (
    <div style={styles.page}>
      <h1 style={styles.title}>Dashboard</h1>
      <p style={styles.subtitle}>
        You are authenticated with X.
      </p>

      <div style={styles.cardsContainer}>
        <div style={styles.card}>
          <h2 style={styles.cardTitle}>Mentions</h2>
          <p style={styles.cardDescription}>
            View all mentions from X posts related to your account. Track conversations and engagement from other users mentioning your profile.
          </p>
          <button
            style={styles.cardButton}
            onClick={() => navigate("/mentions")}
          >
            View Mentions
          </button>
        </div>

        <div style={styles.card}>
          <h2 style={styles.cardTitle}>Recent Posts</h2>
          <p style={styles.cardDescription}>
            View your recent posts from X and explore engagement metrics. Analyze likes, retweets, and replies to understand your content performance.
          </p>
          <button
            style={styles.cardButton}
            onClick={() => navigate("/recent-posts")}
          >
            View Posts
          </button>
        </div>

        <div style={styles.card}>
          <h2 style={styles.cardTitle}>Generate Replies</h2>
          <p style={styles.cardDescription}>
            Generate AI-powered replies for posts using our intelligent system. Create engaging and contextual responses automatically.
          </p>
          <button
            style={styles.cardButton}
            onClick={() => navigate("/generate-replies")}
          >
            Generate Replies
          </button>
        </div>

        <div style={styles.card}>
          <h2 style={styles.cardTitle}>Filtered Posts</h2>
          <p style={styles.cardDescription}>
            View posts filtered by relevance to specific criteria like hiring and job opportunities. Prioritize high-value content.
          </p>
          <button
            style={styles.cardButton}
            onClick={() => navigate("/filtered-posts")}
          >
            View Filtered Posts
          </button>
        </div>
        <div style={styles.card}>
          <h2 style={styles.cardTitle}>Posting</h2>
          <p style={styles.cardDescription}>
            View generated replies and auto-post them to X. Manage your outgoing content efficiently.
          </p>
          <button
            style={styles.cardButton}
            onClick={() => navigate("/posting")}
          >
            Go to Posting
          </button>
        </div>
      </div>

      <button
        style={styles.logout}
        onClick={() => {
          fetch("http://localhost:5000/auth/logout", {
            method: "GET",
            credentials: "include",
          }).then(() => {
            window.location.href = "/";
          });
        }}
      >
        Logout
      </button>
    </div>
  );
};

const styles = {
  page: {
    height: "100vh",
    width: "100vw",
    background: "#0b0b0b",
    color: "#fff",
    padding: "40px",
    fontFamily: "Inter, system-ui, sans-serif",
    boxSizing: "border-box",
    overflowY: "auto",
  },
  title: {
    fontSize: "28px",
    fontWeight: "600",
  },
  subtitle: {
    color: "#aaa",
    marginTop: "8px",
    marginBottom: "40px",
  },
  cardsContainer: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))",
    gap: "24px",
    marginBottom: "40px",
  },
  card: {
    background: "#1a1a1a",
    border: "1px solid #333",
    borderRadius: "12px",
    padding: "24px",
    display: "flex",
    flexDirection: "column",
    transition: "all 0.3s ease",
  },
  cardTitle: {
    fontSize: "18px",
    fontWeight: "600",
    marginBottom: "12px",
  },
  cardDescription: {
    color: "#aaa",
    fontSize: "14px",
    lineHeight: "1.6",
    marginBottom: "20px",
    flex: "1",
  },
  cardButton: {
    padding: "10px 16px",
    background: "#fff",
    color: "#000",
    border: "none",
    borderRadius: "8px",
    fontWeight: "600",
    cursor: "pointer",
    fontSize: "14px",
    transition: "all 0.2s",
  },
  logout: {
    padding: "10px 16px",
    background: "#fff",
    color: "#000",
    border: "none",
    borderRadius: "8px",
    fontWeight: "600",
    cursor: "pointer",
  },
  center: {
    minHeight: "100vh",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    background: "#0b0b0b",
  },
  text: {
    color: "#aaa",
  },
};

export default Dashboard;
