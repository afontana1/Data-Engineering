mod models;
mod storage;

use clap::Parser;
use rayon::prelude::*;
use std::fs::{self, File};
use std::io::{BufRead, BufReader};
use std::sync::mpsc::{Receiver, Sender};
use tokio::task::JoinHandle;
use tracing::{info, warn};
use crate::models::bert::BertModelWrapper;

#[derive(Parser)]
pub struct Cli {
    #[clap(short, long)]
    input_directory: String,
    #[clap(short, long)]
    db_uri: String,
}

struct EmbeddingEntry {
    filename: String,
    embedding: Vec<f32>,
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    // init_tracing();
    let cli_args = Cli::parse();
    let ts_mark = std::time::Instant::now();

    let (sender, receiver) = std::sync::mpsc::channel::<EmbeddingEntry>();
    let db_writer_task = init_db_writer_task(receiver, cli_args.db_uri.as_str(), "vectors_table_1", 100).await?;

    let files_dir = fs::read_dir(cli_args.input_directory)?;

    let file_list = files_dir
        .into_iter()
        .map(|file| file.unwrap().path().to_str().unwrap().to_string())
        .collect::<Vec<String>>();

    file_list.par_iter().for_each(|filename| {
        if let Err(e) = process_text_file(sender.clone(), filename.as_str()) {
            warn!("Error processing file: {}: Error{}", filename, e)
        }
    });

    drop(sender);
    info!("All files processed, waiting for the write task to finish");
    db_writer_task.await?;
    info!(
        "{} files indexed in: {:?}",
        file_list.len(),
        ts_mark.elapsed()
    );
    Ok(())
}

fn process_text_file(sender: Sender<EmbeddingEntry>, filename: &str) -> anyhow::Result<()> {
    let bert_model = models::bert::get_model_reference()?;
    info!("reading file: {}", filename);
    let text_chunks = read_file_in_chunks(filename, 256)?;
    let text_chunks: Vec<&str> = text_chunks.iter().map(AsRef::as_ref).collect();
    let file_vector = embed_multiple_sentences(&text_chunks, false, &bert_model)?;

    sender.send(EmbeddingEntry {
        filename: filename.to_string(),
        embedding: file_vector[0].clone()
    })?;
    Ok(())
}

async fn init_db_writer_task(
    receiver: Receiver<EmbeddingEntry>,
    db_uri: &str,
    table_name: &str,
    buffer_size: usize
) -> anyhow::Result<JoinHandle<()>> {
    let db = storage::VecDB::connect(db_uri, table_name).await?;
    let task_handle = tokio::spawn(async move {
        let mut embeddings_buffer = Vec::new();
        while let Ok(embedding) = receiver.recv() {
            embeddings_buffer.push(embedding);
            if embeddings_buffer.len() >= buffer_size {
                let (keys, vectors) = extract_keys_and_vectors(&embeddings_buffer);
                db.add_vector(&keys, vectors, 384).await.unwrap();
                embeddings_buffer.clear();
            }
        }
        if !embeddings_buffer.is_empty() {
            let (keys, vectors) = extract_keys_and_vectors(&embeddings_buffer);
            db.add_vector(&keys, vectors, 384).await.unwrap();
        }
    });
    Ok(task_handle)
}

fn extract_keys_and_vectors(embeddings_buffer: &[EmbeddingEntry]) -> (Vec<&str>, Vec<Vec<f32>>) {
    embeddings_buffer
        .iter()
        .map(|entry| (entry.filename.as_str(), entry.embedding.clone()))
        .unzip::<&str, Vec<f32>, Vec<&str>, Vec<Vec<f32>>>()
}

fn embed_multiple_sentences(
    sentences: &[&str],
    apply_mean: bool,
    bert_model: &BertModelWrapper
) -> anyhow::Result<Vec<Vec<f32>>> {
    let multiple_embeddings = bert_model.embed_sentences(sentences, apply_mean)?;
    if apply_mean {
        let multiple_embeddings = multiple_embeddings.to_vec1::<f32>()?;
        Ok(vec![multiple_embeddings])
    } else {
        let multiple_embeddings = multiple_embeddings.to_vec2::<f32>()?;
        Ok(multiple_embeddings)
    }
}

fn embed_sentence(
    sentence: &str,
    bert_model: &BertModelWrapper
) -> anyhow::Result<Vec<f32>> {
    let embedding = bert_model.embed_sentence(sentence)?;
    println!("Embedding Tensor: {:?}", embedding);
    let embedding = embedding.squeeze(0)?;
    println!("Embedding Tensor Squeeze: {:?}", embedding);
    let embedding = embedding.to_vec1::<f32>().unwrap();
    Ok(embedding)
}

fn init_tracing() {
    if let Ok(level_filter) = tracing_subscriber::EnvFilter::try_from_env("LOG_LEVEL") {
        tracing_subscriber::fmt()
            .with_env_filter(level_filter)
            .with_ansi(true)
            .with_file(true)
            .with_line_number(true)
            .init();
    } else {
        println!("Failed to parse LOG_LEVEL env variable, using default log level: INFO");
        tracing_subscriber::fmt()
            .with_ansi(true)
            .with_file(true)
            .with_line_number(true)
            .init();
    }
}

fn read_file_in_chunks(
    file_path: &str,
    chunk_size: usize
) -> anyhow::Result<Vec<String>> {
    let file = File::open(file_path).unwrap();
    let reader = BufReader::new(file);
    let mut sentences = Vec::new();
    let mut text_buffer = String::new();

    for text in reader.lines() {
        let text = text?;
        text_buffer.push_str(text.as_str());
        let word_count = text_buffer.split_whitespace().count();
        if word_count >= chunk_size {
            sentences.push(text_buffer.clone());
            text_buffer.clear();
        }
    }

    if !text_buffer.is_empty() {
        sentences.push(text_buffer.clone());
    }
    Ok(sentences)
}

#[cfg(test)]
mod tests {
    use arrow_array::StringArray;
    use super::*;
    use crate::embed_sentence;

    #[tokio::test]
    async fn test_full_flow() {
        let temp_folder = "test_test_folder";
        let temp_table = "temp_test_table";

        fs::create_dir(temp_folder).unwrap();

        let (test_sender, test_receiver) = std::sync::mpsc::channel::<EmbeddingEntry>();
        let db_writer_task = init_db_writer_task(test_receiver, temp_folder, temp_table, 100)
            .await.unwrap();

        let files_dir = fs::read_dir("embedding_file_test").unwrap();
        let file_list = files_dir
            .into_iter()
            .map(|file| file.unwrap().path().to_str().unwrap().to_string())
            .collect::<Vec<String>>();

        file_list.par_iter().for_each(|filename| {
            if let Err(e) = process_text_file(test_sender.clone(), filename.as_string()) {
                panic!("Error processing file: {}: Error:{}", filename, e)
            }
        });

        drop(test_sender);
        db_writer_task.await.unwrap();

        let db = storage::VecDB::connect(temp_folder, temp_table)
            .await
            .unwrap();

        let bert_model = models::bert::get_model_reference().unwrap();
        let animals_vector = embed_sentence("I like all animals and especially dogs", &bert_model).unwrap();
        let record_batch = db.file_similar(animals_vector, 1).await.unwrap();
        let files_array = record_batch.column_by_name("filename").unwrap();
        let files = files_array.as_any().downcast_ref::<StringArray>().unwrap(); // @XXX downcast
        let v = files.value(0);

        assert_eq!(v, "embedding_files_test/embedding_content_99996.txt");
        fs::remove_dir_all(temp_folder).unwrap();
    }
}