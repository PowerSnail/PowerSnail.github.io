use maud::{html, Markup};

use crate::components::{common_header, navigation, page};

pub async fn index() -> Markup {
    page(html! {
        head {
            (common_header())
            title { "SnailShell" }
        }
        body {
            (navigation())
            h1 {
                "SnailShell"
            }
            p {
                "Hello, World!"
            }
        }
    })
}
