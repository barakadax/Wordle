use reqwest;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
struct StartGame {
    session: String
}

fn extract_session(data: &str) -> serde_json::Result<String> {
    let start_game: StartGame = serde_json::from_str(data)?;
    Ok(start_game.session)
}

async fn start_match(url: String) -> std::result::Result<String, reqwest::Error> {
    let response = reqwest::get(url).await?;

    let status = response.status();
    let body = response.text().await?;

    if !status.is_success() {
        panic!("Status code: {}\nBody:\n{}", status, body);
    }

    Ok(body)
}

pub async fn get_session(url: String) -> std::string::String {
    let new_game = start_match(url).await;

    let body = match new_game {
        Ok(_) => new_game.unwrap(),
        Err(e) => panic!("Error: {}", e)
    };

    let session_result = extract_session(&body);

    return match session_result {
        Ok(session) => session,
        Err(e) => panic!("Error: {}", e),
    }
}
