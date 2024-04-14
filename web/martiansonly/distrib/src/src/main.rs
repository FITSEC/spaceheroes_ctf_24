use std::{fs, io, path, process, env};
use axum::{
    routing::get,
    http::StatusCode,
    Router,
    extract::{Path, DefaultBodyLimit, Multipart},
    response::{IntoResponse, Response},
};
use hyper::header;
use path_absolutize::*;
use regex::bytes::Regex;
use once_cell::sync::Lazy;

#[tokio::main]
async fn main() {
    let key = env::var("KEY").expect("pls give me a key :c");
    let app = Router::new()
        .route(format!("/{key}/").as_str(), get(get_page_root))
        .route(format!("/{key}/*path").as_str(), get(get_page).post(create_profile))
        .layer(DefaultBodyLimit::max(256 * 1024));

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await.unwrap();
    axum::serve(listener, app).await.unwrap();
}

async fn apply_templating(page: &mut Vec<u8>) {
    static TEMPLATE_REGEX: Lazy<Regex> = Lazy::new(|| {
        Regex::new(r#"(?s-u)(?<tag><z\s+content\s*?=\s*?"(?<cmd>.*?)"\s*?>.*?</z>)"#).unwrap()
    });

    let mut page_offset: isize = 0;
    for (tag, cmd) in TEMPLATE_REGEX.captures_iter(&page.to_owned()[..]).filter_map(|c| match (c.name("tag"), c.name("cmd")) {
        (Some(tag), Some(cmd)) => Some((tag, cmd)),
        _ => None,
    }) {
        if let Ok(output) = process::Command::new("sh").args(["-c", &String::from_utf8_lossy(cmd.as_bytes())]).output() {
            page.splice((tag.start() as isize + page_offset) as usize..(tag.end() as isize + page_offset) as usize, output.stdout.clone());
            page_offset += (tag.start() as isize + page_offset + output.stdout.len() as isize) - (tag.end() as isize + page_offset);
        }
    }
}

async fn get_page_root() -> Response {
    get_page(Path("/".to_string())).await
}

async fn get_page(Path(req_path): Path<String>) -> Response {
    let req_path = match req_path.ends_with('/') || req_path.is_empty() {
        true => req_path + "/index.html",
        false => req_path,
    };
    let req_path = req_path.trim_start_matches('/');
    let cwd = std::env::current_dir().ok().unwrap();
    let full_path = cwd.join("www/").join(req_path);
    let full_path = full_path.absolutize().unwrap();
    let path = full_path.strip_prefix(cwd.join("www/"));
    let path = match path {
        Ok(path) => path,
        Err(_) => return StatusCode::NOT_FOUND.into_response()
    };
    let path = std::path::Path::new("www/").join(path);

    let mut file = match std::fs::read(path.clone()) {
        Ok(contents) => contents,
        Err(e) 
            if [io::ErrorKind::NotFound, io::ErrorKind::PermissionDenied]
                .into_iter()
                .any(|x| x == e.kind()) => 
        {
            return StatusCode::NOT_FOUND.into_response()
        }
        Err(_) => return StatusCode::INTERNAL_SERVER_ERROR.into_response(),
    };

    apply_templating(&mut file).await;

    let mime = match infer::get(&file) {
        Some(mime) => mime.to_string(),
        None => mime_guess::from_path(path)
            .first_or_octet_stream()
            .to_string(),
    };

    let headers = [(header::CONTENT_TYPE, mime)];
    (headers, file).into_response()
}

async fn create_profile(Path(req_path): Path<String>, mut multipart: Multipart) -> Response {
    if req_path != "profile" {
        return (StatusCode::NOT_FOUND, "").into_response();
    }
    let mut name: String = Default::default();
    let mut bio: String = Default::default();
    let mut pic: axum::body::Bytes = Default::default();
    while let Some(field) = multipart.next_field().await.unwrap() {
        match (field.name(), field.content_type()) {
            (Some("name"), Some("text/plain") | None) if name.is_empty() => name = field.text().await.unwrap(),
            (Some("bio"), Some("text/plain") | None) if bio.is_empty() => bio = field.text().await.unwrap(),
            (Some("pic"), Some("image/jpeg")) if pic.is_empty() => pic = field.bytes().await.unwrap(),
            _ => return (StatusCode::BAD_REQUEST, "error 400: bad request").into_response()
        }
    }
    name.retain(|x| x.is_alphanumeric() || " .,-".contains(x));
    if name.is_empty() || bio.is_empty() || pic.is_empty() {
        return (StatusCode::BAD_REQUEST, "").into_response();
    }

    let profile_dir = path::Path::new("www/profiles/").join(name);
    match fs::create_dir_all(profile_dir.clone()) {
        Ok(_) => {},
        Err(_) => return (StatusCode::INTERNAL_SERVER_ERROR, "error 500: internal server error").into_response(),
    }

    if [
        fs::write(profile_dir.join("bio.txt"), bio),
        fs::write(profile_dir.join("pic.jpg"), pic)
    ]
    .iter()
    .any(|x| x.is_err())
    {
        return (StatusCode::INTERNAL_SERVER_ERROR, "error 500: internal server error").into_response();
    }
    
    
    get_page(Path("/browse/".to_string())).await.into_response()
}
