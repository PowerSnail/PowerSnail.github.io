use maud::{html, Markup, DOCTYPE};

pub fn common_header() -> Markup {
    html! {
        meta charset="utf-8";
        meta name="viewport" content="width=device-width, initial-scale=1";
    }
}


pub fn navigation() -> Markup {
    html! {
        nav {
            a href="/posts/" { "Posts" };
        }
    }
}

pub fn page(content: Markup) -> Markup {
    html! {
        (DOCTYPE);
        html {
            (content)
        }
    }
}

