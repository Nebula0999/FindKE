import React, { useState } from "react";
import { getCurrentUser, loginUser } from "./services";

const initialForm = {
	username: "",
	password: "",
};

export default function LoginUser({ onLoggedIn }) {
	const [form, setForm] = useState(initialForm);
	const [submitting, setSubmitting] = useState(false);
	const [error, setError] = useState("");
	const [message, setMessage] = useState("");

	function handleChange(event) {
		const { name, value } = event.target;
		setForm((prev) => ({ ...prev, [name]: value }));
	}

	async function handleSubmit(event) {
		event.preventDefault();
		setSubmitting(true);
		setError("");
		setMessage("");

		try {
			const loginResult = await loginUser(form);
			const profile = await getCurrentUser(loginResult.token);
			setMessage(`Welcome back, ${profile.username}.`);

			if (onLoggedIn) {
				onLoggedIn({ token: loginResult.token, user: profile });
			}
		} catch (err) {
			setError(err.message);
		} finally {
			setSubmitting(false);
		}
	}

	return (
		<main style={styles.page}>
			<section style={styles.card}>
				<h1 style={styles.heading}>Sign In</h1>
				<p style={styles.subheading}>Access your FindKE account.</p>

				<form onSubmit={handleSubmit} style={styles.form}>
					<label style={styles.label}>
						Username
						<input
							name="username"
							value={form.username}
							onChange={handleChange}
							required
							style={styles.input}
						/>
					</label>

					<label style={styles.label}>
						Password
						<input
							name="password"
							type="password"
							value={form.password}
							onChange={handleChange}
							required
							style={styles.input}
						/>
					</label>

					<button type="submit" disabled={submitting} style={styles.button}>
						{submitting ? "Signing in..." : "Sign In"}
					</button>
				</form>

				{error ? <p style={styles.error}>{error}</p> : null}
				{message ? <p style={styles.success}>{message}</p> : null}
			</section>
		</main>
	);
}

const styles = {
	page: {
		minHeight: "100vh",
		display: "grid",
		placeItems: "center",
		padding: 20,
		background:
			"radial-gradient(circle at 20% 15%, #fef3c7 0%, transparent 35%), radial-gradient(circle at 80% 85%, #bfdbfe 0%, transparent 32%), #f8fafc",
		fontFamily: "Segoe UI, Tahoma, Geneva, Verdana, sans-serif",
	},
	card: {
		width: "100%",
		maxWidth: 420,
		padding: 24,
		borderRadius: 18,
		background: "rgba(255, 255, 255, 0.95)",
		border: "1px solid #cbd5e1",
		boxShadow: "0 20px 45px rgba(30, 41, 59, 0.16)",
	},
	heading: {
		margin: "0 0 6px",
		fontSize: 28,
	},
	subheading: {
		margin: "0 0 20px",
		color: "#334155",
	},
	form: {
		display: "grid",
		gap: 14,
	},
	label: {
		display: "grid",
		gap: 6,
		fontWeight: 600,
		color: "#1e293b",
	},
	input: {
		borderRadius: 10,
		border: "1px solid #94a3b8",
		padding: "11px 12px",
		fontSize: 14,
	},
	button: {
		marginTop: 6,
		border: "none",
		borderRadius: 10,
		padding: "12px 14px",
		color: "white",
		fontSize: 15,
		fontWeight: 700,
		background: "linear-gradient(135deg, #0f766e, #2563eb)",
		cursor: "pointer",
	},
	error: {
		marginTop: 12,
		color: "#b91c1c",
		fontWeight: 600,
	},
	success: {
		marginTop: 12,
		color: "#166534",
		fontWeight: 600,
	},
};
