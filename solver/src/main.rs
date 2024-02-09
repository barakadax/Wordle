pub mod words;
pub mod start;
pub mod game_logic;

use crate::game_logic::GameData;
use crate::game_logic::solve;
use crate::start::get_session;
use crate::words::read_words_from_file;

#[tokio::main]
async fn main() {
    let file_path = "../valid-wordle-words.txt";
    let words = read_words_from_file(file_path).unwrap();

    let host = "http://127.0.0.1:8000".to_string();
    let start_game_endpoint = "/start".to_string();

    let session = get_session(host.clone() + &start_game_endpoint.clone()).await;
    let play_game_endpoint = "/play/session/".to_owned() + &session;

    let game = GameData {
        url: host.clone() + &play_game_endpoint,
        words
    };

    solve(game).await;
}
