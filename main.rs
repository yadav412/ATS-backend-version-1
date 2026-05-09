use axum::{
    routing::{get, post},
    Json, Router,
};
use serde::{Deserialize, Serialize};
use tokio::net::TcpListener;


#[derive(Deserialize)]
struct SkillMatchRequest {
    resume_text: String,
    phrases: Vec<String>,
}

#[derive(Serialize)]
struct SkillMatchResponse {
    percent: f32,
    matched: usize,
    total: usize,
}


fn skill_match(resume: &str, phrases: &[String]) -> (f32, usize, usize) {
    let resume_lower = resume.to_lowercase();

    let mut matched = 0;

    for phrase in phrases {
        if resume_lower.contains(&phrase.to_lowercase()) {
            matched += 1;
        }
    }

    let total = phrases.len();

    let percent = if total > 0 {
        (matched as f32 / total as f32) * 100.0
    } else {
        0.0
    };

    (percent, matched, total)
}


async fn root() -> &'static str {
    "rust-skill-service alive"
}

async fn skill_match_handler(
    Json(payload): Json<SkillMatchRequest>,
) -> Json<SkillMatchResponse> {
    let (percent, matched, total) =
        skill_match(&payload.resume_text, &payload.phrases);

    Json(SkillMatchResponse {
        percent,
        matched,
        total,
    })
}

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/", get(root))
        .route("/skill-match", post(skill_match_handler));

    let listener = TcpListener::bind("0.0.0.0:8001")
        .await
        .expect("failed to bind port 8001");

    println!("Rust service running on 8001");

    axum::serve(listener, app)
        .await
        .expect("server failed");
}





