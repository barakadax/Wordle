use reqwest;
use serde_json::Error;
use serde::{Deserialize, Serialize};
use crate::words::get_most_common_word;
use crate::words::get_more_accurate_dict;
use crate::words::remove_words_with_letter;

#[derive(Serialize, Deserialize)]
struct Retry {
    #[serde(rename = "retries left")]
    retries: u32,
    #[serde(rename = "0")]
    index_0: String,
    #[serde(rename = "1")]
    index_1: String,
    #[serde(rename = "2")]
    index_2: String,
    #[serde(rename = "3")]
    index_3: String,
    #[serde(rename = "4")]
    index_4: String,
}

#[derive(Serialize, Deserialize)]
pub struct GameData {
    pub url: String,
    pub words: Vec<String>
}

async fn make_request(client: &reqwest::Client, url: &str, word: String) -> reqwest::Response {
    let response = client
        .post(url)
        .header(reqwest::header::CONTENT_TYPE, "text/plain")
        .body(word)
        .send()
        .await;

    return response.unwrap();
}

async fn process_response(response: reqwest::Response) -> Result<Retry, Error> {
    let text = response.text().await;
    let body: Result<Retry, serde_json::Error> = serde_json::from_str(&text.unwrap()).map_err(Error::from);
    body
}

fn handle_retry_index(index_result: String, common_char: char, mut words: Vec<String>, index: usize) ->  Vec<String> {
    if index_result == "correct" {
        words = get_more_accurate_dict(words, common_char, Some(index));
    }
    else if index_result == "correct letter wrong placement" {
        words = get_more_accurate_dict(words, common_char, None);
    }
    else if index_result == "wrong" {
        words = remove_words_with_letter(words, common_char);
    }
    else {
        panic!("Returned unhandled value: {}", index_result);
    }

    return words;
}

fn handle_retry(round: Retry, common_word: String, mut words: Vec<String>) ->  Vec<String> {
    words = handle_retry_index(round.index_0, common_word.chars().nth(0).unwrap(), words, 0);
    words = handle_retry_index(round.index_1, common_word.chars().nth(1).unwrap(), words, 1);
    words = handle_retry_index(round.index_2, common_word.chars().nth(2).unwrap(), words, 2);
    words = handle_retry_index(round.index_3, common_word.chars().nth(3).unwrap(), words, 3);
    words = handle_retry_index(round.index_4, common_word.chars().nth(4).unwrap(), words, 4);

    return words;
}

pub async fn solve(mut _game: GameData) {
    let client = reqwest::Client::new();

    for _ in 0..=4 {
        let most_common_word = get_most_common_word(_game.words.clone());

        let response = make_request(&client, &_game.url, most_common_word.clone()).await;

        let headers = response.headers();
        if let Some(header_value) = headers.get("statues") {
            if header_value.to_str().unwrap_or("Invalid header value") == "retry" {
                let round_result =  process_response(response).await.unwrap();

                println!("{}\n{}\n{}\n{}\n{}\n{}\n", round_result.retries, round_result.index_0,
                round_result.index_1, round_result.index_2, round_result.index_3, round_result.index_4);

                _game.words = handle_retry(round_result, most_common_word.clone(), _game.words);
            }
            else if header_value.to_str().unwrap_or("Invalid header value") == "won" {
                println!("won");
                return; // Implement later
            }
            else if header_value.to_str().unwrap_or("Invalid header value") == "done" {
                println!("done");
                return; // Implement later
            }
            else if header_value.to_str().unwrap_or("Invalid header value") == "deleted" {
                println!("deleted");
                return; // Implement later
            }
        }
    }
}