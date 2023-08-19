use maud::{html, Markup};

use crate::{components::{common_header, navigation, page}, post::Post};

pub async fn posts(posts: &Vec<Post>) -> Markup {
    page(html! {
        head {
            (common_header())
            title { "Posts" }
        }
        body {
            (navigation())
            h1 { "Posts" }
            ul {
                @for post in posts {
                    li {
                        a href=(post.url()) {
                            (post.meta.title)
                        }
                    }
                }
            }
        }
    })
}