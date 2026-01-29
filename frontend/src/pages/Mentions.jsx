import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const Mentions = () => {
  const [loading, setLoading] = useState(false);
  const [authenticated, setAuthenticated] = useState(false);
  const [mentions, setMentions] = useState([]);
  const [inputUserId, setInputUserId] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    // Step 1: auth check
    fetch("http://localhost:5000/auth/check", {
      method: "GET",
      credentials: "include",
    })
      .then((res) => res.json())
      .then((data) => {
        if (!data.authenticated) {
          navigate("/");
          return;
        }
        setAuthenticated(true);
      })
      .catch(() => {
        navigate("/");
      });
  }, [navigate]);

  const handleFetch = () => {
    if (!inputUserId) return;
    setLoading(true);
    fetch("http://localhost:5000/api/fetch_mentions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ id: inputUserId }),
      credentials: "include",
    })
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data)) {
          setMentions(data);
        } else {
          console.error("Expected array but got:", data);
        }
      })
      .catch((err) => {
        console.error("Error fetching mentions:", err);
      })
      .finally(() => {
        setLoading(false);
      });
  };

  if (!authenticated && loading) { 
    return (
      <div style={styles.center}>
        <p style={styles.text}>Checking authentication...</p>
      </div>
    );
  }

  if (!authenticated) return null;

  return (
    <div style={styles.page}>
      <button
        style={styles.backButton}
        onClick={() => navigate("/dashboard")}
      >
        ← Back to Dashboard
      </button>

      <h1 style={styles.title}>Mentions</h1>
      <p style={styles.subtitle}>
        Enter a User ID to view mentions.
      </p>

      <div style={styles.inputContainer}>
        <input
          style={styles.input}
          type="text"
          placeholder="Enter User ID"
          value={inputUserId}
          onChange={(e) => setInputUserId(e.target.value)}
        />
        <button style={styles.fetchButton} onClick={handleFetch} disabled={loading}>
          {loading ? "Loading..." : "Fetch Mentions"}
        </button>
      </div>

      <div style={styles.content}>
        {mentions.length === 0 ? (
          <p style={styles.placeholder}>No mentions fetched yet.</p>
        ) : (
          mentions.map((mention) => (
            <div key={mention.id} style={styles.mentionCard}>
              <p style={styles.mentionText}>{mention.text}</p>

              <div style={styles.meta}>
                <span>Author: {mention.author_id ?? "unknown"}</span>
                <span>ID: {mention.id}</span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

const styles = {
  page: {
    minHeight: "100vh",
    width: "100%",
    background: "#0b0b0b",
    color: "#fff",
    padding: "40px",
    fontFamily: "Inter, system-ui, sans-serif",
    boxSizing: "border-box",
    overflowX: "hidden",
  },
  backButton: {
    marginBottom: "20px",
    padding: "8px 16px",
    background: "#1a1a1a",
    color: "#fff",
    border: "1px solid #333",
    borderRadius: "6px",
    cursor: "pointer",
    fontSize: "14px",
  },
  title: {
    fontSize: "28px",
    fontWeight: "600",
    marginTop: "20px",
  },
  subtitle: {
    color: "#aaa",
    marginTop: "8px",
    fontSize: "14px",
    marginBottom: "30px",
  },
  content: {
    display: "flex",
    flexDirection: "column",
    gap: "16px",
  },
  mentionCard: {
    background: "#1a1a1a",
    border: "1px solid #333",
    borderRadius: "10px",
    padding: "16px",
  },
  mentionText: {
    fontSize: "15px",
    lineHeight: "1.6",
    marginBottom: "12px",
  },
  meta: {
    display: "flex",
    gap: "16px",
    fontSize: "13px",
    color: "#aaa",
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
  inputContainer: {
    display: "flex",
    gap: "10px",
    marginBottom: "20px",
  },
  input: {
    padding: "10px",
    borderRadius: "6px",
    border: "1px solid #333",
    background: "#1a1a1a",
    color: "#fff",
    flex: 1,
    maxWidth: "300px",
  },
  fetchButton: {
    padding: "10px 20px",
    borderRadius: "6px",
    border: "none",
    background: "#1d9bf0",
    color: "#fff",
    cursor: "pointer",
    fontWeight: "bold",
  },
  placeholder: {
    color: "#666",
    fontSize: "16px",
  },
};

export default Mentions;
