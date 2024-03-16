use redis_om;
use std::env;
use teloxide::{prelude::*, utils::command::BotCommands};

mod models;
// use models::*;


#[tokio::main]
async fn main() {

    let redis_url = env::var("REDIS_URL").unwrap_or_else(|_| "redis://redis:6379/".to_string());
    let client = redis_om::Client::open(redis_url).unwrap();
    let mut conn = client.get_tokio_connection().await.unwrap();

    pretty_env_logger::init();
    log::info!("Starting command bot...");

    let bot = Bot::from_env();
    Command::repl(bot, answer).await;
    // let jane_db = Customer::get(&jane.id, &mut conn).await.unwrap_or_else(|_|Customer::default());
    // jane.save(&mut conn).await.unwrap();
    // let jane_db = Customer::get(&jane.id, &mut conn).await.unwrap();
    // Customer::delete(&jane.id, &mut conn).await.unwrap();

    println!("YEP");
}


#[derive(BotCommands, Clone)]
#[command(rename_rule = "lowercase", description = "These commands are supported:")]
enum Command {
    #[command(description = "display this text.")]
    Help,
    #[command(description = "handle a username.")]
    Username(String),
    #[command(description = "handle a username and an age.", parse_with = "split")]
    UsernameAndAge { username: String, age: u8 },
}

async fn answer(bot: Bot, msg: Message, cmd: Command) -> ResponseResult<()> {
    match cmd {
        Command::Help => bot.send_message(msg.chat.id, Command::descriptions().to_string()).await?,
        Command::Username(username) => {
            bot.send_message(msg.chat.id, format!("Your username is @{username}.")).await?
        }
        Command::UsernameAndAge { username, age } => {
            bot.send_message(msg.chat.id, format!("Your username is @{username} and age is {age}."))
                .await?
        }
    };

    Ok(())
}
