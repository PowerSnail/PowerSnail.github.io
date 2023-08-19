use std::path::{Path, PathBuf};

use anyhow::Context;
use chrono::{DateTime, Utc};
use maud::{html, Markup, PreEscaped};
use tokio::process::Command;

use crate::components::{common_header, navigation, page};
use serde::de::Error;
use serde::{Deserialize, Deserializer};

pub struct Post {
    pub path: PathBuf,
    pub meta: Meta,
    pub content: String,
}

pub fn post(p: &Post) -> Markup {
    page(html! {
        head {
            (common_header())
            title { "Post" }
        }
        body {
            (navigation())
            article {
            h1 {
                (&p.meta.title)
            }
            (PreEscaped(&p.content))
            }
        }
    })
}

impl Post {
    pub async fn new(path: &Path) -> anyhow::Result<Self> {
        let meta = parse_meta(path).await?;
        Ok(Self {
            path: path.to_path_buf(),
            meta,
            content: compile_content(path).await?,
        })
    }

    pub fn url(&self) -> String {
        format!("/{}/{}", self.meta.date.format("%Y"), self.meta.slug)
    }
}

#[derive(Deserialize)]
pub struct Meta {
    pub title: String,

    #[serde(deserialize_with = "parse_date")]
    pub date: DateTime<Utc>,
    pub slug: String,
    pub description: String,
}

async fn compile_content(path: &Path) -> anyhow::Result<String> {
    let content = Command::new("pandoc")
        .arg(path)
        .arg("--to=html")
        .output()
        .await?
        .stdout
        ;
    Ok(String::from_utf8(content)?)
}

fn parse_date<'de, D>(deserializer: D) -> Result<DateTime<Utc>, D::Error>
where
    D: Deserializer<'de>,
{
    let s: &str = Deserialize::deserialize(deserializer)?;
    let date = dateparser::parse(s).map_err(D::Error::custom)?;
    Ok(date)
}

async fn parse_meta(filename: &Path) -> anyhow::Result<Meta> {
    let s = Command::new("pandoc")
        .arg(filename)
        .arg("--template=template/meta.pandoc")
        .output()
        .await
        .unwrap()
        .stdout;
    let m: Meta = serde_json::from_slice(&s)
        .with_context(|| format!("Metadata parse error. File: {}", filename.display()))?;
    Ok(m)
}
