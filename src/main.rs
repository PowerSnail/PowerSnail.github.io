mod components;
mod index;
mod post;
mod posts;

use std::{path::PathBuf, sync::Arc};

use axum::{extract::State, routing::get, Router};
use maud::Markup;
use post::Post;
use walkdir::WalkDir;

struct Website {
    post_list: Vec<Post>,
}

#[tokio::main]
async fn main() {
    let post_root = PathBuf::from("content/posts");

    let post_path_list: Vec<_> = WalkDir::new(post_root.as_path())
        .into_iter()
        .filter_map(|e| e.ok())
        .filter(|e| e.path().extension().and_then(|e| e.to_str()) == Some("md"))
        .map(|e| e.to_owned().into_path())
        .collect();

    let post_list = futures::future::join_all(
        post_path_list
            .iter()
            .map(|e| async { Post::new(e.as_path()).await.expect("Post parse error") }),
    )
    .await;

    let website = Arc::new(Website { post_list });

    let mut app: Router =
        Router::new() //
            .route("/", get(index::index))
            .route(
                "/posts/",
                get(|State(state): State<Arc<Website>>| async move {
                    posts::posts(&state.post_list).await
                })
                .with_state(website.clone()),
            );

    for (i, post) in website.post_list.iter().enumerate() {
        app = app.route(
            &post.url(),
            get(move |State(website): State<Arc<Website>>| async move {
                post::post(&website.post_list[i])
            })
            .with_state(website.clone()),
        );
    }

    axum::Server::bind(&"0.0.0.0:9999".parse().unwrap())
        .serve(app.into_make_service())
        .await
        .unwrap();
}
