use std::fs::File;
use std::io::{self, BufRead};
use std::collections::HashMap;

pub fn read_words_from_file(file_path: &str) -> io::Result<Vec<String>> {
    let file = File::open(file_path)?;
    let mut words = Vec::new();

    for line in io::BufReader::new(file).lines() {
        let line = line?;
        let word = line.trim().to_string();
        words.push(word);
    }

    Ok(words)
}

pub fn remove_words_with_letter(words: Vec<String>, letter: char) -> Vec<String> {
    words.into_iter()
        .filter(|word| !word.contains(letter))
        .collect()
}

pub fn get_more_accurate_dict(mut words: Vec<String>, common_char: char, index: Option<usize>) -> Vec<String> {
    if let Some(idx) = index {
        words.retain(|word| word.chars().nth(idx).unwrap_or('\0') == common_char);
        words
    } else {
        words.into_iter().filter(|word| word.contains(common_char)).collect()
    }
}

pub fn get_most_common_word(words: Vec<String>) -> String {
    let mut words_copy = words.clone();

    for i in 0..=4 {
        let mut char_counts: HashMap<char, usize> = HashMap::new();

        for word in &words_copy {
            let c = word.chars().nth(i).unwrap_or('\0');
            *char_counts.entry(c).or_insert(0) += 1;
        }

        let (most_common_char, _) = char_counts.iter().max_by_key(|&(_, count)| count).unwrap();

        words_copy = get_more_accurate_dict(words_copy, *most_common_char, Some(i));
    };

    return words_copy[0].clone();
}
