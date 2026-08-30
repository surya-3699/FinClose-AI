import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts";
import "./styles.css";

const API =
  import.meta.env.VITE_API_URL || "https://finclose-ai.onrender.com";

type Result = {
  settlement_id?: string | null;
  settlement_reference?: string | null;
  settlement_amount?: number | null;
  ledger_id?: string | null;
  status: string;
  confidence: number;
  method: string;
  reason: string;
  evidence: string[];
};

type Dashboard = {
  metrics: Record<string, number>;
  results: Result[];
  settlements_count: number;
  ledger_count: number;
};

function App() {
  const [data, setData] = useState<Dashboard | null>(null);
  const [selected, setSelected] = useState<Result | null>(null);
  const [loading, setLoading] = useState(false);

  const loadDemo = async () => {
    try {
      setLoading(true);

      const res = await fetch(`${API}/api/demo/load`, {
        method: "POST",
      });

      if (!res.ok) {
        throw new Error(`Failed to load demo: ${res.status}`);
      }

      const payload = await res.json();

      setData({
        ...payload,
        settlements_count: payload.settlements_count ?? 8,
        ledger_count: payload.ledger_count ?? 8,
      });
    } catch (error) {
      console.error("Load demo error:", error);
      alert("Failed to load demo dataset. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const loadDashboard = async () => {
    try {
      const res = await fetch(`${API}/api/dashboard`);

      if (!res.ok) {
        throw new Error(`Failed to load dashboard: ${res.status}`);
      }

      const payload = await res.json();

      if (payload.results?.length) {
        setData(payload);
      }
    } catch (error) {
      console.error("Dashboard load error:", error);
    }
  };

  useEffect(() => {
    loadDashboard();
  }, []);

  const investigate = async (item: Result) => {
    if (!item.settlement_id) {
      setSelected(item);
      return;
    }

    try {
      const res = await fetch(
        `${API}/api/investigate/${item.settlement_id}`
      );

      if (!res.ok) {
        throw new Error(`Investigation failed: ${res.status}`);
      }

      const payload = await res.json();

      setSelected({
        ...item,
        reason:
          payload.controller_recommendation +
          " — " +
          item.reason,
      });
    } catch (error) {
      console.error("Investigation error:", error);
      alert("Failed to investigate this record.");
    }
  };

  const m = data?.metrics || {};

  const chart = [
    {
      name: "Reconciled",
      value: m.reconciled || 0,
    },
    {
      name: "Review",
      value: m.needs_review || 0,
    },
    {
      name: "Exceptions",
      value: m.exceptions || 0,
    },
  ];

  return (
    <main>
      <header>
        <div>
          <div className="eyebrow">
            AI FINANCE CONTROLLER
          </div>

          <h1>FinClose AI</h1>

          <p>
            Agentic financial reconciliation with confidence controls and
            auditable exceptions.
          </p>
        </div>

        <button onClick={loadDemo} disabled={loading}>
          {loading ? "Loading…" : "Load Demo Dataset"}
        </button>
      </header>

      {!data && (
        <section className="empty">
          <h2>Ready for reconciliation</h2>

          <p>
            Load the synthetic demo dataset to start the complete controller
            workflow.
          </p>
        </section>
      )}

      {data && (
        <>
          <section className="metrics">
            <Card
              label="Settlement records"
              value={data.settlements_count}
            />

            <Card
              label="Ledger records"
              value={data.ledger_count}
            />

            <Card
              label="Reconciliation rate"
              value={`${m.reconciliation_rate || 0}%`}
            />

            <Card
              label="Avg confidence"
              value={`${m.average_confidence || 0}%`}
            />
          </section>

          <section className="grid">
            <div className="panel chart-panel">
              <h2>Controller outcome</h2>

              <ResponsiveContainer width="100%" height={240}>
                <PieChart>
                  <Pie
                    data={chart}
                    dataKey="value"
                    nameKey="name"
                    outerRadius={82}
                    label
                  >
                    <Cell fill="#22c55e" />
                    <Cell fill="#f59e0b" />
                    <Cell fill="#ef4444" />
                  </Pie>

                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>

            <div className="panel">
              <h2>Safety policy</h2>

              <ul>
                <li>Exact matches can be auto-reconciled.</li>
                <li>
                  Strong fuzzy matches require conservative confidence.
                </li>
                <li>Ambiguous records enter human review.</li>
                <li>Unmatched records remain explicit exceptions.</li>
                <li>Every result stores reason and evidence.</li>
              </ul>
            </div>
          </section>

          <section className="panel">
            <div className="section-title">
              <div>
                <h2>Reconciliation results</h2>

                <p>
                  Click a row to inspect the controller evidence.
                </p>
              </div>

              <span className="badge">
                {m.total_items || 0} items
              </span>
            </div>

            <div className="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>Settlement</th>
                    <th>Ledger</th>
                    <th>Amount</th>
                    <th>Status</th>
                    <th>Confidence</th>
                    <th>Method</th>
                  </tr>
                </thead>

                <tbody>
                  {data.results.map((r, i) => (
                    <tr
                      key={i}
                      onClick={() => investigate(r)}
                    >
                      <td>
                        {r.settlement_reference || "—"}
                      </td>

                      <td>{r.ledger_id || "—"}</td>

                      <td>
                        {r.settlement_amount ?? "—"}
                      </td>

                      <td>
                        <span
                          className={`status ${r.status}`}
                        >
                          {r.status.replace("_", " ")}
                        </span>
                      </td>

                      <td>
                        {Math.round(r.confidence * 100)}%
                      </td>

                      <td>{r.method}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>

          {selected && (
            <section className="panel investigation">
              <div className="section-title">
                <div>
                  <h2>Controller investigation</h2>

                  <p>
                    {selected.settlement_reference ||
                      "Ledger-only exception"}
                  </p>
                </div>

                <button
                  className="secondary"
                  onClick={() => setSelected(null)}
                >
                  Close
                </button>
              </div>

              <div className="recommendation">
                {selected.reason}
              </div>

              <h3>Evidence</h3>

              <ul>
                {selected.evidence.map((e, i) => (
                  <li key={i}>{e}</li>
                ))}
              </ul>

              <p className="audit">
                Audit rule: low-confidence recommendations are never silently
                approved.
              </p>
            </section>
          )}
        </>
      )}
    </main>
  );
}

function Card({
  label,
  value,
}: {
  label: string;
  value: React.ReactNode;
}) {
  return (
    <div className="metric">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

createRoot(document.getElementById("root")!).render(<App />);